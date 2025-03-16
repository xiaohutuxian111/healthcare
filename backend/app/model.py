#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2025/3/16 18:08
# @Author  : stone
# @File    : model.py
# @Desc    :
from pydantic import BaseModel


class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    age: int | None = Field(default=None, index=True)
    secret_name: str


class Patient(BaseModel):
    __table__ = 'patient'
    user_id =
    userId: string;
    name: string;
    email: string;
    phone: string;
    birthDate: Date;
    gender: Gender;
    address: string;
    occupation: string;
    emergencyContactName: string;
    emergencyContactNumber: string;
    primaryPhysician: string;
    insuranceProvider: string;
    insurancePolicyNumber: string;
    allergies: string | undefined;
    currentMedication: string | undefined;
    familyMedicalHistory: string | undefined;
    pastMedicalHistory: string | undefined;
    identificationType: string | undefined;
    identificationNumber: string | undefined;
    identificationDocument: FormData | undefined;
    privacyConsent: boolean;


class Appointment(BaseModel):
    __table__ = 'Appointment'

    patient: Patient;
    schedule: Date;
    status: Status;
    primaryPhysician: string;
    reason: string;
    note: string;
    userId: string;
    cancellationReason: string | null;
