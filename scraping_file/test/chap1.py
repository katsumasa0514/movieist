import requests
from bs4 import BeautifulSoup

load_url = "https://movies.yahoo.co.jp/review/"
html = requests.get(load_url)
soup = BeautifulSoup(html.content, "html.parser")

for element in soup.find_all(class_="color-sub"):
    print(element.text)
