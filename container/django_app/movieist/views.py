from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import FindMovieForm, FindReviewerForm, ReviewForm, ProfileForm, UserForm
from .models import Review, Profile, Follow, Goodbad
import requests
import json
from pprint import pprint
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.urls import reverse
from faker import Faker
from faker.generator import random
import csv
from io import TextIOWrapper, StringIO
import random
import datetime
from django.db.models import Count
from django.contrib import messages
from .my_modules import goodbadModule, followModule


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
        url = f'{self.base_url_}genre/movie/list?api_key=8b69f0f0a440bb756a0214210c6ed6c2&language=ja'
        return self._json_by_get_request(url)


api = TMDB(token)


def homepage(request):
    one_week_ago = datetime.datetime.now() - datetime.timedelta(days=7)
    topicDataOrg = Review.objects.filter(
        datetime__range=[one_week_ago, datetime.datetime.now()]).order_by("-countgood")[:5]
    topicData = (add_review_info(review) for review in topicDataOrg)

    searchDataOrg = Review.objects.all().order_by("-countgood")[:5]
    searchData = (add_review_info(review) for review in searchDataOrg)

    rankingDataOrg = Follow.objects.values('owner').annotate(total=Count(
        'follower')).order_by('-total')[:5]
    rankingData = (add_ranking_info(request, ranking) for ranking in rankingDataOrg)

    if (request.POST.get('good') or request.POST.get('bad')):
        goodbadModule.goodbad(request)
        url = reverse('homepage')
        return redirect(url)

    if (request.POST.get('follow')):
        followModule.follow(request)
        url = reverse('homepage')
        return redirect(url)

    params = {
        'title': 'homepage',
        'topicData': topicData,
        'searchData': searchData,
        'rankingData': rankingData,
        'request.user.id': request.user.id,
    }
    return render(request, 'movieist/homepage.html', params)


def reviewer_ranking(request):
    rankingDataOrg = Follow.objects.values('owner').annotate(total=Count(
        'follower')).order_by('-total')[:15]
    rankingData = (add_ranking_info(request, ranking) for ranking in rankingDataOrg)

    if (request.POST.get('follow')):
        followModule.follow(request)
        url = reverse('reviewer_ranking')
        return redirect(url)

    params = {
        'rankingData': rankingData,
        'request.user.id': request.user.id,
    }
    return render(request, 'movieist/reviewer_ranking.html', params)


def add_ranking_info(request, ranking):
    ranking['profile'] = Profile.objects.filter(user=ranking['owner'])

    ranking['countFollowing'] = Follow.objects.filter(
        owner=ranking['owner'], following__isnull=False).values('following').count()
    ranking['countFollower'] = Follow.objects.filter(
        owner=ranking['owner'], follower__isnull=False).values('follower').count()

    reviewedDataOrg = Review.objects.filter(owner=ranking['owner'])
    ranking['reviewed'] = (add_review_info(review) for review in reviewedDataOrg)

    if (Follow.objects.filter(owner=request.user.id, following=ranking['owner'])):
        ranking['button'] = "フォロー中"
    else:
        ranking['button'] = "フォロー"

    return ranking


