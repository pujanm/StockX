#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 17 14:57:32 2018

@author: pujan
"""
import requests
from bs4 import BeautifulSoup

page = requests.get("https://www.marketwatch.com/investing/index/djia/news")
soup = BeautifulSoup(page.content, 'html.parser')
t = soup.find_all('div', class_='headlinewrapper')
for i in t:
    print(i.get_text())