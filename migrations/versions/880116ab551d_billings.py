"""billings

Revision ID: 880116ab551d
Revises: 6dc08f1efb09
Create Date: 2024-07-23 16:35:41.895831

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '880116ab551d'
down_revision: Union[str, None] = '6dc08f1efb09'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('billings',
    sa.Column('billing_id', sa.UUID(), nullable=False),
    sa.Column('patient_id', sa.UUID(), nullable=False),
    sa.Column('doctor_id', sa.UUID(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('status', sa.String(), nullable=False),
    sa.Column('amount', sa.Float(), nullable=False),
    sa.Column('date_created', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('date_updated', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['doctor_id'], ['doctors.doctor_id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['patient_id'], ['users.user_id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('billing_id'),
    sa.UniqueConstraint('billing_id')
    )
    op.alter_column('visits', 'patient_id',
               existing_type=sa.UUID(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('visits', 'patient_id',
               existing_type=sa.UUID(),
               nullable=True)
    op.drop_table('billings')
    # ### end Alembic commands ###
