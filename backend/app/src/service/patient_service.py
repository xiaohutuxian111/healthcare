# -*- coding:utf-8 -*-

from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from config.constant import CommonConstant
from exceptions.exception import ServiceException
from src.entity.vo.commom_vo import CrudResponseModel
from src.entity.vo.patient_vo import PatientDeTailModel
from utils.common_util import CamelCaseUtil, export_list2excel
from utils.page_util import PageResponseModel
from fastapi import Request
from backend.app.src.dao.patient_dao import PatientDao, PatientDeTailDao
from backend.app.src.entity.vo.patient_vo import PatientModel
from utils.修改区域编码文件 import result_dict


class PatientService:
    """
    用户管理模块服务层
    """

    @classmethod
    async def get_patient_list(cls, request: Request, query_db: AsyncSession, page_object: PatientModel,
                               is_page: bool = False):
        """
        获取患者信息的services
        :param request:
        :param query_db:
        :param page_object:
        :param is_page:
        :return:
        """
        patient_list_result = await   PatientDao.get_patient_list(query_db, page_object, is_page)
        return patient_list_result

    @classmethod
    async def add_patient(cls, request: Request, query_db: AsyncSession, page_object: PatientModel):
        if not await  cls.check_patient_unique_services(query_db, page_object):
            raise ServiceException(message="该用户已存在")
        try:
            await   PatientDao.add_patient(query_db, page_object)
            await   query_db.commit()
            result = dict(is_success=True, message="添加成功")
        except Exception as e:
            await   query_db.rollback()
            raise e
        return CrudResponseModel(**result)

    @classmethod
    async def check_patient_unique_services(cls, query_db, page_object: PatientModel):
        patient_id = -1 if page_object.id is None else page_object.id
        patient = await  PatientDao.get_patient_detail_by_info(query_db, page_object)
        if patient and patient_id != page_object.id:
            return CommonConstant.NOT_UNIQUE
        return CommonConstant.UNIQUE

    @classmethod
    async def get_patient_detail_by_id(cls, query_db: AsyncSession, patient_id: int):
        patient_query = PatientModel(id=patient_id)
        patient = await  PatientDao.get_patient_detail_by_info(query_db, patient_query)
        return patient

    @classmethod
    async def get_patient_info(cls, query_db: AsyncSession, query_patient: PatientModel):
        patient = await PatientDao.get_patient_detail_by_info(query_db, query_patient)
        return patient


class PatientDetailService:

    @classmethod
    async def add_patient_info_services(cls, request, query_db: AsyncSession, add_patient_info: PatientDeTailModel):
        try:
            await  PatientDeTailDao.add_patient_detail_info(query_db, add_patient_info)
            await query_db.commit()
            result = dict(is_success=True, message="添加患者详情信息成功")
        except Exception as e:
            await query_db.rollback()
            raise e
        return CrudResponseModel(**result)
