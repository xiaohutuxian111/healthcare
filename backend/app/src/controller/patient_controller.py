# -*- coding:utf-8 -*-
from datetime import datetime
from venv import logger

from fastapi import APIRouter, Depends, Form, Request
from pydantic_validation_decorator import ValidateFields
from sqlalchemy.ext.asyncio import AsyncSession

from config.get_db import get_db
from backend.app.utils.response_util import ResponseUtil

from backend.app.src.entity.vo.patient_vo import PatientModel, PatientBase, PatientDeTailModel
from backend.app.src.service.patient_service import PatientService
from src.service.patient_service import PatientDetailService

# patientController = APIRouter(prefix='/patients', dependencies=[Depends(LoginService.get_current_user)])
patientController = APIRouter(prefix='/patient')


@patientController.post("/add")
@ValidateFields(validate_model='add_patient')
async def add_patient(request: Request, add_patient: PatientModel,
                      query_db: AsyncSession = Depends(get_db)):
    add_patient.create_time = datetime.now()
    add_patient.update_time = datetime.now()
    add_patient.del_flag = '0'
    add_patient.gender = add_patient.gender if add_patient.gender else '0'
    add_patient_result = await   PatientService.add_patient(request, query_db, add_patient)

    return ResponseUtil.success(msg='添加患者成功', data=add_patient_result)


@patientController.post('/login')
@ValidateFields(validate_model='login_patient')
async def login(request: Request, login_patient: PatientBase, query_db: AsyncSession = Depends(get_db)):
    query_patient = PatientModel(**login_patient.model_dump())
    patient_info = await PatientService.get_patient_info(query_db, query_patient)
    if patient_info:
        return ResponseUtil.success(msg='登录成功', data=patient_info)
    else:
        return ResponseUtil.failure(msg='登录失败,请检查邮箱')


@patientController.post("/detail/add/{patient_id}")
@ValidateFields(validate_model='add_patient_info')
async def add_patient_info(request: Request, patient_id: int, add_patient_detail_info: PatientDeTailModel,
                           query_db: AsyncSession = Depends(get_db)):
    patient = await  PatientService.get_patient_detail_by_id(query_db, patient_id)
    if not patient:
        return ResponseUtil.failure(msg='患者不存在')
    add_patient_detail_info.pid = patient.id
    add_patient_detail_info.create_time = datetime.now()
    add_patient_detail_info.update_time = datetime.now()
    add_patient_info_result = await   PatientDetailService.add_patient_info_services(request, query_db,
                                                                                     add_patient_detail_info)
    return ResponseUtil.success(msg='添加患者信息成功', data=add_patient_info_result)
