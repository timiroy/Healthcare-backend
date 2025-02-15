"""add: make date time zone aware

Revision ID: 7fa2cc00953b
Revises: 09a95a01be55
Create Date: 2024-07-20 20:27:55.488670

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '7fa2cc00953b'
down_revision: Union[str, None] = '09a95a01be55'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'appointments', ['appointment_id'])
    op.create_unique_constraint(None, 'doctors', ['doctor_id'])
    op.create_unique_constraint(None, 'labreports', ['report_id'])
    op.create_unique_constraint(None, 'medical_history', ['history_id'])
    op.create_unique_constraint(None, 'medications', ['medication_id'])
    op.alter_column('users', 'date_of_birth',
               existing_type=postgresql.TIMESTAMP(),
               type_=sa.DateTime(timezone=True),
               existing_nullable=True)
    op.create_unique_constraint(None, 'users', ['user_id'])
    op.create_unique_constraint(None, 'visits', ['visit_id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'visits', type_='unique')
    op.drop_constraint(None, 'users', type_='unique')
    op.alter_column('users', 'date_of_birth',
               existing_type=sa.DateTime(timezone=True),
               type_=postgresql.TIMESTAMP(),
               existing_nullable=True)
    op.drop_constraint(None, 'medications', type_='unique')
    op.drop_constraint(None, 'medical_history', type_='unique')
    op.drop_constraint(None, 'labreports', type_='unique')
    op.drop_constraint(None, 'doctors', type_='unique')
    op.drop_constraint(None, 'appointments', type_='unique')
    # ### end Alembic commands ###
