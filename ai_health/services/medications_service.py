import logging
from datetime import datetime, timezone
from fastapi import HTTPException, status

from ai_health.schemas.medication_schema import MedicationCreate, MedicationUpdate, Medication, MedicationList
from ai_health.database.db_handlers import medications_db_handler
from ai_health.services.utils.exceptions import RecordExistsException, ServiceException, NotFoundException

LOGGER = logging.getLogger(__name__)


async def create_medication(medication_create: MedicationCreate):
    try:
        created_medication = await medications_db_handler.create_medication(medication_create)
    except RecordExistsException as e:
        LOGGER.error(f"Duplicate record found for medication {medication_create.name}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except ServiceException as e:
        LOGGER.exception(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    except Exception as e:
        LOGGER.exception(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unknown error occurred")

    return Medication(**created_medication.model_dump())


async def get_medication_by_id(medication_id: str):
    try:
        medication = await medications_db_handler.get_medication(medication_id)
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ServiceException as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    except Exception as e:
        LOGGER.exception(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unknown error occurred")

    return Medication(**medication.model_dump())


async def get_all_medications(patient_id: str = None, doctor_id: str = None):
    try:
        medications = await medications_db_handler.get_medications(patient_id=patient_id, doctor_id=doctor_id)
    except ServiceException as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    except Exception as e:
        LOGGER.exception(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unknown error occurred")

    return medications


async def update_medication(medication_id: str, medication_update: MedicationUpdate):
    try:
        updated_medication = await medications_db_handler.update_medication(medication_id, medication_update)
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ServiceException as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    except Exception as e:
        LOGGER.exception(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unknown error occurred")

    return Medication(**updated_medication.model_dump())


async def delete_medication(medication_id: str):
    try:
        success = await medications_db_handler.delete_medication(medication_id)
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ServiceException as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    except Exception as e:
        LOGGER.exception(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unknown error occurred")

    return {"deleted": success}
