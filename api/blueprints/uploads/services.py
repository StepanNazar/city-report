"""Storage service implementations for file uploads."""

import abc
import os
import uuid
from typing import TYPE_CHECKING

import filetype
from flask import send_from_directory, url_for
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

if TYPE_CHECKING:
    from api.blueprints.uploads.models import Image


class StorageService(abc.ABC):
    @abc.abstractmethod
    def _upload(self, file: FileStorage) -> str:
        """Upload a file to storage and return its URL
        :param file: werkzeug's FileStorage object
        :return: URL of the uploaded file
        :raises RuntimeError: If the upload failed
        """
        pass

    @staticmethod
    def _check_file_is_image(file: FileStorage) -> bool:
        """Check if the provided file is an image
        :param file: werkzeug's FileStorage object
        :return: True if the file is an image, False otherwise
        """
        header = file.read(261)
        kind = filetype.guess(header)
        file.seek(0)
        return kind is not None and kind.mime.split("/")[0] == "image"

    def upload_image(self, image_file: FileStorage, db_session) -> "Image":
        """Upload an image to storage and return the Image model instance
        :param image_file: werkzeug's FileStorage object
        :param db_session: Database session for adding the image record
        :return: Image model instance
        :raises ValueError: If the file is not an image
        :raises RuntimeError: If the upload failed
        """
        from api.blueprints.uploads.models import Image

        if not self._check_file_is_image(image_file):
            raise ValueError("File is not a valid image")

        url = self._upload(image_file)
        image = Image(url=url)  # type: ignore
        db_session.add(image)
        db_session.commit()
        return image

    @abc.abstractmethod
    def send_file(self, filename: str):
        """Send a file to the client"""
        pass


class LocalFolderStorageService(StorageService):
    def _upload(self, file: FileStorage) -> str:
        """Upload a file to a local folder and return its URL"""
        filename = uuid.uuid4().hex + secure_filename(file.filename or "")
        file_path = os.path.join("uploaded_images", filename)
        try:
            file.save(file_path)
        except Exception as e:
            raise RuntimeError("Failed to save file") from e
        return url_for("uploads.image", filename=filename)

    def send_file(self, filename: str):
        return send_from_directory("uploaded_images", filename)
