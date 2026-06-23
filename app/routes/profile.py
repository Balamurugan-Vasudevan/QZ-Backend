from fastapi                   import APIRouter, Depends
from app.controllers.profile   import (
    get_profile, update_profile,
    update_password, delete_account,
    UpdateProfileSchema, UpdatePasswordSchema
)
from app.middleware.auth        import get_current_user

router = APIRouter(prefix="/api/profile", tags=["Profile"])

@router.get("/")
async def profile(current_user: dict = Depends(get_current_user)):
    return await get_profile(current_user)

@router.put("/")
async def update(
    data: UpdateProfileSchema,
    current_user: dict = Depends(get_current_user)
):
    return await update_profile(data, current_user)

@router.put("/password")
async def password(
    data: UpdatePasswordSchema,
    current_user: dict = Depends(get_current_user)
):
    return await update_password(data, current_user)

@router.delete("/")
async def delete(current_user: dict = Depends(get_current_user)):
    return await delete_account(current_user)