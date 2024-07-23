import logging
from sqlalchemy import insert, select, delete, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload

from ai_health.schemas.auth_schemas import User, UserCreate, UserEdit, UserExtended, UserWithAllRelations
from ai_health.root.database import async_session

from ai_health.database.orms.auth_orm import User as UserDB
from ai_health.database.orms.visits_orm import Visit as VisitDB
from ai_health.database.orms.medication_n_dosage_orm import Medication as MedicationDB, Appointment as AppointmentDB
from ai_health.services.utils.exceptions import NotFoundException, RecordExistsException, ServiceException


LOGGER = logging.getLogger(__name__)


async def create_user(user: UserCreate):
    async with async_session() as session:

        data = user.model_dump()

        stmt = insert(UserDB).values(**data).returning(UserDB)

        # stmt2 = delete(UserDB).where(UserDB.email == user.email)

        # result = (await session.execute(statement=stmt2))
        # await session.commit()

        # return None

        try:
            result = (await session.execute(statement=stmt)).scalar_one_or_none()

        except IntegrityError as e:
            print(e)
            LOGGER.error(f"Duplicate record found for user {user.email}")
            await session.rollback()
            raise RecordExistsException(message=f"Duplicate record found for {user.email}")
        except Exception as e:
            LOGGER.exception(e)
            LOGGER.error(f"An unknown error occurred")
            await session.rollback()
            raise ServiceException(message=f"An unknown error occurred")

        if result is None:
            LOGGER.error(f"Couldnt create account found for user with email {user.email}")
            await session.rollback()
            raise ServiceException(message=f"Couldnt create record for {user.email}")

        await session.commit()

        return User.model_validate(result)


async def update_user(
    user_edit_data: UserEdit,
    user_email: str = None,
    user_id: str = None,
):

    async with async_session() as session:
        if not user_id and not user_email:
            raise Exception("user_id and user_email not given")

        if user_id is not None:
            stmt = (
                update(UserDB)
                .values(user_edit_data.model_dump(exclude_none=True, exclude_unset=True))
                .where(UserDB.user_id == user_id)
                .returning(UserDB)
            )
        else:
            stmt = (
                update(UserDB)
                .values(user_edit_data.model_dump(exclude_none=True, exclude_unset=True))
                .where(UserDB.email == user_email)
                .returning(UserDB)
            )

        result = (await session.execute(statement=stmt)).scalar_one_or_none()

        if result is None:
            raise ServiceException(message="User details couldbt be updated")

        await session.commit()

        return User.model_validate(result)


async def get_user_with_email(email: str):
    async with async_session() as session:

        stmt = select(UserDB).where(UserDB.email == email)

        result = (await session.execute(statement=stmt)).scalar_one_or_none()

        if result is None:
            raise NotFoundException(message=f"Couldnt find user with email {email}")

        return UserExtended.model_validate(result)


async def get_user_with_user_id(user_id: str):
    async with async_session() as session:

        stmt = select(UserDB).where(UserDB.user_id == user_id)

        result = (await session.execute(statement=stmt)).scalar_one_or_none()

        if result is None:
            raise NotFoundException(message=f"Couldnt find user with user_id {user_id}")

        return UserExtended.model_validate(result)


async def get_user_with_id_and_relations(user_id: str):
    async with async_session() as session:

        stmt = (
            select(UserDB)
            .filter(UserDB.user_id == user_id)
            .options(
                joinedload(UserDB.medical_history),
                joinedload(UserDB.lab_reports),
                joinedload(UserDB.visits).options(
                    joinedload(VisitDB.doctor),
                ),
                joinedload(UserDB.appointments).options(
                    joinedload(AppointmentDB.doctor),
                ),
                joinedload(UserDB.medications),
            )
        )

        result = (await session.execute(statement=stmt)).unique().scalar_one_or_none()

        if result is None:
            raise NotFoundException(message=f"Couldnt find user with user_id {user_id}")
        
        print(f"This is teh result {result}")

        return UserWithAllRelations.model_validate(result)
