from fastapi import APIRouter

from ai_health.routers.auth_router import auth_router


api = APIRouter(prefix="/v1")


api.include_router(auth_router)
