from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium import webdriver
from datetime import datetime
import requests
import random
import sys
import time
PURPLE = '\033[35m'
RED = '\033[31m'
CYAN = '\033[36m'
OKBLUE = '\033[94m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
UNDERLINE = '\033[4m'

# Selectタグが扱えるエレメントに変化させる為の関数を呼び出す

# ターゲットとなるECサイト・商品一覧１ページ目のURL
URL = 'https://shop.faber-hobby.jp/products/list.php?name=SALE1&disp_number=52&isStock=yes'

f = open('out.csv', 'w')
b = webdriver.Chrome('./chromedriver')
b.get(URL)
time.sleep(1)
flag = 0
while True:
    classes = b.find_elements_by_class_name('itemname')
    print(len(classes))
    for i in list(classes):
        a = i.find_elements_by_css_selector("a")
        name = str(a[0].text.replace(',', ''))
        url = str(a[0].get_attribute("href"))
        print(OKBLUE+UNDERLINE+url+ENDC)
        print(name)
        f.write(name+','+url+'\n')

    q = b.find_element_by_class_name('navi')
    a = q.find_elements_by_css_selector("a")
    for i in a:
        name = str(i.text)
        url = str(i.get_attribute("href"))
        if name == '次へ>>':
            flag = 1
            i.click()
        else:
            flag = 0
    if flag == 0:
        break
    else:
        time.sleep(1)
        continue
f.close()
