"""Tests for solutions with images functionality."""

from io import BytesIO
from typing import Any

from conftest import post_data, solution_data


def upload_image(client, filename="test.png", content=b"fake image content"):
    """Helper function to upload an image and return its ID and URL."""
    data = {"image": (BytesIO(content), filename)}
    response = client.post(
        "/uploads/images", data=data, content_type="multipart/form-data"
    )
    assert response.status_code == 201
    return response.json["id"], response.json["url"]


def create_post(client):
    """Helper to create a post and return its URL."""
    response = client.post("/posts", json=dict(post_data))
    assert response.status_code == 201
    return response.headers["Location"]


def test_create_solution_with_single_image(authenticated_client):
    """Test creating a solution with a single image."""
    post_url = create_post(authenticated_client)

    # Upload an image
    image_id, image_url = upload_image(authenticated_client)

    # Create a solution with the image
    solution_data_with_image: dict[str, Any] = dict(solution_data)
    solution_data_with_image["imagesIds"] = [image_id]

    response = authenticated_client.post(
        f"{post_url}/solutions", json=solution_data_with_image
    )

    assert response.status_code == 201
    assert "Location" in response.headers
    assert "images" in response.json
    assert len(response.json["images"]) == 1
    assert response.json["images"][0] == image_url


def test_create_solution_with_multiple_images(authenticated_client):
    """Test creating a solution with multiple images."""
    post_url = create_post(authenticated_client)

    # Upload multiple images
    image1_id, image1_url = upload_image(authenticated_client, "test1.png", b"image 1")
    image2_id, image2_url = upload_image(authenticated_client, "test2.png", b"image 2")
    image3_id, image3_url = upload_image(authenticated_client, "test3.png", b"image 3")

    # Create a solution with all images
    solution_data_with_images: dict[str, Any] = dict(solution_data)
    solution_data_with_images["imagesIds"] = [image1_id, image2_id, image3_id]

    response = authenticated_client.post(
        f"{post_url}/solutions", json=solution_data_with_images
    )

    assert response.status_code == 201
    assert "images" in response.json
    assert len(response.json["images"]) == 3
    assert image1_url in response.json["images"]
    assert image2_url in response.json["images"]
    assert image3_url in response.json["images"]


def test_get_solution_with_images(authenticated_client):
    """Test retrieving a solution that has images."""
    post_url = create_post(authenticated_client)

    # Upload images and create a solution
    image1_id, image1_url = upload_image(authenticated_client, "test1.png", b"image 1")
    image2_id, image2_url = upload_image(authenticated_client, "test2.png", b"image 2")

    solution_data_with_images: dict[str, Any] = dict(solution_data)
    solution_data_with_images["imagesIds"] = [image1_id, image2_id]

    create_response = authenticated_client.post(
        f"{post_url}/solutions", json=solution_data_with_images
    )
    solution_url = create_response.headers["Location"]

    # Get the solution
    get_response = authenticated_client.get(solution_url)

    assert get_response.status_code == 200
    assert len(get_response.json["images"]) == 2
    assert image1_url in get_response.json["images"]
    assert image2_url in get_response.json["images"]


def test_update_solution_add_images(authenticated_client):
    """Test adding images to an existing solution."""
    post_url = create_post(authenticated_client)

    # Create a solution without images
    create_response = authenticated_client.post(
        f"{post_url}/solutions", json=dict(solution_data)
    )
    solution_url = create_response.headers["Location"]

    # Verify no images initially
    assert len(create_response.json["images"]) == 0

    # Upload images
    image1_id, image1_url = upload_image(authenticated_client, "test1.png", b"image 1")
    image2_id, image2_url = upload_image(authenticated_client, "test2.png", b"image 2")

    # Update the solution to add images
    updated_solution_data: dict[str, Any] = dict(solution_data)
    updated_solution_data["imagesIds"] = [image1_id, image2_id]

    update_response = authenticated_client.put(solution_url, json=updated_solution_data)

    assert update_response.status_code == 200
    assert len(update_response.json["images"]) == 2
    assert image1_url in update_response.json["images"]
    assert image2_url in update_response.json["images"]


