"""Tests for posts with images functionality."""

import uuid
from typing import Any

from conftest import (
    assert_resource_images,
    create_post_with_images,
    post_data,
    upload_image,
)


def test_create_post_with_images(authenticated_client, images):
    """Test creating a post with multiple images."""
    images_ids = [img_id for img_id, _ in images]
    post_data_with_images: dict[str, Any] = dict(post_data)
    post_data_with_images["imagesIds"] = images_ids

    response = authenticated_client.post("/posts", json=post_data_with_images)

    assert response.status_code == 201
    assert_resource_images(response, images)


def test_get_post_with_images(authenticated_client, post_with_images, images):
    """Test retrieving a post that has images."""
    response = authenticated_client.get(post_with_images)

    assert response.status_code == 200
    assert_resource_images(response, images)


def test_add_images_to_post_without_images(authenticated_client, post, images):
    """Test adding images to an existing post with no images"""
    images_subset = images[:2]
    images_ids = [img_id for img_id, _ in images_subset]
    updated_post_data: dict[str, Any] = dict(post_data)
    updated_post_data["imagesIds"] = images_ids

    update_response = authenticated_client.put(post, json=updated_post_data)

    assert update_response.status_code == 200
    assert_resource_images(update_response, images_subset)


def test_add_images_to_post_with_existing_images(
    authenticated_client, post_with_images, images
):
    """Test adding images to an existing post that already has images."""
    get_response = authenticated_client.get(post_with_images)
    current_images = get_response.json["images"]
    current_image_ids = [img["id"] for img in current_images]
    new_image = upload_image(authenticated_client)
    new_image_id = new_image[0]
    updated_post_data: dict[str, Any] = dict(post_data)
    updated_post_data["imagesIds"] = [*current_image_ids, new_image_id]

    update_response = authenticated_client.put(post_with_images, json=updated_post_data)

    assert update_response.status_code == 200
    expected_images = [*current_images, new_image]
    assert_resource_images(update_response, expected_images)


def test_update_post_replace_image(authenticated_client, images):
    """Test replacing images of an existing post."""
    post_url = create_post_with_images(
        authenticated_client, [images[0][0], images[1][0]]
    )

    get_response = authenticated_client.get(post_url)

    first_image = get_response.json["images"][0]
    new_images_subset = [(first_image["id"], first_image["url"]), images[2]]
    new_images_ids = [img_id for img_id, _ in new_images_subset]
    updated_post_data: dict[str, Any] = dict(post_data)
    updated_post_data["imagesIds"] = new_images_ids

    update_response = authenticated_client.put(post_url, json=updated_post_data)

    assert update_response.status_code == 200
    assert_resource_images(update_response, new_images_subset)


def test_update_post_remove_all_images_with_empty_list(
    authenticated_client, post_with_images
):
    """Test removing all images from a post with empty imagesIds list."""
    updated_post_data: dict[str, Any] = dict(post_data)
    updated_post_data["imagesIds"] = []

    update_response = authenticated_client.put(post_with_images, json=updated_post_data)

    assert update_response.status_code == 200
    assert update_response.json.get("images") == []


def test_update_post_remove_all_images_without_key(
    authenticated_client, post_with_images
):
    """Test removing all images by omitting imagesIds key."""
    updated_post_data: dict[str, Any] = dict(post_data)
    # Don't include imagesIds key at all

    update_response = authenticated_client.put(post_with_images, json=updated_post_data)

    assert update_response.status_code == 200
    assert update_response.json.get("images") == []


def test_update_post_remove_one_image(authenticated_client, images):
    """Test removing one image while keeping others."""
    # Create post with all 3 images
    all_images_ids = [img[0] for img in images]
    post_url = create_post_with_images(authenticated_client, all_images_ids)

    # Get the post to see current images
    get_response = authenticated_client.get(post_url)
    current_images = get_response.json["images"]

    # Update to keep only first 2 images using IDs from response
    updated_images_ids = [current_images[0]["id"], current_images[1]["id"]]
    expected_images = images[:2]

    updated_post_data: dict[str, Any] = dict(post_data)
    updated_post_data["imagesIds"] = updated_images_ids

    update_response = authenticated_client.put(post_url, json=updated_post_data)

    assert update_response.status_code == 200
    assert_resource_images(update_response, expected_images)


def test_update_post_reorder_images(authenticated_client, images):
    """Test changing the order of images."""
    # Create post with images in order 0,1,2
    original_order_ids = [img[0] for img in images]
    post_url = create_post_with_images(authenticated_client, original_order_ids)

    # Get the post to retrieve current images
    get_response = authenticated_client.get(post_url)
    current_images = get_response.json["images"]

    # Update with reversed order 2,1,0 using IDs from response
    reversed_order_ids = [
        current_images[2]["id"],
        current_images[1]["id"],
        current_images[0]["id"],
    ]
    expected_images = [images[2], images[1], images[0]]

    updated_post_data: dict[str, Any] = dict(post_data)
    updated_post_data["imagesIds"] = reversed_order_ids

    update_response = authenticated_client.put(post_url, json=updated_post_data)

    assert update_response.status_code == 200
    assert_resource_images(update_response, expected_images)


