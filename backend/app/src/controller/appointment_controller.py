# -*- coding:utf-8 -*-

from fastapi import APIRouter, Depends, Form
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from config.get_db import get_db
from src.entity.vo.appointment_vo import AppointmentPageModel, AppointmentModel
from src.service.appointment_service import AppointmentService


from utils.response_util import ResponseUtil
from utils.common_util import bytes2file_response

appointmentController = APIRouter(prefix='/appointment', )

