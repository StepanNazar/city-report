import time

import pytest
from conftest import (
    post,
    solution,
)

from api.tests.api.assertions import assert_response_matches_resource
from api.tests.api.data import (
    additional_post_keys,
    additional_solution_keys,
    excluded_post_keys,
    post_data,
    solution_data,
    updated_post_data,
    updated_solution_data,
)
from api.tests.api.helpers import lf


@pytest.fixture
def base_api_path():
    return ""


@pytest.mark.parametrize(
    "resource_parent,resource_name,resource_data,additional_keys,excluded_keys",
    [
        (
            lf(base_api_path),
            "posts",
            post_data,
            additional_post_keys,
            excluded_post_keys,
        ),
        (lf(post), "solutions", solution_data, additional_solution_keys, None),
    ],
)
def test_post_resource(
    authenticated_client,
    resource_parent,
    resource_name,
    resource_data,
    additional_keys,
    excluded_keys,
):
    """General test case for testing creation of any resource."""
    response = authenticated_client.post(
        f"{resource_parent}/{resource_name}", json=resource_data.copy()
    )

    assert response.status_code == 201
    assert "Location" in response.headers
    assert_response_matches_resource(
        response,
        resource_data,
        additional_keys=additional_keys,
        excluded_keys=excluded_keys,
    )


@pytest.mark.parametrize(
    "resource,resource_data,additional_keys,excluded_keys",
    [
        (lf(post), post_data, additional_post_keys, excluded_post_keys),
        (lf(solution), solution_data, additional_solution_keys, None),
    ],
)
def test_get_resource(
    authenticated_client, resource, resource_data, additional_keys, excluded_keys
):
    """General test case for testing reading of any resource."""
    response = authenticated_client.get(resource)

    assert response.status_code == 200
    assert_response_matches_resource(
        response,
        resource_data,
        additional_keys=additional_keys,
        excluded_keys=excluded_keys,
    )


@pytest.mark.parametrize(
    "resource,updated_resource_data,additional_keys,excluded_keys",
    [
        (lf(post), updated_post_data, additional_post_keys, excluded_post_keys),
        (lf(solution), updated_solution_data, additional_solution_keys, None),
    ],
)
def test_put_resource(
    authenticated_client,
    resource,
    updated_resource_data,
    additional_keys,
    excluded_keys,
):
    """General test case for testing updating of any resource."""
    time.sleep(0.01)  # Ensure the updated timestamp is different
    response = authenticated_client.put(resource, json=updated_resource_data.copy())

    assert response.status_code == 200
    assert_response_matches_resource(
        response,
        updated_resource_data,
        additional_keys=additional_keys,
        excluded_keys=excluded_keys,
    )
    assert response.json["updatedAt"] != response.json["createdAt"]


@pytest.mark.parametrize(
    "resource",
    [lf(post), lf(solution)],
)
def test_delete_resource(authenticated_client, resource):
    """General test case for testing deletion of any resource."""
    response = authenticated_client.delete(resource)

    assert response.status_code == 204

    response = authenticated_client.get(resource)

    assert response.status_code == 404
