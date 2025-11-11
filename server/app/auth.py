from datetime import datetime, timedelta, timezone  # For token expiration.
from jose import JWTError, jwt  # PyJWT under jose.
from fastapi import Depends, HTTPException, status  # For dependencies and errors.
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm  # For login form.
from passlib.context import CryptContext  # For hashing.
from sqlalchemy.orm import Session  # For DB.
from . import schemas, models, database  # Imports.
from os import environ  # For secret.

SECRET_KEY = environ.get("JWT_SECRET")  # From .env.
ALGORITHM = "HS256"  # Signing algorithm.
ACCESS_TOKEN_EXPIRE_MINUTES = int(environ.get("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", 30))
REFRESH_TOKEN_EXPIRE_MINUTES = int(environ.get("JWT_REFRESH_TOKEN_EXPIRE_MINUTES", 1440))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")  # Hashing context.

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")  # Tells FastAPI where login is.

def verify_password(plain_password, hashed_password):  # Check password.
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):  # Hash password.
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta = None):  # Create JWT.
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: dict):  # Longer-lived token.
    return create_access_token(data, expires_delta=timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES))

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):  # Decode token to get user.
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = db.query(models.User).filter(models.User.username == token_data.username).first()
    if user is None:
        raise credentials_exception
    return user