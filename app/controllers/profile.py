from fastapi      import HTTPException, status
from bson         import ObjectId
from datetime     import datetime
from app.database import get_db
from pydantic     import BaseModel, EmailStr
from typing       import Optional
import bcrypt

class UpdateProfileSchema(BaseModel):
    name:         Optional[str]      = None
    email:        Optional[EmailStr] = None

class UpdatePasswordSchema(BaseModel):
    current_password: str
    new_password:     str

async def get_profile(current_user: dict):
    return {
        "id":         current_user["_id"],
        "name":       current_user["name"],
        "email":      current_user["email"],
        "role":       current_user["role"],
        "created_at": current_user.get("created_at"),
    }

async def update_profile(data: UpdateProfileSchema, current_user: dict):
    db          = get_db()
    update_data = {}

    if data.name:
        update_data["name"] = data.name

    if data.email:
        # check email not taken by another user
        existing = await db["users"].find_one({
            "email": data.email,
            "_id":   {"$ne": current_user["_id"]}
        })
        if existing:
            raise HTTPException(
                status_code = status.HTTP_400_BAD_REQUEST,
                detail      = "Email already in use"
            )
        update_data["email"] = data.email

    if not update_data:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail      = "No fields to update"
        )

    update_data["updated_at"] = datetime.utcnow()

    await db["users"].update_one(
        {"_id": current_user["_id"]},
        {"$set": update_data}
    )

    updated = await db["users"].find_one({"_id": current_user["_id"]})
    return {
        "id":    updated["_id"],
        "name":  updated["name"],
        "email": updated["email"],
        "role":  updated["role"],
    }

async def update_password(data: UpdatePasswordSchema, current_user: dict):
    db   = get_db()
    user = await db["users"].find_one({"_id": current_user["_id"]})

    # verify current password
    if not bcrypt.checkpw(
        data.current_password.encode('utf-8'),
        user["password"].encode('utf-8')
    ):
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail      = "Current password is incorrect"
        )

    if len(data.new_password) < 6:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail      = "New password must be at least 6 characters"
        )

    hashed = bcrypt.hashpw(
        data.new_password.encode('utf-8'),
        bcrypt.gensalt()
    ).decode('utf-8')

    await db["users"].update_one(
        {"_id": current_user["_id"]},
        {"$set": {"password": hashed, "updated_at": datetime.utcnow()}}
    )
    return {"message": "Password updated successfully"}

async def delete_account(current_user: dict):
    db = get_db()
    await db["users"].delete_one({"_id": current_user["_id"]})
    await db["attempts"].delete_many({"user_id": current_user["_id"]})
    return {"message": "Account deleted successfully"}