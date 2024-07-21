from datetime import datetime, timedelta
import json
from logging import getLogger
from random import randint
from typing import Annotated, Optional
from uuid import UUID

from fastapi import Depends, HTTPException, status
import jwt
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext
from itsdangerous.url_safe import URLSafeSerializer
from itsdangerous import BadTimeSignature, BadSignature


from ai_health.root.settings import Settings
from ai_health.schemas.auth_schemas import Token, User, UserType
from ai_health.schemas.error_messages_schema import AuthMessage
from ai_health.services.utils.exceptions import NotFoundException, ServiceException
from ai_health.database.db_handlers import auth_db_handler


settings = Settings()

ENCODE_ALGORITHM = settings.JWT_ALGORITHM
ACCESS_TOKEN_SECRET = settings.ACCESS_TOKEN_SECRET
REFRESH_TOKEN_SECRET = settings.REFRESH_TOKEN_SECRET
ACCESS_TOKEN_EXPIRY = 26 * 60 * 60  # 1 Day
REFRESH_TOKEN_EXPIRY = 24 * 60 * 60 * 14  # 2 Weeks

RESET_PASSWORD_TOKEN_EXPIRY = 60 * 60  # 1 hour

RESET_PASSWORD_SECRET = settings.RESET_PASSWORD_SECRET


ITS_DANGEROUS_SECRET = settings.SECRET_KEY

Logger = getLogger(__name__)


prototype_pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

security = HTTPBearer()


class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            # if the obj is uuid, we simply return the value of uuid
            return obj.hex
        return json.JSONEncoder.default(self, obj)


def credential_exception(
    message: str = "Could not validate credentials", request_status: int = status.HTTP_401_UNAUTHORIZED
):

    raise HTTPException(
        status_code=request_status,
        detail=message,
        headers={"WWW-Authenticate": "Bearer"},
    )


def encrypt_jwt_data(jwt_token: str) -> str:
    s1 = URLSafeSerializer(ITS_DANGEROUS_SECRET)

    token = s1.dumps(jwt_token)

    return token


def decrypt_jwt_data(encrypted_jwt_token: str) -> (str | None, str):
    """
    Decodes the string.

    Returns (str | None, str)
    it is (str, str) if the token was successfully decoded

    it is (None, str) if the token was unsuccessful
    """

    s1 = URLSafeSerializer(ITS_DANGEROUS_SECRET)

    try:
        token = s1.loads(encrypted_jwt_token)
    except BadTimeSignature as e:
        Logger.exception(e)
        return None, "Invalid Token"

    except BadSignature as e:
        Logger.exception(e)
        return None, "Invalid Token"

    except Exception as e:
        Logger.info(f"An exception occurred {e}")

        return None, "An unknown error occurred"

    return token, ""


def verify_password(plain_password, hashed_password):
    """
    Verifies the supplied password with the hashed password
    """
    return prototype_pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    """
    Generates the hash for a password
    """
    return prototype_pwd_context.hash(password)


def create_access_token(data: dict):
    expiry_date = timedelta(seconds=ACCESS_TOKEN_EXPIRY) + datetime.utcnow()
    data.update({"exp": expiry_date})

    token = jwt.encode(data, settings.ACCESS_TOKEN_SECRET, algorithm=ENCODE_ALGORITHM, json_encoder=UUIDEncoder)
    return token


def create_jwt_token_for_reset_password(data: dict):
    expiry_date = timedelta(seconds=RESET_PASSWORD_TOKEN_EXPIRY) + datetime.utcnow()
    data.update({"exp": expiry_date})

    token = jwt.encode(data, settings.RESET_PASSWORD_SECRET, algorithm=ENCODE_ALGORITHM, json_encoder=UUIDEncoder)
    return token


def create_refresh_token(data: dict):
    expiry_date = timedelta(seconds=REFRESH_TOKEN_EXPIRY) + datetime.utcnow()
    data.update({"exp": expiry_date})

    token = jwt.encode(data, settings.REFRESH_TOKEN_SECRET, algorithm=ENCODE_ALGORITHM, json_encoder=UUIDEncoder)
    return token