def search(request, genre):
    if (request.POST.get('good') or request.POST.get('bad')):
        goodbadModule.goodbad(request)
        url = reverse('search', kwargs={'genre': genre})
        return redirect(url)

    if (genre == "allgenre"):
        actionDataOrg = Review.objects.filter(genre="アクション").order_by('-countgood')[:5]
        actionData = (add_review_info(review) for review in actionDataOrg)

        SFDataOrg = Review.objects.filter(genre="サイエンスフィクション").order_by('-countgood')[:5]
        SFData = (add_review_info(review) for review in SFDataOrg)

        mysteryDataOrg = Review.objects.filter(genre="謎").order_by('-countgood')[:5]
        mysteryData = (add_review_info(review) for review in mysteryDataOrg)

        dramaDataOrg = Review.objects.filter(genre="ドラマ").order_by('-countgood')[:5]
        dramaData = (add_review_info(review) for review in dramaDataOrg)

        comedyDataOrg = Review.objects.filter(genre="コメディ").order_by('-countgood')[:5]
        comedyData = (add_review_info(review) for review in comedyDataOrg)

        fantasyDataOrg = Review.objects.filter(genre="ファンタジー").order_by('-countgood')[:5]
        fantasyData = (add_review_info(review) for review in fantasyDataOrg)

        animeDataOrg = Review.objects.filter(genre="アニメーション").order_by('-countgood')[:5]
        animeData = (add_review_info(review) for review in animeDataOrg)

        romanceDataOrg = Review.objects.filter(genre="ロマンス").order_by('-countgood')[:5]
        romanceData = (add_review_info(review) for review in romanceDataOrg)

        adventureDataOrg = Review.objects.filter(genre="アドベンチャー").order_by('-countgood')[:5]
        adventureData = (add_review_info(review) for review in adventureDataOrg)

        crimeDataOrg = Review.objects.filter(genre="犯罪").order_by('-countgood')[:5]
        crimeData = (add_review_info(review) for review in crimeDataOrg)

        horrorDataOrg = Review.objects.filter(genre="ホラー").order_by('-countgood')[:5]
        horrorData = (add_review_info(review) for review in horrorDataOrg)

        documentaryDataOrg = Review.objects.filter(genre="ドキュメンタリー").order_by('-countgood')[:5]
        documentaryData = (add_review_info(review) for review in documentaryDataOrg)

    elif (genre == "action"):
        genreDataOrg = Review.objects.filter(genre="アクション").order_by('-countgood')[:10]
        genreData = (add_review_info(review) for review in genreDataOrg)

        params = {
            'genreData': genreData,
            'genrename': 'アクション',
            'genre': genre,
        }

        return render(request, 'movieist/searchgenre.html', params)

    elif (genre == "sf"):
        genreDataOrg = Review.objects.filter(genre="サイエンスフィクション").order_by('-countgood')[:10]
        genreData = (add_review_info(review) for review in genreDataOrg)

        params = {
            'genreData': genreData,
            'genrename': 'SF',
            'genre': genre,
        }

        return render(request, 'movieist/searchgenre.html', params)

    elif (genre == "mystery"):
        genreDataOrg = Review.objects.filter(genre="謎").order_by('-countgood')[:10]
        genreData = (add_review_info(review) for review in genreDataOrg)

        params = {
            'genreData': genreData,
            'genrename': 'サスペンス',
            'genre': genre,
        }

        return render(request, 'movieist/searchgenre.html', params)

    elif (genre == "drama"):
        genreDataOrg = Review.objects.filter(genre="ドラマ").order_by('-countgood')[:10]
        genreData = (add_review_info(review) for review in genreDataOrg)

        params = {
            'genreData': genreData,
            'genrename': 'ドラマ',
            'genre': genre,
        }

        return render(request, 'movieist/searchgenre.html', params)

    elif (genre == "comedy"):
        genreDataOrg = Review.objects.filter(genre="コメディ").order_by('-countgood')[:10]
        genreData = (add_review_info(review) for review in genreDataOrg)

        params = {
            'genreData': genreData,
            'genrename': 'コメディ',
            'genre': genre,
        }

        return render(request, 'movieist/searchgenre.html', params)

    elif (genre == "anime"):
        genreDataOrg = Review.objects.filter(genre="アニメーション").order_by('-countgood')[:10]
        genreData = (add_review_info(review) for review in genreDataOrg)

        params = {
            'genreData': genreData,
            'genrename': 'アニメ',
            'genre': genre,
        }

        return render(request, 'movieist/searchgenre.html', params)

    elif (genre == "romance"):
        genreDataOrg = Review.objects.filter(genre="ロマンス").order_by('-countgood')[:10]
        genreData = (add_review_info(review) for review in genreDataOrg)

        params = {
            'genreData': genreData,
            'genrename': 'ロマンス',
            'genre': genre,
        }

        return render(request, 'movieist/searchgenre.html', params)

    elif (genre == "adventure"):
        genreDataOrg = Review.objects.filter(genre="アドベンチャー").order_by('-countgood')[:10]
        genreData = (add_review_info(review) for review in genreDataOrg)

        params = {
            'genreData': genreData,
            'genrename': 'アドベンチャー',
            'genre': genre,
        }

        return render(request, 'movieist/searchgenre.html', params)

    elif (genre == "crime"):
        genreDataOrg = Review.objects.filter(genre="犯罪").order_by('-countgood')[:10]
        genreData = (add_review_info(review) for review in genreDataOrg)

        params = {
            'genreData': genreData,
            'genrename': 'クライム',
            'genre': genre,
        }

        return render(request, 'movieist/searchgenre.html', params)

    elif (genre == "horror"):
        genreDataOrg = Review.objects.filter(genre="ホラー").order_by('-countgood')[:10]
        genreData = (add_review_info(review) for review in genreDataOrg)

        params = {
            'genreData': genreData,
            'genrename': 'ホラー',
            'genre': genre,
        }

        return render(request, 'movieist/searchgenre.html', params)

    elif (genre == "documentary"):
        genreDataOrg = Review.objects.filter(genre="ドキュメンタリー").order_by('-countgood')[:10]
        genreData = (add_review_info(review) for review in genreDataOrg)

        params = {
            'genreData': genreData,
            'genrename': 'ドキュメンタリー',
            'genre': genre,
        }

        return render(request, 'movieist/searchgenre.html', params)

    elif (genre == "fantasy"):
        genreDataOrg = Review.objects.filter(genre="ファンタジー").order_by('-countgood')[:10]
        genreData = (add_review_info(review) for review in genreDataOrg)

        params = {
            'genreData': genreData,
            'genrename': 'ファンタジー',
            'genre': genre,
        }

        return render(request, 'movieist/searchgenre.html', params)

    elif (genre == "topic"):
        one_week_ago = datetime.datetime.now() - datetime.timedelta(days=7)
        topicDataOrg = Review.objects.filter(
            datetime__range=[one_week_ago, datetime.datetime.now()]).order_by("-countgood")[:10]
        topicData = (add_review_info(review) for review in topicDataOrg)

        params = {
            'genreData': topicData,
            'genrename': '注目の投稿',
            'genre': genre,
        }

        return render(request, 'movieist/searchgenre.html', params)

    params = {
        'actionData': actionData,
        'SFData': SFData,
        'mysteryData': mysteryData,
        'dramaData': dramaData,
        'comedyData': comedyData,
        'fantasyData': fantasyData,
        'animeData': animeData,
        'romanceData': romanceData,
        'adventureData': adventureData,
        'crimeData': crimeData,
        'horrorData': horrorData,
        'documentaryData': documentaryData,
        'genre': genre,
    }

    return render(request, 'movieist/search.html', params)


