"""Tests for posts with images functionality."""

from io import BytesIO
from typing import Any

from conftest import post_data


def upload_image(client, filename="test.png", content=b"fake image content"):
    """Helper function to upload an image and return its ID and URL."""
    data = {"image": (BytesIO(content), filename)}
    response = client.post(
        "/uploads/images", data=data, content_type="multipart/form-data"
    )
    assert response.status_code == 201
    return response.json["id"], response.json["url"]


def test_create_post_with_images(authenticated_client):
    """Test creating a post with multiple images."""
    # Upload multiple images
    image1_id, image1_url = upload_image(authenticated_client, "test1.png", b"image 1")
    image2_id, image2_url = upload_image(authenticated_client, "test2.png", b"image 2")
    image3_id, image3_url = upload_image(authenticated_client, "test3.png", b"image 3")

    # Create a post with all images
    post_data_with_images: dict[str, Any] = dict(post_data)
    post_data_with_images["imagesIds"] = [image1_id, image2_id, image3_id]

    response = authenticated_client.post("/posts", json=post_data_with_images)

    assert response.status_code == 201
    assert "images" in response.json
    assert len(response.json["images"]) == 3
    assert image1_url in response.json["images"]
    assert image2_url in response.json["images"]
    assert image3_url in response.json["images"]


def test_get_post_with_images(authenticated_client):
    """Test retrieving a post that has images."""
    # Upload images and create a post
    image1_id, image1_url = upload_image(authenticated_client, "test1.png", b"image 1")
    image2_id, image2_url = upload_image(authenticated_client, "test2.png", b"image 2")

    post_data_with_images: dict[str, Any] = dict(post_data)
    post_data_with_images["imagesIds"] = [image1_id, image2_id]

    create_response = authenticated_client.post("/posts", json=post_data_with_images)
    post_url = create_response.headers["Location"]

    # Get the post
    get_response = authenticated_client.get(post_url)

    assert get_response.status_code == 200
    assert len(get_response.json["images"]) == 2
    assert image1_url in get_response.json["images"]
    assert image2_url in get_response.json["images"]


def test_update_post_add_images(authenticated_client):
    """Test adding images to an existing post."""
    # Create a post without images
    create_response = authenticated_client.post("/posts", json=dict(post_data))
    post_url = create_response.headers["Location"]

    # Verify no images initially
    assert len(create_response.json["images"]) == 0

    # Upload images
    image1_id, image1_url = upload_image(authenticated_client, "test1.png", b"image 1")
    image2_id, image2_url = upload_image(authenticated_client, "test2.png", b"image 2")

    # Update the post to add images
    updated_post_data: dict[str, Any] = dict(post_data)
    updated_post_data["imagesIds"] = [image1_id, image2_id]

    update_response = authenticated_client.put(post_url, json=updated_post_data)

    assert update_response.status_code == 200
    assert len(update_response.json["images"]) == 2
    assert image1_url in update_response.json["images"]
    assert image2_url in update_response.json["images"]


def test_update_post_replace_images(authenticated_client):
    """Test replacing images of an existing post."""
    # Upload initial images
    image1_id, image1_url = upload_image(authenticated_client, "test1.png", b"image 1")
    image2_id, image2_url = upload_image(authenticated_client, "test2.png", b"image 2")

    # Create a post with initial images
    post_data_with_images: dict[str, Any] = dict(post_data)
    post_data_with_images["imagesIds"] = [image1_id, image2_id]
    create_response = authenticated_client.post("/posts", json=post_data_with_images)
    post_url = create_response.headers["Location"]

    # Upload new images
    image3_id, image3_url = upload_image(authenticated_client, "test3.png", b"image 3")
    image4_id, image4_url = upload_image(authenticated_client, "test4.png", b"image 4")

    # Update the post with new images
    updated_post_data: dict[str, Any] = dict(post_data)
    updated_post_data["imagesIds"] = [image3_id, image4_id]

    update_response = authenticated_client.put(post_url, json=updated_post_data)

    assert update_response.status_code == 200
    assert len(update_response.json["images"]) == 2
    assert image3_url in update_response.json["images"]
    assert image4_url in update_response.json["images"]
    assert image1_url not in update_response.json["images"]
    assert image2_url not in update_response.json["images"]


