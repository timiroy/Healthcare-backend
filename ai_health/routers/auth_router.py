from typing import Annotated
from fastapi import APIRouter, Body, Depends
from ai_health.schemas.auth_schemas import (
    Login,
    ResetPassword,
    SignUpUser,
    SigninResponse,
    Token,
    User,
    UserEdit,
    UserEditBase,
    UserWithAllRelations,
    VerifyRestPasswordToken,
)
from ai_health.schemas.response_info_schema import ResponseInfo
from ai_health.services import auth_services
from ai_health.services.utils import auth_utils


auth_router = APIRouter(prefix="/auth", tags=["Authentication"])


@auth_router.post("/signup", response_model=Token)
async def signup(signup_data: SignUpUser):
    return await auth_services.signup(signup_user=signup_data)


@auth_router.post("/signin", response_model=SigninResponse)
async def signin(signin_data: Login):
    return await auth_services.signin(login_data=signin_data)


@auth_router.patch("/update", response_model=User)
async def update_user(user_edit_data: UserEditBase, user: User = Depends(auth_utils.get_current_user)):
    return await auth_services.update_user_details(user_id=user.user_id, user_edit_data=user_edit_data)


@auth_router.post("/verify-account", response_model=ResponseInfo)
async def verify_otp(email: str = Body(), otp: str = Body()):
    return await auth_services.verify_account_verification_otp(otp=otp, user_email=email)


@auth_router.post("/request-otp", response_model=ResponseInfo)
async def resend_verification_otp(email: str = Body(embed=True)):
    return await auth_services.resend_verification_otp(user_email=email)


@auth_router.get("/me", response_model=UserWithAllRelations)
async def me(user: User = Depends(auth_utils.get_current_user)):
    return await auth_services.get_complete_user_details_by_id(user_id=user.user_id)


@auth_router.post("/refresh-token", response_model=Token)
async def refresh_token(refresh_token: str = Body(embed=True)):
    return await auth_services.get_new_tokens(refresh_token=refresh_token)


@auth_router.post("/request-forgot-password", response_model=ResponseInfo)
async def request_forgot_password(email: str = Body(embed=True)):
    return await auth_services.request_forgot_password_link(user_email=email)


@auth_router.post("/verify-reset-password", response_model=VerifyRestPasswordToken)
async def verify_reset_password_token(token: str = Body(embed=True)):
    return await auth_services.verify_reset_password_token(verify_password_token=token)


@auth_router.post("/reset-password", response_model=ResponseInfo)
async def reset_password(reset_password: ResetPassword):
    return await auth_services.reset_password(reset_password=reset_password)
