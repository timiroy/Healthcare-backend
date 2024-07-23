import logging
from fastapi import HTTPException, status
from ai_health.schemas.billings_schema import (
    BillingCreate,
    BillingUpdate,
    Billing,
    BillingWithDoctor,
    BillingsWithDoctorList,
)
from ai_health.database.db_handlers import billing_db_handler
from ai_health.services.utils.exceptions import NotFoundException, RecordExistsException, ServiceException

LOGGER = logging.getLogger(__name__)


async def create_billing_service(billing_create: BillingCreate) -> Billing:
    try:
        return await billing_db_handler.create_billing(billing_create)
    except RecordExistsException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except ServiceException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        LOGGER.error(f"An error occurred: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="An unknown error occurred")


async def get_billing_service(billing_id: str) -> BillingWithDoctor:
    try:
        return await billing_db_handler.get_billing_by_id(billing_id)
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ServiceException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        LOGGER.error(f"An error occurred: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="An unknown error occurred")


async def update_billing_service(billing_id: str, billing_update: BillingUpdate) -> Billing:
    try:
        return await billing_db_handler.update_billing(billing_id, billing_update)
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ServiceException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        LOGGER.error(f"An error occurred: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="An unknown error occurred")


async def delete_billing_service(billing_id: str) -> bool:
    try:
        return await billing_db_handler.delete_billing(billing_id)
    except ServiceException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        LOGGER.error(f"An error occurred: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="An unknown error occurred")


async def get_billings_for_user(user_id: str) -> BillingsWithDoctorList:
    try:
        billings = await billing_db_handler.get_billings(user_id)
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ServiceException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        LOGGER.error(f"An error occurred: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="An unknown error occurred")

    return BillingsWithDoctorList(billings=billings)
