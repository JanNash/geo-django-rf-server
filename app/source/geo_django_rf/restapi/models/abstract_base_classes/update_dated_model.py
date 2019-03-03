from django.db import models


class UpdateDatedModel(models.Model):
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        abstract = True
