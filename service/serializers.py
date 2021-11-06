from rest_framework import serializers
from . import models


class PolySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Poly
        fields = ['id', 'geometry', 'live_humans_2021', 'live_humans_2025', 'potreb_2021', 'potreb_2025', 'optima', 'school', 'work_humans', 'colors']


class SchoolSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.School
        fields = ['id', 'point', 'name', 'address', 'rating', 'chief_name', 'web_site', 'phone', 'email', 'pupils_cnt', 'nagruzka', 'nagruzka_2025year', 'year', 'nagruzka_rat', 'nagruzka_rat_5year']
