import pytest
from fastapi.testclient import TestClient
from apps import models, schemas
from apps.main import app
from .database import engine
from apps.oauth import create_access_token
from typing import List, Optional


@pytest.fixture(scope="module")  # Initialize/Create a test client for the app.
def client():
    # Instruct sqlalchemy to build tables defined under models.
    # drop the tables so that same test data can be reused.
    #print("Hello from Test client fixture.")
    models.Base.metadata.drop_all(bind=engine)
    models.Base.metadata.create_all(bind=engine)  # recreate the tables
    yield TestClient(app)

"""
    # Alembic can also be used for creating DB tables etc.
    # from alembic.config import command
    # command.downgrade("base")
    # command.upgrade("head")
"""


# Although a user is created by test func- test_user_create(), but to ensure independence of other test cases ,
# a separate test user is created through ficture, though it will invoke the same functionality.
@pytest.fixture(scope="module")
def user_for_test(client):  # refer the fixture- "client"
    #print("Hello from 'user_for_test' fixture.")
    user_data = {"email": "testuser@gmail.com", "password": "testpassword"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201  # checks the http code 201 was returned.
    test_user = res.json()
    # bcz pwd will be used for login.
    test_user['password'] = user_data['password']
    return test_user


# Create Auth token for the test user.
@pytest.fixture(scope="module")
def token(user_for_test):
    #print("Hello from token fixture")
    token = create_access_token (data={"user_id": user_for_test['id']})
    return token


# Creates first post and returns back to caller, comes back creates 2nd post returns back to caller... 
# All posts are not created in single shot.
@pytest.fixture(scope="module", params=[{"title":"First post by PyTest", "content":"Content of first post by PyTest"},
                        {"title":"Second post by PyTest", "content":"Content of second post by PyTest"},
                        {"title":"Third post by PyTest", "content":"Content of third post by PyTest"}
                        ])
def posts_for_test(client, token, request):
    res = client.post(
    "/posts/", json={"title": request.param['title'], "content": request.param['content']},
    headers={"Authorization": f"Bearer {token}"}
    )
    #print(res.json())
    assert res.status_code == 201 # checks the http code 201 was returned.
    schemas.PostResponse(**res.json()) # checks the response is of expected format.
    return res.json() # return the created posts.
