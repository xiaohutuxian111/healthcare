# -*- coding:utf-8 -*-
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel
from typing import Optional,Literal

from pydantic_validation_decorator import NotBlank

from utils.pydantic_annotation import as_query


class AppointmentModel(BaseModel):
    """
    表对应pydantic模型
    """
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)

    id: Optional[int] = Field(default=None, description='订单ID')
    cancellation_reason: Optional[str] = Field(default=None, description='取消原因')
    del_flag: Literal['0','1'] = Field(default='0', description='删除标志(0代表存在 1代表删除)')
    did: Optional[int] = Field(default=None, description='医生ID')
    note: Optional[str] = Field(default=None, description='预约备注')
    pid: Optional[int] = Field(default=None, description='患者ID')
    reason: Optional[str] = Field(default=None, description='预约原因')
    schedule_start_time: Optional[datetime] = Field(default=None, description='预约开始时间')
    schedule_end_time: Optional[datetime] = Field(default=None, description='预约结束时间')
    status: Optional[int] = Field(default=None, description='预约状态:')
    create_time: Optional[datetime] = Field(default=None, description='创建时间')
    update_time: Optional[datetime] = Field(default=None, description='更新时间')

    @NotBlank(field_name='pid', message='患者ID不能为空')
    def get_pid(self):
        return self.pid

    @NotBlank(field_name='did', message='医生ID不能为空')
    def get_did(self):
        return self.did

    def validate_fields(self):
        self.get_pid()
        self.get_did()


class AppointmentBase(AppointmentModel):
    patient_name: Optional[str] = Field(default=None, description='患者姓名')
    doctor_name: Optional[str] = Field(default=None, description='医生姓名')

    appoint_begin_time: Optional[str] = Field(default=None, description='预约开始时间')
    appoint_end_time: Optional[str] = Field(default=None, description='预约结束时间')


@as_query
class AppointmentPageModel(AppointmentBase):
    """
    分页查询模型
    """
    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')
