
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
import common
## 代理
def get_proxy():
    return {}

# Md5 加密函数 32 返回32位的加密结果
def md5_use(text: str) -> str:
    result = md5(bytes(text, encoding="utf-8")).hexdigest()
    return result

def base64_encode(encoded_str, encode='utf-8'):
    """
    Base64解密函数
    :param encoded_str: Base64编码的字符串
    :return: 原始的二进制数据
    """
    encoded_str = encoded_str.encode(encode)
    encoded_str = base64.b64encode(encoded_str)
    encoded_str = encoded_str.decode()
    return encoded_str.strip('=')

def get_dm_cover_img_str(num=650):
    num = random.randrange(350, 651)
    ### sss = f'ANGLE (Intel Inc., Intel(R) Iris(TM) Plus Graphics {num}, OpenGL 4.1)Google Inc. (Intel Inc.)'
    ### sss = f'ANGLE (Apple, ANGLE Metal Renderer: Apple M3 Pro, Unspecified Version)Google Inc. (Apple)'
    sss = f'Intel(R) HD GraphicsIntel'
    dm_cover_img_str = base64_encode(sss)
    ## dm_cover_img_str = 'QU5HTEUgKEFwcGxlLCBBTkdMRSBNZXRhbCBSZW5kZXJlcjogQXBwbGUgTTMgUHJvLCBVbnNwZWNpZmllZCBWZXJzaW9uKUdvb2dsZSBJbmMuIChBcHBsZS'
    return dm_cover_img_str

print(get_dm_cover_img_str())

def get_dm_img_str():
    sss = f'WebGL 1.0 (OpenGL ES 2.0 Chromium)'
    ### /sss = f'WebGL 1.0'
    dm_img_str = base64_encode(sss)
    ## V2ViR0wgMS4wIChPcGVuR0wgRVMgMi4wIENocm9taXVtKQ
    return dm_img_str


def get_dm_list():
    dm_list = [{"x":1584,"y":1836,"z":0,"timestamp":99,"k":109,"type":0},{"x":4046,"y":3761,"z":25,"timestamp":222,"k":91,"type":0},{"x":4468,"y":3010,"z":56,"timestamp":51106,"k":122,"type":0},{"x":4502,"y":2910,"z":124,"timestamp":51207,"k":86,"type":0},{"x":4601,"y":3003,"z":218,"timestamp":51329,"k":66,"type":0},{"x":5156,"y":2699,"z":498,"timestamp":51429,"k":78,"type":0},{"x":5103,"y":2069,"z":244,"timestamp":51530,"k":72,"type":0},{"x":5698,"y":-65,"z":79,"timestamp":53289,"k":124,"type":0},{"x":5669,"y":-484,"z":415,"timestamp":53389,"k":113,"type":0},{"x":5903,"y":-250,"z":649,"timestamp":53490,"k":113,"type":0},{"x":6091,"y":-251,"z":783,"timestamp":53748,"k":108,"type":0},{"x":6401,"y":-690,"z":879,"timestamp":53902,"k":96,"type":0},{"x":6534,"y":-564,"z":1010,"timestamp":54009,"k":79,"type":0},{"x":5319,"y":-2331,"z":278,"timestamp":54109,"k":112,"type":0},{"x":5440,"y":-2598,"z":643,"timestamp":54209,"k":88,"type":0},{"x":5684,"y":-2462,"z":912,"timestamp":54310,"k":97,"type":0},{"x":6331,"y":-1899,"z":1535,"timestamp":54412,"k":80,"type":0},{"x":6191,"y":-1940,"z":1420,"timestamp":54512,"k":116,"type":0},{"x":5036,"y":-3107,"z":347,"timestamp":54612,"k":77,"type":0},{"x":4926,"y":-3229,"z":273,"timestamp":54713,"k":124,"type":0},{"x":6203,"y":-1961,"z":1669,"timestamp":54814,"k":69,"type":0},{"x":5203,"y":-3059,"z":894,"timestamp":54915,"k":106,"type":0},{"x":4934,"y":-3336,"z":626,"timestamp":55015,"k":82,"type":0},{"x":4488,"y":-3772,"z":173,"timestamp":55115,"k":99,"type":0},{"x":7028,"y":-1199,"z":2683,"timestamp":55215,"k":98,"type":0},{"x":6109,"y":-2105,"z":1748,"timestamp":55316,"k":110,"type":0},{"x":7299,"y":-915,"z":2938,"timestamp":55417,"k":126,"type":0},{"x":5179,"y":-3034,"z":815,"timestamp":55519,"k":77,"type":0},{"x":4445,"y":-3768,"z":81,"timestamp":55672,"k":63,"type":0}]
    dm_img_list = json.dumps(dm_list, separators=(',', ':'))
    return dm_img_list


def get_dm_img_inter():
    ## dm_img_inter = {"ds":[{"t":10,"c":"YmUtcGFnZXItaXRlbQ","p":[3939,81,4453],"s":[278,475,552]}],"wh":[5265,3620,63],"of":[1392,2094,357]}
    dm_img_inter = {"ds":[{"t":0,"c":"","p":[267,89,89],"s":[253,6548,106]}],"wh":[5220,3605,48],"of":[235,470,235]}
    return json.dumps(dm_img_inter, separators=(',', ':'))

def get_wts(if_new = True):
    if if_new:
        wts = str(int(time.time()))
    else:
        wts = 1714722176
    return wts

def get_video_audio():
    h, cookies = common.get_header_and_cookie()
    api = f'https://www.bilibili.com/video/BV1C1421o7bB'
    dm_img_list = [{"x":5741,"y":7072,"z":0,"timestamp":1028879,"k":110,"type":0},{"x":6018,"y":6511,"z":31,"timestamp":1030556,"k":84,"type":0}]
    dm_img_list = json.dumps(dm_img_list, separators=(',', ':'))
    # params = {  # 顺序很重要
    #     "dm_cover_img_str": get_dm_cover_img_str(),
    #     "dm_img_inter": get_dm_img_inter(),
    #     "dm_img_list": get_dm_list(),
    #     "dm_img_str": get_dm_img_str(),
    #     'keyword': keyword,
    #     "mid": userId,
    #     "order": "pubdate",
    #     "order_avoided": "true",
    #     "platform": "web",
    #     "pn": pcursor,
    #     "ps": "30",
    #     "tid": "0",
    #     "web_location": "1550101",
    #     "wts": get_wts(True),
    # }
    # w_rid = md5_use(urlencode(params) + 'ea1db124af3c7062474693fa704f4ff8')
    # params['w_rid'] = w_rid
    h.update({'referer': f'https://www.bilibili.com'})
    res = requests.get(
        api,
        headers=h,
        cookies=cookies,
        proxies=get_proxy(),
        timeout=15,
    )
    print(res.text)
    data_temp = 'BiliBili_临时'  # 视频与音频的零时保存文件
    title = 'test'
    json_data = re.findall('<script>window.__playinfo__=(.*?)</script>', res.text)[0]
    null = None
    false = False
    true = True
    json_data = eval(json_data)['data']['dash']
    audio_url = json_data['audio'][0]['backupUrl'][0]
    audio_place = path.join(data_temp, f'{title}.mp3')
    video_url = json_data['video'][0]['backupUrl'][0]
    video_place = path.join(data_temp, f'{title}.mp4')
    print(audio_url)
    print(video_url)
    return

if __name__ == "__main__":
    get_video_audio()