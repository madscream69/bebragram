from fastapi import APIRouter, Depends, HTTPException, status  # For router and deps.
from sqlalchemy.orm import Session  # For DB.
from .. import schemas, crud, auth, models  # Imports.
from ..database import get_db  # From database.py.

router = APIRouter(prefix="/users", tags=["users"])  # Group under /users.

@router.post("/", response_model=schemas.User)  # Register.
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@router.post("/login", response_model=schemas.Token)  # Login.
def login_for_access_token(form_data: auth.OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.get_user_by_username(db, form_data.username)
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    access_token = auth.create_access_token(data={"sub": user.username})
    refresh_token = auth.create_refresh_token(data={"sub": user.username})
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

@router.get("/me", response_model=schemas.User)  # Get current user profile.
def read_users_me(current_user: models.User = Depends(auth.get_current_user)):
    return current_user

@router.put("/me", response_model=schemas.User)  # Update profile.
def update_user_me(user_update: schemas.UserBase, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    current_user.email = user_update.email or current_user.email
    current_user.username = user_update.username or current_user.username
    current_user.bio = user_update.bio or current_user.bio
    db.commit()
    db.refresh(current_user)
    return current_user