from fastapi import HTTPException, Depends, status, APIRouter, Response
from typing import List, Optional

from sqlalchemy import func
from .. import schemas, models, oauth
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


@router.get("/", response_model=List[schemas.PostResponseWithVotes])
# limit is to limit no. of records, skip is for pagination
def get_posts(db: Session = Depends(get_db), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Post.id == models.Vote.post_id, isouter=True).group_by(
        models.Post.id).filter(
        models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts


# Fast Api auto extract the path param of the incoming request.
@router.get("/{id}", response_model=schemas.PostResponseWithVotes)
# Path params extracted by fastapi are string, so "int" ensures that request accepts only int value.
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Post.id == models.Vote.post_id, isouter=True).group_by(
        models.Post.id).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id: {id} not found')
    return post


# Sets this code when request is successful
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
# post is a variable of type "Post" class (model/schema).
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: schemas.UserResponse = Depends(oauth.get_current_user)):
    try:
        # Convert Pydantic model 'post' to a python dict and unpack.
        new_post = models.Post(user_id=current_user.id, **post.dict())
        db.add(new_post)
        db.commit()
        db.refresh(new_post)  # fetch the saved record from DB for returning.
        return new_post
    except Exception as exp:
        print(exp)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Failure while executing the request.")


# Fast Api auto extract the path param of the incoming request.
@router.delete("/{id}")
# Path params extracted by fastapi are of string type, so "int" ensures that request accepts only int value.
def delete_post(id: int, db: Session = Depends(get_db), current_user: schemas.UserResponse = Depends(oauth.get_current_user)):
    #print(current_user.email)  # current_user details are not used yet.
    post_query = db.query(models.Post).filter(models.Post.id == id)
    query_result = post_query.first()
    if query_result == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id: {id} not found')
    if query_result.user_id != current_user.id:  # If user is not the owner of the post
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f'Not authorized to perform the requested operation.')
    post_query.delete(synchronize_session=False)
    db.commit()
    # Only HTTP_STATUS_CODE set as response.
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.PostResponse)
# post is a variable of type "Post" class (model/schema).
def update_post(id: int, post: schemas.PostUpdate, db: Session = Depends(get_db), current_user: schemas.UserResponse = Depends(oauth.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    query_result = post_query.first()
    if query_result == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id: {id} not found')
    if query_result.user_id != current_user.id:  # If user is not the owner of the post
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f'Not authorized to perform the requested operation.')
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()
