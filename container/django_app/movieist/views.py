from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import FindForm, ReviewForm, ProfileForm, UserForm
from .models import Review, Profile, Follow
import requests
import json
from pprint import pprint
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.urls import reverse
from faker import Faker


token = 'eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI4YjY5ZjBmMGE0NDBiYjc1NmEwMjE0MjEwYzZlZDZjMiIsInN1YiI6IjVmY2FlMWNlMzk0YTg3MDA0MWQ2MDBlNiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.Y4BNiKaz70SktudaUey9MOHMAbhW6dEqCMqFO8RKN9Y'


class TMDB:
    def __init__(self, token):
        self.token = token
        self.headers_ = {'Authorization': f'Bearer {self.token}',
                         'Content-Type': 'application/json;charset=utf-8'}
        self.base_url_ = 'https://api.themoviedb.org/3/'
        self.img_base_url_ = 'https://image.tmdb.org/t/p/w500'

    def _json_by_get_request(self, url, params={}):
        res = requests.get(url, headers=self.headers_, params=params)
        return json.loads(res.text)

    def search_movies(self, query):
        params = {'query': query}
        url = f'{self.base_url_}search/movie?api_key=8b69f0f0a440bb756a0214210c6ed6c2&language=ja-JA&page=1&include_adult=false'
        return self._json_by_get_request(url, params)

    def get_movie(self, movie_id):
        url = f'{self.base_url_}movie/{movie_id}?api_key=8b69f0f0a440bb756a0214210c6ed6c2&language=ja&page=1&include_adult=false'
        return self._json_by_get_request(url)

    def get_movie_account_states(self, movie_id):
        url = f'{self.base_url_}movie/{movie_id}/account_states'
        return self._json_by_get_request(url)

    def get_movie_alternative_titles(self, movie_id, country=None):
        url = f'{self.base_url_}movie/{movie_id}/alternative_titles'
        return self._json_by_get_request(url)

    def get_movie_changes(self, movie_id, start_date=None, end_date=None):
        url = f'{self.base_url_}movie/{movie_id}'
        return self._json_by_get_request(url)

    def get_movie_credits(self, movie_id):
        url = f'{self.base_url_}movie/{movie_id}/credits'
        return self._json_by_get_request(url)

    def get_movie_external_ids(self, movie_id):
        url = f'{self.base_url_}movie/{movie_id}/external_ids'
        return self._json_by_get_request(url)

    def get_movie_images(self, movie_id, language=None):
        url = f'{self.base_url_}movie/{movie_id}/images?api_key=8b69f0f0a440bb756a0214210c6ed6c2&include_image_language=en'
        return self._json_by_get_request(url)

    def get_movie_keywords(self, movie_id):
        url = f'{self.base_url_}movie/{movie_id}/keywords'
        return self._json_by_get_request(url)

    def get_movie_release_dates(self, movie_id):
        url = f'{self.base_url_}movie/{movie_id}/release_dates'
        return self._json_by_get_request(url)

    def get_movie_videos(self, movie_id, language=None):
        url = f'{self.base_url_}movie/{movie_id}/videos'
        return self._json_by_get_request(url)

    def get_movie_translations(self, movie_id):
        url = f'{self.base_url_}movie/{movie_id}/translations'
        return self._json_by_get_request(url)

    def get_movie_recommendations(self, movie_id, language=None):
        url = f'{self.base_url_}movie/{movie_id}/recommendations'
        return self._json_by_get_request(url)

    def get_similar_movies(self, movie_id, language=None):
        url = f'{self.base_url_}movie/{movie_id}/similar'
        return self._json_by_get_request(url)

    def get_movie_reviews(self, movie_id, language=None):
        url = f'{self.base_url_}movie/{movie_id}/reviews'
        return self._json_by_get_request(url)

    def get_movie_lists(self, movie_id, language=None):
        url = f'{self.base_url_}movie/{movie_id}/lists'
        return self._json_by_get_request(url)

    def get_latest_movies(self, language=None):
        url = f'{self.base_url_}movie/latest'
        return self._json_by_get_request(url)

    def get_now_playing_movies(self, language=None, region=None):
        url = f'{self.base_url_}movie/now_playing'
        return self._json_by_get_request(url)

    def get_popular_movies(self, language=None, region=None):
        url = f'{self.base_url_}movie/popular'
        return self._json_by_get_request(url)

    def get_top_rated_movies(self, language=None, region=None):
        url = f'{self.base_url_}movie/top_rated'
        return self._json_by_get_request(url)

    def get_upcoming_movies(self, language=None, region=None):
        url = f'{self.base_url_}movie/upcoming'
        return self._json_by_get_request(url)

    def get_genre_movies(self):
        url = f'{self.base_url_}genre/movie/list?api_key=8b69f0f0a440bb756a0214210c6ed6c2&language=en'
        return self._json_by_get_request(url)


