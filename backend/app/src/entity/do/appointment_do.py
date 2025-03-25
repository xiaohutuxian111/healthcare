# -*- coding:utf-8 -*-
import datetime

from sqlalchemy import String, DateTime, Integer, ForeignKey
from sqlalchemy.orm import relationship, mapped_column, Mapped

from config.database import BaseMixin, Base


class Appointment(Base, BaseMixin):
    __tablename__ = "appointment"

    schedule: Mapped[datetime.datetime] = mapped_column(DateTime, comment='预约时间')
    status: Mapped[int] = mapped_column(Integer, comment='预约状态:')
    reason: Mapped[str] = mapped_column(String(500), comment='预约原因')
    note: Mapped[str] = mapped_column(String(500), comment='预约备注')
    cancellation_reason: Mapped[str] = mapped_column(String(500), nullable=True, comment='取消原因')
    pid: Mapped[int] = mapped_column(Integer, ForeignKey('patient.id'), comment='患者ID')
    did: Mapped[int] = mapped_column(Integer, ForeignKey('doctor.id'), comment='医生ID')

    patient = relationship('Patient', back_populates='appointment')
    doctor = relationship('Doctor', back_populates='appointment')
