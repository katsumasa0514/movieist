import urllib.request
import urllib.error
from bs4 import BeautifulSoup
from time import sleep
import requests
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import asyncio
import gspread_asyncio
from google.oauth2.service_account import Credentials
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import re

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


def get_creds():
    # To obtain a service account JSON file, follow these steps:
    # https://gspread.readthedocs.io/en/latest/oauth2.html#for-bots-using-service-account
    creds = Credentials.from_service_account_file(
        "/Users/nawakatsushou/Documents/コード/my_app_Movieist/movieist-b7c9917e1dde.json")
    scoped = creds.with_scopes([
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ])
    return scoped

# Create an AsyncioGspreadClientManager object which
# will give us access to the Spreadsheet API.


agcm = gspread_asyncio.AsyncioGspreadClientManager(get_creds)

# Here's an example of how you use the API:


async def example(agcm):
    N = 100  # ページネートの数
    BT = 2
    add_num = 0

    agc = await agcm.authorize()

    ss = await agc.open('スクレイピング_映画')

    for i in range(1, N + 1):
        sleep(BT)
        zero_ws = await ss.get_worksheet(0)

        url = 'https://www.themoviedb.org/movie?page=' + str(i) + '&language=ja'

        html = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(html, 'html.parser')
        div = soup.findAll('div', class_='options')

        for index, movie_id in enumerate(div):
            num = index + 1 + add_num
            data = movie_id.get('data-id')
            res = api.get_movie(data)
            title = res["title"]

            try:
                options = Options()
                options.add_argument('--disable-gpu')
                options.add_argument('--disable-extensions')
                options.add_argument('--proxy-server="direct://"')
                options.add_argument('--proxy-bypass-list=*')
                options.add_argument('--start-maximized')

                DRIVER_PATH = '/Users/nawakatsushou/Documents/コード/my_app_Movieist/Selenium/chromedriver'

                driver = webdriver.Chrome(executable_path=DRIVER_PATH, chrome_options=options)

                driver.implicitly_wait(10)

                url = 'https://eiga.com/search/'
                driver.get(url)

                selector = '#document_2773744664 > main > div > div > div.site-search > form > input[type=text]'
                element = WebDriverWait(driver, 30).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, selector)))
                element.send_keys(title)

                element.send_keys(Keys.ENTER)

                html = driver.page_source
                soup = BeautifulSoup(html, 'html.parser')

                selector = '#rslt-movie > ul > li:nth-child(1) > a > p'
                titlecom = soup.select_one(selector).get_text()

                titletmdb = re.sub(r"[－・／：　/: ]", "", title)
                titlecom = re.sub(r"[－・／：　/: ]", "", titlecom)

                if (titletmdb == titlecom):
                    await zero_ws.update_acell('A' + str(num), data)
                    await zero_ws.update_acell('B' + str(num), title)

                    selector = '#rslt-movie > ul > li:nth-child(1) > a'
                    element = WebDriverWait(driver, 30).until(
                        EC.visibility_of_element_located((By.CSS_SELECTOR, selector)))
                    driver.execute_script('arguments[0].click();', element)

                    html = driver.page_source
                    soup = BeautifulSoup(html, 'html.parser')

                    selector = '.review-title > a '
                    comment_title = soup.select_one(selector).get_text()

                    await zero_ws.update_acell('D' + str(num), comment_title)

                    selector = '.txt-block > p '
                    comment = soup.select_one(selector).get_text()

                    await zero_ws.update_acell('E' + str(num), comment)

                    selector = '.review-title > span '
                    star = soup.select_one(selector).get_text()

                    await zero_ws.update_acell('F' + str(num), star)

            except:
                print('検索失敗')

            driver.quit()

        add_num = int(num)

asyncio.run(example(agcm), debug=True)
