from fastapi          import Depends, HTTPException, status
from app.middleware.auth import get_current_user

def require_admin(current_user: dict = Depends(get_current_user)):
    if current_user.get("role") != "admin":
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail      = "Admin access required"
        )
    return current_user

def require_student(current_user: dict = Depends(get_current_user)):
    if current_user.get("role") != "student":
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail      = "Student access required"
        )
    return current_user