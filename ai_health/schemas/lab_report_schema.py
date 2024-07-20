from datetime import datetime
from pydantic import BaseModel, Field
from uuid import UUID
from typing import List, Optional

class LabReportBase(BaseModel):
    patient_id: UUID
    report_name: str
    test_date: datetime
    result: str
    notes: str

class LabReportCreate(LabReportBase):
    pass

class LabReportUpdate(BaseModel):
    patient_id: Optional[UUID]
    report_name: Optional[str]
    test_date: Optional[datetime]
    result: Optional[str]
    notes: Optional[str]

class LabReport(LabReportBase):
    report_id: UUID

    class Config:
        orm_mode = True

class LabReportList(BaseModel):
    detail: str
    lab_reports: List[LabReport]
