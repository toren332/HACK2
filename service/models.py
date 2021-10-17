from django.db import models
from django.contrib.gis.db import models as gis_models


class Building(models.Model):
    point = gis_models.PointField()
    optimal = models.FloatField()


class Poly(models.Model):
    polygon = gis_models.PolygonField()
    live_humans_2021 = models.IntegerField()
    live_humans_2025 = models.IntegerField()
    live_humans_2030 = models.IntegerField()
    work_humans = models.IntegerField()
    transports = models.IntegerField()
    colors = models.JSONField()

