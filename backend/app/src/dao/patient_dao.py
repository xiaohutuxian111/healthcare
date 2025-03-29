# -*- coding:utf-8 -*-
from datetime import datetime, time
from typing import List

from dns.e164 import query
from sqlalchemy import and_, delete, desc, func, or_, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.src.entity.do.patient_do import Patient, PatientDetail
from backend.app.src.entity.vo.patient_vo import PatientModel, PatientPageQueryModel
from backend.app.utils.page_util import PageUtil, PageResponseModel
from src.entity.vo.patient_vo import PatientDeTailModel


class PatientDao:

    @classmethod
    async   def  get_patient_by_id(cls, db: AsyncSession, patient_id: int):
        """
        通过患者ID获取患者信息
        :param db:
        :param patient_id:
        :return:
        """
        db_patient = (
            (
                await db.execute(
                    select(Patient)
                    .where(
                        Patient.id == patient_id,
                        Patient.del_flag == '0'
                    )
                )
            ).scalars().first()
        )
        return   db_patient
    @classmethod
    async def get_patient_detail_by_info(cls, db: AsyncSession, patient_info: PatientModel):
        """
        通过用户名和手机号确定唯一患者
        :param db:
        :param patient_info:
        :return:
        """
        patient_info = (
            (
                await db.execute(
                    select(Patient)
                    .where(
                        Patient.name == patient_info.name if patient_info.name else True,
                        Patient.email == patient_info.email if patient_info.email else True,
                        Patient.del_flag == '0'
                    )
                )
            ).scalars().first()
        )
        return patient_info

    @classmethod
    async def add_patient(cls, db: AsyncSession, patient: PatientModel):
        db_patient = Patient(**patient.model_dump())
        db.add(db_patient)
        await db.flush()

        return db_patient

    @classmethod
    async def get_patient_list(cls, db: AsyncSession, query_object: PatientPageQueryModel, is_page: bool = False):
        """
        通过查询参数对象获取患者信息列表
        :param db:
        :param query_object:
        :param is_page:
        :return:
        """
        query = (
            select(Patient).where(
                Patient.name.like(f'%{query_object.name}%') if query_object.name else True,
                Patient.email.like(f'%{query_object.email}%') if query_object.email else True,
                Patient.id == query_object.id if query_object.id else True,
                Patient.gender == query_object.gender if query_object.gender else True,
                Patient.occupation.like(f'%{query_object.occupation}%') if query_object.occupation else True,
                Patient.identification_number.like(
                    f'%{query_object.identification_number}%') if query_object.identification_number else True,
                Patient.del_flag == '0',
                Patient.create_time.between(
                    datetime.combine(datetime.strptime(query_object.begin_time, '%Y-%m-%d'), time(00, 00, 00)),
                    datetime.combine(datetime.strptime(query_object.end_time, '%Y-%m-%d'), time(23, 59, 59)),
                ),
                Patient.birth_date.between(
                    datetime.combine(datetime.strptime(query_object.birth_begin_time, '%Y-%m-%d'), time(00, 00, 00)),
                    datetime.combine(datetime.strptime(query_object.birth_end_time, '%Y-%m-%d'), time(23, 59, 59)),
                )
            )
            .order_by(desc(Patient.create_time))
        )
        patient_list = await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page)
        return patient_list


class PatientDeTailDao:

    @classmethod
    async def add_patient_detail_info(cls, db: AsyncSession, add_patient_info: PatientDeTailModel):
        db_patient_detail = PatientDetail(**add_patient_info.model_dump())
        db.add(db_patient_detail)
        await db.flush()

        return db_patient_detail
