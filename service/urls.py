from django.urls import path
from django.conf.urls import url
from rest_framework import routers
from rest_framework.authtoken import views as rf_views
from . import views

app_name = 'HACK2'
router = routers.DefaultRouter()

router.register('poly_new', views.PolyNewViewSet, basename='poly_new')
router.register('schools', views.SchoolViewSet, basename='schools')

urlpatterns = router.urls

urlpatterns += [
]
