from fastapi import status, APIRouter,  Depends, HTTPException
from .. import models, schemas, utils, oauth
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter(
    tags=["Authentication"]
)


@router.post("/login", response_model=schemas.AccessToken)
def user_login(user_creds: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # OAuth2PasswordRequestForm extracts the incoming fields and put them under username and password.
    # the fields- username, password should now come as form-data in the request body.

    # username actually holds email.
    user = db.query(models.User).filter(
        models.User.email == user_creds.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials.")

    if not utils.verify(user_creds.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials.")

    access_token = oauth.create_access_token(data={"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}
