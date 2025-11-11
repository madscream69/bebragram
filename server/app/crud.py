from sqlalchemy.orm import Session  # For DB sessions.
from . import models, schemas  # Imports.
from .auth import get_password_hash  # For hashing.

def get_user(db: Session, user_id: int):  # Read user by ID.
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):  # Create user with hashed password.
    hashed_password = get_password_hash(user.password)
    db_user = models.User(email=user.email, username=user.username, hashed_password=hashed_password, bio=user.bio)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Similar for Post
def create_post(db: Session, post: schemas.PostCreate, owner_id: int):
    db_post = models.Post(**post.dict(), owner_id=owner_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

def get_posts(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Post).offset(skip).limit(limit).all()

def get_post(db: Session, post_id: int):
    return db.query(models.Post).filter(models.Post.id == post_id).first()

# Likes
def create_like(db: Session, like: schemas.LikeCreate, user_id: int):
    db_like = models.Like(**like.dict(), user_id=user_id)
    db.add(db_like)
    db.commit()
    db.refresh(db_like)
    return db_like

def delete_like(db: Session, like_id: int):
    db_like = db.query(models.Like).filter(models.Like.id == like_id).first()
    if db_like:
        db.delete(db_like)
        db.commit()
    return db_like

# Comments
def create_comment(db: Session, comment: schemas.CommentCreate, user_id: int):
    db_comment = models.Comment(**comment.dict(), user_id=user_id)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

# Follows
def create_follow(db: Session, follow: schemas.FollowCreate, follower_id: int):
    db_follow = models.Follow(follower_id=follower_id, followed_id=follow.followed_id)
    db.add(db_follow)
    db.commit()
    db.refresh(db_follow)
    return db_follow

def delete_follow(db: Session, follow_id: int):
    db_follow = db.query(models.Follow).filter(models.Follow.id == follow_id).first()
    if db_follow:
        db.delete(db_follow)
        db.commit()
    return db_follow

# Add more as needed, e.g., get_followers: db.query(models.Follow).filter(models.Follow.followed_id == user_id).all()