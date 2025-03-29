# -*- coding:utf-8 -*-
from datetime import datetime

from fastapi import APIRouter, Depends, Form
from pydantic_validation_decorator import ValidateFields
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from config.get_db import get_db
from src.entity.vo.appointment_vo import AppointmentPageModel, AppointmentModel
from src.service.appointment_service import AppointmentService
from src.service.doctor_service import DoctorService
from src.service.patient_service import PatientService
from backend.app.utils.log_util import logger
from utils.response_util import ResponseUtil
from utils.common_util import bytes2file_response


appointmentController = APIRouter(prefix='/appointment')


@appointmentController.get('/list', summary='获取预约列表')
async def get_appointment_list(
        request: Request,
        appointment_page_query: AppointmentPageModel = Form(),
        query_db: AsyncSession = Depends(get_db)
):
    pass


@appointmentController.post('/add', summary='添加预约')
@ValidateFields(validate_model='add_appointment_info')
async def add_appointment(
        request: Request,
        add_appointment_info: AppointmentModel,
        query_db: AsyncSession = Depends(get_db)
):
    patient = await PatientService.get_patient_by_id(query_db, add_appointment_info.pid)
    logger.warning(patient)
    if not patient:
        return ResponseUtil.failure(msg='患者不存在')
    doctor = await  DoctorService.get_doctor_by_id(query_db, add_appointment_info.did)
    logger.warning(f"{doctor}")
    if not doctor:
        return ResponseUtil.failure(msg='医生不存在')
    add_appointment_info.create_time = datetime.now()
    add_appointment_info.update_time = datetime.now()
    add_appointment_result = await AppointmentService.add_appointment_services(request, query_db, add_appointment_info)
    return ResponseUtil.success(msg='添加预约成功', data=add_appointment_result)
