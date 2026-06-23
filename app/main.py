from fastapi              import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib           import asynccontextmanager
from app.database         import connect_db, close_db
from app.routes           import auth, quiz, attempt, profile   # ← add profile
import os

@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_db()
    yield
    await close_db()

app = FastAPI(
    title    = "Quiz Builder API",
    version  = "1.0.0",
    lifespan = lifespan
)

origins = [
    "http://localhost:5173",
    os.getenv("FRONTEND_URL", "*"),
]

app.add_middleware(
    CORSMiddleware,
    allow_origins     = origins,
    allow_credentials = True,
    allow_methods     = ["*"],
    allow_headers     = ["*"],
)

app.include_router(auth.router)
app.include_router(quiz.router)
app.include_router(attempt.router)
app.include_router(profile.router)    # ← add this

@app.get("/")
async def root():
    return {"message": "Quiz Builder API is running"}

@app.get("/api/health")
async def health():
    return {"status": "healthy"}