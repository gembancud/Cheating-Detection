from django.db import models
from django.utils.html import mark_safe
from io import BytesIO
from django.core.files import File
from PIL import Image
import os
from django.core.files.storage import default_storage

# Create your models here.


class Snapshot(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField()

    def image_tag(self):
        return mark_safe(f'<img src="{self.image.url}" width="150" height="150" />')

    def save(self, *args, **kwargs):
        self.image = make_thumbnail(self.image)

        super().save(*args, **kwargs)

    image_tag.short_description = 'Image'


def make_thumbnail(image, size=(150, 150)):
    """Makes thumbnails of given size from given image"""
    im = Image.open(image)
    im.convert('RGB')  # convert mode
    im.thumbnail(size)  # resize image
    thumb_io = BytesIO()  # create a BytesIO object
    im.save(thumb_io, 'JPEG', quality=85)  # save image to BytesIO object
    # create a django friendly File object
    thumbnail = File(thumb_io, name=image.name)

    return thumbnail
