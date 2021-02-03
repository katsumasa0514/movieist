from django.urls import path, include
from . import views
from django.views.generic import TemplateView


urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('movieselect', views.movieselect, name='movieselect'),
    path('overview/<movie_id>/', views.overview, name='overview'),
    path('overview/<movie_id>/review', views.review, name='review'),
    path('search', views.search, name='search'),
    path('accounts/', include('allauth.urls')),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('profile', views.profile, name='profile'),
    path('editprofile', views.editprofile, name='editprofile'),
    path('add_user', views.add_user, name='add_user'),
    path('reviewer/<int:user_id>', views.reviewer, name='reviewer'),
]
