import logging
from datetime import datetime, timezone
from fastapi import HTTPException, status

from ai_health.schemas.visits_schema import VisitCreate, VisitUpdate, Visit, VisitList
from ai_health.database.db_handlers import visits_db_handler
from ai_health.services.utils.exceptions import RecordExistsException, ServiceException, NotFoundException

LOGGER = logging.getLogger(__name__)


async def create_visit(visit_create: VisitCreate):
    try:
        created_visit = await visits_db_handler.create_visit(visit_create)
    except RecordExistsException as e:
        LOGGER.error(f"Duplicate record found for visit {visit_create.patient_id}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except ServiceException as e:
        LOGGER.exception(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    except Exception as e:
        LOGGER.exception(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unknown error occurred")

    return Visit.model_validate(created_visit)


async def get_visit_by_id(visit_id: str):
    try:
        visit = await visits_db_handler.get_visit(visit_id)
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ServiceException as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    except Exception as e:
        LOGGER.exception(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unknown error occurred")

    return Visit.model_validate(visit)


async def get_all_visits():
    try:
        visits = await visits_db_handler.get_visits()
    except ServiceException as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    except Exception as e:
        LOGGER.exception(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unknown error occurred")

    return visits


async def update_visit(visit_id: str, visit_update: VisitUpdate):
    try:
        updated_visit = await visits_db_handler.update_visit(visit_id, visit_update)
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ServiceException as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    except Exception as e:
        LOGGER.exception(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unknown error occurred")

    return Visit.model_validate(updated_visit)


async def delete_visit(visit_id: str):
    try:
        success = await visits_db_handler.delete_visit(visit_id)
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ServiceException as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    except Exception as e:
        LOGGER.exception(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unknown error occurred")

    return {"deleted": success}
