from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import schemas, crud
from ..database import get_db
from ..auth import get_current_user
from ..models import User

router = APIRouter(prefix="/posts", tags=["posts"])

@router.post("/", response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return crud.create_post(db=db, post=post, owner_id=current_user.id)

@router.get("/", response_model=List[schemas.Post])  # Feed: posts from followed users.
def read_feed(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Query posts from following.
    following_ids = [f.followed_id for f in current_user.following]
    return db.query(models.Post).filter(models.Post.owner_id.in_(following_ids)).offset(skip).limit(limit).all()

@router.post("/{post_id}/like", response_model=schemas.Like)
def like_post(post_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    like = schemas.LikeCreate(post_id=post_id)
    return crud.create_like(db=db, like=like, user_id=current_user.id)

@router.delete("/{post_id}/like/{like_id}")
def unlike_post(like_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    like = crud.delete_like(db, like_id)
    if not like:
        raise HTTPException(status_code=404, detail="Like not found")
    return {"detail": "Unliked"}

@router.post("/{post_id}/comment", response_model=schemas.Comment)
def comment_post(post_id: int, comment: schemas.CommentCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    comment.post_id = post_id
    return crud.create_comment(db=db, comment=comment, user_id=current_user.id)