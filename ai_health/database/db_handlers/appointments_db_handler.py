import logging
from sqlalchemy import and_, insert, update, delete, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload

from ai_health.database.orms.medication_n_dosage_orm import Appointment as AppointmentDB
from ai_health.schemas.appointment_schema import (
    Appointment,
    AppointmentCreate,
    AppointmentList,
    AppointmentUpdate,
    AppointmentWithDoctor,
)
from ai_health.root.database import async_session
from ai_health.services.utils.exceptions import NotFoundException, RecordExistsException, ServiceException

LOGGER = logging.getLogger(__name__)


async def create_appointment(appointment: AppointmentCreate):
    async with async_session() as session:
        appointment_dict = appointment.model_dump()
        stmt = insert(AppointmentDB).values(appointment_dict).returning(AppointmentDB)

        try:
            result = (await session.execute(statement=stmt)).scalar_one_or_none()
        except IntegrityError as e:
            LOGGER.error(f"Duplicate record or record  not found")
            await session.rollback()
            raise RecordExistsException(message=f"{e.detail}")
        except Exception as e:
            LOGGER.exception(e)
            LOGGER.error("An unknown error occurred")
            await session.rollback()
            raise ServiceException(message="An unknown error occurred")

        if result is None:
            LOGGER.error(f"Couldn't create record")
            await session.rollback()
            raise ServiceException(message=f"Couldn't create record")

        await session.commit()
        return Appointment.model_validate(result)


async def get_appointment(appointment_id: int):
    async with async_session() as session:
        stmt = select(AppointmentDB).filter(AppointmentDB.appointment_id == appointment_id)

        result = (await session.execute(statement=stmt)).scalar_one_or_none()

        if result is None:
            raise ServiceException(f"Appointment not found for appointment_id {appointment_id}")

        return Appointment.model_validate(result)


async def get_appointments(**kwargs):
    async with async_session() as session:
        patient_id = kwargs.get("patient_id", None)
        doctor_id = kwargs.get("doctor_id", None)

        filter_conditions = []
        if patient_id:
            filter_conditions.append(AppointmentDB.patient_id == patient_id)
        if doctor_id:
            filter_conditions.append(AppointmentDB.doctor_id == doctor_id)

        stmt = (
            select(AppointmentDB)
            .filter(and_(*filter_conditions))
            .order_by(AppointmentDB.appointment_date.desc())
            .options(
                joinedload(
                    AppointmentDB.doctor,
                )
            )
        )

        result = (await session.execute(statement=stmt)).unique().scalars().all()

        result_set = []

        for x in result:
            result_set.append(AppointmentWithDoctor.model_validate(x))

        return AppointmentList(detail="Appointments retrieved", appointments=result_set)


async def update_appointment(appointment_id: int, appointment_update: AppointmentUpdate):
    async with async_session() as session:
        stmt = (
            update(AppointmentDB)
            .where(AppointmentDB.appointment_id == appointment_id)
            .values(appointment_update.model_dump(exclude_none=True, exclude_unset=True))
            .returning(AppointmentDB)
        )

        result = (await session.execute(statement=stmt)).scalar_one_or_none()

        if result is None:
            raise ServiceException(f"Appointment could not be updated for appointment_id {appointment_id}")

        await session.commit()
        return Appointment.model_validate(result)


async def delete_appointment(appointment_id: int):
    async with async_session() as session:
        stmt = delete(AppointmentDB).where(AppointmentDB.appointment_id == appointment_id)

        result = await session.execute(statement=stmt)
        return result is not None
