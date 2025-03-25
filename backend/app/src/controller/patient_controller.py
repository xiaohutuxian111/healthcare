# -*- coding:utf-8 -*-

from fastapi import APIRouter, Depends, Form
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from config.enums import BusinessType
from config.get_db import get_db

from src.service.login_service import LoginService

from src.entity.vo.user_vo import CurrentUserModel
from utils.response_util import ResponseUtil
from utils.common_util import bytes2file_response

from src.entity.vo.patient_vo import PatientPageModel, PatientModel
from src.service.patient_service import PatientService

patientController = APIRouter(prefix='/patient/patient', dependencies=[Depends(LoginService.get_current_user)])


@patientController.get('/list')
async def get_patient_list(
        request: Request,
        query_db: AsyncSession = Depends(get_db),
        page_query: PatientPageModel = Depends( PatientPageModel.as_query),
):
    patient_result = await PatientService.get_patient_list(query_db, page_query)

    return ResponseUtil.success(model_content=patient_result)

@patientController.get('/getById/{patientId}')
async def get_patient_by_id(
        request: Request,
        patientId: int,
        query_db: AsyncSession = Depends(get_db),
):
    patient = await PatientService.get_patient_by_id(query_db, patientId)
    return ResponseUtil.success(data=patient)


@patientController.post('/add')
@Log(title='patient', business_type=BusinessType.INSERT)
async def add_patient (
    request: Request,
    add_model: PatientModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):

    add_model.create_by = current_user.user.user_id
    add_model.dept_id = current_user.user.dept_id
    add_dict_type_result = await PatientService.add_patient(query_db, add_model)
    return ResponseUtil.success(data=add_dict_type_result)

@patientController.put('/update')
@Log(title='patient', business_type=BusinessType.UPDATE)
async def update_patient(
    request: Request,
    edit_model: PatientModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    add_dict_type_result = await PatientService.update_patient(query_db, edit_model)
    return ResponseUtil.success(data=add_dict_type_result)


@patientController.delete('/delete/{patientIds}')
@Log(title='patient', business_type=BusinessType.DELETE)
async def del_patient(
    request: Request,
    patientIds: str,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    ids = patientIds.split(',')
    del_result = await PatientService.del_patient(query_db, ids)
    return ResponseUtil.success(data=del_result)

@patientController.post('/export')
@Log(title='patient', business_type=BusinessType.EXPORT)
async def export_patient(
    request: Request,
    patient_form: PatientPageModel = Form(),
    query_db: AsyncSession = Depends(get_db),
):
    # 获取全量数据
    export_result = await PatientService.export_patient_list(
        query_db, patient_form
    )
    return ResponseUtil.streaming(data=bytes2file_response(export_result))

