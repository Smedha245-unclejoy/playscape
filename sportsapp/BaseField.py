import re
import base64
import uuid
import imghdr

from django.core.files.base import ContentFile
from rest_framework import serializers


class Base64ImageField(serializers.ImageField):
    """ Django-rest-framework field for base64 encoded image data. """
    def from_native(self, base64_data):
        if isinstance(base64_data, basestring):
            # Strip data header if it exists
            base64_data = re.sub(r"^data\:.+base64\,(.+)$", r"\1", base64_data)

            # Try to decode the file. Return validation error if it fails.
            try:
                decoded_file = base64.b64decode(base64_data)
            except TypeError:
                msg = "Please upload a valid image."
                raise serializers.ValidationError(msg)

            # Get the file name extension:
            extension = imghdr.what("file_name", decoded_file)
            if extension not in ("jpeg", "jpg", "png"):
                msg = "{0} is not a valid image type.".format(extension)
                raise serializers.ValidationError(msg)

            extension = "jpg" if extension == "jpeg" else extension
            file_name = ".".join([str(uuid.uuid4()), extension])
            data = ContentFile(decoded_file, name=file_name)

        return super(Base64ImageField, self).from_native(data)
