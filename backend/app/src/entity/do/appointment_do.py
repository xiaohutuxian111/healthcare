# -*- coding:utf-8 -*-
import datetime

from sqlalchemy import String, DateTime, Integer, ForeignKey
from sqlalchemy.orm import relationship, mapped_column, Mapped
from backend.app.config.database import BaseMixin, Base
from backend.app.src.entity.do.doctor_do import Doctor
from backend.app.src.entity.do.patient_do import Patient


class Appointment(Base, BaseMixin):
    __tablename__ = "appointment"

    schedule: Mapped[datetime.datetime] = mapped_column(DateTime, comment='预约时间')
    status: Mapped[int] = mapped_column(Integer, comment='预约状态:')
    reason: Mapped[str] = mapped_column(String(500), comment='预约原因')
    note: Mapped[str] = mapped_column(String(500), comment='预约备注')
    cancellation_reason: Mapped[str] = mapped_column(String(500), nullable=True, comment='取消原因')
    pid: Mapped[int] = mapped_column(Integer, ForeignKey('patient.id'), comment='患者ID')
    did: Mapped[int] = mapped_column(Integer, ForeignKey('doctor.id'), comment='医生ID')

    patient: Mapped['Patient'] = relationship(lazy=False, back_populates='appointment')
    doctor: Mapped['Doctor'] = relationship(lazy=False, back_populates='appointment')

    def __repr__(self):
        return f"<Appointment(id={self.id}, schedule={self.schedule}, status={self.status}, reason={self.reason}, note={self.note}, pid={self.pid}, did={self.did})>"
