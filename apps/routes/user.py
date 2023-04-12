from fastapi import HTTPException, Depends, status, APIRouter
from typing import List
from .. import schemas, models, utils
from ..database import get_db
from sqlalchemy.orm import Session


router = APIRouter(
   prefix="/users",
    tags=["Users"]
    )

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse) # Sets this code when request is successful
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):    # post is a variable of type "Post" class (model/schema).
    try:
      # hash the pwd and set the pydantic model variable to same value.
      hashed_pwd = utils.hash(user.password)
      user.password = hashed_pwd
      new_user = models.User(**user.dict()) # Convert Pydantic model to a python dict and unpack.
      db.add(new_user)
      db.commit()
      db.refresh(new_user) # fetch the saved record from DB for returning.
      return new_user
    except Exception as exp:
      exp_cause = exp.__str__()
      if exp_cause.__contains__("violates unique constraint"):
         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already in use.")
      raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failure while executing the request.")


@router.put("/{id}", response_model=schemas.UserResponse)
def update_user(id:int, user: schemas.UserPwdUpdate, db: Session = Depends(get_db)):    # user is a variable of type "User" class (model/schema).
    user_query = db.query(models.User).filter(models.User.id == id)
    query_result = user_query.first()
    if query_result == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'user with id: {id} not found')
    # hash the pwd and set the pydantic model variable to same value.
    hashed_pwd = utils.hash(user.password)
    user.password = hashed_pwd
    user_query.update(user.dict(),synchronize_session=False)
    db.commit()
    return user_query.first()


@router.get("/{id}", response_model=schemas.UserResponse) # Fast Api auto extract the path param of the incoming request. 
def get_user(id: int, db: Session = Depends(get_db)):  # Path params extracted by fastapi are string, so "int" ensures that request accepts only int value.
      user = db.query(models.User).filter(models.User.id == id).first() # get first record.
      if not user :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'user with id: {id} not found')
      return user