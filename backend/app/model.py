#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2025/3/16 18:08
# @Author  : stone
# @File    : model.py
# @Desc    :

from sqlalchemy import Column, DateTime, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from config.database import Base


class Patient(Base):
    __tablename__ = 'patient'

    pid = Column(Integer, primary_key=True, index=True, comment='患者唯一标识符')
    name = Column(String(50), index=True, comment='患者姓名')
    email = Column(String(50), unique=True, index=True, comment='患者电子邮件')
    phone = Column(String(20), unique=True, index=True, comment='患者电话号码')
    birth_date = Column(DateTime, comment='患者出生日期')
    gender = Column(String, comment='患者性别')
    address = Column(String(255), comment='患者地址')
    occupation = Column(String(255), comment='患者职业')
    emergency_contact_name = Column(String(50), comment='紧急联系人姓名')
    emergency_contact_number = Column(String(20), comment='紧急联系人电话号码')
    primary_physician = Column(String(50), comment='主治医生')
    insurance_provider = Column(String(50), comment='保险提供商')
    insurance_policy_number = Column(String(50), comment='保险政策编号')
    allergies = Column(String(500), nullable=True, comment='过敏情况')
    current_medication = Column(String(500), nullable=True, comment='当前用药')
    family_medical_history = Column(String(500), nullable=True, comment='家族病史')
    past_medical_history = Column(String(500), nullable=True, comment='既往病史')
    identification_type = Column(String(50), nullable=True, comment='身份证明类型')
    identification_number = Column(String(50), nullable=True, comment='身份证明编号')
    identification_document = Column(String(50), nullable=True, comment='身份证明文件路径或URL')
    privacy_consent = Column(Boolean, comment='隐私同意')


class AppointMent(Base):
    __tablename__ = 'appointment'

    aid = Column(Integer, primary_key=True, index=True, comment='预约唯一标识符')
    patient_id = Column(Integer, ForeignKey('patient.user_id'), index=True, comment='患者唯一标识符')
    schedule = Column(DateTime, comment='预约时间')
    status = Column(Integer, comment='预约状态:')
    reason = Column(String, comment='预约原因')
    note = Column(String, comment='预约备注')
    cancellation_reason = Column(String, nullable=True, comment='取消原因')
    pid = Column(Integer, ForeignKey('patient.pid'), comment='患者ID')
    did = Column(Integer, ForeignKey('doctor.did'), comment='医生ID')


class Doctor(Base):
    did = Column(Integer, primary_key=True, index=True, comment='医生唯一标识符')
    name = Column(String(50), nullable=False, comment='医生姓名')
    image_path = Column(String(255), nullable=True, comment='医生头像')
