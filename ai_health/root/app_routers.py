from fastapi import APIRouter

from ai_health.routers.auth_router import auth_router
from ai_health.routers.appointments_router import appointment_router
from ai_health.routers.labreports_router import lab_report_router
from ai_health.routers.medical_hostory_router import medical_history_router
from ai_health.routers.medication_router import medication_router
from ai_health.routers.visits_router import visit_router


api = APIRouter(prefix="/v1")


api.include_router(auth_router)
api.include_router(appointment_router)
api.include_router(lab_report_router)
api.include_router(medical_history_router)
api.include_router(medication_router)
api.include_router(visit_router)