def test_update_solution_replace_images(authenticated_client):
    """Test replacing images of an existing solution."""
    post_url = create_post(authenticated_client)

    # Upload initial images
    image1_id, image1_url = upload_image(authenticated_client, "test1.png", b"image 1")
    image2_id, image2_url = upload_image(authenticated_client, "test2.png", b"image 2")

    # Create a solution with initial images
    solution_data_with_images: dict[str, Any] = dict(solution_data)
    solution_data_with_images["imagesIds"] = [image1_id, image2_id]
    create_response = authenticated_client.post(
        f"{post_url}/solutions", json=solution_data_with_images
    )
    solution_url = create_response.headers["Location"]

    # Upload new images
    image3_id, image3_url = upload_image(authenticated_client, "test3.png", b"image 3")
    image4_id, image4_url = upload_image(authenticated_client, "test4.png", b"image 4")

    # Update the solution with new images
    updated_solution_data: dict[str, Any] = dict(solution_data)
    updated_solution_data["imagesIds"] = [image3_id, image4_id]

    update_response = authenticated_client.put(solution_url, json=updated_solution_data)

    assert update_response.status_code == 200
    assert len(update_response.json["images"]) == 2
    assert image3_url in update_response.json["images"]
    assert image4_url in update_response.json["images"]
    assert image1_url not in update_response.json["images"]
    assert image2_url not in update_response.json["images"]


def test_update_solution_remove_all_images(authenticated_client):
    """Test removing all images from a solution."""
    post_url = create_post(authenticated_client)

    # Upload images and create a solution
    image1_id, image1_url = upload_image(authenticated_client, "test1.png", b"image 1")
    image2_id, image2_url = upload_image(authenticated_client, "test2.png", b"image 2")

    solution_data_with_images: dict[str, Any] = dict(solution_data)
    solution_data_with_images["imagesIds"] = [image1_id, image2_id]
    create_response = authenticated_client.post(
        f"{post_url}/solutions", json=solution_data_with_images
    )
    solution_url = create_response.headers["Location"]

    # Update the solution to remove all images
    updated_solution_data: dict[str, Any] = dict(solution_data)
    updated_solution_data["imagesIds"] = []

    update_response = authenticated_client.put(solution_url, json=updated_solution_data)

    assert update_response.status_code == 200
    assert len(update_response.json["images"]) == 0


def test_update_solution_partial_image_change(authenticated_client):
    """Test keeping some images and adding/removing others."""
    post_url = create_post(authenticated_client)

    # Upload initial images
    image1_id, image1_url = upload_image(authenticated_client, "test1.png", b"image 1")
    image2_id, image2_url = upload_image(authenticated_client, "test2.png", b"image 2")
    image3_id, image3_url = upload_image(authenticated_client, "test3.png", b"image 3")

    # Create a solution with initial images
    solution_data_with_images: dict[str, Any] = dict(solution_data)
    solution_data_with_images["imagesIds"] = [image1_id, image2_id]
    create_response = authenticated_client.post(
        f"{post_url}/solutions", json=solution_data_with_images
    )
    solution_url = create_response.headers["Location"]

    # Update the solution: keep image2, remove image1, add image3
    updated_solution_data: dict[str, Any] = dict(solution_data)
    updated_solution_data["imagesIds"] = [image2_id, image3_id]

    update_response = authenticated_client.put(solution_url, json=updated_solution_data)

    assert update_response.status_code == 200
    assert len(update_response.json["images"]) == 2
    assert image2_url in update_response.json["images"]
    assert image3_url in update_response.json["images"]
    assert image1_url not in update_response.json["images"]


