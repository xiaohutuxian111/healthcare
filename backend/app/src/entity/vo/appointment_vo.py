# -*- coding:utf-8 -*-
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel
from typing import Optional
from utils.pydantic_annotation import as_query


class AppointmentModel(BaseModel):
    """
    表对应pydantic模型
    """
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)
    cancellation_reason: Optional[str] = Field(default=None, description='取消原因')
    create_time: Optional[datetime] = Field(default=None, description='创建时间')
    del_flag: Optional[str] = Field(default=None, description='删除标志(0代表存在 1代表删除)')
    did: Optional[int] = Field(default=None, description='医生ID')
    id: Optional[int] = Field(default=None, description='')
    note: Optional[str] = Field(default=None, description='预约备注')
    pid: Optional[int] = Field(default=None, description='患者ID')
    reason: Optional[str] = Field(default=None, description='预约原因')
    schedule: Optional[datetime] = Field(default=None, description='预约时间')
    status: Optional[int] = Field(default=None, description='预约状态:')
    update_time: Optional[datetime] = Field(default=None, description='更新时间')


@as_query
class AppointmentPageModel(AppointmentModel):
    """
    分页查询模型
    """
    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')
