from apps import schemas
# fixture- "client", "post_for_test", "token" are auto imported from "conftest.py"

count_test_posts=0
# This function runs multiple times (=no. of params in fixture) bcz fixture-"posts_for_test" that is parametrized.
def test_get_all_posts(client, posts_for_test):
    res = client.get("/posts/")
    assert res.status_code == 200              # checks the http code 200 was returned.
    global count_test_posts 
    count_test_posts = len(res.json())    # count will be updated in each run of this function.
    for post_index in range(len(res.json())):
        #print(res.json()[post_index])
        schemas.PostResponseWithVotes(**res.json()[post_index]) # bcz schema's __init__() support named args.


def test_get_post_with_id(client):
    for index in range(count_test_posts):
        post_id = index+1
        res = client.get(f"/posts/{post_id}")
        assert res.status_code == 200  # checks the http code 200 was returned.
        schemas.PostResponseWithVotes(**res.json()) # checks the response is of expected format.


def test_update_post(client, token):
    for index in range(count_test_posts):
        post_id = index+1
        res = client.put(f"/posts/{post_id}", json={"title": f"Updated post-{post_id} by PyTest",
                                                    "content": f"Updated content of post-{post_id} by PyTest",
                                                    "visibility": "private"},
                        headers={"Authorization": f"Bearer {token}"}
                        )
        #print(res.json())
        assert res.status_code == 200  # checks the http code 200 was returned.
        assert res.json()['visibility'] == 'private' # Check visibility has been updated.
        schemas.PostResponse(**res.json()) # checks the response is of expected format.


def test_delete_post(client, token):
    # Try to delete the post with last id.
    res = client.delete(f"/posts/{count_test_posts}", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 204   # checks the http code 204 was returned.
    # try deleting same post again. It should report "404-NOT_FOUND" status code.
    res = client.delete(f"/posts/{count_test_posts}", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 404 


def test_create_post(client, token):
    res = client.post(
        "/posts/", json={"title": "Sample Post", "content": "Sample Post Content."},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert res.status_code == 201  # checks the http code 201 was returned.
    schemas.PostResponse(**res.json()) # checks the response is of expected format.






