from fastapi      import HTTPException
from bson         import ObjectId
from datetime     import datetime
from app.database import get_db
from app.schemas.attempt import SubmitAttemptSchema

async def get_public_quizzes():
    db      = get_db()
    cursor  = db["quizzes"].find({
        "status":     "published",
        "visibility": {"$in": ["public", "link"]}
    }).sort("created_at", -1)
    quizzes = await cursor.to_list(length=100)
    for q in quizzes:
        q["id"] = q["_id"]
        # hide correct answers from students
        for question in q.get("questions", []):
            for option in question.get("options", []):
                option.pop("isCorrect", None)
    return quizzes

async def get_public_quiz(quiz_id: str):
    db   = get_db()
    quiz = await db["quizzes"].find_one({
        "_id":    quiz_id,
        "status": "published"
    })
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")

    quiz["id"] = quiz["_id"]
    # hide correct answers
    for question in quiz.get("questions", []):
        for option in question.get("options", []):
            option.pop("isCorrect", None)
    return quiz

async def submit_attempt(data: SubmitAttemptSchema, current_user: dict):
    db   = get_db()

    # get quiz with answers
    quiz = await db["quizzes"].find_one({"_id": data.quiz_id})
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")

    # check max attempts
    if quiz.get("max_attempts"):
        existing = await db["attempts"].count_documents({
            "quiz_id": data.quiz_id,
            "user_id": current_user["_id"]
        })
        if existing >= quiz["max_attempts"]:
            raise HTTPException(
                status_code = 400,
                detail      = f"Maximum attempts ({quiz['max_attempts']}) reached"
            )

    # calculate score
    score = 0
    total = len(quiz["questions"])

    for answer in data.answers:
        idx = answer.question_index
        if idx >= total:
            continue
        question       = quiz["questions"][idx]
        correct        = [o["text"] for o in question["options"] if o["isCorrect"]]
        selected       = answer.selected_options
        if set(selected) == set(correct):
            score += 1

    percentage = (score / total * 100) if total > 0 else 0
    passed     = None
    if quiz.get("passing_score"):
        passed = percentage >= quiz["passing_score"]

    attempt = {
        "_id":        str(ObjectId()),
        "quiz_id":    data.quiz_id,
        "quiz_title": quiz["title"],
        "user_id":    current_user["_id"],
        "user_name":  current_user["name"],
        "score":      score,
        "total":      total,
        "percentage": round(percentage, 2),
        "passed":     passed,
        "answers":    [a.dict() for a in data.answers],
        "created_at": datetime.utcnow(),
    }
    await db["attempts"].insert_one(attempt)
    attempt["id"] = attempt["_id"]
    return attempt

async def get_my_attempts(current_user: dict):
    db      = get_db()
    cursor  = db["attempts"].find(
        {"user_id": current_user["_id"]}
    ).sort("created_at", -1)
    attempts = await cursor.to_list(length=100)
    for a in attempts:
        a["id"] = a["_id"]
    return attempts

async def get_quiz_attempts(quiz_id: str, current_user: dict):
    # only admin can see all attempts for a quiz
    db      = get_db()
    quiz    = await db["quizzes"].find_one({"_id": quiz_id})
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    if quiz["user_id"] != current_user["_id"]:
        raise HTTPException(status_code=403, detail="Not authorized")

    cursor   = db["attempts"].find({"quiz_id": quiz_id}).sort("created_at", -1)
    attempts = await cursor.to_list(length=100)
    for a in attempts:
        a["id"] = a["_id"]
    return attempts