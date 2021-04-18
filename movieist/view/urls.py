from django.urls import path, include
from . import views
from django.views.generic import TemplateView


urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('movieselect', views.movieselect, name='movieselect'),
    path('overview/<int:movie_id>/', views.overview, name='overview'),
    path('overview/<int:movie_id>/review', views.review, name='review'),
    path('search/<str:genre>', views.search, name='search'),
    path('profile', views.profile, name='profile'),
    path('editprofile', views.editprofile, name='editprofile'),
    path('reviewer/<int:user_id>', views.reviewer, name='reviewer'),
    path('following/<int:user_id>', views.following, name='following'),
    path('follower/<int:user_id>', views.follower, name='follower'),
    path('reviewer_ranking', views.reviewer_ranking, name='reviewer_ranking'),
    path('reviewerselect', views.reviewerselect, name='reviewerselect'),
    path('accounts/', include('allauth.urls')),
]
