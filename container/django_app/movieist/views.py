from django.shortcuts import render
from django.http import HttpResponse
from .forms import FindForm
from .forms import ReviewForm
from .models import Review, Profile, Follow
import requests
import json
from pprint import pprint
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth.models import User

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
    if (request.method == 'POST'):
        msg = request.POST['find']
        dataFind = Search.object.filter(title__icontains=msg).order_by('good')[
            int(list[0]): int(list[10])]
        form = FindForm(request.POST)

    else:
        genreList = api.get_genre_movies()
        for i in genreList:
            dataFind = Search.object.filter(genres=i['genres'][0]['name']).order_by('good')[
                int(list[0]): int(list[3])]
        form = FindForm()
    params = {
        'data': dataFind,
        'form': form,
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
    review = ("レビュー>")

    params = {
        'title': res['title'],
        'overview': res['overview'],
        'image': image,
        'form': FindForm(request.POST),
        'review': review,
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
        if form.is_valid():
            review = form.save(commit=False)
            review.owner = request.user
            review.movie_id = movie_id
            review.save()
        return redirect(to='/movieist/movieselect')
    params = {
        'form': ReviewForm(),
        'title': title,
        'movie': movie_id
    }

    return render(request, 'movieist/review.vue', params)


@login_required(login_url='/movieist/accounts/login/')
def profile(request):
    reviewData = Review.objects.filter(owner=request.user.id)
    params = {
        'reviewData': reviewData,
    }

    return render(request, 'movieist/profile.html', params)
