"""Tests for resources with images functionality."""

import uuid
from typing import Any

import pytest
from conftest import (
    post,
    post_with_images,
    solution,
    solution_with_images,
)

from api.tests.api.assertions import assert_resource_images
from api.tests.api.data import post_data, solution_data
from api.tests.api.helpers import (
    create_post_with_images,
    create_solution_with_images,
    lf,
    upload_image,
)


@pytest.mark.parametrize(
    "resource_parent,resource_create_func,resource_data",
    [
        ("", create_post_with_images, post_data),
        (lf(post), create_solution_with_images, solution_data),
    ],
)
def test_create_resource_with_images(
    authenticated_client, images, resource_parent, resource_create_func, resource_data
):
    """Test creating a resource with multiple images."""
    images_ids = [img_id for img_id, _ in images]

    if resource_parent:
        resource_url = resource_create_func(
            authenticated_client, resource_parent, images_ids, resource_data
        )
    else:
        resource_url = resource_create_func(
            authenticated_client, images_ids, resource_data
        )

    response = authenticated_client.get(resource_url)

    assert response.status_code == 200
    assert_resource_images(response, images)


@pytest.mark.parametrize(
    "resource_with_images",
    [lf(post_with_images), lf(solution_with_images)],
)
def test_get_resource_with_images(authenticated_client, resource_with_images, images):
    """Test retrieving a resource that has images."""
    response = authenticated_client.get(resource_with_images)

    assert response.status_code == 200
    assert_resource_images(response, images)


@pytest.mark.parametrize(
    "resource,resource_data",
    [
        (lf(post), post_data),
        (lf(solution), solution_data),
    ],
)
def test_add_images_to_resource_without_images(
    authenticated_client, resource, resource_data, images
):
    """Test adding images to an existing resource with no images"""
    images_subset = images[:2]
    images_ids = [img_id for img_id, _ in images_subset]
    updated_resource_data: dict[str, Any] = dict(resource_data)
    updated_resource_data["imagesIds"] = images_ids

    update_response = authenticated_client.put(resource, json=updated_resource_data)

    assert update_response.status_code == 200
    assert_resource_images(update_response, images_subset)


@pytest.mark.parametrize(
    "resource_with_images,resource_data",
    [
        (lf(post_with_images), post_data),
        (lf(solution_with_images), solution_data),
    ],
)
def test_add_images_to_resource_with_existing_images(
    authenticated_client, resource_with_images, resource_data, images
):
    """Test adding images to an existing resource that already has images."""
    get_response = authenticated_client.get(resource_with_images)
    current_images = get_response.json["images"]
    current_image_ids = [img["id"] for img in current_images]
    new_image = upload_image(authenticated_client)
    new_image_id = new_image[0]
    updated_resource_data: dict[str, Any] = dict(resource_data)
    updated_resource_data["imagesIds"] = [*current_image_ids, new_image_id]

    update_response = authenticated_client.put(
        resource_with_images, json=updated_resource_data
    )

    assert update_response.status_code == 200
    expected_images = [*current_images, new_image]
    assert_resource_images(update_response, expected_images)


@pytest.mark.parametrize(
    "resource_parent,resource_create_func,resource_data",
    [
        ("", create_post_with_images, post_data),
        (lf(post), create_solution_with_images, solution_data),
    ],
)
def test_update_resource_replace_image(
    authenticated_client, images, resource_parent, resource_create_func, resource_data
):
    """Test replacing images of an existing resource."""
    if resource_parent:
        resource_url = resource_create_func(
            authenticated_client,
            resource_parent,
            [images[0][0], images[1][0]],
            resource_data,
        )
    else:
        resource_url = resource_create_func(
            authenticated_client, [images[0][0], images[1][0]], resource_data
        )

    get_response = authenticated_client.get(resource_url)

    first_image = get_response.json["images"][0]
    new_images_subset = [(first_image["id"], first_image["url"]), images[2]]
    new_images_ids = [img_id for img_id, _ in new_images_subset]
    updated_resource_data: dict[str, Any] = dict(resource_data)
    updated_resource_data["imagesIds"] = new_images_ids

    update_response = authenticated_client.put(resource_url, json=updated_resource_data)

    assert update_response.status_code == 200
    assert_resource_images(update_response, new_images_subset)


