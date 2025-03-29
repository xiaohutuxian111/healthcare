# -*- coding:utf-8 -*-
from typing import List

from pydantic import EmailStr
from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped, relationship

from backend.app.config.database import BaseMixin, Base



class Doctor(Base, BaseMixin):
    __tablename__ = "doctor"

    name: Mapped[str] = mapped_column(String(50), nullable=False, comment='医生姓名')
    email: Mapped[EmailStr] = mapped_column(String(50), nullable=False, comment='医生邮箱')
    image_path: Mapped[str] = mapped_column(String(255), nullable=True, comment='医生头像')


    def __repr__(self):
        return f"Doctor(id={self.id},name={self.name}, email={self.email}, image_path={self.image_path})"



