from datetime import datetime
from pydantic import BaseModel, Field
from uuid import UUID
from typing import List, Optional

from ai_health.root.utils.base_models_abstract import AbstractModel
from ai_health.schemas.doctor_schema import Doctor


class AppointmentBase(AbstractModel):
    patient_id: UUID
    doctor_id: UUID
    appointment_date: datetime
    reason_for_appointment: str
    status: str
    next_appointment_date: datetime


class AppointmentCreate(AppointmentBase):
    pass


class AppointmentUpdate(AbstractModel):
    doctor_id: Optional[UUID] = None
    appointment_date: Optional[datetime] = None
    reason: Optional[str] = None


class Appointment(AppointmentBase):
    appointment_id: UUID


class AppointmentList(BaseModel):
    detail: str
    appointments: List[Appointment]


class AppointmentFilter(BaseModel):
    doctor_id: Optional[UUID] = None
    patient_id: Optional[UUID] = None

class AppointmentWithDoctor(Appointment):
    doctor: Doctor


