from pydantic import BaseModel
from typing   import Optional, List
from datetime import datetime

class AnswerSchema(BaseModel):
    question_index: int
    selected_options: List[str]

class SubmitAttemptSchema(BaseModel):
    quiz_id: str
    answers: List[AnswerSchema]

class AttemptResponse(BaseModel):
    id:          str
    quiz_id:     str
    user_id:     str
    score:       int
    total:       int
    percentage:  float
    passed:      Optional[bool]
    answers:     List[AnswerSchema]
    created_at:  Optional[datetime]