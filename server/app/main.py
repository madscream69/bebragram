# main.py
import sys
from pathlib import Path

from .routers import users, posts, follows

sys.path.append(str(Path(__file__).parent.parent))  # Fix editor import

from fastapi import FastAPI
from . import models
from .database import engine
from dotenv import load_dotenv  # <-- NEW: Load .env
from fastapi.middleware.cors import CORSMiddleware  # Add this import.

# Load environment variables from .env file
load_dotenv()  # <-- THIS IS THE KEY LINE

app = FastAPI()
# After app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Frontend URL, change if different.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(users.router)
app.include_router(posts.router)
app.include_router(follows.router)
@app.get("/health")
def health_check():
    return {"status": "healthy"}

# Create tables (only runs once)
models.Base.metadata.create_all(bind=engine)

# step 19
# run server:
# uvicorn app.main:app --reload