def add_review_info(review):
    movie_info = api.get_movie(review.movie_id)
    image = api.get_movie_images(review.movie_id)

    review.title = movie_info['title']
    try:
        review.image_path = f"{api.img_base_url_}{image['posters'][0]['file_path']}"
    except IndexError:
        review.image_path = '/media/documents/noimage.jpg'

    review.profile = Profile.objects.filter(user=review.owner)

    return review


def reviewerselect(request):
    if (request.method == 'POST'):
        profiles = Profile.objects.filter(user__username__icontains=request.POST['find'])[:10]
        params = {
            'profiles': profiles,
            'form': FindReviewerForm(request.POST),
        }
    else:
        params = {
            'form': FindReviewerForm(),
        }

    return render(request, 'movieist/reviewerselect.html', params)


def movieselect(request):
    if (request.method == 'POST'):
        msg = request.POST['find']
        res = api.search_movies(msg)
        res = res['results']

        params = {
            'res': res,
            'form': FindMovieForm(request.POST),
        }
    else:
        params = {
            'form': FindMovieForm(),
        }

    return render(request, 'movieist/movieselect.html', params)


def overview(request, movie_id):
    res = api.get_movie(movie_id)
    image = api.get_movie_images(movie_id)
    image = f"{api.img_base_url_}{image['posters'][0]['file_path']}"
    reviewDataOrg = Review.objects.filter(movie_id=movie_id)[:10]
    reviewData = (add_review_info(review) for review in reviewDataOrg)

    if (request.POST.get('good') or request.POST.get('bad')):
        goodbadModule.goodbad(request)
        url = reverse('overview', kwargs={'movie_id': movie_id})
        return redirect(url)

    params = {
        'title': res['title'],
        'overview': res['overview'],
        'image': image,
        'form': FindMovieForm(request.POST),
        'movie_id': movie_id,
        'reviewDataOrg': reviewDataOrg,
        'reviewData': reviewData,
    }

    return render(request, 'movieist/overview.html', params)


@login_required(login_url='/movieist/accounts/login/')
def review(request, movie_id):
    res = api.get_movie(movie_id)
    title = res['title']
    genre_1 = res['genres'][0]['name']

    if (request.method == 'POST'):
        obj = Review()
        form = ReviewForm(request.POST, instance=obj)
        star = request.POST["star"]
        if form.is_valid():
            review = form.save(commit=False)
            review.owner = request.user
            review.movie_id = movie_id
            review.star = star
            review.genre = genre_1
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

    if (request.POST.get('good') or request.POST.get('bad')):
        goodbadModule.goodbad(request)
        url = reverse('profile')
        return redirect(url)

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

        else:
            messages.error(request, '入力に誤りがあります。')

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

    if (request.POST.get('good') or request.POST.get('bad')):
        goodbadModule.goodbad(request)
        url = reverse('reviewer', kwargs={'user_id': user_id})
        return redirect(url)

    if (Follow.objects.filter(owner=request.user.id, following=user_id)):
        follow = "フォロー中"
        if (request.method == 'POST'):
            # 自分のフォロー中から相手を削除
            Follow.objects.filter(owner=request.user.id, following=user_id).delete()
            # 相手のフォロワーから自分を削除
            Follow.objects.filter(owner=user_id, follower=request.user.id).delete()
            url = reverse('reviewer', kwargs={'user_id': user_id})
            return redirect(url)

    else:
        follow = "フォロー"
        if (request.method == 'POST'):
            createFollowing = Follow.objects.filter(owner=request.user.id).create(
                following=user_id, owner_id=request.user.id)
            createFollowing.save()
            createFollower = Follow.objects.filter(owner=user_id).create(
                follower=request.user.id, owner_id=user_id)
            createFollower.save()
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
        'request.user.id': request.user.id,
    }

    return render(request, 'movieist/reviewer.html', params)


