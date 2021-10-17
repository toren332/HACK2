from rest_framework import serializers
from . import models


class PolySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Poly
        fields = ['id', 'polygon', 'live_humans_2021', 'live_humans_2025', 'live_humans_2030', 'potreb_2021', 'potreb_2025', 'potreb_2030', 'optima', 'school', 'work_humans', 'transports', 'colors']