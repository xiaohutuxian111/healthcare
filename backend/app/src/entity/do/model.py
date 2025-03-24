#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2025/3/16 18:08
# @Author  : stone
# @File    : model.py
# @Desc    :

import datetime

from sqlalchemy import DateTime, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import mapped_column, Mapped, relationship
from config.database import BaseMixin, Base

from typing import Literal


class Patient(Base, BaseMixin):
    __tablename__ = 'patient'

    name: Mapped[str] = mapped_column(String(50), index=True, comment='患者姓名')
    email: Mapped[str] = mapped_column(String(50), unique=True, index=True, comment='患者电子邮件')
    phone: Mapped[str] = mapped_column(String(20), unique=True, index=True, comment='患者电话号码')
    birth_date: Mapped[datetime.datetime] = mapped_column(DateTime, comment='患者出生日期')
    gender: Mapped[Literal['0', '1', '2']] = mapped_column(String(1), comment='患者性别(0:未知,1:男,2:女)')
    address: Mapped[str] = mapped_column(String(255), comment='患者地址')
    occupation: Mapped[str] = mapped_column(String(255), comment='患者职业')
    emergency_contact_name: Mapped[str] = mapped_column(String(50), comment='紧急联系人姓名')
    emergency_contact_number: Mapped[str] = mapped_column(String(20), comment='紧急联系人电话号码')
    primary_physician: Mapped[str] = mapped_column(String(50), comment='主治医生')
    insurance_provider: Mapped[str] = mapped_column(String(50), comment='保险提供商')
    insurance_policy_number: Mapped[str] = mapped_column(String(50), comment='保险政策编号')
    allergies: Mapped[str] = mapped_column(String(500), nullable=True, comment='过敏情况')
    current_medication: Mapped[str] = mapped_column(String(500), nullable=True, comment='当前用药')
    family_medical_history: Mapped[str] = mapped_column(String(500), nullable=True, comment='家族病史')
    past_medical_history: Mapped[str] = mapped_column(String(500), nullable=True, comment='既往病史')
    identification_type: Mapped[str] = mapped_column(String(50), nullable=True, comment='身份证明类型')
    identification_number: Mapped[str] = mapped_column(String(50), nullable=True, comment='身份证明编号')
    identification_document: Mapped[str] = mapped_column(String(50), nullable=True, comment='身份证明文件路径或URL')
    privacy_consent: Mapped[bool] = mapped_column(Boolean, comment='隐私同意')


class AppointMent(Base, BaseMixin):
    __tablename__ = 'appointment'

    schedule: Mapped[datetime.datetime] = mapped_column(DateTime, comment='预约时间')
    status: Mapped[int] = mapped_column(Integer, comment='预约状态:')
    reason: Mapped[str] = mapped_column(String(500), comment='预约原因')
    note: Mapped[str] = mapped_column(String(500), comment='预约备注')
    cancellation_reason: Mapped[str] = mapped_column(String(500), nullable=True, comment='取消原因')
    pid: Mapped[int] = mapped_column(Integer, ForeignKey('patient.id'), comment='患者ID')
    did: Mapped[int] = mapped_column(Integer, ForeignKey('doctor.id'), comment='医生ID')

    patient = relationship('Patient', back_populates='appointment')
    doctor = relationship('Doctor', back_populates='appointment')


class Doctor(Base, BaseMixin):
    __tablename__ = 'doctor'
    name: Mapped[str] = mapped_column(String(50), nullable=False, comment='医生姓名')
    image_path: Mapped[str] = mapped_column(String(255), nullable=True, comment='医生头像')
