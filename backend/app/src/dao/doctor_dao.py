# -*- coding:utf-8 -*-

from typing import List
from datetime import datetime, time
from sqlalchemy import and_, delete, desc, func, or_, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.entity.do.doctor_do import Doctor
from src.entity.vo.doctor_vo import DoctorPageModel, DoctorModel
from utils.page_util import PageUtil, PageResponseModel


class DoctorDao:

    @classmethod
    async def get_by_id(cls, db: AsyncSession, doctor_id: int) -> Doctor:
        """根据主键获取单条记录"""
        doctor = (((await db.execute(
                            select(Doctor)
                            .where(Doctor.id == doctor_id)))
                       .scalars())
                       .first())
        return doctor

    """
    查询
    """
    @classmethod
    async def get_doctor_list(cls, db: AsyncSession,
                             query_object: DoctorPageModel,
                             data_scope_sql: str = None,
                             is_page: bool = False) -> [list | PageResponseModel]:

        query = (
            select(Doctor)
            .where(
                Doctor.image_path == query_object.image_path if query_object.image_path else True,
                Doctor.name == query_object.name if query_object.name else True,
                Doctor.del_flag == '0',
                eval(data_scope_sql) if data_scope_sql else True,
            )
            .order_by(desc(Doctor.create_time))
            .distinct()
        )
        doctor_list = await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page)
        return doctor_list


    @classmethod
    async def add_doctor(cls, db: AsyncSession, add_model: DoctorModel, auto_commit: bool = True) -> Doctor:
        """
        增加
        """
        doctor =  Doctor(**add_model.model_dump(exclude_unset=True))
        db.add(doctor)
        await db.flush()
        if auto_commit:
            await db.commit()
        return doctor

    @classmethod
    async def edit_doctor(cls, db: AsyncSession, edit_model: DoctorModel, auto_commit: bool = True) -> Doctor:
        """
        修改
        """
        edit_dict_data = edit_model.model_dump(exclude_unset=True)
        await db.execute(update(Doctor), [edit_dict_data])
        await db.flush()
        if auto_commit:
            await db.commit()
        return await cls.get_by_id(db, edit_model.id)

    @classmethod
    async def del_doctor(cls, db: AsyncSession, doctor_ids: List[str], soft_del: bool = True, auto_commit: bool = True):
        """
        删除
        """
        if soft_del:
            await db.execute(update(Doctor).where(Doctor.id.in_(doctor_ids)).values(del_flag='2'))
        else:
            await db.execute(delete(Doctor).where(Doctor.id.in_(doctor_ids)))
        await db.flush()
        if auto_commit:
            await db.commit()