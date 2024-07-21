from datetime import datetime
from typing import Optional
import uuid

from sqlalchemy import Column, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from ai_health.database.orms.medication_n_dosage_orm import Appointment, LabReport, MedicalHistory, Medication
from ai_health.database.orms.visits_orm import Visit
from ai_health.root.utils.abstract_base import AbstractBase


class User(AbstractBase):
    """
    The ai_health User table, who are the patients
    """

    __tablename__ = "users"

    user_id = Column(UUID(as_uuid=True), primary_key=True, unique=True, nullable=False, default=uuid.uuid4)
    first_name: Mapped[str]
    last_name: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    phone_number: Mapped[Optional[str]]
    user_type: Mapped[str]
    profile_image: Mapped[Optional[str]]
    is_verified: Mapped[bool] = mapped_column(default=False)
    date_of_birth: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    gender: Mapped[str]
    address: Mapped[str]

    visits: Mapped[list["Visit"]] = relationship("Visit", back_populates="patient")
    medications: Mapped[list["Medication"]] = relationship("Medication", back_populates="patient")
    appointments: Mapped[list["Appointment"]] = relationship("Appointment", back_populates="patient")
    lab_reports: Mapped[list["LabReport"]] = relationship("LabReport", back_populates="patient")
    medical_history: Mapped[list["MedicalHistory"]] = relationship("MedicalHistory", back_populates="patient")
