from django.db import models
from django.contrib.gis.db import models as gis_models


class Poly(models.Model):
    polygon = gis_models.PolygonField()
    live_humans_2021 = models.IntegerField()
    live_humans_2025 = models.IntegerField()
    potreb_2021 = models.IntegerField()
    potreb_2025 = models.IntegerField()
    work_humans = models.IntegerField()
    optima = models.IntegerField()
    school = models.IntegerField()
    colors = models.JSONField()


class School(models.Model):
    point = gis_models.PointField()
    name = models.CharField(max_length=256, blank=True, null=True)
    address = models.CharField(max_length=512, blank=True, null=True)
    rating = models.IntegerField()
    chief_name = models.CharField(max_length=256, blank=True, null=True)
    web_site = models.URLField(blank=True, null=True)
    phone = models.CharField(max_length=32, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    pupils_cnt = models.IntegerField()
    nagruzka = models.FloatField()
    nagruzka_2025year = models.FloatField()

