from fastapi import APIRouter, Depends, HTTPException, status
from ai_health.schemas.visits_schema import (
    VisitCreate,
    Visit,
    VisitList,
    VisitUpdate,
)
from ai_health.services import visits_service
from ai_health.services.utils.auth_utils import get_current_user
from ai_health.schemas.auth_schemas import User, UserType

visit_router = APIRouter(prefix="/visits", tags=["Visit Management"])


@visit_router.post("/", response_model=Visit)
async def create_visit(visit_create: VisitCreate, user: User = Depends(get_current_user)):
    return await visits_service.create_visit(visit_create)


@visit_router.get("/{visit_id}", response_model=Visit)
async def get_visit(visit_id: str, user: User = Depends(get_current_user)):
    return await visits_service.get_visit_by_id(visit_id)


@visit_router.get("/", response_model=VisitList)
async def get_all_visits(user: User = Depends(get_current_user)):
    return await visits_service.get_all_visits()


@visit_router.patch("/{visit_id}", response_model=Visit)
async def update_visit(visit_id: str, visit_update: VisitUpdate, user: User = Depends(get_current_user)):
    return await visits_service.update_visit(visit_id, visit_update)


@visit_router.delete("/{visit_id}")
async def delete_visit(visit_id: str, user: User = Depends(get_current_user)):
    return await visits_service.delete_visit(visit_id)
