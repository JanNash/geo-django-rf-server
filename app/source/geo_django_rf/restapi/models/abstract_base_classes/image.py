from django.db import models


class Image(models.Model):
    image = models.ImageField(null=True)

    class Meta:
        abstract = True
