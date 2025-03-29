# -*- coding:utf-8 -*-
from datetime import datetime

from fastapi import APIRouter, Depends, Form, Request
from pydantic_validation_decorator import ValidateFields
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.config.get_db import get_db

from src.service.login_service import LoginService

from src.entity.vo.user_vo import CurrentUserModel
from utils.page_util import PageResponseModel
from utils.response_util import ResponseUtil
from utils.common_util import bytes2file_response
from backend.app.utils.log_util import logger

from src.entity.vo.doctor_vo import DoctorModel, DoctorPageQueryModel, DeleteDoctorModel
from backend.app.src.service.doctor_service import DoctorService

# doctorController = APIRouter(prefix='/doctor', dependencies=[Depends(LoginService.get_current_user)])
doctorController = APIRouter(prefix='/doctor')


@doctorController.get('/list', response_model=PageResponseModel)
async def get_doctor_list(
        request: Request,
        doctor_page_query: DoctorPageQueryModel = Depends(DoctorPageQueryModel.as_query),
        query_db: AsyncSession = Depends(get_db)
):
    """
    分页查询数据
    :param request:
    :param query_db:
    :return:
    """
    doctor_page_query_result = await DoctorService.get_doctor_list_services(query_db, doctor_page_query, is_page=True)
    logger.info("doctor分页查询成功")

    return ResponseUtil.success(model_content=doctor_page_query_result)


@doctorController.post('/add')
@ValidateFields(validate_model='add_doctor')
async def add_doctor(
        request: Request,
        add_doctor: DoctorModel,
        query_db: AsyncSession = Depends(get_db)

):
    add_doctor.create_time = datetime.now()
    add_doctor.update_time = datetime.now()
    add_doctor.del_flag = '0'
    add_doctor_result = await   DoctorService.add_doctor_services(request, query_db, add_doctor)
    return ResponseUtil.success(msg=add_doctor_result)


@doctorController.put('/edit')
@ValidateFields(validate_model='edit_doctor')
async def edit_doctor(request: Request, edit_doctor: DoctorModel, query_db: AsyncSession = Depends(get_db)):
    edit_doctor.update_time = datetime.now()
    if edit_doctor.id is None:
        return ResponseUtil.error(msg='id不能为空')
    edit_doctor_result = await DoctorService.edit_doctor_services(request, query_db, edit_doctor)
    logger.info(edit_doctor_result)
    return ResponseUtil.success(msg=edit_doctor_result.message)


@doctorController.delete('/delete/{doctor_ids}')
async def delete_doctor(
        request: Request,
        doctor_ids: str,
        query_db: AsyncSession = Depends(get_db)
):
    delete_doctor = DeleteDoctorModel(doctorIds=doctor_ids)
    delete_doctor_result = await DoctorService.del_doctor_services(request, query_db, delete_doctor)
    logger.info(delete_doctor_result.message)
    return ResponseUtil.success(msg=delete_doctor_result.message)
