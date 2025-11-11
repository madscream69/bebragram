from sqlalchemy import create_engine  # Import to create DB engine.
from sqlalchemy.ext.declarative import declarative_base  # For base model class.
from sqlalchemy.orm import sessionmaker  # For creating sessions.
from dotenv import load_dotenv  # NEW: To load .env file
import os  # To read env vars.

load_dotenv()  # NEW: Load .env at the very top, before accessing env vars

DATABASE_URL = os.environ.get("DATABASE_URL")  # Now this will find the value from .env

engine = create_engine(DATABASE_URL)  # Engine is the core connection. Like starting a car engine to drive to the DB.

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)  # Session factory. Sessions are like temporary keys to access DB.

Base = declarative_base()  # Base class for all models. All DB tables will inherit from this.

def get_db():  # Dependency function to get a DB session.
    db = SessionLocal()  # Create a new session.
    try:
        yield db  # Yield for use in endpoints (async-friendly).
    finally:
        db.close()  # Always close to free resources, like hanging up a phone.