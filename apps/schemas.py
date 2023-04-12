from pydantic import BaseModel, EmailStr, conint  # installed with fast api
from datetime import datetime
from typing import Optional

# defines what fields should be there in the request and response sent by user and their type.
# FastAPI auto validates the content (say incoming request) against this type. So, CLIENT SIDE VALIDATION.


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserPwdUpdate(BaseModel):
    password: str


class UserResponse(BaseModel):
    id: int
    email: str
    created_at: datetime

    # this class is required so that Pydantic can convert SQLAlchemy model to dictionary.
    class Config:
        orm_mode = True


class UserDetails(BaseModel):
    email: str

    # this class is required so that Pydantic can convert SQLAlchemy model to dictionary.
    class Config:
        orm_mode = True


# Note without Config orm_mode, we get error like-
"""pydantic.error_wrappers.ValidationError: 1 validation error for UserResponse
response
  value is not a valid dict (type=type_error.dict)"""


class PostRequest(BaseModel):
    title: str
    content: str
    visibility: str = "public"      # set default value.


class PostCreate(PostRequest):
    pass


class PostUpdate(PostRequest):
    visibility: str


class PostResponse(PostRequest):
    id: int
    created_at: datetime
    user_id: int
    # refer to pydantic schema (defined above) for extra details about user.
    user: UserDetails
    # userDetails are fetched from "users" table through RELATIONSHIP feature of SqlAlchemy.

    # this class is required so that Pydantic can convert SQLAlchemy model to dictionary.
    class Config:
        orm_mode = True


class PostResponseWithVotes(BaseModel):
    Post: PostResponse
    votes: int

    # this class is required so that Pydantic can convert SQLAlchemy model to dictionary.
    class Config:
        orm_mode = True


## Auth Schemas ###
class UserAuthentication(BaseModel):
    email: EmailStr
    password: str


class AccessToken(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


# Votes Schema
class Vote(BaseModel):
    post_id: int
    direction: conint(ge=0, le=1)  # 0 is used for downvote and 1 for upvote)