def test_image_shared_between_multiple_solutions(authenticated_client):
    """Test that an image can be shared between multiple solutions."""
    post_url = create_post(authenticated_client)

    # Upload an image
    image_id, image_url = upload_image(authenticated_client)

    # Create first solution with the image
    solution1_data: dict[str, Any] = dict(solution_data)
    solution1_data["title"] = "Solution 1"
    solution1_data["imagesIds"] = [image_id]
    response1 = authenticated_client.post(f"{post_url}/solutions", json=solution1_data)
    solution1_url = response1.headers["Location"]

    # Create second solution with the same image
    solution2_data: dict[str, Any] = dict(solution_data)
    solution2_data["title"] = "Solution 2"
    solution2_data["imagesIds"] = [image_id]
    response2 = authenticated_client.post(f"{post_url}/solutions", json=solution2_data)
    solution2_url = response2.headers["Location"]

    # Verify both solutions have the same image
    get_response1 = authenticated_client.get(solution1_url)
    get_response2 = authenticated_client.get(solution2_url)

    assert image_url in get_response1.json["images"]
    assert image_url in get_response2.json["images"]

    # Verify the image is still accessible
    image_response = authenticated_client.get(image_url)
    assert image_response.status_code == 200


def test_image_shared_between_post_and_solution(authenticated_client):
    """Test that an image can be shared between a post and a solution."""
    # Upload an image
    image_id, image_url = upload_image(authenticated_client)

    # Create a post with the image
    post_data_with_image: dict[str, Any] = dict(post_data)
    post_data_with_image["imagesIds"] = [image_id]
    post_response = authenticated_client.post("/posts", json=post_data_with_image)
    post_url = post_response.headers["Location"]

    # Create a solution with the same image
    solution_data_with_image: dict[str, Any] = dict(solution_data)
    solution_data_with_image["imagesIds"] = [image_id]
    solution_response = authenticated_client.post(
        f"{post_url}/solutions", json=solution_data_with_image
    )
    solution_url = solution_response.headers["Location"]

    # Verify both post and solution have the same image
    get_post_response = authenticated_client.get(post_url)
    get_solution_response = authenticated_client.get(solution_url)

    assert image_url in get_post_response.json["images"]
    assert image_url in get_solution_response.json["images"]


def test_delete_solution_with_images_keeps_images_if_used_elsewhere(
    authenticated_client, db
):
    """Test that deleting a solution doesn't delete images used by other resources."""

    post_url = create_post(authenticated_client)

    # Upload an image
    image_id, image_url = upload_image(authenticated_client)

    # Create two solutions with the same image
    solution1_data: dict[str, Any] = dict(solution_data)
    solution1_data["title"] = "Solution 1"
    solution1_data["imagesIds"] = [image_id]
    response1 = authenticated_client.post(f"{post_url}/solutions", json=solution1_data)
    solution1_url = response1.headers["Location"]

    solution2_data: dict[str, Any] = dict(solution_data)
    solution2_data["title"] = "Solution 2"
    solution2_data["imagesIds"] = [image_id]
    response2 = authenticated_client.post(f"{post_url}/solutions", json=solution2_data)
    solution2_url = response2.headers["Location"]

    # Delete the first solution
    delete_response = authenticated_client.delete(solution1_url)
    assert delete_response.status_code == 204

    # Verify the image is still accessible
    image_response = authenticated_client.get(image_url)
    assert image_response.status_code == 200

    # Verify the second solution still has the image
    get_response2 = authenticated_client.get(solution2_url)
    assert image_url in get_response2.json["images"]


def test_create_solution_with_nonexistent_image_id(authenticated_client):
    """Test creating a solution with an image ID that doesn't exist."""
    import uuid

    post_url = create_post(authenticated_client)

    # Try to create a solution with a non-existent image ID
    solution_data_with_fake_image: dict[str, Any] = dict(solution_data)
    solution_data_with_fake_image["imagesIds"] = [str(uuid.uuid4())]

    response = authenticated_client.post(
        f"{post_url}/solutions", json=solution_data_with_fake_image
    )

    # The solution should be created successfully but with no images
    assert response.status_code == 201
    assert len(response.json["images"]) == 0
