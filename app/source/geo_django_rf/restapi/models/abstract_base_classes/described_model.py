from django.db import models


class DescribedModel(models.Model):
    description = models.TextField(blank=True, null=True, max_length=4096)

    class Meta:
        abstract = True
