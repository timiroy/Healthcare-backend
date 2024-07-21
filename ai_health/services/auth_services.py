from datetime import datetime
import uuid

from fastapi import HTTPException, status
import nanoid

from ai_health.schemas.auth_schemas import (
    Login,
    ResetPassword,
    SignUpUser,
    SigninResponse,
    Token,
    User,
    UserBase,
    UserCreate,
    UserEdit,
    UserEditBase,
    UserExtended,
    VerifyRestPasswordToken,
)
from ai_health.schemas.response_info_schema import ResponseInfo
from ai_health.services.utils import auth_utils, token_utils
from ai_health.database.db_handlers import auth_db_handler
from ai_health.services.utils.exceptions import NotFoundException, RecordExistsException, ServiceException
from ai_health.job_manager import job_runner
from ai_health.root.redis_manager import redis_manager


async def signup(signup_user: SignUpUser) -> Token:
    """
    Handles signing up a user
    """

    sign_up_data = signup_user.model_dump()

    hashed_password = auth_utils.get_password_hash(password=signup_user.password)
    sign_up_data["password"] = hashed_password
    sign_up_data["date_created"] = datetime.now()

    user_create = UserCreate(**sign_up_data)

    try:
        user = await auth_db_handler.create_user(user=user_create)
    except RecordExistsException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"User with email address {signup_user.email} exists"
        )

    except ServiceException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unknown error occurred")

    # Send a OTP to the client
    otp = token_utils.random_with_N_digits()

    # Save Otp Data to redis
    data = {"user_email": signup_user.email, "otp": otp}
    key = token_utils.gen_otp_verification_redis_key(user_email=signup_user.email)
    redis_manager.cache_json_item(key=key, value=data)

    # Send the email to the client
    # payload = {
    #     "info": "You have been invited to try out ai_health",
    #     "more_info": f"Your verification code is {otp}",
    #     "action_text": "Go",
    #     "link": "https://ai_health.com",
    # }
    # job_runner.background_mailer(
    #     reciepients=[signup_user.email],
    #     subject="Please conform your account for ai_health",
    #     payload=payload,
    #     template="auth/info_email_template.html",
    # )

    token_data = auth_utils.get_token_data_from_data(data={"user_id": user.user_id})

    return token_data


async def verify_account_verification_otp(otp: str, user_email: str) -> ResponseInfo:
    """
    Handles verificaio that the enrered account verificaiton otp code is valid
    """

    key = token_utils.gen_otp_verification_redis_key(user_email=user_email)
    data = redis_manager.get_cached_json_item(key=key)

    if data is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"OTP invalid, it has expired")

    data_user_email = data.get("user_email", None)
    if data_user_email is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"OTP invalid")

    data_otp = data.get("otp", "")

    if otp != str(data_otp):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"OTP invalid")

    # It is confirmed to be valid
    user_edit_data = UserEdit(**{"is_verified": True})

    try:
        user = await auth_db_handler.update_user(user_email=user_email, user_edit_data=user_edit_data)

    except ServiceException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unknown error occurred")

    redis_manager.delete_key(key=key)

    # return User(**user.model_dump())
    return ResponseInfo(details="Account verified successfully")


async def resend_verification_otp(user_email: str) -> ResponseInfo:
    """
    Handles generating an otp for the user
    """
    otp = token_utils.random_with_N_digits()

    try:
        user = await auth_db_handler.get_user_with_email(email=user_email)
    except NotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"User with email {user_email} does not exist"
        )

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unknown error occurred")

    if user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"User with email {user_email} is verified"
        )

    # Save Otp Data to redis
    data = {"user_email": user_email, "otp": otp}
    key = token_utils.gen_otp_verification_redis_key(user_email=user_email)
    redis_manager.cache_json_item(key=key, value=data)

    # Send the email to the client
    payload = {
        "info": f"You verificaiton code is {otp}",
        "more_info": f"Your verification code is {otp}",
        "action_text": "Go",
        "link": "https://ai_health.com",
    }
    # job_runner.background_mailer(
    #     reciepients=[user_email],
    #     subject="Please conform your account for ai_health",
    #     payload=payload,
    #     template="auth/info_email_template.html",
    # )

    return ResponseInfo(details="Verification code sent!")


