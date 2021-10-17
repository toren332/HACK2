from service import serializers
from service import models
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.gis.geos import Polygon
from django.core.serializers import serialize
from rest_framework.response import Response
import json
from django.core.cache import cache


class PolyViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.PolySerializer
    permission_classes = [AllowAny]

    def get_bbox(self):
        lat_min = self.request.GET.get('lat_min')
        lat_max = self.request.GET.get('lat_max')
        lon_min = self.request.GET.get('lon_min')
        lon_max = self.request.GET.get('lon_max')
        if None not in [lat_max, lat_min, lon_min, lon_max]:
            lat_min = float(lat_min)
            lat_max = float(lat_max)
            lon_min = float(lon_min)
            lon_max = float(lon_max)
        return lat_min, lat_max, lon_min, lon_max

    def get_queryset(self):
        qs = models.Poly.objects.all()
        lat_min, lat_max, lon_min, lon_max = self.get_bbox()
        if None in [lat_max, lat_min, lon_min, lon_max]:
            return qs
        poly = Polygon(
            ((lat_min, lon_min), (lat_max, lon_min), (lat_max, lon_max), (lat_min, lon_max), (lat_min, lon_min)),
            srid=4326)
        qs = qs.filter(polygon__intersects=poly)
        return qs

    def list(self, request, *args, **kwargs):
        lat_min, lat_max, lon_min, lon_max = self.get_bbox()
        queryset = self.get_queryset()
        if None in [lat_max, lat_min, lon_min, lon_max]:
            d = cache.get('poly')
            d = None
            if d is None:
                d = json.loads(serialize('geojson', queryset,
                                         geometry_field='polygon',
                                         fields=('id', 'live_humans_2021', 'live_humans_2025', 'live_humans_2030','potreb_2021', 'potreb_2025', 'potreb_2030', 'optima', 'school','work_humans', 'transports', 'colors')))
                cache.set('poly', d, 60 * 60 * 24)
        else:
            d = json.loads(serialize('geojson', queryset,
                                     geometry_field='polygon',
                                     fields=('id', 'live_humans_2021', 'live_humans_2025', 'live_humans_2030','potreb_2021', 'potreb_2025', 'potreb_2030', 'optima', 'school','work_humans', 'transports', 'colors')))

        resp = Response(d)
        resp["Access-Control-Allow-Origin"] = '*'
        resp["Access-Control-Allow-Methods"] = 'GET,PUT, OPTIONS'
        resp["Access-Control-Max-Age"] = '1000'
        resp["Access-Control-Allow-Headers"] = 'X-Requested-With, Content-Type'
        return resp


