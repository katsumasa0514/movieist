from django.urls import path, include
from . import views
from django.views.generic import TemplateView


urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('movieselect', views.movieselect, name='movieselect'),
    path('overview/<int:movie_id>/', views.overview, name='overview'),
    path('overview/<int:movie_id>/review', views.review, name='review'),
    path('search/<str:genre>', views.search, name='search'),
    path('accounts/', include('allauth.urls')),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('profile', views.profile, name='profile'),
    path('editprofile', views.editprofile, name='editprofile'),
    path('reviewer/<int:user_id>', views.reviewer, name='reviewer'),
    path('following/<int:user_id>', views.following, name='following'),
    path('follower/<int:user_id>', views.follower, name='follower'),
    path('add_user', views.add_user, name='add_user'),

    path('add_csv', views.add_csv, name='add_csv'),
    path('add_follow', views.add_follow, name='add_follow'),
    path('add_goodbad', views.add_goodbad, name='add_goodbad'),
]