api = TMDB(token)


def homepage(request):
    params = {
        'title': 'Hello/homepage',
    }
    return render(request, 'movieist/homepage.html', params)


def search(request):

    genreList = api.get_genre_movies()
    print(genreList)

    params = {

    }

    return render(request, 'movieist/search.html', params)


def movieselect(request):
    if (request.method == 'POST'):
        msg = request.POST['find']
        res = api.search_movies(msg)
        res = res['results']

        params = {
            'res': res,
            'form': FindForm(request.POST),
        }
    else:
        params = {
            'form': FindForm(),
        }

    return render(request, 'movieist/movieselect.html', params)


def overview(request, movie_id):
    res = api.get_movie(movie_id)
    image = api.get_movie_images(movie_id)
    image = f"{api.img_base_url_}{image['posters'][0]['file_path']}"

    params = {
        'title': res['title'],
        'overview': res['overview'],
        'image': image,
        'form': FindForm(request.POST),
        'movie_id': movie_id,
    }

    return render(request, 'movieist/overview.html', params)


@login_required(login_url='/movieist/accounts/login/')
def review(request, movie_id):
    res = api.get_movie(movie_id)
    title = res['title']

    if (request.method == 'POST'):
        obj = Review()
        form = ReviewForm(request.POST, instance=obj)
        star = request.POST["star"]
        if form.is_valid():
            review = form.save(commit=False)
            review.owner = request.user
            review.movie_id = movie_id
            review.star = star
            review.save()
        return redirect(to='/movieist/profile')
    params = {
        'form': ReviewForm(),
        'title': title,
        'movie': movie_id
    }

    return render(request, 'movieist/review.html', params)


@login_required(login_url='/movieist/accounts/login/')
def profile(request):
    profileData = Profile.objects.filter(user=request.user.id)
    reviewDataOrg = Review.objects.filter(owner=request.user.id)
    reviewData = (add_movie_info(review) for review in reviewDataOrg)
    followingData = Follow.objects.filter(
        owner=request.user.id, following__isnull=False).values('following').count()
    followerData = Follow.objects.filter(
        owner=request.user.id, follower__isnull=False).values('follower').count()

    params = {
        'reviewDataOrg': reviewDataOrg,
        'profileData': profileData,
        'reviewData': reviewData,
        'followingData': followingData,
        'followerData': followerData,

    }

    return render(request, 'movieist/profile.html', params)


def add_movie_info(review):
    movie_info = api.get_movie(review.movie_id)
    image = api.get_movie_images(review.movie_id)

    review.title = movie_info['title']
    review.image_path = f"{api.img_base_url_}{image['posters'][0]['file_path']}"

    return review


def editprofile(request):
    profileData = Profile.objects.get(user=request.user.id)
    userData = User.objects.get(id=request.user.id)

    if (request.method == 'POST'):
        profileForm = ProfileForm(request.POST, request.FILES, instance=profileData)
        userForm = UserForm(request.POST, instance=userData)
        if profileForm.is_valid() and userForm.is_valid():
            userForm.save()
            profileForm.save()
            return redirect(to='/movieist/profile')

    params = {
        'profileForm': ProfileForm(instance=profileData),
        'userForm': UserForm(instance=userData),
    }

    return render(request, 'movieist/editprofile.html', params)


def reviewer(request, user_id):
    profileData = Profile.objects.filter(user=user_id)
    reviewDataOrg = Review.objects.filter(owner=user_id)

    reviewData = (add_movie_info(review) for review in reviewDataOrg)
    followingData = Follow.objects.filter(
        owner=user_id, following__isnull=False).values('following').count()
    followerData = Follow.objects.filter(
        owner=user_id, follower__isnull=False).values('follower').count()

    if (Follow.objects.filter(owner=request.user.id, following=user_id)):
        follow = "フォロー中"
        if (request.method == 'POST'):
            following = Follow.objects.filter(owner=request.user.id, following=user_id).delete()
            url = reverse('reviewer', kwargs={'user_id': user_id})
            return redirect(url)

    else:
        follow = "フォロー"
        if (request.method == 'POST'):
            following = Follow.objects.filter(owner=request.user.id).create(
                following=user_id, owner_id=request.user.id)
            following.save()
            url = reverse('reviewer', kwargs={'user_id': user_id})
            return redirect(url)

    params = {
        'reviewDataOrg': reviewDataOrg,
        'profileData': profileData,
        'reviewData': reviewData,
        'followingData': followingData,
        'followerData': followerData,
        'user_id': user_id,
        'follow': follow,
    }

    return render(request, 'movieist/reviewer.html', params)


def add_user(request):
    fakegen = Faker('ja_JP')
    fake_name = fakegen.name()
    fake_email = fakegen.email()
    user, created = User.objects.get_or_create(username=fake_name, email=fake_email)
    if created:
        user.set_password('nawa0514')
        user.save()
    return user, created
