from datetime import datetime
from typing import Optional
import uuid

from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from ai_health.database.orms.doctor_orm import Doctor
from ai_health.root.utils.abstract_base import AbstractBase


class Medication(AbstractBase):
    __tablename__ = "medications"
    medication_id = Column(UUID(as_uuid=True), primary_key=True, unique=True, nullable=False, default=uuid.uuid4)
    medication_name: Mapped[str]
    dosage: Mapped[str]
    start_date: Mapped[datetime]
    end_date: Mapped[datetime]

    patient_id = mapped_column(ForeignKey("users.user_id", ondelete="CASCADE"))
    patient = relationship("User", back_populates="medications")

    doctor_id: Mapped[UUID] = mapped_column(UUID, ForeignKey("doctors.doctor_id", ondelete="CASCADE"))
    doctor = relationship("Doctor", back_populates="medications")


class Appointment(AbstractBase):
    __tablename__ = "appointments"
    appointment_id = Column(UUID(as_uuid=True), primary_key=True, unique=True, nullable=False, default=uuid.uuid4)

    appointment_date: Mapped[datetime]
    reason_for_appointment: Mapped[str]
    status: Mapped[str]
    next_appointment_date: Mapped[datetime]

    patient_id: Mapped[UUID] = mapped_column(ForeignKey("users.user_id", ondelete="CASCADE"))
    patient = relationship("User", back_populates="appointments")

    doctor_id: Mapped[UUID] = mapped_column(ForeignKey("doctors.doctor_id", ondelete="CASCADE"))
    doctor: Mapped["Doctor"] = relationship(back_populates="appointments")


class LabReport(AbstractBase):
    __tablename__ = "labreports"
    report_id = Column(UUID(as_uuid=True), primary_key=True, unique=True, nullable=False, default=uuid.uuid4)
    test_name: Mapped[str]
    test_date: Mapped[datetime]
    result: Mapped[str]
    notes: Mapped[str]

    patient_id: Mapped[UUID] = mapped_column(ForeignKey("users.user_id", ondelete="CASCADE"))
    patient = relationship("User", back_populates="lab_reports")


class MedicalHistory(AbstractBase):
    __tablename__ = "medical_history"
    history_id = Column(UUID(as_uuid=True), primary_key=True, unique=True, nullable=False, default=uuid.uuid4)
    condition: Mapped[str]
    diagnosis_date: Mapped[datetime]
    notes: Mapped[str]

    patient_id: Mapped[UUID] = mapped_column(ForeignKey("users.user_id", ondelete="CASCADE"))
    patient = relationship("User", back_populates="medical_history")
