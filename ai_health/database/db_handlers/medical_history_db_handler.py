import logging
from sqlalchemy import and_, insert, update, delete, select
from sqlalchemy.exc import IntegrityError

from ai_health.database.orms.medication_n_dosage_orm import MedicalHistory as MedicalHistoryDB
from ai_health.schemas.medical_history_schema import (
    MedicalHistory,
    MedicalHistoryCreate,
    MedicalHistoryList,
    MedicalHistoryUpdate,
)
from ai_health.root.database import async_session
from ai_health.services.utils.exceptions import NotFoundException, RecordExistsException, ServiceException

LOGGER = logging.getLogger(__name__)


async def create_medical_history(medical_history: MedicalHistoryCreate):
    async with async_session() as session:
        medical_history_dict = medical_history.model_dump()
        stmt = insert(MedicalHistoryDB).values(medical_history_dict).returning(MedicalHistoryDB)

        try:
            result = (await session.execute(statement=stmt)).scalar_one_or_none()
        except IntegrityError as e:
            LOGGER.error(f"Duplicate record found for history_id {medical_history.history_id}")
            await session.rollback()
            raise RecordExistsException(message=f"Duplicate record found for history_id {medical_history.history_id}")
        except Exception as e:
            LOGGER.exception(e)
            LOGGER.error("An unknown error occurred")
            await session.rollback()
            raise ServiceException(message="An unknown error occurred")

        if result is None:
            LOGGER.error(f"Couldn't create record for history_id {medical_history.history_id}")
            await session.rollback()
            raise ServiceException(message=f"Couldn't create record for history_id {medical_history.history_id}")

        await session.commit()
        return MedicalHistory.model_validate(result)


async def get_medical_history(history_id: int):
    async with async_session() as session:
        stmt = select(MedicalHistoryDB).filter(MedicalHistoryDB.history_id == history_id)

        result = (await session.execute(statement=stmt)).scalar_one_or_none()

        if result is None:
            raise ServiceException(f"Medical history not found for history_id {history_id}")

        return MedicalHistory.model_validate(result)


async def get_medical_histories(**kwargs):
    async with async_session() as session:
        patient_id = kwargs.get("patient_id", None)

        filter_conditions = []
        if patient_id:
            filter_conditions.append(MedicalHistoryDB.patient_id == patient_id)

        stmt = (
            select(MedicalHistoryDB).filter(and_(*filter_conditions)).order_by(MedicalHistoryDB.diagnosis_date.desc())
        )

        result = (await session.execute(statement=stmt)).unique().scalars().all()

        result_set = []

        for x in result:
            result_set.append(MedicalHistory.model_validate(x))

        return MedicalHistoryList(detail="Medical histories retrieved", medical_histories=result_set)


async def update_medical_history(history_id: int, medical_history_update: MedicalHistoryUpdate):
    async with async_session() as session:
        stmt = (
            update(MedicalHistoryDB)
            .where(MedicalHistoryDB.history_id == history_id)
            .values(medical_history_update.model_dump(exclude_none=True, exclude_unset=True))
            .returning(MedicalHistoryDB)
        )

        result = (await session.execute(statement=stmt)).scalar_one_or_none()

        if result is None:
            raise ServiceException(f"Medical history could not be updated for history_id {history_id}")

        await session.commit()
        return MedicalHistory.model_validate(result)


async def delete_medical_history(history_id: int):
    async with async_session() as session:
        stmt = delete(MedicalHistoryDB).where(MedicalHistoryDB.history_id == history_id)

        result = await session.execute(statement=stmt)
        return result is not None
