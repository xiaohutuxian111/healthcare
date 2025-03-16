#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2025/3/16 18:23
# @Author  : stone
# @File    : emu.py
# @Desc    :
import enum


class Gender(enum.Enum):
    """
    性别
    """
    Male = "Male"
    Female = "Female"
    Other = "Other"
