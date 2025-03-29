# -*- coding:utf-8 -*-
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, EmailStr
from pydantic.alias_generators import to_camel
from typing import Optional, List, Literal

from pydantic_validation_decorator import NotBlank, Size

from backend.app.utils.pydantic_annotation import as_query


class DoctorModel(BaseModel):
    """
    表对应pydantic模型
    """
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)

    id: Optional[int] = Field(default=None, description='医生ID')
    name: Optional[str] = Field(default=None, description='医生姓名')
    email: Optional[EmailStr] = Field(default=None, description='医生邮箱')
    image_path: Optional[str] = Field(default=None, description='医生头像')

    create_time: Optional[datetime] = Field(default=None, description='创建时间')
    del_flag: Literal['0', '1'] = Field(default=None, description='删除标志(0代表存在 1代表删除)')
    update_time: Optional[datetime] = Field(default=None, description='更新时间')

    @NotBlank(field_name='name', message='医生姓名不能为空')
    @Size(field_name='name', min_length=3, max_length=20, message='医生姓名长度在3-20位之间')
    def get_name(self):
        return self.name

    @NotBlank(field_name='email', message='医生邮箱不能为空')
    def get_email(self):
        return self.email

    def validate_fields(self):
        self.get_name()
        self.get_email()


@as_query
class DoctorPageQueryModel(DoctorModel):
    """
    分页查询模型
    """
    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')


class DoctorQueryModel(DoctorModel):
    """
    查询模型
    """
    begin_time: Optional[str] = Field(default=None, description='开始时间')
    end_time: Optional[str] = Field(default=None, description='结束时间')


class DeleteDoctorModel(BaseModel):
    """
    删除模型
    """
    doctor_ids: List[int] = Field(default=None, description='医生id')
