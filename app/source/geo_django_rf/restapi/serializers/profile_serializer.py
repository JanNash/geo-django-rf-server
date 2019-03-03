from rest_framework import serializers
from drf_extra_fields.geo_fields import PointField
from .abstract_base_classes import GetFieldNamesMixin
from .photo_serializer import PhotoSerializer
from ..models import Profile, Photo


class ProfileSerializer(GetFieldNamesMixin, serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # FIXME: Right now, this is always overwriting the image/s.
        # It should of course check for their existence
        # (as soon as there's more than an 'image' field on the Image class)
        image_data = validated_data.pop('image')
        instance.image = Photo.objects.create(**image_data)
        # TODO: instance.images
        return super().update(instance, validated_data)

    # user = serializers.HyperlinkedRelatedField(read_only=True, view_name='user-detail')
    # last_saved_location = PointField(required=False)
    # photo = PhotoSerializer(required=False, allow_null=True)
