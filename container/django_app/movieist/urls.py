from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('overview', views.overview, name='overview'),
    path('search', views.search, name='search'),
]
