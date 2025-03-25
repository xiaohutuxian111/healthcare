# -*- coding:utf-8 -*-

from fastapi import APIRouter, Depends, Form,Request
from sqlalchemy.ext.asyncio import AsyncSession
from config.get_db import get_db

from src.service.login_service import LoginService

from src.entity.vo.user_vo import CurrentUserModel
from utils.response_util import ResponseUtil
from utils.common_util import bytes2file_response

from src.entity.vo.doctor_vo import DoctorPageModel, DoctorModel
from src.service.doctor_service import DoctorService

doctorController = APIRouter(prefix='/doctor', dependencies=[Depends(LoginService.get_current_user)])


@doctorController.get('/list')
async def get_doctor_list(
        request: Request,
        query_db: AsyncSession = Depends(get_db),
        page_query: DoctorPageModel = Depends( DoctorPageModel.as_query),
):
    doctor_result = await DoctorService.get_doctor_list(query_db, page_query)

    return ResponseUtil.success(model_content=doctor_result)

@doctorController.get('/getById/{doctorId}')
async def get_doctor_by_id(
        request: Request,
        doctorId: int,
        query_db: AsyncSession = Depends(get_db),

):
    doctor = await DoctorService.get_doctor_by_id(query_db, doctorId)
    return ResponseUtil.success(data=doctor)


@doctorController.post('/add')
async def add_doctor (
    request: Request,
    add_model: DoctorModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):

    add_model.create_by = current_user.user.user_id
    add_model.dept_id = current_user.user.dept_id
    add_dict_type_result = await DoctorService.add_doctor(query_db, add_model)
    return ResponseUtil.success(data=add_dict_type_result)

@doctorController.put('/update')
async def update_doctor(
    request: Request,
    edit_model: DoctorModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    add_dict_type_result = await DoctorService.update_doctor(query_db, edit_model)
    return ResponseUtil.success(data=add_dict_type_result)


@doctorController.delete('/delete/{doctorIds}')
async def del_doctor(
    request: Request,
    doctorIds: str,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    ids = doctorIds.split(',')
    del_result = await DoctorService.del_doctor(query_db, ids)
    return ResponseUtil.success(data=del_result)

@doctorController.post('/export')

async def export_doctor(
    request: Request,
    doctor_form: DoctorPageModel = Form(),
    query_db: AsyncSession = Depends(get_db),
):
    # 获取全量数据
    export_result = await DoctorService.export_doctor_list(
        query_db, doctor_form
    )
    return ResponseUtil.streaming(data=bytes2file_response(export_result))

