# -*- coding:utf-8 -*-

from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from utils.common_util import CamelCaseUtil, export_list2excel
from utils.page_util import PageResponseModel
from src.dao.appointment_dao import AppointmentDao
from src.entity.vo.appointment_vo import AppointmentPageModel, AppointmentModel


class AppointmentService:
    """
    用户管理模块服务层
    """

    @classmethod
    async def get_appointment_list(cls, query_db: AsyncSession, query_object: AppointmentPageModel, data_scope_sql: str) -> [list | PageResponseModel]:
        appointment_list = await AppointmentDao.get_appointment_list(query_db, query_object, data_scope_sql, is_page=True)
        return appointment_list

    @classmethod
    async def get_appointment_by_id(cls, query_db: AsyncSession, appointment_id: int) -> AppointmentModel:
        appointment = await  AppointmentDao.get_by_id(query_db, appointment_id)
        appointment_model = AppointmentModel(**CamelCaseUtil.transform_result(appointment))
        return appointment_model


    @classmethod
    async def add_appointment(cls, query_db: AsyncSession, query_object: AppointmentModel) -> AppointmentModel:
        appointment = await AppointmentDao.add_appointment(query_db, query_object)
        appointment_model = AppointmentModel(**CamelCaseUtil.transform_result(appointment))
        return appointment_model


    @classmethod
    async def update_appointment(cls, query_db: AsyncSession, query_object: AppointmentModel) -> AppointmentModel:
        appointment = await AppointmentDao.edit_appointment(query_db, query_object)
        appointment_model = AppointmentModel(**CamelCaseUtil.transform_result(appointment))
        return appointment_model


    @classmethod
    async def del_appointment(cls, query_db: AsyncSession, appointment_ids: List[str]):
        await AppointmentDao.del_appointment(query_db, appointment_ids)

