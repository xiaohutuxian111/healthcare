# -*- coding:utf-8 -*-

from typing import List
from datetime import datetime, time
from sqlalchemy import and_, delete, desc, func, or_, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.src.entity.do.appointment_do import Appointment
from backend.app.src.entity.vo.appointment_vo import AppointmentPageModel, AppointmentModel
from utils.page_util import PageUtil, PageResponseModel


class AppointmentDao:

    @classmethod
    async def get_appointment_by_info(cls, db: AsyncSession, query_appointment: AppointmentModel):
        """
        判断订单是否是唯一的,相同的pid,did 且时间有交接
        :param db:
        :param query_appointment:
        :return:
        """
        db_appointment = (
            await  db.execute(
                select(Appointment).where(
                    Appointment.did == query_appointment.did if query_appointment.did else True,
                    Appointment.pid == query_appointment.pid if query_appointment.pid else True,
                    or_(
                        and_(
                            Appointment.schedule_start_time <= query_appointment.schedule_end_time,
                            Appointment.schedule_end_time >= query_appointment.schedule_start_time
                        ),
                        and_(
                            query_appointment.schedule_start_time <= Appointment.schedule_end_time,
                            query_appointment.schedule_end_time >= Appointment.schedule_start_time
                        )
                    ) if query_appointment.schedule_start_time and query_appointment.schedule_end_time else True,
                    Appointment.del_flag == '0'

                )
            )

        ).scalars().first()
        return db_appointment

    @classmethod
    async def add_appointment(cls, db: AsyncSession, appoint: AppointmentModel):
        """
        添加订单预约
        :param db:
        :param appoint:
        :return:
        """
        db_appoint = Appointment(**appoint.model_dump())
        db.add(db_appoint)
        await  db.flush()

        return db_appoint
