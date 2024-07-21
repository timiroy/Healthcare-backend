from datetime import datetime
from pydantic import BaseModel, Field
from uuid import UUID
from typing import List, Optional

from ai_health.root.utils.base_models_abstract import AbstractModel


class LabReportBase(AbstractModel):
    patient_id: UUID
    test_name: str
    test_date: datetime
    result: str
    notes: str


class LabReportCreate(LabReportBase):
    pass


class LabReportUpdate(AbstractModel):
    patient_id: Optional[UUID] = None
    report_name: Optional[str] = None
    test_date: Optional[datetime] = None
    result: Optional[str] = None
    notes: Optional[str] = None


class LabReport(LabReportBase):
    report_id: UUID


class LabReportList(BaseModel):
    detail: str
    lab_reports: List[LabReport]
