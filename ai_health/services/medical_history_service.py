import logging
from datetime import datetime, timezone
from fastapi import HTTPException, status

from ai_health.schemas.medical_history_schema import (
    MedicalHistoryCreate,
    MedicalHistoryUpdate,
    MedicalHistory,
    MedicalHistoryList,
)
from ai_health.database.db_handlers import medical_history_db_handler
from ai_health.services.utils.exceptions import RecordExistsException, ServiceException, NotFoundException

LOGGER = logging.getLogger(__name__)


async def create_medical_history(medical_history_create: MedicalHistoryCreate):
    try:
        created_medical_history = await medical_history_db_handler.create_medical_history(medical_history_create)
    except RecordExistsException as e:
        LOGGER.error(f"Duplicate record found for medical history {medical_history_create.patient_id}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except ServiceException as e:
        LOGGER.exception(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    except Exception as e:
        LOGGER.exception(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unknown error occurred")

    return MedicalHistory(**created_medical_history.model_dump())


async def get_medical_history_by_id(medical_history_id: str):
    try:
        medical_history = await medical_history_db_handler.get_medical_history(medical_history_id)
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ServiceException as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    except Exception as e:
        LOGGER.exception(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unknown error occurred")

    return MedicalHistory(**medical_history.model_dump())


async def get_all_medical_histories():
    try:
        medical_histories = await medical_history_db_handler.get_medical_histories()
    except ServiceException as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    except Exception as e:
        LOGGER.exception(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unknown error occurred")

    return medical_histories


async def update_medical_history(medical_history_id: str, medical_history_update: MedicalHistoryUpdate):
    try:
        updated_medical_history = await medical_history_db_handler.update_medical_history(
            medical_history_id, medical_history_update
        )
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ServiceException as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    except Exception as e:
        LOGGER.exception(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unknown error occurred")

    return MedicalHistory(**updated_medical_history.model_dump())


async def delete_medical_history(medical_history_id: str):
    try:
        success = await medical_history_db_handler.delete_medical_history(medical_history_id)
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ServiceException as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    except Exception as e:
        LOGGER.exception(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unknown error occurred")

    return {"deleted": success}
