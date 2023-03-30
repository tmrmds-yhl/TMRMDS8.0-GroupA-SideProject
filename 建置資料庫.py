import requests
import json
import time
import numpy as np
import os
from bs4 import BeautifulSoup
import pandas as pd
import datetime
from api爬蟲 import course_searching, collect_comments

#https://api.hahow.in/api/products/search?groups=more-language&limit=100&page=0

url = f'https://api.hahow.in/api/groups'

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                            'AppleWebKit/537.36 (KHTML, like Gecko) '
                            'Chrome/59.0.3071.115 Safari/537.36'}

resp_categories = requests.get(url, headers=headers).json()

for main in range(len(resp_categories)):
    for sub in range(len(resp_categories[main]['subGroups'])):
        course_searching(resp_categories[main]['subGroups'][sub]['title'])