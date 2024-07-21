from datetime import datetime
from pydantic import BaseModel, Field
from uuid import UUID
from typing import List, Optional

from ai_health.root.utils.base_models_abstract import AbstractModel


class MedicalHistoryBase(AbstractModel):
    patient_id: UUID
    condition: str
    diagnosis_date: datetime
    notes: str


class MedicalHistoryCreate(MedicalHistoryBase):
    pass


class MedicalHistoryUpdate(AbstractModel):
    patient_id: Optional[UUID] = None
    condition: Optional[str] = None
    diagnosis_date: Optional[datetime] = None
    notes: Optional[str] = None


class MedicalHistory(MedicalHistoryBase):
    history_id: UUID


class MedicalHistoryList(AbstractModel):
    detail: str
    medical_histories: List[MedicalHistory]
