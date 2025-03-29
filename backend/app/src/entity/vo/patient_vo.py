# -*- coding:utf-8 -*-
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, EmailStr
from pydantic.alias_generators import to_camel
from typing import Optional, Sized, Any, Self, Literal

from pydantic_validation_decorator import NotBlank, Size
from utils.pydantic_annotation import as_query



class PatientBase(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)
    name: Optional[str] = Field(default=None, description='患者姓名')
    email: Optional[EmailStr] = Field(default=None, description='患者电子邮件')

    @NotBlank(field_name='name', message='患者姓名不能为空')
    @Size(field_name='name', min_length=2, max_length=50)
    def get_name(self):
        return self.name

    @NotBlank(field_name='email', message='患者电子邮件不能为空')
    def get_email(self):
        return self.email

    def validate_fields(self):
        self.get_name()
        self.get_email()


class PatientModel(PatientBase):
    id: Optional[int] = Field(default=None, description='患者ID')
    birth_date: Optional[datetime] = Field(default=None, description='患者出生日期')
    gender: Optional[Literal['0', '1', '2']] = Field(default=None, description='患者性别(0:未知,1:男,2:女)')
    address: Optional[str] = Field(default=None, description='患者地址')
    occupation: Optional[str] = Field(default=None, description='患者职业')
    emergency_contact_name: Optional[str] = Field(default=None, description='紧急联系人姓名')
    emergency_contact_number: Optional[str] = Field(default=None, description='紧急联系人电话号码')
    insurance_provider: Optional[str] = Field(default=None, description='保险提供商')
    insurance_policy_number: Optional[str] = Field(default=None, description='保险政策编号')
    identification_type: Optional[str] = Field(default=None, description='身份证明类型')
    identification_number: Optional[str] = Field(default=None, description='身份证明编号')
    identification_document: Optional[str] = Field(default=None, description='身份证明文件路径或URL')
    del_flag: Literal['0', '1'] = Field(default=None, description='删除标志(0代表存在 1代表删除)')
    create_time: Optional[datetime] = Field(default=None, description='创建时间')
    update_time: Optional[datetime] = Field(default=None, description='更新时间')


class PatientQueryModel(PatientModel):
    """
    分页查询模型
    """
    begin_time: Optional[str] = Field(default=None, description='开始时间')
    end_time: Optional[str] = Field(default=None, description='结束时间')

    birth_begin_time:Optional[str] =Field(default=None,description='出生日期开始时间')
    birth_end_time:Optional[str] = Field(default=None,description='出生日期结束时间')

@as_query
class PatientPageQueryModel(PatientQueryModel):
    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')


class PatientDeTailModel(BaseModel):
    """
    表对应pydantic模型
    """
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)

    id: Optional[int] = Field(default=None, description='患者详情ID')
    primary_physician: Optional[str] = Field(default=None, description='主治医生')
    allergies: Optional[str] = Field(default=None, description='过敏情况')
    current_medication: Optional[str] = Field(default=None, description='当前用药')
    family_medical_history: Optional[str] = Field(default=None, description='家族病史')
    past_medical_history: Optional[str] = Field(default=None, description='既往病史')
    privacy_consent: Optional[int] = Field(default=None, description='隐私同意')
    pid: Optional[int] = Field(default=None, description='患者ID')
