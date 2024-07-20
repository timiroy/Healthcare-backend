from datetime import datetime
from enum import Enum, StrEnum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr

from ai_health.root.utils.base_models_abstract import AbstractModel


class UserType(StrEnum):
    founder = "FOUNDER"
    investor = "INVESTOR"
    job_seeker = "JOB_SEEKER"
    admin = "ADMIN"


class UserBase(AbstractModel):
    first_name: str
    last_name: str
    user_type: UserType
    phone_number: str
    email: EmailStr
    profile_image: str | None = None


class Login(AbstractModel):
    email: EmailStr
    password: str


class Token(AbstractModel):
    access_token: str
    refresh_token: str


class SignUpUser(Login, UserBase):
    pass


class User(UserBase):
    # Todo: add company field for founders
    is_verified: bool = False
    user_id: UUID
    # date_created: datetime
    # date_updated: datetime


class UserCreate(UserBase):
    password: str  # Hashed password
    date_created: datetime
    is_verified: bool = False


class UserExtended(UserCreate):
    date_updated: datetime
    user_id: UUID



class UserEditBase(AbstractModel):
    first_name: str | None = None
    last_name: str | None = None
    phone_number: str | None = None
    profile_image: str | None = None


class UserEdit(UserEditBase):
    is_verified: bool | None = None
    password: str | None = None


class SigninResponse(AbstractModel):
    token: Token
    user: User


class VerifyRestPasswordToken(AbstractModel):
    token: str
    details: str


class ResetPassword(AbstractModel):
    password: str
    token: str
