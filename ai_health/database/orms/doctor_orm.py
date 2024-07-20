from datetime import datetime
from typing import Optional
import uuid

from sqlalchemy import Column
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from ai_health.root.utils.abstract_base import AbstractBase


class Doctor(AbstractBase):
    __tablename__ = "doctors"
    doctor_id = Column(UUID(as_uuid=True), primary_key=True, unique=True, nullable=False, default=uuid.uuid4)
    first_name: Mapped[str]
    last_name: Mapped[str]
    specialty: Mapped[str]
    contact_number: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)

    visits = relationship("Visit", back_populates="doctor")
    medications = relationship("Medication", back_populates="doctor")
    appointments = relationship("Appointment", back_populates="doctor")
