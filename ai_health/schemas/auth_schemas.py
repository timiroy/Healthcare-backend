from datetime import datetime
from enum import Enum, StrEnum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr

from ai_health.root.utils.base_models_abstract import AbstractModel
from ai_health.schemas.appointment_schema import Appointment, AppointmentWithDoctor
from ai_health.schemas.lab_report_schema import LabReport
from ai_health.schemas.medical_history_schema import MedicalHistory
from ai_health.schemas.medication_schema import Medication, MedicationWithDoctor
from ai_health.schemas.visits_schema import Visit, VisitWithDoctor


class UserType(StrEnum):
    PATIENT = "PATIENT"
    ADMIN = "ADMIN"


class UserBase(AbstractModel):
    first_name: str
    last_name: str
    user_type: UserType
    phone_number: str
    email: EmailStr
    profile_image: str | None = None
    date_of_birth: datetime
    gender: str
    address: str


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

class UserWithAllRelations(User):
    visits: list["VisitWithDoctor"]
    medications: list["MedicationWithDoctor"]
    appointments: list["AppointmentWithDoctor"]
    lab_reports: list["LabReport"]
    medical_history: list["MedicalHistory"]