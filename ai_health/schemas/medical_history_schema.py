from datetime import datetime
from pydantic import BaseModel, Field
from uuid import UUID
from typing import List, Optional

class MedicalHistoryBase(BaseModel):
    patient_id: UUID
    condition: str
    diagnosis_date: datetime
    treatment: str
    outcome: str

class MedicalHistoryCreate(MedicalHistoryBase):
    pass

class MedicalHistoryUpdate(BaseModel):
    patient_id: Optional[UUID]
    condition: Optional[str]
    diagnosis_date: Optional[datetime]
    treatment: Optional[str]
    outcome: Optional[str]

class MedicalHistory(MedicalHistoryBase):
    history_id: UUID

    class Config:
        orm_mode = True

class MedicalHistoryList(BaseModel):
    detail: str
    medical_histories: List[MedicalHistory]
