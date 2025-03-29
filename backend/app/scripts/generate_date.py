#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2025/3/28 22:16
# @Author  : stone
# @File    : generate_date.py
# @Desc    :
import asyncio




from backend.app.utils.fake_util import IDcardInfo, FakerUtil
from backend.app.src.entity.do.doctor_do import Doctor
from backend.app.config.database import *


async def generate_doctor_data(number: int):
    async with AsyncSessionLocal() as current_db:
        for _ in range(number):
            doctor = Doctor(
                name=FakerUtil.get_fake_name(),
                email=FakerUtil.get_fake_email(),
                image_path=FakerUtil.get_fake_word(),
            )
            current_db.add(doctor)
        await current_db.commit()


if __name__ == '__main__':
    asyncio.run(generate_doctor_data(50))
