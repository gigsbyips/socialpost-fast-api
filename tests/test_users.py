from apps import schemas
import pytest

# fixture- "client" is auto imported from "conftest.py"
def test_user_create(client): 
    res = client.post(
        "/users/", json={"email": "sample_email@gmail.com", "password": "sample_password"})
    assert res.status_code == 201 # checks the http code 201 was returned.
    schemas.UserResponse(**res.json()) # checks the response is of expected format.


# 422 will be the case of pydantic schema failure.
@pytest.mark.parametrize("email, password, status_code",
                          [("testuser@gmail.com", "testpassword", 200),
                           ("testuser@gmail.com", "wrongpassword", 403),
                           ("wronguser@gmail.com", "testpassword", 403),
                           (None, "testpassword", 422),
                           ("testuser@gmail.com", None, 422)
                           ]
                          )
def test_user_login(client, user_for_test, email, password, status_code):
    res = client.post(
        "/login", data={"username": email, "password": password})  # login expects input as form-data.
    assert res.status_code == status_code
