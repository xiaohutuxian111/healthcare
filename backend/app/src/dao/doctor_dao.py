# -*- coding:utf-8 -*-

from typing import List
from datetime import datetime, time

from pydantic import EmailStr
from sqlalchemy import and_, delete, desc, func, or_, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.src.entity.do.doctor_do import Doctor
from backend.app.src.entity.vo.doctor_vo import DoctorModel
from utils.page_util import PageUtil, PageResponseModel


class DoctorDao:

    @classmethod
    async def get_doctor_by_info(cls, db: AsyncSession, page_object: DoctorModel):
        """
        根据医生的数据查询医生信息
        """
        doctor_info = (
            (
                await   db.execute(
                    select(Doctor).where(
                        Doctor.name == page_object.name,
                        Doctor.email == page_object.email,
                        Doctor.del_flag == '0'
                    )
                )
            )
            .scalars()
            .first()
        )
        return doctor_info

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
    async def get_doctor_detail_by_id(cls, db: AsyncSession, doctor_id: int):
        doctor_info = (
            (await db.execute(select(Doctor).where(Doctor.id == doctor_id))).scalars().first()
        )
        return doctor_info

    @classmethod
    async def edit_doctor(cls, db: AsyncSession, doctor: dict):
        await  db.execute(update(Doctor), doctor)
