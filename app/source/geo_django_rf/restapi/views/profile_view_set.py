from rest_framework import viewsets
from rest_framework.parsers import JSONParser
from ..models import Profile
from ..parsers import MultiPartWithJSONParser
from ..serializers import ProfileSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows profiles to be viewed or edited.
    """
    queryset = Profile.objects.all()
    parser_classes = (JSONParser, MultiPartWithJSONParser,)
    serializer_class = ProfileSerializer
