import os
import re
import subprocess
import threading
from os import makedirs
from os import path
from queue import Queue
import random
import requests
import base64
import json
from urllib.parse import urlencode
from hashlib import md5
from retrying import retry
import time
import pandas as pd

def get_header_and_cookie():
    h = {
    'authority': 'api.bilibili.com',
    'cache-control': 'max-age=0',
    'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
    'sec-ch-ua-mobile': '?0',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'none',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'accept-language': 'zh-CN,zh;q=0.9',
    }
    response = requests.get('https://www.bilibili.com', headers=h)
    ## print(response.text)
    cookies = dict(response.cookies)
    ## string cooikes into  cookie dict
    cookies_str = 'buvid3=DBC5D6D2-8513-71A2-4C85-1ACF01EBFC7990611infoc; b_nut=1714904790; b_lsid=9C94D44E_18F484A7798; _uuid=317A3977-97FA-16CC-6FDF-D9FC6106101B4B90939infoc; buvid_fp=5eae6ad8b65f5fde0bb9aa703ed20368; buvid4=81018F35-F818-9635-0541-AD78960F55AF91111-024050510-Hxur8FzLbEOET1cyY3Q1fw%3D%3D; enable_web_push=DISABLE; header_theme_version=undefined; home_feed_column=5; browser_resolution=2560-1294; CURRENT_FNVAL=4048; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MTUxNjQwMjEsImlhdCI6MTcxNDkwNDc2MSwicGx0IjotMX0.ZxF18kT7DOEqueqYxheVNG6hIQebpUllt7ObepBZn18; bili_ticket_expires=1715163961; SESSDATA=34dd3a7c%2C1730456879%2C52cca%2A52CjCyImbTWVhYw3tlwfsBWXqRY2nXqvCR0pI-dAy3tkBQB59z_4lNRRsknwrv04wWZPkSVmZ0Y3d0d3RReEFwYXZNSUF5b2pSSVBEd2xaQ1RZb2N3Tlp6Zi04bWtvVl9kcDZSMF85UEdCNWx3NzdzY3ptWWp4RW1wWTdqcExmcDJTMGExanVQRDBBIIEC; bili_jct=2928c92c37491073768cf0cc2d7571a8; DedeUserID=270658591; DedeUserID__ckMd5=85771fc837a19a55; sid=6b3lo703; x-bili-gaia-vtoken=fba60c7908694d3b9524c27700f022e5'
    cookies_list = cookies_str.split(" ")
    cookies = dict([item.split("=") for item in cookies_list])
    return h, cookies

def get_proxy():
    return {}