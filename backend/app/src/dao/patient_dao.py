# -*- coding:utf-8 -*-

from typing import List
from sqlalchemy import and_, delete, desc, func, or_, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.entity.do.patient_do import Patient
from src.entity.vo.patient_vo import PatientPageModel, PatientModel
from utils.page_util import PageUtil, PageResponseModel


class PatientDao:

    @classmethod
    async def get_by_id(cls, db: AsyncSession, patient_id: int) -> Patient:
        """根据主键获取单条记录"""
        patient = (((await db.execute(
                            select(Patient)
                            .where(Patient.id == patient_id)))
                       .scalars())
                       .first())
        return patient

    """
    查询
    """
    @classmethod
    async def get_patient_list(cls, db: AsyncSession,
                             query_object: PatientPageModel,
                             data_scope_sql: str = None,
                             is_page: bool = False) -> [list | PageResponseModel]:

        query = (
            select(Patient)
            .where(
                Patient.address == query_object.address if query_object.address else True,
                Patient.allergies == query_object.allergies if query_object.allergies else True,
                Patient.birth_date == query_object.birth_date if query_object.birth_date else True,
                Patient.current_medication == query_object.current_medication if query_object.current_medication else True,
                Patient.email == query_object.email if query_object.email else True,
                Patient.emergency_contact_name == query_object.emergency_contact_name if query_object.emergency_contact_name else True,
                Patient.emergency_contact_number == query_object.emergency_contact_number if query_object.emergency_contact_number else True,
                Patient.family_medical_history == query_object.family_medical_history if query_object.family_medical_history else True,
                Patient.gender == query_object.gender if query_object.gender else True,
                Patient.identification_document == query_object.identification_document if query_object.identification_document else True,
                Patient.identification_number == query_object.identification_number if query_object.identification_number else True,
                Patient.identification_type == query_object.identification_type if query_object.identification_type else True,
                Patient.insurance_policy_number == query_object.insurance_policy_number if query_object.insurance_policy_number else True,
                Patient.insurance_provider == query_object.insurance_provider if query_object.insurance_provider else True,
                Patient.name == query_object.name if query_object.name else True,
                Patient.occupation == query_object.occupation if query_object.occupation else True,
                Patient.past_medical_history == query_object.past_medical_history if query_object.past_medical_history else True,
                Patient.phone == query_object.phone if query_object.phone else True,
                Patient.primary_physician == query_object.primary_physician if query_object.primary_physician else True,
                Patient.privacy_consent == query_object.privacy_consent if query_object.privacy_consent else True,
                Patient.del_flag == '0',
                eval(data_scope_sql) if data_scope_sql else True,
            )
            .order_by(desc(Patient.create_time))
            .distinct()
        )
        patient_list = await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page)
        return patient_list


    @classmethod
    async def add_patient(cls, db: AsyncSession, add_model: PatientModel, auto_commit: bool = True) -> Patient:
        """
        增加
        """
        patient =  Patient(**add_model.model_dump(exclude_unset=True))
        db.add(patient)
        await db.flush()
        if auto_commit:
            await db.commit()
        return patient

    @classmethod
    async def edit_patient(cls, db: AsyncSession, edit_model: PatientModel, auto_commit: bool = True) -> Patient:
        """
        修改
        """
        edit_dict_data = edit_model.model_dump(exclude_unset=True)
        await db.execute(update(Patient), [edit_dict_data])
        await db.flush()
        if auto_commit:
            await db.commit()
        return await cls.get_by_id(db, edit_model.id)

    @classmethod
    async def del_patient(cls, db: AsyncSession, patient_ids: List[str], soft_del: bool = True, auto_commit: bool = True):
        """
        删除
        """
        if soft_del:
            await db.execute(update(Patient).where(Patient.id.in_(patient_ids)).values(del_flag='2'))
        else:
            await db.execute(delete(Patient).where(Patient.id.in_(patient_ids)))
        await db.flush()
        if auto_commit:
            await db.commit()