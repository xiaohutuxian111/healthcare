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
    async def get_by_id(cls, db: AsyncSession, appointment_id: int) -> Appointment:
        """根据主键获取单条记录"""
        appointment = (((await db.execute(
                            select(Appointment)
                            .where(Appointment.id == appointment_id)))
                       .scalars())
                       .first())
        return appointment

    """
    查询
    """
    @classmethod
    async def get_appointment_list(cls, db: AsyncSession,
                             query_object: AppointmentPageModel,
                             data_scope_sql: str = None,
                             is_page: bool = False) -> [list | PageResponseModel]:

        query = (
            select(Appointment)
            .where(
                Appointment.cancellation_reason == query_object.cancellation_reason if query_object.cancellation_reason else True,
                Appointment.did == query_object.did if query_object.did else True,
                Appointment.note == query_object.note if query_object.note else True,
                Appointment.pid == query_object.pid if query_object.pid else True,
                Appointment.reason == query_object.reason if query_object.reason else True,
                Appointment.schedule == query_object.schedule if query_object.schedule else True,
                Appointment.status == query_object.status if query_object.status else True,
                Appointment.del_flag == '0',
                eval(data_scope_sql) if data_scope_sql else True,
            )
            .order_by(desc(Appointment.create_time))
            .distinct()
        )
        appointment_list = await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page)
        return appointment_list


    @classmethod
    async def add_appointment(cls, db: AsyncSession, add_model: AppointmentModel, auto_commit: bool = True) -> Appointment:
        """
        增加
        """
        appointment =  Appointment(**add_model.model_dump(exclude_unset=True))
        db.add(appointment)
        await db.flush()
        if auto_commit:
            await db.commit()
        return appointment

    @classmethod
    async def edit_appointment(cls, db: AsyncSession, edit_model: AppointmentModel, auto_commit: bool = True) -> Appointment:
        """
        修改
        """
        edit_dict_data = edit_model.model_dump(exclude_unset=True)
        await db.execute(update(Appointment), [edit_dict_data])
        await db.flush()
        if auto_commit:
            await db.commit()
        return await cls.get_by_id(db, edit_model.id)

    @classmethod
    async def del_appointment(cls, db: AsyncSession, appointment_ids: List[str], soft_del: bool = True, auto_commit: bool = True):
        """
        删除
        """
        if soft_del:
            await db.execute(update(Appointment).where(Appointment.id.in_(appointment_ids)).values(del_flag='2'))
        else:
            await db.execute(delete(Appointment).where(Appointment.id.in_(appointment_ids)))
        await db.flush()
        if auto_commit:
            await db.commit()