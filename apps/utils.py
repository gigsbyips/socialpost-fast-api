from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") # asking passlib to use "bcrypt" algo for hashing the pwd.

def hash(input_val: str):
    return pwd_context.hash(input_val)

def verify(plain_pwd, hased_pwd):
    return pwd_context.verify(plain_pwd, hased_pwd)
