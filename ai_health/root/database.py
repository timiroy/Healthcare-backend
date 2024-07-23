from alembic import command
from alembic.config import Config
from sqlalchemy import MetaData, create_engine, inspect
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from ai_health.root.settings import Settings
from ai_health.root.utils.abstract_base import AbstractBase
from ai_health.database.orms.auth_orm import User
from ai_health.database.orms.doctor_orm import Doctor   
from ai_health.database.orms.medication_n_dosage_orm import Medication, Appointment, LabReport, MedicalHistory
from ai_health.database.orms.visits_orm import Visit
from ai_health.database.orms.billing_orm import Billing

settings = Settings()

engine = create_async_engine(url=str(settings.POSTGRES_URL))


async_session = async_sessionmaker(engine, expire_on_commit=False)


# Handles creating migration from the changed
def create_migration():
    # Initialize Alembic configuration
    alembic_ini_path = "alembic.ini"
    alembic_config = Config(alembic_ini_path)

    metadata = MetaData()
    postgres_url = str(settings.POSTGRES_URL).split("//")

    metadata.reflect(
        bind=create_engine(
            url=f"postgresql://{postgres_url[-1]}",
        )
    )

    existing_tables = set(metadata.tables.keys())
    defined_tables = set(AbstractBase.metadata.tables.keys())

    print(defined_tables)

    changed_columns = []
    table_names = []
    print("New tables found:", list(defined_tables - existing_tables))
    new_table = list(defined_tables - existing_tables)

    message = "_".join(new_table)
    if list(defined_tables - existing_tables):

        # Generate migration script
        command.revision(config=alembic_config, autogenerate=True, message=message)
        command.upgrade(alembic_config, "head")
    else:

        for table_name, table in AbstractBase.metadata.tables.items():
            existing_columns = {c.name: c for c in inspect(metadata.tables[table_name]).c}
            defined_columns = {c.name: c for c in table.c}

            # Check for changes in columns
            for column_name, column in defined_columns.items():
                if column_name not in existing_columns or not isinstance(
                    existing_columns[column_name].type, type(column.type)
                ):
                    table_names.append(table_name)
                    changed_columns.append(column_name)
                    print(changed_columns)

    if changed_columns:
        message = f"Columns changed in table { '_'.join(table_names)}:" f" {', '.join(changed_columns)}"

        # Generate migration script
        command.revision(config=alembic_config, autogenerate=True, message=message)
        command.upgrade(alembic_config, "head")
    else:
        print("No new changes found.")
