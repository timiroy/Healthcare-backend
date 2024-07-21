from datetime import datetime
from typing import Optional
import uuid

from sqlalchemy import Column, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from ai_health.database.orms.doctor_orm import Doctor
from ai_health.root.utils.abstract_base import AbstractBase


class Visit(AbstractBase):
    __tablename__ = "visits"
    visit_id = Column(UUID(as_uuid=True), primary_key=True, unique=True, nullable=False, default=uuid.uuid4)
    visit_date: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    reason_for_visit: Mapped[str]
    notes: Mapped[str]

    vistor_name: Mapped[str]
    visitor_relationship: Mapped[str]

    patient_id = mapped_column(ForeignKey("users.user_id", ondelete="CASCADE"))
    patient = relationship("User", back_populates="visits")

    doctor_id: Mapped[UUID] = mapped_column(ForeignKey("doctors.doctor_id", ondelete="CASCADE"))
    doctor: Mapped["Doctor"] = relationship("Doctor", back_populates="visits")
