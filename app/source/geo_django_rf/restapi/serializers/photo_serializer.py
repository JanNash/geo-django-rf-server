from rest_framework import serializers
from drf_extra_fields.geo_fields import PointField
from .abstract_base_classes import GetFieldNamesMixin
from ..models import Photo


class PhotoSerializer(GetFieldNamesMixin, serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = '__all__'
