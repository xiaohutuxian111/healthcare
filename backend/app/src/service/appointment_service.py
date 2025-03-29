# -*- coding:utf-8 -*-

from typing import List
from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession

from config.constant import CommonConstant
from exceptions.exception import ServiceException
from src.entity.vo.commom_vo import CrudResponseModel
from utils.common_util import CamelCaseUtil, export_list2excel
from utils.page_util import PageResponseModel
from src.dao.appointment_dao import AppointmentDao
from src.entity.vo.appointment_vo import AppointmentPageModel, AppointmentModel
from backend.app.utils.log_util import logger


class AppointmentService:
    """
    预定管理服务层
    """

    @classmethod
    async def add_appointment_services(cls, request: Request, query_db: AsyncSession, page_object: AppointmentModel):
        """

        :param request:
        :param query_db:
        :param page_object:
        :return:
        """
        if not await  cls.check_appointment_unique_services(query_db, page_object):
            raise ServiceException(message="当前患者和医生已有预约")

        else:
            try:
                appointment = await AppointmentDao.add_appointment(query_db, page_object)
                return CrudResponseModel(is_success=True, message="预约成功")
            except Exception as e:
                logger.error(f"Unexpected error: {e}")
                raise ServiceException(message=f"预约失败")

    @classmethod
    async def check_appointment_unique_services(cls, query_db: AsyncSession, page_object: AppointmentModel):
        """
        检查订单的唯一性
        :param query_db:
        :param page_object:
        :return:
        """
        appoint_id = -1 if page_object.id is None else page_object.id
        appointment = await AppointmentDao.get_appointment_by_info(query_db, page_object)
        if appointment and appoint_id != appointment.id:
            return CommonConstant.NOT_UNIQUE
        return CommonConstant.UNIQUE
