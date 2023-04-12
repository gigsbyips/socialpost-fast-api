from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas, database, models
from fastapi.security import OAuth2PasswordBearer
from fastapi import status, Depends, HTTPException
from sqlalchemy.orm import Session
from .config import settings

# Set Env variables.
SIGN_KEY = settings.SIGN_KEY
ACCESS_TOKEN_EXPIRE_MINUTE = settings.ACCESS_TOKEN_EXPIRE_MINUTE
SIGN_ALGORITHM = settings.SIGN_ALGORITHM

# Indicates it is a "Bearer" JWT token received from the login endpoint.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def create_access_token(data: dict):
    # set token expiry.
    expiry = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTE)
    # Add expiry to the copy of data.
    to_encode = data.copy()
    to_encode.update({"exp": expiry})
    encoded_jwt = jwt.encode(to_encode, key=SIGN_KEY, algorithm=SIGN_ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str, credentails_exception):
    try:
        payload = jwt.decode(token, key=SIGN_KEY, algorithms=[SIGN_ALGORITHM])
        # extract user_id field from decoded token.
        id = payload.get("user_id")
        if id is None:
            raise credentails_exception
        # validation that token_data is as per schema.
        token_data = schemas.TokenData(id=id)
        return token_data
    except JWTError:
        raise credentails_exception

# Set dependency on the getting the token from /login endpoint call.
# basically a header named "Authorization" : "Bearer <<JWT Token>>" should come in the user request.
# user can get this <<JWT token>> by calling "/login" endpoint from userLogin request.


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentails_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail=f"Could not validate credentials.",
                                          headers={"WWW-Authenticate": "Bearer"})
    token_data = verify_access_token(token, credentails_exception)
    user: schemas.UserResponse = db.query(models.User).filter(
        models.User.id == token_data.id).first()
    return user
