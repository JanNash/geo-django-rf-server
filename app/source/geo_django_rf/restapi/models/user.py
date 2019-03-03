from django.contrib.auth.models import AbstractUser
from .abstract_base_classes import UpdateDatedModel


class User(AbstractUser, UpdateDatedModel):
    pass
