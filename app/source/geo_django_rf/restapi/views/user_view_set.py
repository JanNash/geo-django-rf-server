from django.contrib.auth import get_user_model
from rest_framework import viewsets
from ..serializers import UserSerializer
from ..permissions import AnonCreateAndUpdateOwnerOnly, ListAdminOnly


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = get_user_model().objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = (AnonCreateAndUpdateOwnerOnly, ListAdminOnly)

    def retrieve(self, request, *args, **kwargs):
        """
        If provided 'pk' is "me" then return the current user.
        """
        if request.user and self.kwargs["pk"] == 'me':
            self.kwargs["pk"] = request.user.pk
        return super(UserViewSet, self).retrieve(request, args, kwargs)
