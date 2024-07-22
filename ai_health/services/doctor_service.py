import logging
from uuid import UUID
from fastapi import HTTPException, status
from typing import List
from ai_health.schemas.doctor_schema import DoctorCreate, DoctorUpdate, Doctor, DoctorList
from ai_health.database.db_handlers import doctor_db_handler
from ai_health.services.utils.exceptions import RecordExistsException, ServiceException

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)


async def create_doctor(doctor_create: DoctorCreate) -> Doctor:
    try:
        doctor_in_db = await doctor_db_handler.create_doctor(doctor_create)
    except RecordExistsException:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Doctor already exists")
    except ServiceException as e:
        LOGGER.error(f"Service exception: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)
    except Exception as e:
        LOGGER.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="An unknown error occurred")

    return Doctor.model_validate(doctor_in_db)


async def get_doctor(doctor_id: UUID) -> Doctor:
    try:
        doctor_in_db = await doctor_db_handler.get_doctor_by_id(doctor_id)
        if not doctor_in_db:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Doctor not found")
    except ServiceException as e:
        LOGGER.error(f"Service exception: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)
    except Exception as e:
        LOGGER.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="An unknown error occurred")

    return Doctor.model_validate(doctor_in_db)


async def update_doctor(doctor_id: UUID, doctor_update: DoctorUpdate) -> Doctor:
    try:
        doctor_in_db = await doctor_db_handler.update_doctor(doctor_id, doctor_update)
        if not doctor_in_db:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Doctor not found")
    except ServiceException as e:
        LOGGER.error(f"Service exception: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)
    except Exception as e:
        LOGGER.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="An unknown error occurred")

    return Doctor.model_validate(doctor_in_db)


async def delete_doctor(doctor_id: UUID) -> None:
    try:
        await doctor_db_handler.delete_doctor(doctor_id)
    except ServiceException as e:
        LOGGER.error(f"Service exception: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)
    except Exception as e:
        LOGGER.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="An unknown error occurred")


async def get_all_doctors() -> DoctorList:
    try:
        doctors = await doctor_db_handler.get_all_doctors()
    except ServiceException as e:
        LOGGER.error(f"Service exception: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)
    except Exception as e:
        LOGGER.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="An unknown error occurred")

    return DoctorList(doctors=[Doctor.model_validate(doctor) for doctor in doctors])
