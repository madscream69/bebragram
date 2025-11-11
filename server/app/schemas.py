from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List

class UserBase(BaseModel):
    email: EmailStr
    username: str
    bio: Optional[str] = None

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):  # For JWT responses.
    access_token: str
    refresh_token: str
    token_type: str

class TokenData(BaseModel):  # For decoding JWT.
    username: Optional[str] = None

class PostBase(BaseModel):
    content: str

class PostCreate(PostBase):
    pass  # Same as base for create.

class Post(PostBase):
    id: int
    owner_id: int
    created_at: datetime
    likes: List["Like"] = []  # Nested, but simplified.
    comments: List["Comment"] = []

    class Config:
        from_attributes = True

class LikeBase(BaseModel):
    post_id: int

class LikeCreate(LikeBase):
    pass

class Like(LikeBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True

class CommentBase(BaseModel):
    content: str
    post_id: int

class CommentCreate(CommentBase):
    pass

class Comment(CommentBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class FollowBase(BaseModel):
    followed_id: int

class FollowCreate(FollowBase):
    pass

class Follow(FollowBase):
    id: int
    follower_id: int

    class Config:
        from_attributes = True