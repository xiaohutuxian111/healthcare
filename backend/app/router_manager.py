from fastapi import APIRouter

from src.controller.doctor_controller import doctorController
from src.controller.appointment_controller import appointmentController
from src.controller.patient_controller import patientController
from src.controller.login_controller import loginController

app_controllers = [
    {'router': loginController, 'tags': ['登录模块']},
    {'router': patientController, 'tags': ['验证码模块']},
    {'router': doctorController, 'tags': ['系统管理-用户管理']},
    {'router': appointmentController, 'tags': ['系统管理-角色管理']},
]


def get_app_router():
    app_router = APIRouter(prefix="/api/v1")
    for controller in app_controllers:
        app_router.include_router(router=controller.get('router'),
                                  tags=controller.get('tags'))
    return app_router


def register_router():
    all_router = APIRouter()
    all_router.include_router(router=get_app_router())
    return all_router
