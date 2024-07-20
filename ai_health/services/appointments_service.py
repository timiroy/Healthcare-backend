import logging
from datetime import datetime, timezone
from fastapi import HTTPException, status

from ai_health.schemas.appointment_schema import AppointmentCreate, AppointmentUpdate, Appointment, AppointmentList
from ai_health.database.db_handlers import appointments_db_handler
from ai_health.services.utils.exceptions import RecordExistsException, ServiceException, NotFoundException

LOGGER = logging.getLogger(__name__)


async def create_appointment(appointment_create: AppointmentCreate):
    try:
        created_appointment = await appointments_db_handler.create_appointment(appointment_create)
    except RecordExistsException as e:
        LOGGER.error(f"Duplicate record found for appointment {appointment_create.patient_id}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except ServiceException as e:
        LOGGER.exception(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    except Exception as e:
        LOGGER.exception(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unknown error occurred")

    return Appointment(**created_appointment.model_dump())


async def get_appointment_by_id(appointment_id: str):
    try:
        appointment = await appointments_db_handler.get_appointment(appointment_id)
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ServiceException as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    except Exception as e:
        LOGGER.exception(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unknown error occurred")

    return Appointment(**appointment.model_dump())


async def get_all_appointments():
    try:
        appointments = await appointments_db_handler.get_appointments()
    except ServiceException as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    except Exception as e:
        LOGGER.exception(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unknown error occurred")

    return appointments


async def update_appointment(appointment_id: str, appointment_update: AppointmentUpdate):
    try:
        updated_appointment = await appointments_db_handler.update_appointment(appointment_id, appointment_update)
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ServiceException as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    except Exception as e:
        LOGGER.exception(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unknown error occurred")

    return Appointment(**updated_appointment.model_dump())


async def delete_appointment(appointment_id: str):
    try:
        success = await appointments_db_handler.delete_appointment(appointment_id)
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ServiceException as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    except Exception as e:
        LOGGER.exception(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unknown error occurred")

    return {"deleted": success}
