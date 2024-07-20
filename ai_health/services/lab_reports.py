import logging
from datetime import datetime, timezone
from fastapi import HTTPException, status

from ai_health.schemas.lab_report_schema import LabReportCreate, LabReportUpdate, LabReport, LabReportList
from ai_health.database.db_handlers import labreports_db_handler
from ai_health.services.utils.exceptions import RecordExistsException, ServiceException, NotFoundException

LOGGER = logging.getLogger(__name__)


async def create_lab_report(lab_report_create: LabReportCreate):
    try:
        created_lab_report = await labreports_db_handler.create_lab_report(lab_report_create)
    except RecordExistsException as e:
        LOGGER.error(f"Duplicate record found for lab report {lab_report_create.patient_id}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except ServiceException as e:
        LOGGER.exception(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    except Exception as e:
        LOGGER.exception(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unknown error occurred")

    return LabReport(**created_lab_report.model_dump())


async def get_lab_report_by_id(lab_report_id: str):
    try:
        lab_report = await labreports_db_handler.get_lab_report(lab_report_id)
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ServiceException as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    except Exception as e:
        LOGGER.exception(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unknown error occurred")

    return LabReport(**lab_report.model_dump())


async def get_all_lab_reports():
    try:
        lab_reports = await labreports_db_handler.get_lab_reports()
    except ServiceException as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    except Exception as e:
        LOGGER.exception(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unknown error occurred")

    return LabReportList(lab_reports=[LabReport(**lab_report.model_dump()) for lab_report in lab_reports])


async def update_lab_report(lab_report_id: str, lab_report_update: LabReportUpdate):
    try:
        updated_lab_report = await labreports_db_handler.update_lab_report(lab_report_id, lab_report_update)
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ServiceException as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    except Exception as e:
        LOGGER.exception(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unknown error occurred")

    return LabReport(**updated_lab_report.model_dump())


async def delete_lab_report(lab_report_id: str):
    try:
        success = await labreports_db_handler.delete_lab_report(lab_report_id)
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ServiceException as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    except Exception as e:
        LOGGER.exception(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unknown error occurred")

    return {"deleted": success}
