from django.core.exceptions import ValidationError
from django.db.models.fields.files import ImageField
from rest_framework import serializers
from .models import *
from io import BytesIO

from rest_framework import serializers    

class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        from django.core.files.base import ContentFile
        import base64
        import six
        import uuid

        if isinstance(data, six.string_types):
            if 'data:' in data and ';base64,' in data:
                header, data = data.split(';base64,')

            try:
                decoded_file = base64.b64decode(data +  b"==")
            except TypeError:
                self.fail('invalid_image')


            file_name = str(uuid.uuid4())[:12] 
            file_extension = self.get_file_extension(file_name, decoded_file)

            complete_file_name = "%s.%s" % (file_name, file_extension, )

            data = ContentFile(decoded_file, name=complete_file_name)

        return super(Base64ImageField, self).to_internal_value(data)

    def get_file_extension(self, file_name, decoded_file):
        import imghdr

        extension = imghdr.what(file_name, decoded_file)
        extension = "png" if extension == "png" else extension

        return extension
class PostSerializer(serializers.ModelSerializer):
    post_photo = Base64ImageField(max_length=None, use_url=False)

    def validate_image_size(self , image):
        MAX_FILE_SIZE = 10000000
        MIN_FILE_SIZE = 10
        if image.size > MAX_FILE_SIZE or image.size < MIN_FILE_SIZE:
            raise ValidationError("File size is not proper")
    
    def validate_image_format(self , data):
        f = super(Post, self).validate_image_format(data)
        if f is None:
            return None
        try:
            from PIL import Image
        except ImportError:
            from PIL import Image
        
        if hasattr(data, 'temporary_file_path'):
            file = data.temporary_file_path()
        else:
            if hasattr(data , 'read'):
                file = BytesIO(data.read)
            else:
                file = BytesIO(data['content'])
        try:
            im = Image.open(file)
            if im.format not in ('BMP' , 'PNG' ,'JPEG'):
                raise ValidationError("Unsupport image type")
        except ImportError:
            raise
        except Exception:
            raise ValidationError(self.error_messages['invalid_image'])
        
        if hasattr(f , 'seek') and callable(f.seek):
            f.seek(0)
        return f

    class Meta:
        model = Post
        fields = ['post_photo', 'message', 'username', 'date_created', 'post_id']