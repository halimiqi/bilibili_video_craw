import os
import re
import subprocess
import threading
from os import makedirs
from os import path
from queue import Queue
import pandas as pd
import requests
import common
import get_list

q = Queue(300)

data_audio = 'bilibili_audio'  # 视频与音频的零时保存文件
data_video = 'bilibili_video'
save_path = 'BiliBili_视频'  # 真实保存路径

try:  # 创建缓存文件夹
    makedirs(data_audio)
    makedirs(data_video)
except Exception as e:
    print(e)

try:  # 创建保存文件夹
    makedirs(save_path)
except Exception as e:
    print(e)

# 重复运行的时候，保存的视频就跳过
file_data_list = os.listdir(save_path)  # 获取文件里面已经保存的数据
headers, cookies = common.get_header_and_cookie()
headers.update({'referer': f'https://www.bilibili.com'})
def main():
    current_path = os.path.abspath(__file__)
    base_path = os.path.abspath(os.path.dirname(current_path) + os.path.sep + ".")
    ## bv_df = get_list.get_all_pages_bvlist(user_id="433004026", begin_page = 1, end_page = 3)
    bv_df = pd.read_csv(base_path + "/bilibili_bvs/userid_227531152_1_2.csv")
    for idx, rows in bv_df.iterrows():
        title = rows['title']
        bv_id = rows['bvid']
        if bv_id in '\t'.join(file_data_list):
            print(f"title:{title}, \n bv_id:{bv_id}\nhas already exists!!!!!!!!\n SKIP!!")
        else:
            parser_html(title, bv_id, f'https://www.bilibili.com/video/{bv_id}') 

def parser_html(title, bv_id, video_url):
   
    """根据url提取音频和视频"""
    headers.update({'referer': video_url})
    html = requests.get(
        video_url,
        headers=headers,
        cookies=cookies,
        proxies=common.get_proxy(),
        timeout=20,
    )
    json_data = re.findall('<script>window.__playinfo__=(.*?)</script>', html.text)[0]
    null = None
    false = False
    true = True
    json_data = eval(json_data)['data']['dash']
    audio_url = json_data['audio'][0]['backupUrl'][0]
    audio_place = path.join(data_audio, f'{title}_{bv_id}.mp3')
    video_url = json_data['video'][0]['backupUrl'][0]
    video_place = path.join(data_video, f'{title}_{bv_id}.mp4')
    q.put([title, audio_url, audio_place, video_url, video_place, bv_id])
    print(f'存放队列数量{q.qsize()}')
    # download_data(title, audio_url, audio_place, video_url, video_place)


def download_data():
    while True:
        print(f'提取队列数量{q.qsize()}')
        try:
            title, audio_url, audio_place, video_url, video_place, bv_id = q.get(timeout=15)
        except:
            print('视频都获取完成')
            break
        # 保存音频
        ## audio = requests.get(audio_url, headers=headers, stream=True)
        audio = requests.get(
            audio_url,
            headers=headers,
            cookies=cookies,
            proxies=common.get_proxy(),
            timeout=100,
            stream=True
        )
        f_a = open(audio_place, 'wb')
        for i in audio.iter_content(chunk_size=1024):
            f_a.write(i)
        f_a.close()

        # 保存视频
        ## video = requests.get(video_url, headers=headers, stream=True)
        video = requests.get(
            video_url,
            headers=headers,
            cookies=cookies,
            proxies=common.get_proxy(),
            timeout=100,
            stream=True
        )
        f_v = open(video_place, 'wb')
        for i in video.iter_content(chunk_size=1024):
            f_v.write(i)
        f_v.close()

        print(f'{title} 已经下载完成')
        merge_data(title, video_place, audio_place, bv_id)


def merge_data(title, video_place, audio_place, bv_id):
    cmd = f"ffmpeg -loglevel quiet -i {video_place} -i {audio_place} -acodec copy -vcodec copy {save_path}/{title}_{bv_id}.mp4"
    # os.system(cmd)
    subprocess.run(cmd, shell=True)
    # try:  # 合并完成后删除视频和音频
    #     os.remove(video_place)
    # except Exception as e1:
    #     print(e1)

    # try:
    #     os.remove(audio_place)
    # except Exception as e2:
    #     print(e2)


if __name__ == '__main__':
    ## main()
    t1 = threading.Thread(target=main)  # 生产者 获取视频的链接
    t1.start()

    list_t = []  # 消费者 保存数据 操作下载后的数据
    for i in range(10):
        t2 = threading.Thread(target=download_data)
        t2.start()
        list_t.append(t2)

    for i in list_t:  # 等待所有子线程结束
        i.join()
    t1.join()
