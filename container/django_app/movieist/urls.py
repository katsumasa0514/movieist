from django.urls import path, include
from . import views
from django.views.generic import TemplateView


urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('overview', views.overview, name='overview'),
    path('search', views.search, name='search'),
    path('accounts/', include('allauth.urls')),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
]
