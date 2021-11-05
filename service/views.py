from service import serializers
from service import models
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.gis.geos import Polygon
from django.core.serializers import serialize
from rest_framework.response import Response
import json
from django.core.cache import cache
from rest_framework import status
from rest_framework.decorators import action
from django.db.models import Max, Min
import matplotlib.cm as cm
from django.conf import settings
from matplotlib.colors import rgb2hex
from base64 import b64encode


class PolyNewViewSet(viewsets.ReadOnlyModelViewSet):
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
        qs = qs.filter(geometry__intersects=poly)
        return qs

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        lat_min, lat_max, lon_min, lon_max = self.get_bbox()
        if None in [lat_max, lat_min, lon_min, lon_max]:
            d = cache.get('poly_new')
            if d is None:
                serializer = self.get_serializer(queryset, many=True)
                d = serializer.data
                cache.set('poly_new', d, 60 * 60 * 24)
                return Response(serializer.data)
            else:
                return Response(d)
        else:
            serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


    @action(detail=False, methods=['get'])
    def filters(self, request):
        d = {}
        l = []
        for i in ['live_humans_2021', 'live_humans_2025', 'potreb_2021', 'potreb_2025', 'optima', 'school', 'work_humans']:
            l.append(Min(i))
            l.append(Max(i))
        qs = models.Poly.objects.aggregate(*l)
        for i in ['live_humans_2021', 'live_humans_2025', 'potreb_2021', 'potreb_2025', 'optima', 'school', 'work_humans']:
            d[i]=[qs[f'{i}__min'], qs[f'{i}__max']]
        l2 = []
        for i in ['nagruzka', 'nagruzka_2025year']:
            l2.append(Min(i))
            l2.append(Max(i))
        qs_2 = models.School.objects.aggregate(*l2)
        for i in ['nagruzka', 'nagruzka_2025year']:
            d[i] = [qs_2[f'{i}__min'], qs_2[f'{i}__max']]
        return Response(d, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def colors(self, request):
        CMAPS = settings.COLORMAPS_DICT
        d = {}
        for k,v in CMAPS.items():
            cmap = cm.get_cmap(v)(range(256))
            d[k] = [rgb2hex(x) for x in cmap]
        return Response(d, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def colors_png(self, request):
        CMAPS = settings.COLORMAPS_DICT
        d = {}
        for k,v in CMAPS.items():
            d[k] = b64encode(cm.get_cmap(v)._repr_png_())
        return Response(d, status=status.HTTP_200_OK)


class SchoolViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.SchoolSerializer
    permission_classes = [AllowAny]
    # queryset = models.School.objects.all()

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
        qs = models.School.objects.all()
        lat_min, lat_max, lon_min, lon_max = self.get_bbox()
        if None in [lat_max, lat_min, lon_min, lon_max]:
            return qs
        poly = Polygon(
            ((lat_min, lon_min), (lat_max, lon_min), (lat_max, lon_max), (lat_min, lon_max), (lat_min, lon_min)),
            srid=4326)
        qs = qs.filter(point__intersects=poly)
        return qs


    def list(self, request, *args, **kwargs):
        lat_min, lat_max, lon_min, lon_max = self.get_bbox()
        queryset = self.get_queryset()
        if None in [lat_max, lat_min, lon_min, lon_max]:
            d = cache.get('schools')
            # d = None
            if d is None:
                d = json.loads(serialize('geojson', queryset,
                                         geometry_field='point',
                                         fields=('id', 'point', 'name', 'address', 'rating', 'chief_name', 'web_site',
                                                 'pupils_cnt', 'nagruzka', 'nagruzka_2025year', 'phone', 'email')))
                cache.set('schools', d, 60 * 60 * 24)
        else:
            d = json.loads(serialize('geojson', queryset,
                                     geometry_field='point',
                                     fields=(
                                     'id', 'point', 'name', 'address', 'rating', 'chief_name', 'web_site', 'pupils_cnt',
                                     'nagruzka', 'nagruzka_2025year', 'phone', 'email')))


        resp = Response(d)
        resp["Access-Control-Allow-Origin"] = '*'
        resp["Access-Control-Allow-Methods"] = 'GET,PUT, OPTIONS'
        resp["Access-Control-Max-Age"] = '1000'
        resp["Access-Control-Allow-Headers"] = 'X-Requested-With, Content-Type'
        return resp