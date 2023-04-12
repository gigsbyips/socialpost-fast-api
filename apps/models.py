# when DB is used for storing the data.

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, ForeignKey, Integer, String, TIMESTAMP, text
from sqlalchemy.orm import relationship

Base = declarative_base()  # Base model that API extends to define custom model(schema)

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True) # Auto Increments by default.
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    visibility = Column(String, nullable=False, server_default='public')
    created_at=Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()')) #Current time as default.
    user_id=Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False) #users table's id column. #CASCADE means posts will be deleted on user deletion.

    # "RELATIONSHIP" is a way to get info from the other table without writing another sql/custom code.
    user = relationship("User")  # It simply instructs SqlAlchemy to fetch details of user based on user_id of the post.


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True) # Auto Increments by default.
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at=Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()')) #Current time as default.    

class Vote(Base):
    __tablename__ = "votes"

    user_id=Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True, nullable=False) #users table's id column. #CASCADE means posts will be deleted on user deletion.
    post_id=Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True, nullable=False) #posts table's id column. #CASCADE means posts will be deleted on user deletion.