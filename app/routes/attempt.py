from fastapi                  import APIRouter, Depends
from app.controllers.attempt  import (
    get_public_quizzes, get_public_quiz,
    submit_attempt, get_my_attempts,
    get_quiz_attempts
)
from app.schemas.attempt      import SubmitAttemptSchema
from app.middleware.auth       import get_current_user
from app.middleware.role       import require_admin, require_student

router = APIRouter(prefix="/api/attempt", tags=["Attempt"])

# public routes — no auth needed
@router.get("/quizzes")
async def list_public_quizzes():
    return await get_public_quizzes()

@router.get("/quizzes/{quiz_id}")
async def single_public_quiz(quiz_id: str):
    return await get_public_quiz(quiz_id)

# student routes
@router.post("/submit")
async def submit(
    data: SubmitAttemptSchema,
    current_user: dict = Depends(get_current_user)
):
    return await submit_attempt(data, current_user)

@router.get("/my-attempts")
async def my_attempts(current_user: dict = Depends(get_current_user)):
    return await get_my_attempts(current_user)

# admin routes
@router.get("/quiz/{quiz_id}/results")
async def quiz_results(
    quiz_id: str,
    current_user: dict = Depends(require_admin)
):
    return await get_quiz_attempts(quiz_id, current_user)