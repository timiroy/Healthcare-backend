import logging
from sqlalchemy import and_, insert, update, delete, select
from sqlalchemy.exc import IntegrityError

from ai_health.database.orms.visits_orm import Visit as VisitDB
from ai_health.schemas.visits_schema import (
    VisitCreate,
    Visit,
    VisitList,
    VisitUpdate,
)
from ai_health.root.database import async_session
from ai_health.services.utils.exceptions import NotFoundException, RecordExistsException, ServiceException

LOGGER = logging.getLogger(__name__)


async def create_visit(visit: VisitCreate):
    async with async_session() as session:
        visit_dict = visit.model_dump()
        stmt = insert(VisitDB).values(visit_dict).returning(VisitDB)

        try:
            result = (await session.execute(statement=stmt)).scalar_one_or_none()
        except IntegrityError as e:
            LOGGER.error(f"Duplicate record found for visits")
            await session.rollback()
            raise RecordExistsException(message=f"{e.detail}")
        except Exception as e:
            LOGGER.exception(e)
            LOGGER.error("An unknown error occurred")
            await session.rollback()
            raise ServiceException(message="An unknown error occurred")

        if result is None:
            LOGGER.error(f"Couldn't create record for visit")
            await session.rollback()
            raise ServiceException(message=f"Couldn't create record for visit")

        await session.commit()
        return Visit.model_validate(result)


async def get_visit(visit_id: int):
    async with async_session() as session:
        stmt = select(VisitDB).filter(VisitDB.visit_id == visit_id)

        result = (await session.execute(statement=stmt)).scalar_one_or_none()

        if result is None:
            raise ServiceException(f"Visit not found for visit_id {visit_id}")

        return Visit.model_validate(result)


async def get_visits(**kwargs):
    async with async_session() as session:
        patient_id = kwargs.get("patient_id", None)
        doctor_id = kwargs.get("doctor_id", None)

        filter_conditions = []
        if patient_id:
            filter_conditions.append(VisitDB.patient_id == patient_id)
        if doctor_id:
            filter_conditions.append(VisitDB.doctor_id == doctor_id)

        stmt = select(VisitDB).filter(and_(*filter_conditions)).order_by(VisitDB.visit_date.desc())

        result = (await session.execute(statement=stmt)).unique().scalars().all()

        result_set = []

        for x in result:
            result_set.append(Visit.model_validate(x))

        return VisitList(detail="Visits retrieved", visits=result_set)


async def update_visit(visit_id: int, visit_update: VisitUpdate):
    async with async_session() as session:
        stmt = (
            update(VisitDB)
            .where(VisitDB.visit_id == visit_id)
            .values(visit_update.model_dump(exclude_none=True, exclude_unset=True))
            .returning(VisitDB)
        )

        result = (await session.execute(statement=stmt)).scalar_one_or_none()

        if result is None:
            raise ServiceException(f"Visit could not be updated for visit_id {visit_id}")

        await session.commit()
        return Visit.model_validate(result)


async def delete_visit(visit_id: int):
    async with async_session() as session:
        stmt = delete(VisitDB).where(VisitDB.visit_id == visit_id)

        result = await session.execute(statement=stmt)
        return result is not None
