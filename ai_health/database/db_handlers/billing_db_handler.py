import logging
from sqlalchemy import insert, select, delete, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload

from ai_health.database.orms.billing_orm import Billing as BillingDB
from ai_health.schemas.billings_schema import BillingCreate, BillingUpdate, Billing, BillingWithDoctor
from ai_health.root.database import async_session
from ai_health.services.utils.exceptions import NotFoundException, RecordExistsException, ServiceException

LOGGER = logging.getLogger(__name__)


async def create_billing(billing_create: BillingCreate):
    async with async_session() as session:
        billing_dict = billing_create.model_dump()
        stmt = insert(BillingDB).values(billing_dict).returning(BillingDB)
        try:
            result = (await session.execute(statement=stmt)).scalar_one_or_none()
        except IntegrityError:
            LOGGER.error(f"Duplicate record found for billing {billing_create.title}")
            await session.rollback()
            raise RecordExistsException(message=f"Duplicate record found for billing {billing_create.title}")
        except Exception as e:
            LOGGER.exception(e)
            await session.rollback()
            raise ServiceException(message="An unknown error occurred")
        if result is None:
            await session.rollback()
            raise ServiceException(message="Couldn't create billing record")
        await session.commit()
        return Billing.from_orm(result)


async def get_billing_by_id(billing_id: str):
    async with async_session() as session:
        stmt = (
            select(BillingDB)
            .filter(BillingDB.billing_id == billing_id)
            .options(
                joinedload(BillingDB.doctor),
            )
        )
        result = (await session.execute(stmt)).scalar_one_or_none()
        if result is None:
            raise NotFoundException(f"Billing record not found for id {billing_id}")
        return BillingWithDoctor.model_validate(result)


async def update_billing(billing_id: str, billing_update: BillingUpdate):
    async with async_session() as session:
        stmt = (
            update(BillingDB)
            .where(BillingDB.billing_id == billing_id)
            .values(billing_update.model_dump(exclude_unset=True))
            .returning(BillingDB)
        )
        result = (await session.execute(stmt)).scalar_one_or_none()
        if result is None:
            raise NotFoundException(f"Billing record not found for id {billing_id}")
        await session.commit()
        return Billing.from_orm(result)


async def delete_billing(billing_id: str):
    async with async_session() as session:
        stmt = delete(BillingDB).where(BillingDB.billing_id == billing_id)
        result = await session.execute(stmt)
        return result.rowcount > 0
