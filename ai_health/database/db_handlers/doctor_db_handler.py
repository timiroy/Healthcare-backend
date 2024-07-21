import logging
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy import insert, select, update, delete
from ai_health.database.orms.doctor_orm import Doctor as DoctorDB
from ai_health.schemas.doctor_schema import DoctorCreate, DoctorUpdate, Doctor, DoctorList
from ai_health.root.database import async_session
from ai_health.services.utils.exceptions import NotFoundException, RecordExistsException, ServiceException

LOGGER = logging.getLogger(__name__)


async def create_doctor(doctor_create: DoctorCreate):
    async with async_session() as session:
        doctor_dict = doctor_create.model_dump()
        stmt = insert(DoctorDB).values(doctor_dict).returning(DoctorDB)

        try:
            result = (await session.execute(statement=stmt)).scalar_one_or_none()
        except IntegrityError as e:
            LOGGER.error(f"Duplicate record found for doctor {doctor_create.email}")
            await session.rollback()
            raise RecordExistsException(message=f"Duplicate record found for doctor {doctor_create.email}")
        except Exception as e:
            LOGGER.exception(e)
            LOGGER.error(f"An unknown error occurred")
            await session.rollback()
            raise ServiceException(message=f"An unknown error occurred")

        if result is None:
            LOGGER.error(f"Couldn't create record for doctor {doctor_create.email}")
            await session.rollback()
            raise ServiceException(message=f"Couldn't create record for doctor {doctor_create.email}")

        await session.commit()
        return Doctor.model_validate(result)


async def get_doctor_by_id(doctor_id: str):
    async with async_session() as session:
        stmt = select(DoctorDB).filter(DoctorDB.doctor_id == doctor_id)
        result = (await session.execute(statement=stmt)).scalar_one_or_none()

        if result is None:
            raise NotFoundException(f"Doctor not found for id {doctor_id}")

        return Doctor.model_validate(result)


async def update_doctor(doctor_id: str, doctor_update: DoctorUpdate):
    async with async_session() as session:
        stmt = (
            update(DoctorDB)
            .where(DoctorDB.doctor_id == doctor_id)
            .values(doctor_update.model_dump(exclude_none=True, exclude_unset=True))
            .returning(DoctorDB)
        )

        result = (await session.execute(statement=stmt)).scalar_one_or_none()

        if result is None:
            raise NotFoundException(f"Doctor not found for id {doctor_id}")

        await session.commit()
        return Doctor.model_validate(result)


async def delete_doctor(doctor_id: str):
    async with async_session() as session:
        stmt = delete(DoctorDB).where(DoctorDB.doctor_id == doctor_id)
        result = await session.execute(statement=stmt)
        return result.rowcount > 0


async def get_all_doctors():
    async with async_session() as session:
        stmt = select(DoctorDB)
        result = (await session.execute(statement=stmt)).scalars().all()
        return [Doctor.model_validate(doctor) for doctor in result]
