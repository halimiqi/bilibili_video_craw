
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

# 通过时间字符形式 返回时长格式
def unify_duration_format(duar_str_or_s: str):
    """
    01:11 -> 71,'00:01:11'
    00:01:11 -> 71,'00:01:11'
    :param duar_str: '01:11' or '00:01:11'
    :return:  71, '00:01:11'
    """
    error = 0, ''

    def hms(m: int, s: int, h=0):
        if s >= 60:
            m += int(s / 60)
            s = s % 60  #
        if m >= 60:
            h += int(m / 60)
            m = m % 60
        return h * 60 * 60 + m * 60 + s, str(h).zfill(2) + ':' + str(m).zfill(2) + ':' + str(s).zfill(2)

    try:
        s = int(duar_str_or_s)
    except:
        pass
    else:
        return hms(m=s % 3600 // 60, s=s % 60, h=s // 3600)
    try:
        if duar_str_or_s:
            duar_list = duar_str_or_s.split(':')
            if len(duar_list) == 2:
                return hms(m=int(duar_list[0]), s=int(duar_list[1]))
            elif len(duar_list) == 3:
                return hms(m=int(duar_list[1]), s=int(duar_list[2]), h=int(duar_list[0]))
            else:
                return error
        else:
            return error
    except Exception as e:
        return error

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
    # dm_cover_img_str = 'QU5HTEUgKEFwcGxlLCBBTkdMRSBNZXRhbCBSZW5kZXJlcjogQXBwbGUgTTMgUHJvLCBVbnNwZWNpZmllZCBWZXJzaW9uKUdvb2dsZSBJbmMuIChBcHBsZS'
    return dm_cover_img_str

print(get_dm_cover_img_str())

def get_dm_img_str():
    sss = f'WebGL 1.0 (OpenGL ES 2.0 Chromium)'
    ### /sss = f'WebGL 1.0'
    dm_img_str = base64_encode(sss)
    # dm_img_str = 'V2ViR0wgMS4wIChPcGVuR0wgRVMgMi4wIENocm9taXVtKQ'
    return dm_img_str


def get_dm_list():
    dm_list = [{"x":2927,"y":2561,"z":0,"timestamp":3351,"k":79,"type":0},{"x":2981,"y":2636,"z":60,"timestamp":3452,"k":102,"type":0},{"x":3049,"y":2689,"z":127,"timestamp":3553,"k":80,"type":0},{"x":3527,"y":1915,"z":152,"timestamp":3693,"k":114,"type":0},{"x":3858,"y":1808,"z":256,"timestamp":3794,"k":85,"type":0},{"x":3660,"y":1611,"z":55,"timestamp":4000,"k":102,"type":0},{"x":4778,"y":2335,"z":607,"timestamp":4101,"k":85,"type":0},{"x":5165,"y":3364,"z":586,"timestamp":4202,"k":95,"type":0},{"x":4819,"y":3214,"z":204,"timestamp":4303,"k":66,"type":0},{"x":4800,"y":3194,"z":188,"timestamp":4404,"k":89,"type":0},{"x":5720,"y":4569,"z":985,"timestamp":4505,"k":105,"type":0},{"x":5405,"y":4312,"z":634,"timestamp":4606,"k":85,"type":0},{"x":4339,"y":2356,"z":53,"timestamp":6365,"k":102,"type":0},{"x":4974,"y":2253,"z":1108,"timestamp":6466,"k":120,"type":0},{"x":4477,"y":1756,"z":611,"timestamp":6566,"k":89,"type":0},{"x":4817,"y":2111,"z":929,"timestamp":6669,"k":87,"type":0},{"x":3924,"y":1136,"z":6,"timestamp":6770,"k":64,"type":0},{"x":4241,"y":710,"z":114,"timestamp":6871,"k":124,"type":0},{"x":6160,"y":2629,"z":2033,"timestamp":7016,"k":76,"type":0},{"x":5698,"y":1852,"z":1481,"timestamp":7400,"k":93,"type":0},{"x":6039,"y":21,"z":1346,"timestamp":7500,"k":77,"type":0},{"x":5145,"y":-754,"z":486,"timestamp":7668,"k":108,"type":0},{"x":6413,"y":-476,"z":1665,"timestamp":7769,"k":102,"type":0},{"x":5599,"y":-2428,"z":631,"timestamp":7869,"k":69,"type":0},{"x":7418,"y":-416,"z":2515,"timestamp":7969,"k":96,"type":0},{"x":6100,"y":-1734,"z":1197,"timestamp":8069,"k":103,"type":0},{"x":7797,"y":-67,"z":2915,"timestamp":8169,"k":98,"type":0},{"x":6083,"y":-1862,"z":1329,"timestamp":8270,"k":67,"type":0},{"x":5769,"y":-2213,"z":1103,"timestamp":8371,"k":89,"type":0},{"x":6391,"y":-1599,"z":1726,"timestamp":8471,"k":102,"type":0},{"x":4697,"y":-3316,"z":55,"timestamp":8572,"k":90,"type":0},{"x":7004,"y":-1063,"z":2432,"timestamp":8673,"k":70,"type":0},{"x":4635,"y":-3495,"z":206,"timestamp":8774,"k":109,"type":0},{"x":6840,"y":-1318,"z":2495,"timestamp":8875,"k":103,"type":0},{"x":6588,"y":-1582,"z":2279,"timestamp":8975,"k":82,"type":0},{"x":5997,"y":-2198,"z":1717,"timestamp":9075,"k":98,"type":0},{"x":7641,"y":-569,"z":3383,"timestamp":9176,"k":125,"type":0},{"x":6346,"y":-1866,"z":2094,"timestamp":9277,"k":102,"type":0},{"x":7928,"y":-294,"z":3683,"timestamp":9378,"k":65,"type":0},{"x":6593,"y":-1630,"z":2351,"timestamp":9481,"k":92,"type":0},{"x":8021,"y":-171,"z":3801,"timestamp":9582,"k":76,"type":0},{"x":6545,"y":-1516,"z":2392,"timestamp":9683,"k":118,"type":0},{"x":8197,"y":194,"z":4054,"timestamp":9783,"k":67,"type":0},{"x":6234,"y":-1769,"z":2091,"timestamp":11316,"k":80,"type":0},{"x":6666,"y":-1375,"z":2545,"timestamp":11416,"k":83,"type":0},{"x":7208,"y":-983,"z":3054,"timestamp":11518,"k":115,"type":0},{"x":5043,"y":-3218,"z":869,"timestamp":11619,"k":91,"type":0},{"x":5997,"y":-2286,"z":1820,"timestamp":11720,"k":107,"type":0},{"x":8556,"y":273,"z":4379,"timestamp":11821,"k":118,"type":0},{"x":7396,"y":-887,"z":3219,"timestamp":11968,"k":65,"type":0}]
    dm_img_list = json.dumps(dm_list, separators=(',', ':'))
    return dm_img_list


def get_dm_img_inter():
    ## dm_img_inter = {"ds":[{"t":10,"c":"YmUtcGFnZXItaXRlbQ","p":[3939,81,4453],"s":[278,475,552]}],"wh":[5265,3620,63],"of":[1392,2094,357]}
    dm_img_inter = {"ds":[{"t":10,"c":"YmUtcGFnZXItaXRlbQ","p":[3720,60,4510],"s":[210,407,416]}],"wh":[5385,3660,103],"of":[1352,2014,317]}
    return json.dumps(dm_img_inter, separators=(',', ':'))

def get_wts(if_new = True):
    if if_new:
        wts = str(int(time.time()))
    else:
        wts = 1714722176
    return wts
# 通过链接获取对应的信息
# @retry(stop_max_attempt_number=9, wait_fixed=100)
def get_onepage_bv_titles(userId="", pcursor=1, keyword=""):
    # h = {
    #     'authority': 'api.bilibili.com',
    #     'cache-control': 'max-age=0',
    #     'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
    #     'sec-ch-ua-mobile': '?0',
    #     'upgrade-insecure-requests': '1',
    #     'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    #     'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    #     'sec-fetch-site': 'none',
    #     'sec-fetch-mode': 'navigate',
    #     'sec-fetch-user': '?1',
    #     'sec-fetch-dest': 'document',
    #     'accept-language': 'zh-CN,zh;q=0.9',
    # }
    # response = requests.get('https://www.bilibili.com', headers=h)
    # ## print(response.text)
    # cookies = dict(response.cookies)
    ## get header and cookies
    h, cookies = common.get_header_and_cookie()
    api = 'https://api.bilibili.com/x/space/wbi/arc/search'
    dm_img_list = [{"x":5741,"y":7072,"z":0,"timestamp":1028879,"k":110,"type":0},{"x":6018,"y":6511,"z":31,"timestamp":1030556,"k":84,"type":0}]
    dm_img_list = json.dumps(dm_img_list, separators=(',', ':'))
    params = {  # 顺序很重要
        "dm_cover_img_str": get_dm_cover_img_str(),
        "dm_img_inter": get_dm_img_inter(),
        "dm_img_list": get_dm_list(),
        "dm_img_str": get_dm_img_str(),
        'keyword': keyword,
        "mid": userId,
        "order": "pubdate",
        "order_avoided": "true",
        "platform": "web",
        "pn": pcursor,
        "ps": "30",
        "tid": "0",
        "web_location": "1550101",
        "wts": get_wts(True),
    }
    w_rid = md5_use(urlencode(params) + 'ea1db124af3c7062474693fa704f4ff8')
    params['w_rid'] = w_rid
    h.update({'referer': f'https://m.bilibili.com/space/{userId}'})
    res = requests.get(
        api,
        headers=h,
        params=params,
        cookies=cookies,
        proxies=get_proxy(),
        timeout=15,
    )
    if '风控校验失败' in res.text:
        print('retrying...')
        print(res.text)
        print("\nthe page:")
        print(pcursor)
        raise
    # print(res.text)
    ## print(res.json())
    ## output the fusion ones
    res_list = []
    v_list = res.json()['data']['list']['vlist']
    for j in v_list:
        title = j['title']
        bv_id = j['bvid']
        comment = j['comment']
        play = j['play']
        res_list.append({"title":title, "bvid": bv_id, "comment" : comment, "play": play, "pcursor": pcursor})
    return res_list
def get_all_pages_bvlist(user_id, begin_page, end_page):
    res_list_all = []
    for pcursor in range(begin_page, end_page):
        res_list = get_onepage_bv_titles(user_id, pcursor=pcursor)
        res_list_all.extend(res_list)
        time.sleep(3)
    ## save to csv    
    df = pd.DataFrame(res_list_all)
    current_path = os.path.abspath(__file__)
    base_path = os.path.abspath(os.path.dirname(current_path) + os.path.sep + ".")
    df.to_csv(base_path + '/bilibili_bvs/userid_{}_{}_{}.csv'.format(user_id, begin_page, end_page, int(time.time())))
    return df

if __name__ == "__main__":
    ## print(get_all_pages_bvlist(user_id="433004026", begin_page = 80, end_page = 81))
    print(get_all_pages_bvlist(user_id="227531152", begin_page = 1, end_page = 2))



