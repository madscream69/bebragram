from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, crud
from ..database import get_db
from ..auth import get_current_user
from ..models import User

router = APIRouter(prefix="/follows", tags=["follows"])

@router.post("/", response_model=schemas.Follow)
def follow_user(follow: schemas.FollowCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return crud.create_follow(db=db, follow=follow, follower_id=current_user.id)

@router.delete("/{follow_id}")
def unfollow_user(follow_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    follow = crud.delete_follow(db, follow_id)
    if not follow:
        raise HTTPException(status_code=404, detail="Follow not found")
    return {"detail": "Unfollowed"}