# -*- coding:utf-8 -*-

from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from utils.common_util import CamelCaseUtil, export_list2excel
from utils.page_util import PageResponseModel
from src.dao.patient_dao import PatientDao
from src.entity.vo.patient_vo import PatientPageModel, PatientModel


class PatientService:
    """
    用户管理模块服务层
    """

    @classmethod
    async def get_patient_list(cls, query_db: AsyncSession, query_object: PatientPageModel, data_scope_sql: str) -> [list | PageResponseModel]:
        patient_list = await PatientDao.get_patient_list(query_db, query_object, data_scope_sql, is_page=True)
        return patient_list

    @classmethod
    async def get_patient_by_id(cls, query_db: AsyncSession, patient_id: int) -> PatientModel:
        patient = await  PatientDao.get_by_id(query_db, patient_id)
        patient_model = PatientModel(**CamelCaseUtil.transform_result(patient))
        return patient_model


    @classmethod
    async def add_patient(cls, query_db: AsyncSession, query_object: PatientModel) -> PatientModel:
        patient = await PatientDao.add_patient(query_db, query_object)
        patient_model = PatientModel(**CamelCaseUtil.transform_result(patient))
        return patient_model


    @classmethod
    async def update_patient(cls, query_db: AsyncSession, query_object: PatientModel) -> PatientModel:
        patient = await PatientDao.edit_patient(query_db, query_object)
        patient_model = PatientModel(**CamelCaseUtil.transform_result(patient))
        return patient_model


    @classmethod
    async def del_patient(cls, query_db: AsyncSession, patient_ids: List[str]):
        await PatientDao.del_patient(query_db, patient_ids)


    @classmethod
    async def export_patient_list(cls, query_db: AsyncSession, query_object: PatientPageModel, data_scope_sql) -> bytes:
        patient_list = await PatientDao.get_patient_list(query_db, query_object, data_scope_sql, is_page=False)
        filed_list = await SysTableService.get_sys_table_list(query_db, SysTablePageModel(tableName='patient'), is_page=False)
        filtered_filed = sorted(filter(lambda x: x["show"] == '1', filed_list), key=lambda x: x["sequence"])
        new_data = []
        for item in patient_list:
            mapping_dict = {}
            for fild in filtered_filed:
                if fild["prop"] in item:
                    mapping_dict[fild["label"]] = item[fild["prop"]]
            new_data.append(mapping_dict)
        binary_data = export_list2excel(new_data)
        return binary_data