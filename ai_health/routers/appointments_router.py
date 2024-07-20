from fastapi import APIRouter, Depends, HTTPException, status
from ai_health.schemas.appointment_schema import (
    AppointmentCreate,
    Appointment,
    AppointmentList,
    AppointmentUpdate,
)
from ai_health.services import appointments_service
from ai_health.services.utils.auth_utils import get_current_user
from ai_health.schemas.auth_schemas import User, UserType

appointment_router = APIRouter(prefix="/appointments", tags=["Appointment Management"])


@appointment_router.post("/", response_model=Appointment)
async def create_appointment(appointment_create: AppointmentCreate):
    return await appointments_service.create_appointment(appointment_create)


@appointment_router.get("/{appointment_id}", response_model=Appointment)
async def get_appointment(appointment_id: str):
    return await appointments_service.get_appointment_by_id(appointment_id)


@appointment_router.get("/", response_model=AppointmentList)
async def get_all_appointments():
    return await appointments_service.get_all_appointments()


@appointment_router.patch("/{appointment_id}", response_model=Appointment)
async def update_appointment(appointment_id: str, appointment_update: AppointmentUpdate):
    return await appointments_service.update_appointment(appointment_id, appointment_update)


@appointment_router.delete("/{appointment_id}")
async def delete_appointment(appointment_id: str):
    return await appointments_service.delete_appointment(appointment_id)