def following(request, user_id):
    followingDataOrg = Follow.objects.filter(owner=user_id, following__isnull=False)
    followingData = (following_info(follow, request) for follow in followingDataOrg)

    if (request.POST.get('follow')):
        followModule.follow(request)
        url = reverse('following', kwargs={'user_id': user_id})
        return redirect(url)

    params = {
        'followingData': followingData,
        'user_id': user_id,
        'request.user.id': request.user.id,
    }

    return render(request, 'movieist/following.html', params)


def following_info(follow, request):
    profileData = Profile.objects.filter(user=follow.following)
    follow.profile = profileData

    if (Follow.objects.filter(owner=request.user.id, following=follow.following)):
        follow.button = "フォロー中"
    else:
        follow.button = "フォロー"

    return follow


def follower(request, user_id):
    followerDataOrg = Follow.objects.filter(owner=user_id, follower__isnull=False)
    followerData = (follower_info(follow, request) for follow in followerDataOrg)

    if (request.POST.get('follow')):
        followModule.follow(request)
        url = reverse('follower', kwargs={'user_id': user_id})
        return redirect(url)

    params = {
        'followerData': followerData,
        'user_id': user_id,
        'request.user.id': request.user.id,
    }

    return render(request, 'movieist/follower.html', params)


def follower_info(follow, request):
    profileData = Profile.objects.filter(user=follow.follower)
    follow.profile = profileData

    if (Follow.objects.filter(owner=request.user.id, following=follow.follower)):
        follow.button = "フォロー中"
    else:
        follow.button = "フォロー"

    return follow


def add_user(request):
    fake = Faker('ja_JP')
    fake.random.seed(4321)

    names = set()
    emails = set()
    while len(names) < 1000:

        len(emails)
        names.add(fake.name())
        emails.add(fake.email())

    for (name, email) in zip(names, emails):
        user, created = User.objects.get_or_create(username=name, email=email)
        if created:
            user.set_password('nawa0514')
            user.save()
    return user, created


def add_csv(request):
    if 'csv' in request.FILES:
        form_data = TextIOWrapper(request.FILES['csv'].file, encoding='utf-8')
        csv_file = csv.reader(form_data)
        for line in csv_file:
            movie_info = api.get_movie(line[0])
            genres = movie_info['genres'][0]['name']
            number = random.randrange(1, 1000)
            numbers = User.objects.get(id=number)
            review = Review()
            review.owner = numbers
            review.movie_id = line[0]
            review.commentTitle = line[2]
            review.comment = line[3]
            review.star = line[4]
            review.genre = genres
            review.save()

        return render(request, 'movieist/add_csv.html')

    else:
        return render(request, 'movieist/add_csv.html')


def add_follow(request):
    for i in range(1, 1000):
        number_1 = random.randrange(2, 10)
        for er in range(1, number_1):
            user = User.objects.get(id=i)
            follow = Follow()
            follow.owner = user
            number_2 = random.randrange(1, 1000)
            follow.follower = number_2
            follow.save()

        number_3 = random.randrange(2, 10)
        for er in range(1, number_3):
            user = User.objects.get(id=i)
            follow = Follow()
            follow.owner = user
            number_4 = random.randrange(1, 1000)
            follow.following = number_4
            follow.save()


def add_goodbad(request):
    for i in range(1, 778):
        number_1 = random.randrange(2, 10)
        for g in range(1, number_1):
            review_id = Review.objects.get(id=i)
            goodbad = Goodbad()
            goodbad.owner = review_id
            number_2 = random.randrange(1, 1000)
            goodbad.good = number_2
            goodbad.save()
            review_id.countgood += 1
            review_id.save()
        number_3 = random.randrange(2, 10)
        for b in range(1, number_3):
            review_id = Review.objects.get(id=i)
            goodbad = Goodbad()
            goodbad.owner = review_id
            number_4 = random.randrange(1, 1000)
            goodbad.bad = number_4
            goodbad.save()
            review_id.countbad += 1
            review_id.save()
