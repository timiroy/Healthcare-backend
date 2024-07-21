from pydantic import BaseModel, EmailStr, UUID4
from typing import List, Optional

from ai_health.root.utils.base_models_abstract import AbstractModel


class DoctorBase(AbstractModel):
    first_name: str
    last_name: str
    specialty: str
    contact_number: str
    email: EmailStr


class DoctorCreate(DoctorBase):
    pass


class DoctorUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    specialty: Optional[str] = None
    contact_number: Optional[str] = None


class Doctor(DoctorBase):
    doctor_id: UUID4


class DoctorList(BaseModel):
    doctors: List[Doctor]
