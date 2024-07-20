from fastapi import APIRouter, Depends, HTTPException, status
from ai_health.schemas.medication_schema import (
    MedicationCreate,
    Medication,
    MedicationList,
    MedicationUpdate,
)
from ai_health.services import medications_service
from ai_health.services.utils.auth_utils import get_current_user
from ai_health.schemas.auth_schemas import User, UserType

medication_router = APIRouter(prefix="/medications", tags=["Medication Management"])


@medication_router.post("/", response_model=Medication)
async def create_medication(medication_create: MedicationCreate):
    return await medications_service.create_medication(medication_create)


@medication_router.get("/{medication_id}", response_model=Medication)
async def get_medication(medication_id: str):
    return await medications_service.get_medication_by_id(medication_id)


@medication_router.get("/", response_model=MedicationList)
async def get_all_medications():
    return await medications_service.get_all_medications()


@medication_router.patch("/{medication_id}", response_model=Medication)
async def update_medication(medication_id: str, medication_update: MedicationUpdate):
    return await medications_service.update_medication(medication_id, medication_update)


@medication_router.delete("/{medication_id}")
async def delete_medication(medication_id: str):
    return await medications_service.delete_medication(medication_id)
