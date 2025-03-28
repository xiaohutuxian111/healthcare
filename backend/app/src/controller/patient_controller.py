# -*- coding:utf-8 -*-

from fastapi import APIRouter, Depends, Form
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from backend.app.config.enums import BusinessType
from config.get_db import get_db

from backend.app.src.service.login_service import LoginService

from backend.app.src.entity.vo.user_vo import CurrentUserModel
from backend.app.utils.response_util import ResponseUtil
from backend.app.utils.common_util import bytes2file_response

from backend.app.src.entity.vo.patient_vo import PatientPageModel, PatientModel, PatientRegisterModel
from backend.app.src.service.patient_service import PatientService

patientController = APIRouter(prefix='/patients', dependencies=[Depends(LoginService.get_current_user)])


@patientController.get('/{patient_id}/register', response_model=PatientModel)
async def register_or_create(request: Request, patient_id: int, patient: PatientRegisterModel,
                             query_db: AsyncSession = Depends(get_db)):
    patient_info = await PatientService.get_patient_by_id(query_db, patient_id)

    print(patient_info)

    if patient_info is None:
        await  PatientService.add_patient(query_db, patient)




#
# @patientController.get('/list')
# async def get_patient_list(
#         request: Request,
#         query_db: AsyncSession = Depends(get_db),
#         page_query: PatientPageModel = Depends(PatientPageModel.as_query),
# ):
#     patient_result = await PatientService.get_patient_list(query_db, page_query)
#
#     return ResponseUtil.success(model_content=patient_result)
#
#
# @patientController.get('/getById/{patientId}')
# async def get_patient_by_id(
#         request: Request,
#         patientId: int,
#         query_db: AsyncSession = Depends(get_db),
# ):
#     patient = await PatientService.get_patient_by_id(query_db, patientId)
#     return ResponseUtil.success(data=patient)
#
#
# @patientController.post('/add')
# async def add_patient(
#         request: Request,
#         add_model: PatientModel,
#         query_db: AsyncSession = Depends(get_db),
#         current_user: CurrentUserModel = Depends(LoginService.get_current_user),
# ):
#     add_model.create_by = current_user.user.user_id
#     add_model.dept_id = current_user.user.dept_id
#     add_dict_type_result = await PatientService.add_patient(query_db, add_model)
#     return ResponseUtil.success(data=add_dict_type_result)
#
#
# @patientController.put('/update')
# async def update_patient(
#         request: Request,
#         edit_model: PatientModel,
#         query_db: AsyncSession = Depends(get_db),
#         current_user: CurrentUserModel = Depends(LoginService.get_current_user),
# ):
#     add_dict_type_result = await PatientService.update_patient(query_db, edit_model)
#     return ResponseUtil.success(data=add_dict_type_result)
#
#
# @patientController.delete('/delete/{patientIds}')
# async def del_patient(
#         request: Request,
#         patientIds: str,
#         query_db: AsyncSession = Depends(get_db),
#         current_user: CurrentUserModel = Depends(LoginService.get_current_user),
# ):
#     ids = patientIds.split(',')
#     del_result = await PatientService.del_patient(query_db, ids)
#     return ResponseUtil.success(data=del_result)
#
#
# @patientController.post('/export')
# async def export_patient(
#         request: Request,
#         patient_form: PatientPageModel = Form(),
#         query_db: AsyncSession = Depends(get_db),
# ):
#     # 获取全量数据
#     export_result = await PatientService.export_patient_list(
#         query_db, patient_form
#     )
#     return ResponseUtil.streaming(data=bytes2file_response(export_result))
