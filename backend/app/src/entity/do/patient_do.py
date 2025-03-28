# -*- coding:utf-8 -*-

from typing import Literal
import datetime
from sqlalchemy import String, DateTime, Boolean, ForeignKey, Integer
from backend.app.config.database import BaseMixin, Base
from sqlalchemy.orm import mapped_column, Mapped, relationship


class Patient(Base, BaseMixin):
    __tablename__ = "patient"

    name: Mapped[str] = mapped_column(String(50), index=True, comment='患者姓名')
    email: Mapped[str] = mapped_column(String(50), unique=True, index=True, comment='患者电子邮件')
    phone: Mapped[str] = mapped_column(String(20), unique=True, index=True, comment='患者电话号码')

    def __repr__(self):
        return f"Patient(id={self.id}, name={self.name}, email={self.email}, phone={self.phone})"


class PatientDetail(Base, BaseMixin):
    __tablename__ = "patient_detail"

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
    pid: Mapped[int] = mapped_column(Integer, ForeignKey('patient.id'), comment='患者ID')

    patient: Mapped['Patient'] = relationship(lazy=False, back_populates='patient_detail')

    def __repr__(self):
        return (
            f"PatientDetail(id={self.id}, birth_date={self.birth_date}, gender={self.gender}, address={self.address}, occupation={self.occupation}, "
            f"emergency_contact_name={self.emergency_contact_name}, emergency_contact_number={self.emergency_contact_number}, primary_physician={self.primary_physician},"
            f" insurance_provider={self.insurance_provider}, insurance_policy_number={self.insurance_policy_number}, allergies={self.allergies}, "
            f"current_medication={self.current_medication}, family_medical_history={self.family_medical_history}, past_medical_history={self.past_medical_history}, "
            f"identification_type={self.identification_type}, identification_number={self.identification_number}, identification_document={self.identification_document}, privacy_consent={self.privacy_consent})")
