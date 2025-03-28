from fastapi import APIRouter

from backend.app.src.controller.doctor_controller import doctorController
from backend.app.src.controller.appointment_controller import appointmentController
from backend.app.src.controller.patient_controller import patientController


app_controllers = [
    {'router': patientController, 'tags': ['患者模块']},
    {'router': doctorController, 'tags': ['医生模块']},
    {'router': appointmentController, 'tags': ['预定模块']},
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