@pytest.mark.parametrize(
    "resource_with_images,resource_data",
    [
        (lf(post_with_images), post_data),
        (lf(solution_with_images), solution_data),
    ],
)
def test_update_resource_remove_all_images_with_empty_list(
    authenticated_client, resource_with_images, resource_data
):
    """Test removing all images from a resource with empty imagesIds list."""
    updated_resource_data: dict[str, Any] = dict(resource_data)
    updated_resource_data["imagesIds"] = []

    update_response = authenticated_client.put(
        resource_with_images, json=updated_resource_data
    )

    assert update_response.status_code == 200
    assert update_response.json.get("images") == []


@pytest.mark.parametrize(
    "resource_with_images,resource_data",
    [
        (lf(post_with_images), post_data),
        (lf(solution_with_images), solution_data),
    ],
)
def test_update_resource_remove_all_images_without_key(
    authenticated_client, resource_with_images, resource_data
):
    """Test removing all images by omitting imagesIds key."""
    updated_resource_data: dict[str, Any] = dict(resource_data)
    # Don't include imagesIds key at all

    update_response = authenticated_client.put(
        resource_with_images, json=updated_resource_data
    )

    assert update_response.status_code == 200
    assert update_response.json.get("images") == []


@pytest.mark.parametrize(
    "resource_parent,resource_create_func,resource_data",
    [
        ("", create_post_with_images, post_data),
        (lf(post), create_solution_with_images, solution_data),
    ],
)
def test_update_resource_remove_one_image(
    authenticated_client, images, resource_parent, resource_create_func, resource_data
):
    """Test removing one image while keeping others."""
    all_images_ids = [img[0] for img in images]

    if resource_parent:
        resource_url = resource_create_func(
            authenticated_client, resource_parent, all_images_ids, resource_data
        )
    else:
        resource_url = resource_create_func(
            authenticated_client, all_images_ids, resource_data
        )

    get_response = authenticated_client.get(resource_url)
    current_images = get_response.json["images"]

    updated_images_ids = [current_images[0]["id"], current_images[1]["id"]]
    expected_images = images[:2]

    updated_resource_data: dict[str, Any] = dict(resource_data)
    updated_resource_data["imagesIds"] = updated_images_ids

    update_response = authenticated_client.put(resource_url, json=updated_resource_data)

    assert update_response.status_code == 200
    assert_resource_images(update_response, expected_images)


@pytest.mark.parametrize(
    "resource_parent,resource_create_func,resource_data",
    [
        ("", create_post_with_images, post_data),
        (lf(post), create_solution_with_images, solution_data),
    ],
)
def test_update_resource_reorder_images(
    authenticated_client, images, resource_parent, resource_create_func, resource_data
):
    """Test changing the order of images."""
    original_order_ids = [img[0] for img in images]

    if resource_parent:
        resource_url = resource_create_func(
            authenticated_client, resource_parent, original_order_ids, resource_data
        )
    else:
        resource_url = resource_create_func(
            authenticated_client, original_order_ids, resource_data
        )

    get_response = authenticated_client.get(resource_url)
    current_images = get_response.json["images"]

    reversed_order_ids = [
        current_images[2]["id"],
        current_images[1]["id"],
        current_images[0]["id"],
    ]
    expected_images = [images[2], images[1], images[0]]

    updated_resource_data: dict[str, Any] = dict(resource_data)
    updated_resource_data["imagesIds"] = reversed_order_ids

    update_response = authenticated_client.put(resource_url, json=updated_resource_data)

    assert update_response.status_code == 200
    assert_resource_images(update_response, expected_images)


@pytest.mark.parametrize(
    "resource_parent,resource_name,resource_data",
    [
        ("", "posts", post_data),
        (lf(post), "solutions", solution_data),
    ],
)
def test_create_resource_with_too_many_images(
    authenticated_client, resource_parent, resource_name, resource_data
):
    """Test creating a resource with more than maximum allowed images."""
    resource_data_with_images: dict[str, Any] = dict(resource_data)
    resource_data_with_images["imagesIds"] = [str(uuid.uuid4()) for _ in range(11)]

    response = authenticated_client.post(
        f"{resource_parent}/{resource_name}", json=resource_data_with_images
    )

    assert response.status_code == 422


