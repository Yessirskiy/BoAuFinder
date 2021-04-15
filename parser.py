# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup

engine_url = 'https://ilibrary.ru/'
book = 'Душечка'

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36'
    }

response = requests.get(engine_url, headers=HEADERS)

def find_input():
    bs = BeautifulSoup(response.text, 'html.parser')
    search = bs.find_all(id="qi1")
    print(search)
    r = requests.post(url, data )

find_input()

