from fastapi import FastAPI
from .routes import post, user, user_auth, vote
from fastapi.middleware.cors import CORSMiddleware

# Uncomment the below lines if Alembic is not used for DB operations.
# It instructs sqlalchemy to create the models defined.
# from . import models
# from .database import engine
# models.Base.metadata.create_all(bind=engine)

origins = ["*"]  # Allow all origins as this is just a sample API.

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Home Route


@app.get("/")
def home():
    return {"Detail": "Post API by Inder using Fast API."}


# Add routes of the Models.
app.include_router(post.router)
app.include_router(user.router)
app.include_router(user_auth.router)
app.include_router(vote.router)
