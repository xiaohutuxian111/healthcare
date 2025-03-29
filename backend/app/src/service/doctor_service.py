# -*- coding:utf-8 -*-

from typing import List
from fastapi import Request

from pydantic import EmailStr
from pydantic_core.core_schema import plain_serializer_function_ser_schema
from redis.commands.search.commands import DICT_ADD_CMD
from sqlalchemy.ext.asyncio import AsyncSession

from config.constant import CommonConstant
from exceptions.exception import ServiceException
from src.entity.vo.commom_vo import CrudResponseModel
from src.entity.vo.doctor_vo import DeleteDoctorModel
from utils.common_util import CamelCaseUtil, export_list2excel
from utils.page_util import PageResponseModel
from src.dao.doctor_dao import DoctorDao
from backend.app.src.entity.vo.doctor_vo import DoctorModel, DoctorPageQueryModel
from backend.app.utils.log_util import logger


class DoctorService:
    """
    用户管理模块服务层
    """

    @classmethod
    async def add_doctor_services(cls, request: Request, query_db: AsyncSession, page_object: DoctorModel):
        if not await cls.check_doctor_unique_services(query_db, page_object):
            raise ServiceException(
                message=f'新增医生数据{page_object.name}失败,{page_object.name}已经存在'
            )
        else:
            try:
                await DoctorDao.add_doctor(query_db, page_object)
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='新增成功')
            except Exception as e:
                await query_db.rollback()
                raise e

    @classmethod
    async def check_doctor_unique_services(cls, query_db: AsyncSession, page_object: DoctorModel):
        """
        校验医生数据是否是唯一的service
        """
        doctor_id = -1 if page_object.id is None else page_object.id
        doctor = await DoctorDao.get_doctor_by_info(query_db, page_object)
        if doctor and doctor.id != doctor_id:
            return CommonConstant.NOT_UNIQUE
        return CommonConstant.UNIQUE

    @classmethod
    async def edit_doctor_services(cls, request: Request, query_db: AsyncSession, page_object: DoctorModel):
        """
        编辑doctor的service
        """
        doctor_info = await  cls.doctor_detail_services(query_db, page_object.id)
        if doctor_info.id:
            if not await cls.check_doctor_unique_services(query_db, page_object):
                raise ServiceException(
                    message=f'编辑医生数据{page_object.name}失败,{page_object.name}已经存在'
                )
            else:
                try:
                    edit_doctor_data = page_object.model_dump(exclude_unset=True)
                    await DoctorDao.edit_doctor(query_db, edit_doctor_data)
                    await query_db.commit()
                    return CrudResponseModel(is_success=True, message='更新doctor成功')
                except Exception as e:
                    await query_db.rollback()
                    raise e
        else:
            raise ServiceException(message='需要更改的doctor不存在')

    @classmethod
    async def doctor_detail_services(cls, query_db: AsyncSession, doctor_id: int):
        """
        获取doctor的详情信息
        :param query_db:
        :param doctor_id:
        :return:
        """
        doctor = await  DoctorDao.get_doctor_detail_by_id(query_db, doctor_id=doctor_id)
        if doctor:
            result = DoctorModel(**CamelCaseUtil.transform_result(doctor))
        else:
            result = DoctorModel(**dict())
        return result

    @classmethod
    async def get_doctor_list_services(cls, query_db: AsyncSession, doctor_page_query: DoctorPageQueryModel,
                                       is_page: bool = True):
        """
        获取 doctor.列表信息
        :param query_db:
        :param doctor_page_query:
        :param is_page:
        :return:
        """
        doctor_list_result = await DoctorDao.get_doctor_list(query_db, doctor_page_query, is_page=is_page)
        return doctor_list_result

    @classmethod
    async def del_doctor_services(cls, request: Request, query_db: AsyncSession, page_object: DeleteDoctorModel):
        """
        删除doctor中的信息
        :param request:
        :param query_db:
        :param page_object:
        :return:
        """
        if page_object.doctor_ids:
            doctor_id_list = page_object.doctor_ids.strip().split(',')
            try:
                delete_doctor_list = []
                for doctor_id in doctor_id_list:
                    doctor_info = await cls.doctor_detail_services(query_db, int(doctor_id))
                    # Todo 检查当前医生是否存在预约,存在不能删除

                    await DoctorDao.delete_doctor_dao(query_db, DoctorModel(id=int(doctor_id)))
                    delete_doctor_list.append(doctor_info)
                await   query_db.commit()
                return CrudResponseModel(is_success=True, message='删除doctor成功', result=delete_doctor_list)


            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='需要删除的doctor的id为空')

    @classmethod
    async def export_doctor_list_services(cls, doctor_list: List):
        """
        导出字典信息service
        :param doctor_list:
        :return:
        """
        mapping_dict = {
            'name': '医生姓名',
            'email': '医生邮箱',
            'delFlag': '状态'

        }

        data = doctor_list
        for item in data:
            if item['delFlag'] == '0':
                item['delFlag'] = '启用'
            else:
                item['delFlag'] = '禁用'
        new_data = [
            {mapping_dict.get(key): value for key, value in item.items() if mapping_dict.get(key)} for item in data
        ]
        binary_data = export_list2excel(new_data)

        return binary_data
