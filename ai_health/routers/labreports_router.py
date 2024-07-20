from fastapi import APIRouter, Depends, HTTPException, status
from ai_health.schemas.lab_report_schema import (
    LabReportCreate,
    LabReport,
    LabReportList,
    LabReportUpdate,
)
from ai_health.services import lab_reports
from ai_health.services.utils.auth_utils import get_current_user
from ai_health.schemas.auth_schemas import User, UserType

lab_report_router = APIRouter(prefix="/lab_reports", tags=["Lab Report Management"])


@lab_report_router.post("/", response_model=LabReport)
async def create_lab_report(lab_report_create: LabReportCreate):
    return await lab_reports.create_lab_report(lab_report_create)


@lab_report_router.get("/{lab_report_id}", response_model=LabReport)
async def get_lab_report(lab_report_id: str):
    return await lab_reports.get_lab_report_by_id(lab_report_id)


@lab_report_router.get("/", response_model=LabReportList)
async def get_all_lab_reports():
    return await lab_reports.get_all_lab_reports()


@lab_report_router.patch("/{lab_report_id}", response_model=LabReport)
async def update_lab_report(lab_report_id: str, lab_report_update: LabReportUpdate):
    return await lab_reports.update_lab_report(lab_report_id, lab_report_update)


@lab_report_router.delete("/{lab_report_id}")
async def delete_lab_report(lab_report_id: str):
    return await lab_reports.delete_lab_report(lab_report_id)