@pytest.mark.parametrize(
    "resource,resource_data",
    [
        (lf(post), post_data),
        (lf(solution), solution_data),
    ],
)
def test_update_resource_with_too_many_images(
    authenticated_client, resource, resource_data
):
    """Test updating a resource with more than maximum allowed images."""
    updated_resource_data: dict[str, Any] = dict(resource_data)
    updated_resource_data["imagesIds"] = [str(uuid.uuid4()) for _ in range(11)]

    response = authenticated_client.put(resource, json=updated_resource_data)

    assert response.status_code == 422


@pytest.mark.parametrize(
    "resource1_parent,resource1_create_func,resource1_data,resource2_parent,resource2_create_func,resource2_data",
    [
        (
            "",
            create_post_with_images,
            post_data,
            "",
            create_post_with_images,
            post_data,
        ),
        (
            lf(post),
            create_solution_with_images,
            solution_data,
            lf(post),
            create_solution_with_images,
            solution_data,
        ),
        (
            "",
            create_post_with_images,
            post_data,
            lf(post),
            create_solution_with_images,
            solution_data,
        ),
        (
            lf(post),
            create_solution_with_images,
            solution_data,
            "",
            create_post_with_images,
            post_data,
        ),
    ],
)
def test_image_shared_between_multiple_resources(
    authenticated_client,
    image,
    resource1_parent,
    resource1_create_func,
    resource1_data,
    resource2_parent,
    resource2_create_func,
    resource2_data,
):
    """Test that an image can be shared between multiple resources."""
    image_id, image_url = image

    resource1_data_copy: dict[str, Any] = dict(resource1_data)
    resource2_data_copy: dict[str, Any] = dict(resource2_data)

    if resource1_parent:
        resource1_url = resource1_create_func(
            authenticated_client, resource1_parent, [image_id], resource1_data_copy
        )
    else:
        resource1_url = resource1_create_func(
            authenticated_client, [image_id], resource1_data_copy
        )

    if resource2_parent:
        resource2_url = resource2_create_func(
            authenticated_client, resource2_parent, [image_id], resource2_data_copy
        )
    else:
        resource2_url = resource2_create_func(
            authenticated_client, [image_id], resource2_data_copy
        )

    response1 = authenticated_client.get(resource1_url)
    response2 = authenticated_client.get(resource2_url)

    assert_resource_images(response1, [image])
    assert_resource_images(response2, [image])


@pytest.mark.parametrize(
    "resource1_parent,resource1_create_func,resource1_data,resource2_parent,resource2_create_func,resource2_data",
    [
        (
            "",
            create_post_with_images,
            post_data,
            "",
            create_post_with_images,
            post_data,
        ),
        (
            lf(post),
            create_solution_with_images,
            solution_data,
            lf(post),
            create_solution_with_images,
            solution_data,
        ),
        (
            "",
            create_post_with_images,
            post_data,
            lf(post),
            create_solution_with_images,
            solution_data,
        ),
        (
            lf(post),
            create_solution_with_images,
            solution_data,
            "",
            create_post_with_images,
            post_data,
        ),
    ],
)
def test_delete_resource_with_images_keeps_images_if_used_elsewhere(
    authenticated_client,
    image,
    resource1_parent,
    resource1_create_func,
    resource1_data,
    resource2_parent,
    resource2_create_func,
    resource2_data,
):
    """Test that deleting a resource doesn't delete images used by other resources."""
    image_id, image_url = image

    resource1_data_copy: dict[str, Any] = dict(resource1_data)
    resource2_data_copy: dict[str, Any] = dict(resource2_data)

    if resource1_parent:
        resource1_url = resource1_create_func(
            authenticated_client, resource1_parent, [image_id], resource1_data_copy
        )
    else:
        resource1_url = resource1_create_func(
            authenticated_client, [image_id], resource1_data_copy
        )

    if resource2_parent:
        resource2_url = resource2_create_func(
            authenticated_client, resource2_parent, [image_id], resource2_data_copy
        )
    else:
        resource2_url = resource2_create_func(
            authenticated_client, [image_id], resource2_data_copy
        )

    delete_response = authenticated_client.delete(resource1_url)
    assert delete_response.status_code == 204

    image_response = authenticated_client.get(image_url)
    assert image_response.status_code == 200

    response2 = authenticated_client.get(resource2_url)
    assert_resource_images(response2, [image])


