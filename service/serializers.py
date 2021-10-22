from rest_framework import serializers
from . import models


class PolySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Poly
        fields = ['id', 'polygon', 'live_humans_2021', 'live_humans_2025', 'potreb_2021', 'potreb_2025', 'optima', 'school', 'work_humans', 'colors']


class SchoolSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.School
        fields = ['id', 'point', 'name', 'address', 'rating', 'chief_name', 'web_site', 'pupils_cnt', 'nagruzka', 'nagruzka_2025year','phone', 'email',]