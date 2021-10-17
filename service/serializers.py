from rest_framework import serializers
from . import models


class PolySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Poly
        fields = ['id', 'polygon', 'live_humans_2021', 'live_humans_2025', 'live_humans_2030','work_humans', 'transports', 'colors']