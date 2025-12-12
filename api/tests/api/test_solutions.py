import time

import pytest

from api.tests.api.assertions import (
    assert_pagination_response,
    assert_resources_order_match,
)
from api.tests.api.data import post_data, solution_data
from api.tests.api.helpers import create_post, create_solution


def test_solution_author_link_is_valid(authenticated_client, solution):
    response = authenticated_client.get(solution)
    assert response.json["authorLink"] == f"/users/{response.json['authorId']}"


def test_get_solutions(authenticated_client, authenticated_client2, post):
    solutions = []
    solution_urls = []
    for i in range(3):
        new_solution = solution_data.copy()
        new_solution["title"] = f"Solution {3 - i}"
        solutions.append(new_solution)
        solution_urls.append(create_solution(authenticated_client, post, new_solution))
    # create a solution with another user to ensure solutions from other users are included in the response
    solutions.append(solution_data)
    solution_urls.append(create_solution(authenticated_client2, post, solution_data))
    # create a solution to another post to ensure solutions from other posts are excluded
    another_post = create_post(authenticated_client, post_data)
    create_solution(authenticated_client, another_post, solution_data)
    # update solution
    time.sleep(0.01)
    updated_solution = solution_data.copy()
    updated_solution["title"] = "Updated Solution"
    authenticated_client.put(solution_urls[0], json=updated_solution)
    solutions[0] = updated_solution

    response = authenticated_client.get(
        f"{post}/solutions?order=asc&sort_by=created_at"
    )

    assert_pagination_response(response, total=4, page=1, total_pages=1, items_count=4)
    assert_resources_order_match(response.json["items"], solutions)

    response = authenticated_client.get(f"{post}/solutions?sort_by=edited_at")

    assert_pagination_response(response, total=4, page=1, total_pages=1, items_count=4)
    assert_resources_order_match(
        response.json["items"], [solutions[0], *solutions[3:0:-1]]
    )

    response = authenticated_client.get(
        f"{post}/solutions?order=asc&sort_by=created_at&per_page=2&page=2"
    )

    assert_pagination_response(response, total=4, page=2, total_pages=2, items_count=2)
    assert_resources_order_match(response.json["items"], solutions[2:])


@pytest.mark.parametrize(
    "method,payload",
    [
        ("get", None),
        ("put", solution_data.copy()),
        ("delete", None),
    ],
)
def test_solution_not_found(authenticated_client, method, payload, solution):
    prefix, id = solution.rsplit("/", maxsplit=1)
    non_existent_solution_url = f"{prefix}/{int(id) + 1}"

    response = getattr(authenticated_client, method)(
        non_existent_solution_url, json=payload
    )
    assert response.status_code == 404


def test_post_not_found_on_creating_solution(authenticated_client):
    response = authenticated_client.post(
        "/posts/99999/solutions", json=solution_data.copy()
    )

    assert response.status_code == 404


def test_post_not_found_on_getting_solutions(authenticated_client):
    response = authenticated_client.get("/posts/99999/solutions")

    assert response.status_code == 404
