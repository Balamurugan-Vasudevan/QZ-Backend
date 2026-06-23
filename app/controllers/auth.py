from fastapi      import HTTPException, status
from jose         import jwt
from datetime     import datetime, timedelta
from bson         import ObjectId
from app.config   import settings
from app.database import get_db
from app.schemas.user import RegisterSchema, LoginSchema
import bcrypt

def hash_password(password: str) -> str:
    pwd_bytes = password.encode('utf-8')
    salt      = bcrypt.gensalt()
    return bcrypt.hashpw(pwd_bytes, salt).decode('utf-8')

def verify_password(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(
        plain.encode('utf-8'),
        hashed.encode('utf-8')
    )

def create_token(user_id: str) -> str:
    expire  = datetime.utcnow() + timedelta(minutes=settings.JWT_EXPIRE_MINUTES)
    payload = {"sub": user_id, "exp": expire}
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)

async def register_user(data: RegisterSchema):
    db = get_db()

    existing = await db["users"].find_one({"email": data.email})
    if existing:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail      = "Email already registered"
        )

    # validate role
    if data.role not in ["student", "admin"]:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail      = "Invalid role. Must be student or admin"
        )

    user = {
        "_id":        str(ObjectId()),
        "name":       data.name,
        "email":      data.email,
        "password":   hash_password(data.password),
        "role":       data.role,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
    }
    await db["users"].insert_one(user)

    return {
        "id":    user["_id"],
        "name":  user["name"],
        "email": user["email"],
        "role":  user["role"],
        "token": create_token(user["_id"]),
    }

async def login_user(data: LoginSchema):
    db   = get_db()
    user = await db["users"].find_one({"email": data.email})

    if not user or not verify_password(data.password, user["password"]):
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail      = "Invalid email or password"
        )

    return {
        "id":    user["_id"],
        "name":  user["name"],
        "email": user["email"],
        "role":  user["role"],
        "token": create_token(user["_id"]),
    }

async def get_me(current_user: dict):
    return {
        "id":    current_user["_id"],
        "name":  current_user["name"],
        "email": current_user["email"],
        "role":  current_user["role"],
    }