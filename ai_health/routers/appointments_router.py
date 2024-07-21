from fastapi import APIRouter, Depends, HTTPException, status
from ai_health.schemas.appointment_schema import (
    AppointmentCreate,
    Appointment,
    AppointmentFilter,
    AppointmentList,
    AppointmentUpdate,
)
from ai_health.services import appointments_service
from ai_health.services.utils.auth_utils import get_current_user
from ai_health.schemas.auth_schemas import User, UserType

appointment_router = APIRouter(prefix="/appointments", tags=["Appointment Management"])


@appointment_router.post("/", response_model=Appointment)
async def create_appointment(appointment_create: AppointmentCreate, user: User = Depends(get_current_user)):
    return await appointments_service.create_appointment(appointment_create)


@appointment_router.get("/{appointment_id}", response_model=Appointment)
async def get_appointment(appointment_id: str, user: User = Depends(get_current_user)):
    return await appointments_service.get_appointment_by_id(appointment_id)


@appointment_router.get("/", response_model=AppointmentList)
async def get_all_appointments(
    filter: AppointmentFilter = Depends(AppointmentFilter), user: User = Depends(get_current_user)
):
    return await appointments_service.get_all_appointments(**filter.model_dump())


@appointment_router.patch("/{appointment_id}", response_model=Appointment)
async def update_appointment(
    appointment_id: str, appointment_update: AppointmentUpdate, user: User = Depends(get_current_user)
):
    return await appointments_service.update_appointment(appointment_id, appointment_update)


@appointment_router.delete("/{appointment_id}")
async def delete_appointment(appointment_id: str, user: User = Depends(get_current_user)):
    return await appointments_service.delete_appointment(appointment_id)
