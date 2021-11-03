from django.core.management.base import BaseCommand
from service.models import Poly
import shapefile
import matplotlib as mpl
import matplotlib.cm as cm
from matplotlib.colors import rgb2hex
from django.contrib.gis.geos import Polygon
from tqdm import tqdm
from django.conf import settings


def min_max(l, prop):
    l_ = [int(getattr(x.record,prop)) for x in l]
    return min(l_), max(l_)


def get_norm(l, prop):
    min_, max_ = min_max(l,prop)
    return mpl.colors.Normalize(vmin=min_, vmax=max_)


def min_max_double(l, prop1, prop2):
    l1 = [int(getattr(x.record,prop1)) for x in l]
    l2 = [int(getattr(x.record,prop2)) for x in l]
    return min(min(l1),min(l2)), max(max(l1), max(l2))


def get_norm_double(l, prop1, prop2):
    min_, max_ = min_max_double(l,prop1, prop2)
    return mpl.colors.Normalize(vmin=min_, vmax=max_)


class Command(BaseCommand):
    def handle(self, *args, **options):
        CMAPS = settings.COLORMAPS_DICT
        Poly.objects.all().delete()
        poly_models = []
        shape = shapefile.Reader("cells_final/cells1.shp")
        shape_records = list(shape.shapeRecords())
        live_humans_norm = get_norm_double(shape_records,'home', 'home_5year')
        potrb_norm = get_norm_double(shape_records,'potreb', 'potreb_5ye')
        optima_norm = get_norm(shape_records,'new_school')
        work_humans_norm = get_norm(shape_records,'job')
        for i in tqdm(shape_records):
            polygon = i.shape.__geo_interface__
            data = {
                'live_humans_2021': int(i.record.home),
                'live_humans_2025': int(i.record.home_5year),

                'potreb_2021': int(i.record.potreb),
                'potreb_2025': int(i.record.potreb_5ye),

                'optima': int(i.record.new_school),
                'school': int(i.record.in_schoo_1),
                'work_humans': int(i.record.job),
                'colors': {},
                # 'colors': {
                #     'live_humans_2021': rgb2hex(cm.ScalarMappable(
                #         norm=live_humans_norm, cmap=cm.get_cmap(CMAPS['live_humans_2021'])
                #     ).to_rgba(float(int(i.record.home)))),
                #     'live_humans_2025': rgb2hex(cm.ScalarMappable(
                #         norm=live_humans_norm, cmap=cm.get_cmap(CMAPS['live_humans_2025'])
                #     ).to_rgba(float(int(i.record.home_5year)))),
                #
                #
                #     'potreb_2021': rgb2hex(cm.ScalarMappable(
                #         norm=potrb_norm, cmap=cm.get_cmap(CMAPS['potreb_2021'])
                #     ).to_rgba(float(int(i.record.potreb)))),
                #     'potreb_2025': rgb2hex(cm.ScalarMappable(
                #         norm=potrb_norm, cmap=cm.get_cmap(CMAPS['potreb_2025'])
                #     ).to_rgba(float(int(i.record.potreb_5ye)))),
                #
                #
                #     'work_humans': rgb2hex(cm.ScalarMappable(
                #         norm=work_humans_norm, cmap=cm.get_cmap(CMAPS['work_humans'])
                #     ).to_rgba(float(int(i.record.job)))),
                #     'optima': rgb2hex(cm.ScalarMappable(
                #         norm=optima_norm, cmap=cm.get_cmap(CMAPS['optima'])
                #     ).to_rgba(float(int(i.record.new_school)))),
                # },
            }
            geom = Polygon(polygon['coordinates'][0], srid=4326)
            poly_models.append(Poly(geometry=geom, **data))
        Poly.objects.bulk_create(poly_models, batch_size=10000)
