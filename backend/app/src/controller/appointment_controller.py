# -*- coding:utf-8 -*-

from fastapi import APIRouter, Depends, Form
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from config.get_db import get_db
from src.entity.vo.appointment_vo import AppointmentPageModel, AppointmentModel
from src.entity.vo.user_vo import CurrentUserModel
from src.service.appointment_service import AppointmentService
from src.service.login_service import LoginService

from utils.response_util import ResponseUtil
from utils.common_util import bytes2file_response

appointmentController = APIRouter(prefix='/appointment', )


@appointmentController.get('/list', )
async def get_appointment_list(
        request: Request,
        query_db: AsyncSession = Depends(get_db),
        page_query: AppointmentPageModel = Depends(AppointmentPageModel.as_query),
):
    appointment_result = await AppointmentService.get_appointment_list(query_db, page_query)

    return ResponseUtil.success(model_content=appointment_result)


@appointmentController.get('/getById/{appointmentId}')
async def get_appointment_by_id(
        request: Request,
        appointmentId: int,
        query_db: AsyncSession = Depends(get_db),
):
    appointment = await AppointmentService.get_appointment_by_id(query_db, appointmentId)
    return ResponseUtil.success(data=appointment)


@appointmentController.post('/add')
async def add_appointment(
        request: Request,
        add_model: AppointmentModel,
        query_db: AsyncSession = Depends(get_db),
        current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    add_model.create_by = current_user.user.user_id
    add_model.dept_id = current_user.user.dept_id
    add_dict_type_result = await AppointmentService.add_appointment(query_db, add_model)
    return ResponseUtil.success(data=add_dict_type_result)


@appointmentController.put('/update')
async def update_appointment(
        request: Request,
        edit_model: AppointmentModel,
        query_db: AsyncSession = Depends(get_db),
        current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    add_dict_type_result = await AppointmentService.update_appointment(query_db, edit_model)
    return ResponseUtil.success(data=add_dict_type_result)


@appointmentController.delete('/delete/{appointmentIds}',)
async def del_appointment(
        request: Request,
        appointmentIds: str,
        query_db: AsyncSession = Depends(get_db),

):
    ids = appointmentIds.split(',')
    del_result = await AppointmentService.del_appointment(query_db, ids)
    return ResponseUtil.success(data=del_result)


@appointmentController.post('/export')
async def export_appointment(
        request: Request,
        appointment_form: AppointmentPageModel = Form(),
        query_db: AsyncSession = Depends(get_db),

):
    # 获取全量数据
    export_result = await AppointmentService.export_appointment_list(
        query_db, appointment_form
    )
    return ResponseUtil.streaming(data=bytes2file_response(export_result))


