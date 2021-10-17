from django.core.management.base import BaseCommand
from service.models import Poly
import shapefile
import matplotlib as mpl
import matplotlib.cm as cm
from matplotlib.colors import rgb2hex
from django.contrib.gis.geos import Polygon
from tqdm import tqdm


def min_max(l, prop):
    l_ = [int(getattr(x.record,prop)) for x in l]
    return min(l_), max(l_)


class Command(BaseCommand):
    def handle(self, *args, **options):
        Poly.objects.all().delete()
        poly_models = []
        shape = shapefile.Reader("cells1/cells1.shp")
        shape_records = list(shape.shapeRecords())
        live_humans_2021_min_max = min_max(shape_records,'home')
        live_humans_2025_min_max = min_max(shape_records,'home_5year')
        live_humans_2030_min_max = min_max(shape_records,'home_5year')
        work_humans_min_max = min_max(shape_records,'job')
        transports_min_max = min_max(shape_records,'school_opt')
        for i in tqdm(shape_records):
            polygon = i.shape.__geo_interface__
            data = {
                'live_humans_2021': int(i.record.home),
                'live_humans_2025': int(i.record.home_5year),
                'live_humans_2030': int(i.record.home_5year),
                'work_humans': int(i.record.job),
                'transports': int(i.record.school_opt),
                'colors': {
                    'live_humans_2021': rgb2hex(cm.ScalarMappable(
                        norm=mpl.colors.Normalize(vmin=live_humans_2021_min_max[0], vmax=live_humans_2021_min_max[1]), cmap=cm.get_cmap('Oranges')
                    ).to_rgba(float(int(i.record.home)))),
                    'live_humans_2025': rgb2hex(cm.ScalarMappable(
                        norm=mpl.colors.Normalize(vmin=live_humans_2025_min_max[0], vmax=live_humans_2025_min_max[1]), cmap=cm.get_cmap('Oranges')
                    ).to_rgba(float(int(i.record.home_5year)))),
                    'live_humans_2030': rgb2hex(cm.ScalarMappable(
                        norm=mpl.colors.Normalize(vmin=live_humans_2030_min_max[0], vmax=live_humans_2030_min_max[1]), cmap=cm.get_cmap('Oranges')
                    ).to_rgba(float(int(i.record.home_5year)))),
                    'work_humans': rgb2hex(cm.ScalarMappable(
                        norm=mpl.colors.Normalize(vmin=work_humans_min_max[0], vmax=work_humans_min_max[1]), cmap=cm.get_cmap('Reds')
                    ).to_rgba(float(int(i.record.job)))),
                    'transports': rgb2hex(cm.ScalarMappable(
                        norm=mpl.colors.Normalize(vmin=transports_min_max[0], vmax=transports_min_max[1]), cmap=cm.get_cmap('Greens')
                    ).to_rgba(float(int(i.record.school_opt)))),
                },
            }
            poly = Poly(polygon=Polygon(polygon['coordinates'][0]), **data)
            poly_models.append(poly)
        Poly.objects.bulk_create(poly_models, batch_size=10000)
