from django.db import models
from django.contrib.gis.db import models as gismodels
from django.contrib.auth import get_user_model
from .abstract_base_classes import (
    CreationDatedModel, DescribedModel, NamedModel, PointOfInterest, UpdateDatedModel, Image
)


class Profile(CreationDatedModel, DescribedModel, NamedModel, PointOfInterest, UpdateDatedModel):
    user = models.OneToOneField(get_user_model(), related_name='profile')
    photo = models.OneToOneField('Photo', related_name='+', null=True, default=None)
    # photo_albums: see PhotoAlbum.owner


class PhotoAlbum(CreationDatedModel, DescribedModel, NamedModel, UpdateDatedModel):
    owner = models.OneToOneField(Profile, related_name='photo_albums')
    # photos: see Photo.album


class Photo(CreationDatedModel, DescribedModel, Image, NamedModel):
    location = gismodels.PointField(blank=True, null=True, srid=4326)
    album = models.ForeignKey('PhotoAlbum', related_name='photos')
