import pytest

from api.tests.api.assertions import assert_response_matches_resource
from api.tests.api.data import (
    post_data,
    solution_data,
    updated_post_data,
    updated_solution_data,
)
from api.tests.api.helpers import create_post, create_solution, lf


@pytest.fixture
def cross_user_posts(authenticated_client, authenticated_client2):
    """Creates posts for two different users.
    :returns post's url of one user, post's url of another user, and the original post data used
    """
    return (
        create_post(authenticated_client),
        create_post(authenticated_client2),
        post_data,
    )


@pytest.fixture
def cross_user_solutions(authenticated_client, authenticated_client2, cross_user_posts):
    """Creates solutions for two different users.
    :returns solution's url of one user, solution's url of another user, and the original solution data used
    """
    post1, post2, _ = cross_user_posts
    return (
        create_solution(authenticated_client, post1),
        create_solution(authenticated_client2, post2),
        solution_data,
    )


@pytest.mark.parametrize(
    "method,url,payload",
    [
        ("post", "/posts", post_data.copy()),
        ("put", "/posts/1", updated_post_data.copy()),
        ("delete", "/posts/1", None),
        ("post", "/posts/1/solutions", solution_data.copy()),
        ("put", "/solutions/1", updated_solution_data.copy()),
        ("delete", "/solutions/1", None),
    ],
)
def test_unauthorized_access(client, method, url, payload):
    response = getattr(client, method)(url, json=payload)

    assert response.status_code == 401


@pytest.mark.parametrize(
    "method,payload,cross_user_resources,excluded_keys",
    [
        (
            "put",
            updated_post_data.copy(),
            lf(cross_user_posts),
            ["localityId", "localityProvider"],
        ),
        ("delete", None, lf(cross_user_posts), ["localityId", "localityProvider"]),
        ("put", updated_solution_data.copy(), lf(cross_user_solutions), None),
        ("delete", None, lf(cross_user_solutions), None),
    ],
)
def test_access_unowned_profile(
    authenticated_client,
    authenticated_client2,
    cross_user_resources,
    method,
    payload,
    excluded_keys,
):
    client_resource, client2_resource, original_resource_data = cross_user_resources

    response = getattr(authenticated_client2, method)(client_resource, json=payload)

    assert response.status_code == 403

    response = getattr(authenticated_client, method)(client2_resource, json=payload)

    assert response.status_code == 403

    if method != "get":
        assert_resource_unchanged(
            authenticated_client, client_resource, original_resource_data, excluded_keys
        )
        assert_resource_unchanged(
            authenticated_client2,
            client2_resource,
            original_resource_data,
            excluded_keys,
        )


def assert_resource_unchanged(client, url, expected_data, excluded_keys=None):
    """Verify the resource wasn't modified."""
    response = client.get(url)

    assert response.status_code == 200
    assert_response_matches_resource(
        response, expected_data, excluded_keys=excluded_keys
    )