@pytest.mark.parametrize(
    "resource_parent,resource_create_func,resource_data",
    [
        ("", create_post_with_images, post_data),
        (lf(post), create_solution_with_images, solution_data),
    ],
)
def test_orphaned_by_resource_update_images_are_deleted(
    authenticated_client, image, resource_parent, resource_create_func, resource_data
):
    """Test that images not used by any resources are deleted."""
    image_id, image_url = image

    if resource_parent:
        resource_url = resource_create_func(
            authenticated_client, resource_parent, [image_id], resource_data
        )
    else:
        resource_url = resource_create_func(
            authenticated_client, [image_id], resource_data
        )

    updated_resource_data: dict[str, Any] = dict(resource_data)
    updated_resource_data["imagesIds"] = []
    authenticated_client.put(resource_url, json=updated_resource_data)

    image_response = authenticated_client.get(image_url)
    assert image_response.status_code == 404


@pytest.mark.parametrize(
    "resource_parent,resource_create_func,resource_data",
    [
        ("", create_post_with_images, post_data),
        (lf(post), create_solution_with_images, solution_data),
    ],
)
def test_orphaned_by_resource_deletion_images_are_deleted(
    authenticated_client, image, resource_parent, resource_create_func, resource_data
):
    """Test that images not used by any resources are deleted upon resource deletion."""
    image_id, image_url = image

    if resource_parent:
        resource_url = resource_create_func(
            authenticated_client, resource_parent, [image_id], resource_data
        )
    else:
        resource_url = resource_create_func(
            authenticated_client, [image_id], resource_data
        )

    authenticated_client.delete(resource_url)

    image_response = authenticated_client.get(image_url)
    assert image_response.status_code == 404


@pytest.mark.parametrize(
    "resource_parent,resource_name,resource_data",
    [
        ("", "posts", post_data),
        (lf(post), "solutions", solution_data),
    ],
)
def test_create_resource_with_nonexistent_image_id(
    authenticated_client, resource_parent, resource_name, resource_data
):
    """Test creating a resource with an image ID that doesn't exist."""
    resource_data_with_fake_image: dict[str, Any] = dict(resource_data)
    resource_data_with_fake_image["imagesIds"] = [str(uuid.uuid4())]

    response = authenticated_client.post(
        f"{resource_parent}/{resource_name}", json=resource_data_with_fake_image
    )

    assert response.status_code == 422


@pytest.mark.parametrize(
    "resource,resource_data",
    [
        (lf(post), post_data),
        (lf(solution), solution_data),
    ],
)
def test_update_resource_with_nonexistent_image_id(
    authenticated_client, resource, resource_data
):
    """Test updating a resource with an image ID that doesn't exist."""
    updated_resource_data: dict[str, Any] = dict(resource_data)
    updated_resource_data["imagesIds"] = [str(uuid.uuid4())]

    response = authenticated_client.put(resource, json=updated_resource_data)

    assert response.status_code == 422


@pytest.mark.parametrize(
    "resource_parent,resource_name,resource_data",
    [
        ("", "posts", post_data),
        (lf(post), "solutions", solution_data),
    ],
)
def test_allow_duplicate_image_in_single_resource(
    authenticated_client, image, resource_parent, resource_name, resource_data
):
    """Test that the same image can be used multiple times in one resource."""
    image_id, image_url = image

    resource_data_with_dup: dict[str, Any] = dict(resource_data)
    resource_data_with_dup["imagesIds"] = [image_id, image_id, image_id]

    response = authenticated_client.post(
        f"{resource_parent}/{resource_name}", json=resource_data_with_dup
    )

    assert response.status_code == 201
    assert_resource_images(response, [image, image, image])
