from pydantic import BaseModel
from uuid import UUID
from typing import Optional
import enum

from ai_health.root.utils.base_models_abstract import AbstractModel
from ai_health.schemas.doctor_schema import Doctor

class BillingStatus(str, enum.Enum):
    PENDING = "PENDING"
    PAID = "PAID"
    NOT_PAID = "NOT_PAID"

class BillingBase(AbstractModel):
    title: str
    status: BillingStatus
    amount: float

class BillingCreate(BillingBase):
    doctor_id: UUID
    patient_id: UUID

class BillingUpdate(BaseModel):
    title: Optional[str] = None
    status: Optional[BillingStatus] = None
    amount: Optional[float] = None

class Billing(BillingBase):
    billing_id: UUID
    doctor_id: UUID


class BillingWithDoctor(Billing):
    doctor: Doctor

class BillingsWithDoctorList(BaseModel):
    detail: str = "Billings gotten"
    billings: list[BillingWithDoctor]