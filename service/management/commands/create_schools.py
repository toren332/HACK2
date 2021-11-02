from django.core.management.base import BaseCommand
from service.models import School
from django.contrib.gis.geos import Point
import pandas as pd
from tqdm import tqdm


class Command(BaseCommand):
    def handle(self, *args, **options):
        School.objects.all().delete()
        school_models = []
        df = pd.read_excel('schools_final.xlsx')
        df_rows = list(df.iterrows())
        for id_, i in tqdm(df_rows):
            data = i.to_dict()
            lat = data.pop('latitude')
            lng = data.pop('longitude')
            new_data = {
                'name': data.get('name'),
                'address': data.get('address'),
                'rating': data.get('ratingPlace'),
                'chief_name': data.get('ChiefName'),
                'web_site': data.get('WebSite'),
                'phone': data.get('PublicPhone'),
                'email': data.get('Email'),
                'pupils_cnt': data.get('pupils_cnt'),
                'nagruzka': int(data.get('nagruzka')*100),
                'nagruzka_2025year': int(data.get('nagruzka_5year')*100),
            }
            school = School(point=Point((lng, lat), srid=4326), **new_data)
            school_models.append(school)
        School.objects.bulk_create(school_models, batch_size=10000)
