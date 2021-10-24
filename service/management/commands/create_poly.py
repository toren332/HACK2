from django.core.management.base import BaseCommand
from service.models import Poly
import shapefile
import matplotlib as mpl
import matplotlib.cm as cm
from matplotlib.colors import rgb2hex
from django.contrib.gis.geos import Polygon
from tqdm import tqdm
from django.contrib.gis.gdal import SpatialReference, CoordTransform
from django.conf import settings
import copy
gcoord = SpatialReference(4326)
mycoord = SpatialReference(3857)
trans = CoordTransform(gcoord, mycoord)


def min_max(l, prop):
    l_ = [int(getattr(x.record,prop)) for x in l]
    return min(l_), max(l_)


def get_norm(l, prop):
    min_, max_ = min_max(l,prop)
    return mpl.colors.Normalize(vmin=min_, vmax=max_)


class Command(BaseCommand):
    def handle(self, *args, **options):
        CMAPS = settings.COLORMAPS_DICT
        Poly.objects.all().delete()
        poly_models = []
        shape = shapefile.Reader("cells_final/cells_final.shp")
        shape_records = list(shape.shapeRecords())
        live_humans_2021_norm = get_norm(shape_records,'home')
        live_humans_2025_norm = get_norm(shape_records,'home_5year')
        # live_humans_2030_norm = get_norm(shape_records,'home_5year')
        potreb_2021_norm = get_norm(shape_records,'potreb')
        potreb_2025_norm = get_norm(shape_records,'potreb_5ye')
        # potreb_2030_norm = get_norm(shape_records,'potreb_5ye')
        optima_norm = get_norm(shape_records,'new_school')
        work_humans_norm = get_norm(shape_records,'job')
        for i in tqdm(shape_records):
            polygon = i.shape.__geo_interface__
            data = {
                'live_humans_2021': int(i.record.home),
                'live_humans_2025': int(i.record.home_5year),
                # 'live_humans_2030': int(i.record.home_5year),
                'potreb_2021': int(i.record.potreb),
                'potreb_2025': int(i.record.potreb_5ye),
                # 'potreb_2030': int(i.record.potreb_5ye),
                'optima': int(i.record.new_school),
                'school': int(i.record.in_schoo_1),
                'work_humans': int(i.record.job),
                'colors': {
                    'live_humans_2021': rgb2hex(cm.ScalarMappable(
                        norm=live_humans_2021_norm, cmap=cm.get_cmap(CMAPS['live_humans_2021'])
                    ).to_rgba(float(int(i.record.home)))),
                    'live_humans_2025': rgb2hex(cm.ScalarMappable(
                        norm=live_humans_2025_norm, cmap=cm.get_cmap(CMAPS['live_humans_2025'])
                    ).to_rgba(float(int(i.record.home_5year)))),
                    # 'live_humans_2030': rgb2hex(cm.ScalarMappable(
                    #     norm=live_humans_2030_norm, cmap=cm.get_cmap('Oranges')
                    # ).to_rgba(float(int(i.record.home_5year)))),

                    'potreb_2021': rgb2hex(cm.ScalarMappable(
                        norm=potreb_2021_norm, cmap=cm.get_cmap(CMAPS['potreb_2021'])
                    ).to_rgba(float(int(i.record.potreb)))),
                    'potreb_2025': rgb2hex(cm.ScalarMappable(
                        norm=potreb_2025_norm, cmap=cm.get_cmap(CMAPS['potreb_2025'])
                    ).to_rgba(float(int(i.record.potreb_5ye)))),
                    # 'potreb_2030': rgb2hex(cm.ScalarMappable(
                    #     norm=potreb_2030_norm, cmap=cm.get_cmap('Wistia')
                    # ).to_rgba(float(int(i.record.potreb_5ye)))),

                    'work_humans': rgb2hex(cm.ScalarMappable(
                        norm=work_humans_norm, cmap=cm.get_cmap(CMAPS['work_humans'])
                    ).to_rgba(float(int(i.record.job)))),
                    'optima': rgb2hex(cm.ScalarMappable(
                        norm=optima_norm, cmap=cm.get_cmap(CMAPS['optima'])
                    ).to_rgba(float(int(i.record.new_school)))),
                },
            }
            poly = Polygon(polygon['coordinates'][0], srid=4326)
            geom = Polygon(polygon['coordinates'][0], srid=4326)
            poly_ = Polygon(polygon['coordinates'][0], srid=4326)
            poly_.transform(trans)

            poly_models.append(Poly(polygon=poly,geometry=geom,polygon_3857=poly_, **data))
        Poly.objects.bulk_create(poly_models, batch_size=10000)