async def signin(login_data: Login) -> SigninResponse:
    """
    Handles signing in to the application
    """
    try:
        user = await auth_db_handler.get_user_with_email(email=login_data.email)
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Email or password is invalid")

    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unknown error occurred")

    is_password_valid = auth_utils.verify_password(plain_password=login_data.password, hashed_password=user.password)

    if not is_password_valid:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Email or password is invalid")

    # Todo: Add the company details here manually
    n_user = User(**user.model_dump())
    token_data = auth_utils.get_token_data_from_data(data={"user_id": n_user.user_id})

    return SigninResponse(user=n_user, token=token_data)


async def update_user_details(user_id: str, user_edit_data: UserEditBase):

    user_edit = UserEdit(**user_edit_data.dict())
    try:
        user = await auth_db_handler.update_user(user_id=user_id, user_edit_data=user_edit)

    except ServiceException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unknown error occurred")

    return User(**user.model_dump())


async def get_new_tokens(refresh_token: str) -> Token:
    return auth_utils.get_new_tokens(encrypted_refresh_token=refresh_token)


async def request_forgot_password_link(user_email: str):
    """
    Request the forgot password link

    The flow is to send an email to the user with a link to reset the password.
    The link should be a one-time link that expires after a certain time.

    the token would be stored in the redis cache.
    On the web app routing to the page, the token would be sent the backend and validated. Once validated, a token
    containing the user_id would be sent to the frontend and the rest password endpoint would have to supply the token

    """
    unique_token = nanoid.generate(size=15)  # Unique token to be put in the link

    try:
        user = await auth_db_handler.get_user_with_email(email=user_email)
    except NotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_200_OK, detail=f"Forgot password link send to {user_email} if it exists"
        )

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unknown error occurred")

    # The data would contain the user email.
    # Cache in redis
    data = {"user_email": user_email}
    redis_manager.cache_json_item(key=unique_token, value=data)

    # Send the email to the client
    payload = {
        "info": f"You Reset password link is here!",
        "more_info": f"It expires in 1 hour. Click the link below to reset your password.",
        "action_text": "Reset Password",
        "link": f"https://ai_health.com/reset_password/{unique_token}",
    }
    # job_runner.background_mailer(
    #     reciepients=[user_email],
    #     subject="Please conform your account for ai_health",
    #     payload=payload,
    #     template="auth/info_email_template.html",
    # )

    return ResponseInfo(details=f"Forgot password link send to {user_email} if it exists")


async def verify_reset_password_token(verify_password_token: str):
    """
    Verify the reset password token
    """
    data = redis_manager.get_cached_json_item(key=verify_password_token)

    if data is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Token is invalid")

    user_email = data.get("user_email", None)

    if user_email is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Token is invalid")

    # Delete the token from the redis cache
    redis_manager.delete_key(key=verify_password_token)

    # Since the email is verified now, get a an encrypted token to be sent to the user to rest the password
    data = {"user_email": user_email}
    token = auth_utils.create_jwt_token_for_reset_password(data=data)

    encrypted_token = auth_utils.encrypt_jwt_data(jwt_token=token)

    return VerifyRestPasswordToken(token=encrypted_token, details="Token verified")


async def reset_password(reset_password: ResetPassword):
    """
    Reset the password of the user
    """

    decrypted_token, message = auth_utils.decrypt_jwt_data(encrypted_jwt_token=reset_password.token)

    if decrypted_token is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=message)

    try:
        jwt_data = auth_utils.get_reset_password_token_data(token=decrypted_token)
    except ServiceException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unknown error occurred")

    user_email = jwt_data.get("user_email", None)
    password_hash = auth_utils.get_password_hash(password=reset_password.password)

    user_edit_data = UserEdit(**{"password": password_hash})

    try:
        user = await auth_db_handler.update_user(user_email=user_email, user_edit_data=user_edit_data)
    except ServiceException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unknown error occurred")

    return ResponseInfo(details="Password reset successfully!")

async def get_complete_user_details_by_id(user_id: str) -> User:
    """
    Get a user by id
    """
    try:
        user = await auth_db_handler.get_user_with_id_and_relations(user_id=user_id)
    except NotFoundException as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unknown error occurred")

    return user