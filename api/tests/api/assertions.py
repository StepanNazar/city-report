from typing import Any


def assert_pagination_response(response, total, page, total_pages, items_count):
    """Verify pagination metadata."""
    assert response.status_code == 200
    assert "items" in response.json
    assert response.json["totalItems"] == total
    assert response.json["totalPages"] == total_pages
    assert response.json["page"] == page
    assert len(response.json["items"]) == items_count


def assert_resources_order_match(returned_resources, expected_resources):
    """Verify returned resources match expected resources in the correct pagination order.

    This helper checks that resources are returned in the expected order by comparing
    each field in the expected resources with the corresponding field in the returned
    resources. Only fields present in both the expected and returned resources are compared,
    allowing for fields that may be excluded in pagination responses (like 'body').
    """
    for i, expected_source in enumerate(expected_resources):
        for key, value in expected_source.items():
            if key in returned_resources[i]:
                assert returned_resources[i][key] == value


def assert_response_matches_resource(
    response, resource_data, additional_keys=None, excluded_keys=None
):
    """Asserts that the response matches the resource data and has additional keys."""
    excluded_keys = excluded_keys or []
    for key, value in resource_data.items():
        if key not in excluded_keys:
            assert response.json[key] == value
    if additional_keys:
        for key in additional_keys:
            assert key in response.json


def assert_resource_images(
    response, expected_images: list[tuple[str, str] | dict[str, Any]]
):
    """Assert that response contains expected image objects {id, url} in correct order.

    Args:
        response: Flask response object
        expected_images: List of tuples (id, url) or list of dicts with 'id' and 'url' keys
    """
    assert "images" in response.json
    assert len(response.json["images"]) == len(expected_images)

    for i, expected in enumerate(expected_images):
        actual_image = response.json["images"][i]
        assert "id" in actual_image
        assert "url" in actual_image

        if isinstance(expected, tuple):
            expected_id, expected_url = expected
        else:
            expected_id, expected_url = expected["id"], expected["url"]

        assert actual_image["id"] == expected_id
        assert actual_image["url"] == expected_url
