# -*- coding:utf-8 -*-
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel
from typing import Optional
from utils.pydantic_annotation import as_query


class DoctorModel(BaseModel):
    """
    表对应pydantic模型
    """
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)
    create_time: Optional[datetime] = Field(default=None, description='创建时间')
    del_flag: Optional[str] = Field(default=None, description='删除标志(0代表存在 1代表删除)')
    id: Optional[int] = Field(default=None, description='')
    image_path: Optional[str] = Field(default=None, description='医生头像')
    name: Optional[str] = Field(default=None, description='医生姓名')
    update_time: Optional[datetime] = Field(default=None, description='更新时间')


@as_query
class DoctorPageModel(DoctorModel):
    """
    分页查询模型
    """
    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')
