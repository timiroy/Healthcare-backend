import logging
from sqlalchemy import and_, insert, update, delete, select
from sqlalchemy.exc import IntegrityError

from ai_health.database.orms.medication_n_dosage_orm import Medication as MedicationDB
from ai_health.schemas.medication_schema import (
    Medication,
    MedicationCreate,
    MedicationList,
    MedicationUpdate,
)
from ai_health.root.database import async_session
from ai_health.services.utils.exceptions import NotFoundException, RecordExistsException, ServiceException

LOGGER = logging.getLogger(__name__)


async def create_medication(medication: MedicationCreate):
    async with async_session() as session:
        medication_dict = medication.model_dump()
        stmt = insert(MedicationDB).values(medication_dict).returning(MedicationDB)

        try:
            result = (await session.execute(statement=stmt)).scalar_one_or_none()
        except IntegrityError as e:
            LOGGER.error(f"Duplicate record found for medication_id {medication.medication_id}")
            await session.rollback()
            raise RecordExistsException(message=f"Duplicate record found for medication_id {medication.medication_id}")
        except Exception as e:
            LOGGER.exception(e)
            LOGGER.error("An unknown error occurred")
            await session.rollback()
            raise ServiceException(message="An unknown error occurred")

        if result is None:
            LOGGER.error(f"Couldn't create record for medication_id {medication.medication_id}")
            await session.rollback()
            raise ServiceException(message=f"Couldn't create record for medication_id {medication.medication_id}")

        await session.commit()
        return Medication.model_validate(result)


async def get_medication(medication_id: int):
    async with async_session() as session:
        stmt = select(MedicationDB).filter(MedicationDB.medication_id == medication_id)

        result = (await session.execute(statement=stmt)).scalar_one_or_none()

        if result is None:
            raise ServiceException(f"Medication not found for medication_id {medication_id}")

        return Medication.model_validate(result)


async def get_medications(**kwargs):
    async with async_session() as session:
        patient_id = kwargs.get("patient_id", None)
        doctor_id = kwargs.get("doctor_id", None)

        filter_conditions = []
        if patient_id:
            filter_conditions.append(MedicationDB.patient_id == patient_id)
        if doctor_id:
            filter_conditions.append(MedicationDB.prescribed_by == doctor_id)

        stmt = select(MedicationDB).filter(and_(*filter_conditions)).order_by(MedicationDB.start_date.desc())

        result = (await session.execute(statement=stmt)).unique().scalars().all()

        result_set = []

        for x in result:
            result_set.append(Medication.model_validate(x))

        return MedicationList(detail="Medications retrieved", medications=result_set)


async def update_medication(medication_id: int, medication_update: MedicationUpdate):
    async with async_session() as session:
        stmt = (
            update(MedicationDB)
            .where(MedicationDB.medication_id == medication_id)
            .values(medication_update.model_dump(exclude_none=True, exclude_unset=True))
            .returning(MedicationDB)
        )

        result = (await session.execute(statement=stmt)).scalar_one_or_none()

        if result is None:
            raise ServiceException(f"Medication could not be updated for medication_id {medication_id}")

        await session.commit()
        return Medication.model_validate(result)


async def delete_medication(medication_id: int):
    async with async_session() as session:
        stmt = delete(MedicationDB).where(MedicationDB.medication_id == medication_id)

        result = await session.execute(statement=stmt)
        return result is not None
