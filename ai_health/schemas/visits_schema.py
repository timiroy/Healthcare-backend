from datetime import datetime
from pydantic import BaseModel, Field
from uuid import UUID
from typing import List, Optional

from ai_health.root.utils.base_models_abstract import AbstractModel
from ai_health.schemas.doctor_schema import Doctor


class VisitBase(AbstractModel):
    patient_id: UUID
    visit_date: datetime
    reason_for_visit: str
    notes: str
    vistor_name: str
    visitor_relationship: str
    doctor_id: UUID


class VisitCreate(VisitBase):
    pass


class VisitUpdate(BaseModel):
    patient_id: Optional[UUID]
    visit_date: Optional[datetime]
    reason_for_visit: Optional[str]
    notes: Optional[str]
    vistor_name: Optional[str]
    visitor_relationship: Optional[str]
    doctor_id: Optional[UUID]


class Visit(VisitBase):
    visit_id: UUID


class VisitList(BaseModel):
    detail: str
    visits: List[Visit]

class VisitWithDoctor(Visit):
    doctor: Doctor