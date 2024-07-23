import uuid
from sqlalchemy import Column, String, Enum, Float, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ai_health.root.utils.abstract_base import AbstractBase


class Billing(AbstractBase):
    __tablename__ = "billings"

    billing_id = Column(UUID(as_uuid=True), primary_key=True, unique=True, nullable=False, default=uuid.uuid4)
    title: Mapped[str]
    status: Mapped[str]
    amount: Mapped[float]

    patient_id = mapped_column(ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    patient = relationship("User", back_populates="billings", uselist=False)

    doctor_id = mapped_column(ForeignKey("doctors.doctor_id", ondelete="CASCADE"), nullable=False)
    doctor = relationship("Doctor", back_populates="billings", uselist=False)
