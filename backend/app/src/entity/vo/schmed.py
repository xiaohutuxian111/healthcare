#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2025/3/16 18:13
# @Author  : stone
# @File    : schmed.py
# @Desc    :

from pydantic import BaseModel
from typing import Literal, Optional
from pydantic import FormData



class RegisterUser(BaseModel):
    user_id: str
    birth_date: str
    gender: Literal["Male", "Female", "Other"]
    address: str
    occupation: str
    emergencyContactName: str
    emergencyContactNumber: str
    primaryPhysician: str
    insuranceProvider: str
    insurancePolicyNumber: str
    allergies: Optional[str] = None
    currentMedication: Optional[str] = None
    familyMedicalHistory: Optional[str] = None
    pastMedicalHistory: Optional[str] = None
    identificationType: Optional[str] = None
    identificationNumber: Optional[str] = None
    identificationDocument: Optional[FormData] = None
    privacyConsent: bool


class CreateUser(BaseModel):
    name: str
    email: str
    phone: str



Appointment = dict  # 示例占位，具体类型需根据上下文调整


class CreateAppointment(BaseModel):
    user_id: str
    patient: str
    primary_physician: str
    reason: str
    schedule: str
    status: Literal["pending", "confirmed", "completed", "cancelled"]
    note: Optional[str] = None


class UpdateAppointment(BaseModel):
    appointment_id: str
    user_id: str
    time_zone: str
    appointment: Appointment
    type: str






