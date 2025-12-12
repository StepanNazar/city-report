from io import BytesIO


def test_upload_image(authenticated_client):
    data = {"image": (BytesIO(b"fake image content"), "test.png")}

    response = authenticated_client.post(
        "/uploads/images", data=data, content_type="multipart/form-data"
    )

    assert response.status_code == 201
    assert response.json["url"] != ""
    assert response.json["url"] == response.headers["Location"]
    assert "id" in response.json

    response = authenticated_client.get(response.json["url"])
    assert response.status_code == 200
    assert response.data == b"fake image content"


def test_upload_not_image_as_image(authenticated_client):
    data = {"image": (BytesIO(b"not an image"), "test.txt")}
    response = authenticated_client.post(
        "/uploads/images", data=data, content_type="multipart/form-data"
    )
    assert response.status_code == 422
