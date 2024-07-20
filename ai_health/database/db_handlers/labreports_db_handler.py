import logging
from sqlalchemy import and_, insert, update, delete, select
from sqlalchemy.exc import IntegrityError

from ai_health.database.orms.medication_n_dosage_orm import LabReport as LabReportDB
from ai_health.schemas.lab_report_schema import (
    LabReport,
    LabReportCreate,
    LabReportList,
    LabReportUpdate,
)
from ai_health.root.database import async_session
from ai_health.services.utils.exceptions import NotFoundException, RecordExistsException, ServiceException

LOGGER = logging.getLogger(__name__)


async def create_lab_report(lab_report: LabReportCreate):
    async with async_session() as session:
        lab_report_dict = lab_report.model_dump()
        stmt = insert(LabReportDB).values(lab_report_dict).returning(LabReportDB)

        try:
            result = (await session.execute(statement=stmt)).scalar_one_or_none()
        except IntegrityError as e:
            LOGGER.error(f"Duplicate record found for report_id {lab_report.report_id}")
            await session.rollback()
            raise RecordExistsException(message=f"Duplicate record found for report_id {lab_report.report_id}")
        except Exception as e:
            LOGGER.exception(e)
            LOGGER.error("An unknown error occurred")
            await session.rollback()
            raise ServiceException(message="An unknown error occurred")

        if result is None:
            LOGGER.error(f"Couldn't create record for report_id {lab_report.report_id}")
            await session.rollback()
            raise ServiceException(message=f"Couldn't create record for report_id {lab_report.report_id}")

        await session.commit()
        return LabReport.model_validate(result)


async def get_lab_report(report_id: int):
    async with async_session() as session:
        stmt = select(LabReportDB).filter(LabReportDB.report_id == report_id)

        result = (await session.execute(statement=stmt)).scalar_one_or_none()

        if result is None:
            raise ServiceException(f"Lab report not found for report_id {report_id}")

        return LabReport.model_validate(result)


async def get_lab_reports(**kwargs):
    async with async_session() as session:
        patient_id = kwargs.get("patient_id", None)

        filter_conditions = []
        if patient_id:
            filter_conditions.append(LabReportDB.patient_id == patient_id)

        stmt = select(LabReportDB).filter(and_(*filter_conditions)).order_by(LabReportDB.test_date.desc())

        result = (await session.execute(statement=stmt)).unique().scalars().all()

        result_set = []

        for x in result:
            result_set.append(LabReport.model_validate(x))

        return LabReportList(detail="Lab reports retrieved", lab_reports=result_set)


async def update_lab_report(report_id: int, lab_report_update: LabReportUpdate):
    async with async_session() as session:
        stmt = (
            update(LabReportDB)
            .where(LabReportDB.report_id == report_id)
            .values(lab_report_update.model_dump(exclude_none=True, exclude_unset=True))
            .returning(LabReportDB)
        )

        result = (await session.execute(statement=stmt)).scalar_one_or_none()

        if result is None:
            raise ServiceException(f"Lab report could not be updated for report_id {report_id}")

        await session.commit()
        return LabReport.model_validate(result)


async def delete_lab_report(report_id: int):
    async with async_session() as session:
        stmt = delete(LabReportDB).where(LabReportDB.report_id == report_id)

        result = await session.execute(statement=stmt)
        return result is not None
