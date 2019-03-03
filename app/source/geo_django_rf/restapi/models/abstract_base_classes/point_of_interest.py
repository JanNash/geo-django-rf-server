from django.db import models
from django.contrib.gis.db import models as gismodels


class PointOfInterest(models.Model):
    last_saved_location = gismodels.PointField(blank=True, null=True, srid=4326)

    class Meta:
        abstract = True
