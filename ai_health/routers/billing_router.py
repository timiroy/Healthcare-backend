from fastapi import APIRouter, HTTPException, status, Depends
from uuid import UUID
from ai_health.schemas.auth_schemas import User
from ai_health.services.utils.auth_utils import get_current_user
from ai_health.schemas.billings_schema import (
    BillingCreate,
    BillingUpdate,
    Billing,
    BillingWithDoctor,
    BillingsWithDoctorList,
)
from ai_health.services.billing_service import (
    create_billing_service,
    get_billing_service,
    update_billing_service,
    delete_billing_service,
    get_billings_for_user,
)

billing_router = APIRouter(prefix="/billings", tags=["Billing Management"])


@billing_router.post("/", response_model=Billing)
async def create_billing(billing_create: BillingCreate, user: User = Depends(get_current_user)):
    return await create_billing_service(billing_create)


@billing_router.get("/", response_model=BillingsWithDoctorList)
async def get_billings(user: User = Depends(get_current_user)):
    return await get_billings_for_user(user_id=user.user_id.hex)


@billing_router.get("/{billing_id}", response_model=BillingWithDoctor)
async def get_billing(billing_id: str, user: User = Depends(get_current_user)):
    return await get_billing_service(billing_id)


@billing_router.patch("/{billing_id}", response_model=Billing)
async def update_billing(billing_id: str, billing_update: BillingUpdate, user: User = Depends(get_current_user)):
    return await update_billing_service(billing_id, billing_update)


@billing_router.delete("/{billing_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_billing(billing_id: str):
    if not await delete_billing_service(billing_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Billing record not found")
    return None