def test_create_post_with_too_many_images(authenticated_client):
    """Test creating a post with more than maximum allowed images."""
    post_data_with_images: dict[str, Any] = dict(post_data)
    post_data_with_images["imagesIds"] = [str(uuid.uuid4()) for _ in range(11)]

    response = authenticated_client.post("/posts", json=post_data_with_images)

    assert response.status_code == 422


def test_update_post_with_too_many_images(authenticated_client, post):
    """Test updating a post with more than maximum allowed images."""
    updated_post_data: dict[str, Any] = dict(post_data)
    updated_post_data["imagesIds"] = [str(uuid.uuid4()) for _ in range(11)]

    response = authenticated_client.put(post, json=updated_post_data)

    assert response.status_code == 422


def test_image_shared_between_multiple_posts(authenticated_client, image):
    """Test that an image can be shared between multiple posts."""
    image_id, image_url = image

    # Create two posts with the same image
    post1_data: dict[str, Any] = dict(post_data)
    post1_data["title"] = "Post 1"
    post1_url = create_post_with_images(authenticated_client, [image_id], post1_data)

    post2_data: dict[str, Any] = dict(post_data)
    post2_data["title"] = "Post 2"
    post2_url = create_post_with_images(authenticated_client, [image_id], post2_data)

    # Verify both posts have the same image
    response1 = authenticated_client.get(post1_url)
    response2 = authenticated_client.get(post2_url)

    assert_resource_images(response1, [image])
    assert_resource_images(response2, [image])


def test_delete_post_with_images_keeps_images_if_used_elsewhere(
    authenticated_client, image
):
    """Test that deleting a post doesn't delete images used by other posts."""
    image_id, image_url = image

    # Create two posts with the same image
    post1_data: dict[str, Any] = dict(post_data)
    post1_data["title"] = "Post 1"
    post1_url = create_post_with_images(authenticated_client, [image_id], post1_data)

    post2_data: dict[str, Any] = dict(post_data)
    post2_data["title"] = "Post 2"
    post2_url = create_post_with_images(authenticated_client, [image_id], post2_data)

    delete_response = authenticated_client.delete(post1_url)
    assert delete_response.status_code == 204

    # Verify the image is still accessible
    image_response = authenticated_client.get(image_url)
    assert image_response.status_code == 200

    # Verify the second post still has the image
    response2 = authenticated_client.get(post2_url)
    assert_resource_images(response2, [image])


def test_orphaned_by_post_update_images_are_deleted(authenticated_client, image):
    """Test that images not used by any posts are deleted."""
    image_id, image_url = image

    # Create a post with the image
    post_url = create_post_with_images(authenticated_client, [image_id])

    # Remove the image from the post
    updated_post_data: dict[str, Any] = dict(post_data)
    updated_post_data["imagesIds"] = []
    authenticated_client.put(post_url, json=updated_post_data)

    # Verify the orphaned image is deleted
    image_response = authenticated_client.get(image_url)
    assert image_response.status_code == 404


def test_orphaned_by_post_deletion_images_are_deleted(authenticated_client, image):
    """Test that images not used by any posts are deleted upon post deletion."""
    image_id, image_url = image

    post_url = create_post_with_images(authenticated_client, [image_id])

    authenticated_client.delete(post_url)

    image_response = authenticated_client.get(image_url)
    assert image_response.status_code == 404


def test_create_post_with_nonexistent_image_id(authenticated_client):
    """Test creating a post with an image ID that doesn't exist."""
    post_data_with_fake_image: dict[str, Any] = dict(post_data)
    post_data_with_fake_image["imagesIds"] = [str(uuid.uuid4())]

    response = authenticated_client.post("/posts", json=post_data_with_fake_image)

    assert response.status_code == 422


def test_update_post_with_nonexistent_image_id(authenticated_client, post):
    """Test updating a post with an image ID that doesn't exist."""
    updated_post_data: dict[str, Any] = dict(post_data)
    updated_post_data["imagesIds"] = [str(uuid.uuid4())]

    response = authenticated_client.put(post, json=updated_post_data)

    assert response.status_code == 422


def test_allow_duplicate_image_in_single_post(authenticated_client, image):
    """Test that the same image can be used multiple times in one post."""
    image_id, image_url = image

    # Create post with duplicated image
    post_data_with_dup: dict[str, Any] = dict(post_data)
    post_data_with_dup["imagesIds"] = [image_id, image_id, image_id]

    response = authenticated_client.post("/posts", json=post_data_with_dup)

    assert response.status_code == 201
    assert_resource_images(response, [image, image, image])
