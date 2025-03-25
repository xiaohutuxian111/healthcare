# -*- coding:utf-8 -*-

from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from utils.common_util import CamelCaseUtil, export_list2excel
from utils.page_util import PageResponseModel
from src.dao.doctor_dao import DoctorDao
from src.entity.vo.doctor_vo import DoctorPageModel, DoctorModel


class DoctorService:
    """
    用户管理模块服务层
    """

    @classmethod
    async def get_doctor_list(cls, query_db: AsyncSession, query_object: DoctorPageModel) -> [list | PageResponseModel]:
        doctor_list = await DoctorDao.get_doctor_list(query_db, query_object, is_page=True)
        return doctor_list

    @classmethod
    async def get_doctor_by_id(cls, query_db: AsyncSession, doctor_id: int) -> DoctorModel:
        doctor = await  DoctorDao.get_by_id(query_db, doctor_id)
        doctor_model = DoctorModel(**CamelCaseUtil.transform_result(doctor))
        return doctor_model


    @classmethod
    async def add_doctor(cls, query_db: AsyncSession, query_object: DoctorModel) -> DoctorModel:
        doctor = await DoctorDao.add_doctor(query_db, query_object)
        doctor_model = DoctorModel(**CamelCaseUtil.transform_result(doctor))
        return doctor_model


    @classmethod
    async def update_doctor(cls, query_db: AsyncSession, query_object: DoctorModel) -> DoctorModel:
        doctor = await DoctorDao.edit_doctor(query_db, query_object)
        doctor_model = DoctorModel(**CamelCaseUtil.transform_result(doctor))
        return doctor_model


    @classmethod
    async def del_doctor(cls, query_db: AsyncSession, doctor_ids: List[str]):
        await DoctorDao.del_doctor(query_db, doctor_ids)


