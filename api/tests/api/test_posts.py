import time

import pytest
from conftest import (
    assert_pagination_response,
    assert_resources_order_match,
    create_post,
    post_data,
)


def test_post_author_link_is_valid(authenticated_client, post):
    response = authenticated_client.get(post)
    assert response.json["authorLink"] == f"/users/{response.json['authorId']}"


def test_get_posts(authenticated_client, authenticated_client2):
    posts = []
    post_urls = []
    for i in range(3):
        new_post = post_data.copy()
        new_post["title"] = f"Post {3 - i}"
        posts.append(new_post)
        post_urls.append(create_post(authenticated_client, new_post))
    # create a post with another user to ensure posts from other users are included in the response
    posts.append(post_data)
    post_urls.append(create_post(authenticated_client2, post_data))
    # update post
    time.sleep(0.01)
    updated_data = post_data.copy()
    authenticated_client.put(post_urls[0], json=updated_data)
    posts[0] = updated_data

    response = authenticated_client.get("/posts?order=asc&sort_by=created_at")

    assert_pagination_response(response, total=4, page=1, total_pages=1, items_count=4)
    assert_resources_order_match(response.json["items"], posts)

    response = authenticated_client.get("/posts?sort_by=edited_at")

    assert_pagination_response(response, total=4, page=1, total_pages=1, items_count=4)
    assert_resources_order_match(response.json["items"], [posts[0], *posts[3:0:-1]])

    response = authenticated_client.get(
        "/posts?order=asc&sort_by=created_at&per_page=2&page=2"
    )

    assert_pagination_response(response, total=4, page=2, total_pages=2, items_count=2)
    assert_resources_order_match(response.json["items"], posts[2:])


@pytest.mark.parametrize(
    "method,payload",
    [
        ("get", None),
        ("put", post_data.copy()),
        ("delete", None),
    ],
)
def test_post_not_found(authenticated_client, method, payload, post):
    prefix, id = post.rsplit("/", maxsplit=1)
    non_existent_post_url = f"{prefix}/{int(id) + 1}"

    response = getattr(authenticated_client, method)(
        non_existent_post_url, json=payload
    )
    assert response.status_code == 404
