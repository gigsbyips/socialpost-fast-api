from fastapi import HTTPException, Depends, status, APIRouter, Response
from typing import List, Optional
from .. import schemas, models, oauth
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/vote",
    tags=["Vote"]
    )

@router.post("/", status_code=status.HTTP_201_CREATED) # Sets this code when request is successful
def vote(vote: schemas.Vote, db: Session = Depends(get_db), current_user: schemas.UserResponse = Depends(oauth.get_current_user)):    # post is a variable of type "Post" class (model/schema).
    post_exists=db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if post_exists:
      vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id,  models.Vote.user_id == current_user.id)
      user_has_voted_post=vote_query.first()
      if vote.direction == 1:
        if user_has_voted_post:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                                detail=f"User {current_user.id} has already voted post {vote.post_id}")  
        new_vote = models.Vote(user_id=current_user.id, post_id=vote.post_id)
        db.add(new_vote)
        db.commit()
        return {"message": "Successfully added vote."}
      else:
          if not user_has_voted_post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User didn't vote for post {vote.post_id}.")
          else:
            vote_query.delete(synchronize_session=False) # if found delete the user vote.
            db.commit()
            return {"message": "Successfully deleted vote."}
    else:
      raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                  detail=f"No Post with id- {vote.post_id} exists.")  

