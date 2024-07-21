from datetime import datetime
from pydantic import BaseModel, Field
from uuid import UUID
from typing import List, Optional

from ai_health.root.utils.base_models_abstract import AbstractModel


class MedicationBase(AbstractModel):
    patient_id: UUID
    medication_name: str
    dosage: str
    start_date: datetime
    end_date: datetime
    doctor_id: UUID


class MedicationCreate(MedicationBase):
    pass


class MedicationUpdate(AbstractModel):
    name: Optional[str]
    dosage: Optional[str]
    start_date: Optional[datetime]
    end_date: Optional[datetime]
    prescribed_by: Optional[UUID]


class Medication(MedicationBase):
    medication_id: UUID


class MedicationList(BaseModel):
    detail: str
    medications: List[Medication]

class MedicationFilter(BaseModel):
    doctor_id: Optional[UUID] = None
    patient_id: Optional[UUID] = None
