from datetime import datetime
from pydantic import BaseModel, Field
from uuid import UUID
from typing import List, Optional

class AppointmentBase(BaseModel):
    patient_id: UUID
    doctor_id: UUID
    appointment_date: datetime
    reason: str

class AppointmentCreate(AppointmentBase):
    pass

class AppointmentUpdate(BaseModel):
    doctor_id: Optional[UUID]
    appointment_date: Optional[datetime]
    reason: Optional[str]

class Appointment(AppointmentBase):
    appointment_id: UUID

    class Config:
        orm_mode = True

class AppointmentList(BaseModel):
    detail: str
    appointments: List[Appointment]