def test_update_post_remove_all_images(authenticated_client):
    """Test removing all images from a post."""
    # Upload images and create a post
    image1_id, image1_url = upload_image(authenticated_client, "test1.png", b"image 1")
    image2_id, image2_url = upload_image(authenticated_client, "test2.png", b"image 2")

    post_data_with_images: dict[str, Any] = dict(post_data)
    post_data_with_images["imagesIds"] = [image1_id, image2_id]
    create_response = authenticated_client.post("/posts", json=post_data_with_images)
    post_url = create_response.headers["Location"]

    # Update the post to remove all images
    updated_post_data: dict[str, Any] = dict(post_data)
    updated_post_data["imagesIds"] = []

    update_response = authenticated_client.put(post_url, json=updated_post_data)

    assert update_response.status_code == 200
    assert len(update_response.json["images"]) == 0


def test_update_post_partial_image_change(authenticated_client):
    """Test keeping some images and adding/removing others."""
    # Upload initial images
    image1_id, image1_url = upload_image(authenticated_client, "test1.png", b"image 1")
    image2_id, image2_url = upload_image(authenticated_client, "test2.png", b"image 2")
    image3_id, image3_url = upload_image(authenticated_client, "test3.png", b"image 3")

    # Create a post with initial images
    post_data_with_images: dict[str, Any] = dict(post_data)
    post_data_with_images["imagesIds"] = [image1_id, image2_id]
    create_response = authenticated_client.post("/posts", json=post_data_with_images)
    post_url = create_response.headers["Location"]

    # Update the post: keep image2, remove image1, add image3
    updated_post_data: dict[str, Any] = dict(post_data)
    updated_post_data["imagesIds"] = [image2_id, image3_id]

    update_response = authenticated_client.put(post_url, json=updated_post_data)

    assert update_response.status_code == 200
    assert len(update_response.json["images"]) == 2
    assert image2_url in update_response.json["images"]
    assert image3_url in update_response.json["images"]
    assert image1_url not in update_response.json["images"]


def test_image_shared_between_multiple_posts(authenticated_client):
    """Test that an image can be shared between multiple posts."""
    # Upload an image
    image_id, image_url = upload_image(authenticated_client)

    # Create first post with the image
    post1_data: dict[str, Any] = dict(post_data)
    post1_data["title"] = "Post 1"
    post1_data["imagesIds"] = [image_id]
    response1 = authenticated_client.post("/posts", json=post1_data)
    post1_url = response1.headers["Location"]

    # Create second post with the same image
    post2_data: dict[str, Any] = dict(post_data)
    post2_data["title"] = "Post 2"
    post2_data["imagesIds"] = [image_id]
    response2 = authenticated_client.post("/posts", json=post2_data)
    post2_url = response2.headers["Location"]

    # Verify both posts have the same image
    get_response1 = authenticated_client.get(post1_url)
    get_response2 = authenticated_client.get(post2_url)

    assert image_url in get_response1.json["images"]
    assert image_url in get_response2.json["images"]

    # Verify the image is still accessible
    image_response = authenticated_client.get(image_url)
    assert image_response.status_code == 200


def test_delete_post_with_images_keeps_images_if_used_elsewhere(
    authenticated_client, db
):
    """Test that deleting a post doesn't delete images that are used by other posts."""

    # Upload an image
    image_id, image_url = upload_image(authenticated_client)

    # Create two posts with the same image
    post1_data: dict[str, Any] = dict(post_data)
    post1_data["title"] = "Post 1"
    post1_data["imagesIds"] = [image_id]
    response1 = authenticated_client.post("/posts", json=post1_data)
    post1_url = response1.headers["Location"]

    post2_data: dict[str, Any] = dict(post_data)
    post2_data["title"] = "Post 2"
    post2_data["imagesIds"] = [image_id]
    response2 = authenticated_client.post("/posts", json=post2_data)
    post2_url = response2.headers["Location"]

    # Delete the first post
    delete_response = authenticated_client.delete(post1_url)
    assert delete_response.status_code == 204

    # Verify the image is still accessible
    image_response = authenticated_client.get(image_url)
    assert image_response.status_code == 200

    # Verify the second post still has the image
    get_response2 = authenticated_client.get(post2_url)
    assert image_url in get_response2.json["images"]


# to do check that orphaned images are deleted


def test_create_post_with_nonexistent_image_id(authenticated_client):
    """Test creating a post with an image ID that doesn't exist."""
    import uuid

    # Try to create a post with a non-existent image ID
    post_data_with_fake_image: dict[str, Any] = dict(post_data)
    post_data_with_fake_image["imagesIds"] = [str(uuid.uuid4())]

    response = authenticated_client.post("/posts", json=post_data_with_fake_image)

    # The post should be created successfully but with no images
    # since the image ID doesn't exist in the database
    assert response.status_code == 201
    assert len(response.json["images"]) == 0
