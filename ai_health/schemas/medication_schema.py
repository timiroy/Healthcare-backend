from datetime import datetime
from pydantic import BaseModel, Field
from uuid import UUID
from typing import List, Optional

from ai_health.root.utils.base_models_abstract import AbstractModel


class MedicationBase(AbstractModel):
    patient_id: UUID
    name: str
    dosage: str
    frequency: str
    start_date: datetime
    end_date: datetime
    prescribed_by: UUID


class MedicationCreate(MedicationBase):
    pass


class MedicationUpdate(AbstractModel):
    name: Optional[str]
    dosage: Optional[str]
    frequency: Optional[str]
    start_date: Optional[datetime]
    end_date: Optional[datetime]
    prescribed_by: Optional[UUID]


class Medication(MedicationBase):
    medication_id: UUID


class MedicationList(BaseModel):
    detail: str
    medications: List[Medication]
