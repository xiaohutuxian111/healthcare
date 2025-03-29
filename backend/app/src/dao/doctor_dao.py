# -*- coding:utf-8 -*-

from typing import List
from datetime import datetime, time

from pydantic import EmailStr
from sqlalchemy import and_, delete, desc, func, or_, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.src.entity.do.doctor_do import Doctor
from backend.app.src.entity.vo.doctor_vo import DoctorModel
from src.entity.vo.doctor_vo import DoctorPageQueryModel
from backend.app.utils.page_util import PageUtil, PageResponseModel


class DoctorDao:
    @classmethod
    async def get_doctor_by_id(cls, db: AsyncSession, doctor_id: int):
        doctor_info = (
            (await db.execute(select(Doctor).where(Doctor.id == doctor_id,Doctor.del_flag == '0'))).scalars().first()
        )
        return doctor_info
    @classmethod
    async def get_doctor_by_info(cls, db: AsyncSession, doctor: DoctorModel):
        """
        根据医生的数据查询医生信息
        """

        conditions = [doctor.del_flag == '0']
        if doctor.name is not None:
            conditions.append(doctor.name == doctor.name)
        if doctor.email is not None:
            conditions.append(doctor.email == doctor.email)

        db_doctor = (await db.execute(select(Doctor).where(*conditions))).scalars().first()
        return db_doctor

    @classmethod
    async def add_doctor(cls, db: AsyncSession, doctor: DoctorModel):
        """
        新增医生数据库操作
        """
        db_doctor = Doctor(**doctor.model_dump())
        db.add(db_doctor)
        await  db.flush()

        return db_doctor


    @classmethod
    async def edit_doctor(cls, db: AsyncSession, doctor: dict):
        await  db.execute(update(Doctor), doctor)

    @classmethod
    async def get_doctor_list(cls, db: AsyncSession, query_object: DoctorPageQueryModel, is_page: bool = False):
        """
        根据查询参数获取doctor的列表信息
        :param db:
        :param query_object:
        :param is_page:
        :return:
        """
        query = (
            select(Doctor)
            .where(
                Doctor.name.like(f"%{query_object.name}%") if query_object.name else True,
                Doctor.email.like(f"%{query_object.email}%") if query_object.email else True,
                Doctor.del_flag == query_object.del_flag if query_object.del_flag else True,
                Doctor.create_time.between(
                    datetime.combine(datetime.strptime(query_object.begin_time, '%Y-%m-%d'), time(00, 00, 00)),
                    datetime.combine(datetime.strptime(query_object.end_time, '%Y-%m-%d'), time(23, 59, 59)),
                )
                if query_object.begin_time and query_object.end_time else True,
            )
            .order_by(desc(Doctor.id))
            .distinct()
        )
        doctor_list = await PageUtil.paginate(db=db, query=query, page_num=query_object.page_num,
                                              page_size=query_object.page_size, is_page=is_page)
        return doctor_list

    @classmethod
    async def delete_doctor_dao(cls, db: AsyncSession, doctor: DoctorModel):
        """
        删除doctor的数据库操作
        :param db:
        :param doctor:
        :return:
        """
        await db.execute(delete(Doctor).where(Doctor.id.in_([doctor.id])))
