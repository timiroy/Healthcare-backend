from fastapi import APIRouter, Depends, HTTPException, status
from ai_health.schemas.medical_history_schema import (
    MedicalHistoryCreate,
    MedicalHistory,
    MedicalHistoryList,
    MedicalHistoryUpdate,
)
from ai_health.services import medical_history_service
from ai_health.services.utils.auth_utils import get_current_user
from ai_health.schemas.auth_schemas import User, UserType

medical_history_router = APIRouter(prefix="/medical_history", tags=["Medical History Management"])


@medical_history_router.post("/", response_model=MedicalHistory)
async def create_medical_history(medical_history_create: MedicalHistoryCreate, user: User = Depends(get_current_user)):
    return await medical_history_service.create_medical_history(medical_history_create)


@medical_history_router.get("/{medical_history_id}", response_model=MedicalHistory)
async def get_medical_history(medical_history_id: str, user: User = Depends(get_current_user)):
    return await medical_history_service.get_medical_history_by_id(medical_history_id)


@medical_history_router.get("/", response_model=MedicalHistoryList)
async def get_all_medical_histories(user: User = Depends(get_current_user)):
    return await medical_history_service.get_all_medical_histories()


@medical_history_router.patch("/{medical_history_id}", response_model=MedicalHistory)
async def update_medical_history(
    medical_history_id: str, medical_history_update: MedicalHistoryUpdate, user: User = Depends(get_current_user)
):
    return await medical_history_service.update_medical_history(medical_history_id, medical_history_update)


@medical_history_router.delete("/{medical_history_id}")
async def delete_medical_history(medical_history_id: str, user: User = Depends(get_current_user)):
    return await medical_history_service.delete_medical_history(medical_history_id)
