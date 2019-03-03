from django.db import models


class NamedModel(models.Model):
    name = models.CharField(blank=True, null=True, max_length=1024)

    class Meta:
        abstract = True
