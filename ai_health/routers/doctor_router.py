from fastapi import APIRouter, Depends, HTTPException, status
from uuid import UUID
from ai_health.schemas.doctor_schema import DoctorCreate, DoctorUpdate, Doctor, DoctorList
from ai_health.services import doctor_service
from ai_health.services.utils.auth_utils import get_current_user
from ai_health.schemas.auth_schemas import User, UserType

doctor_router = APIRouter(prefix="/doctors", tags=["Doctor Management"])


@doctor_router.post("/", response_model=Doctor)
async def create_doctor(doctor_create: DoctorCreate, user: User = Depends(get_current_user)):
    # if user.user_type != UserType.ADMIN:
    #     raise HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN, detail="You do not have permission to access this resource"
    #     )
    return await doctor_service.create_doctor(doctor_create)


@doctor_router.get("/{doctor_id}", response_model=Doctor)
async def get_doctor(doctor_id: UUID, user: User = Depends(get_current_user)):
    return await doctor_service.get_doctor(doctor_id)


@doctor_router.patch("/{doctor_id}", response_model=Doctor)
async def update_doctor(doctor_id: UUID, doctor_update: DoctorUpdate, user: User = Depends(get_current_user)):
    # if user.user_type != UserType.ADMIN:
    #     raise HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN, detail="You do not have permission to access this resource"
    #     )
    return await doctor_service.update_doctor(doctor_id, doctor_update)


@doctor_router.delete("/{doctor_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_doctor(doctor_id: UUID, user: User = Depends(get_current_user)):
    # if user.user_type != UserType.ADMIN:
    #     raise HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN, detail="You do not have permission to access this resource"
    #     )
    await doctor_service.delete_doctor(doctor_id)


@doctor_router.get("/", response_model=DoctorList)
async def get_all_doctors(user: User = Depends(get_current_user)):
    # if user.user_type != UserType.ADMIN:
    #     raise HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN, detail="You do not have permission to access this resource"
    #     )
    return await doctor_service.get_all_doctors()