def get_access_token_data(token: str) -> Optional[dict]:
    """
    Gets the data that is stored in the access token
    """

    try:
        data = jwt.decode(token, ACCESS_TOKEN_SECRET, algorithms=ENCODE_ALGORITHM)
    except jwt.ExpiredSignatureError:

        Logger.info("Token is Expired")
        raise ServiceException(message=AuthMessage.token_expired)
    except jwt.InvalidTokenError:
        Logger.info("Token is invalid")
        raise ServiceException(message=AuthMessage.error_with_token)

    except Exception as e:
        Logger.info(f"Error {e} occurred!")
        raise ServiceException(message="Token is expired")

    return data


def get_reset_password_token_data(token: str) -> Optional[dict]:
    """
    Gets the data that is stored in the access token
    """

    try:
        data = jwt.decode(token, RESET_PASSWORD_SECRET, algorithms=ENCODE_ALGORITHM)
    except jwt.ExpiredSignatureError:

        Logger.info("Token is Expired")
        raise ServiceException(message=AuthMessage.token_expired)
    except jwt.InvalidTokenError:
        Logger.info("Token is invalid")
        raise ServiceException(message=AuthMessage.error_with_token)

    except Exception as e:
        Logger.info(f"Error {e} occurred!")
        raise ServiceException(message="Token is expired")

    return data


def get_refresh_token_data(token: str) -> Optional[dict]:

    try:
        data = jwt.decode(token, REFRESH_TOKEN_SECRET, algorithms=ENCODE_ALGORITHM)
    except jwt.ExpiredSignatureError:
        Logger.info("Token is Expired")
        raise ServiceException(message=AuthMessage.token_expired)
    except jwt.InvalidTokenError:
        Logger.info("Token is invalid")
        raise ServiceException(message=AuthMessage.error_with_token)

    except Exception as e:
        Logger.info(f"Error {e} occurred!")
        raise ServiceException(message="Token is expired")

    return data


def get_token_data_from_data(data: dict) -> Token:
    access_token = create_access_token(data=data)
    refresh_token = create_refresh_token(data=data)

    encrypted_access_token = encrypt_jwt_data(jwt_token=access_token)
    encrypted_refresh_token = encrypt_jwt_data(jwt_token=refresh_token)

    return Token(
        **{
            "access_token": encrypted_access_token,
            "refresh_token": encrypted_refresh_token,
        }
    )


def get_new_tokens(encrypted_refresh_token: str) -> Token:

    _refresh_token, message = decrypt_jwt_data(encrypted_jwt_token=encrypted_refresh_token)

    if _refresh_token is None:
        credential_exception(message=message)

    # The token has been gotten
    # Get the payload
    try:
        payload = get_refresh_token_data(token=_refresh_token)
    except ServiceException as e:
        credential_exception(message=e.message)

    # Double check to be sure that the payload has been gotten
    if payload is None:
        credential_exception()

    user_id = payload.get("user_id")

    data = {"user_id": user_id}

    return get_token_data_from_data(data=data)


async def verify_access_token(encrypted_token: str):

    # Unencrypt the token
    token, message = decrypt_jwt_data(encrypted_jwt_token=encrypted_token)

    if token is None:
        credential_exception(message=message)

    # The token has been gotten
    # Get the payload
    try:
        payload = get_access_token_data(token=token)
    except ServiceException as e:
        credential_exception(message=e.message)

    # Double check to be sure that the oayload has been gotten
    if payload is None:
        credential_exception()

    user_id = payload.get("user_id")

    return user_id


async def extract_token(credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)]):

    if not credentials.credentials:
        credential_exception()

    return await verify_access_token(encrypted_token=credentials.credentials)


async def get_current_user(user_id: str = Depends(extract_token)):
    # Get the user details from the user id

    return await _get_user_from_user_id(user_id=user_id)


async def _get_user_from_user_id(user_id: str):
    """
    An abstraction over the get_user_from_userid of the auth_db_handler

    Gets the user details from the db and populates needed fields for the user
    """
    try:
        user_extended = await auth_db_handler.get_user_with_user_id(user_id=user_id)
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    user = User(**user_extended.model_dump())

    return user


async def _get_user_from_email(email: str):
    """
    An abstraction over the get_user_from_email of the auth_db_handler

    Gets the user details from the db and populates needed fields for the user
    """

    user_extended = await auth_db_handler.get_user_with_email(email=email)

    user = User(user_extended.model_dump())

    if user.user_type == UserType.founder:
        # Fetch company details and add it here
        pass

    return user
