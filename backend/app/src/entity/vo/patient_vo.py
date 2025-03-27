# -*- coding:utf-8 -*-
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, EmailStr
from pydantic.alias_generators import to_camel
from typing import  Optional
from utils.pydantic_annotation import as_query


class PatientModel(BaseModel):
    """
    表对应pydantic模型
    """
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)
    address: Optional[str] =  Field(default=None, description='患者地址')
    allergies: Optional[str] =  Field(default=None, description='过敏情况')
    birth_date: Optional[datetime] =  Field(default=None, description='患者出生日期')
    create_time: Optional[datetime] =  Field(default=None, description='创建时间')
    current_medication: Optional[str] =  Field(default=None, description='当前用药')
    del_flag: Optional[str] =  Field(default=None, description='删除标志(0代表存在 1代表删除)')
    email: Optional[str] =  Field(default=None, description='患者电子邮件')
    emergency_contact_name: Optional[str] =  Field(default=None, description='紧急联系人姓名')
    emergency_contact_number: Optional[str] =  Field(default=None, description='紧急联系人电话号码')
    family_medical_history: Optional[str] =  Field(default=None, description='家族病史')
    gender: Optional[str] =  Field(default=None, description='患者性别(0:未知,1:男,2:女)')
    id: Optional[int] =  Field(default=None, description='')
    identification_document: Optional[str] =  Field(default=None, description='身份证明文件路径或URL')
    identification_number: Optional[str] =  Field(default=None, description='身份证明编号')
    identification_type: Optional[str] =  Field(default=None, description='身份证明类型')
    insurance_policy_number: Optional[str] =  Field(default=None, description='保险政策编号')
    insurance_provider: Optional[str] =  Field(default=None, description='保险提供商')
    name: Optional[str] =  Field(default=None, description='患者姓名')
    occupation: Optional[str] =  Field(default=None, description='患者职业')
    past_medical_history: Optional[str] =  Field(default=None, description='既往病史')
    phone: Optional[str] =  Field(default=None, description='患者电话号码')
    primary_physician: Optional[str] =  Field(default=None, description='主治医生')
    privacy_consent: Optional[int] =  Field(default=None, description='隐私同意')
    update_time: Optional[datetime] =  Field(default=None, description='更新时间')


@as_query
class PatientPageModel(PatientModel):
    """
    分页查询模型
    """
    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')


class PatientRegisterModel(PatientModel):
    """
    导出模型
    """
    name:Optional[str]  =Field(default=None, description='患者姓名' ,max_length=50)
    email:Optional[EmailStr]  =Field(default=None, description='患者电子邮件')
    phone:Optional[str]  =Field(default=None, description='患者电话号码',max_length=20)
