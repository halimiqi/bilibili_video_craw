# 第一步-获取用户的视频列表以及对应的视频信息
python get_list.py
# 第二步-根据获取的视频信息爬对应的 audio, video， 然后合并文件
python main.py 

# 额外需要注意的点
- 需要新建的文件夹
  bilibili_bvs: 用语存放对应 user_id的视频链接列表
  bilibili_audio: 用于存放爬下来的音频
  bilibil_video:用语存放爬下来的视频
  bilibili_merge: 用于存放之后合并的视频文件
- user_id如何获取：
  找到你需要找的 up主，进入主页后，url中的数字，就是他需要的 user_id
  ![image](https://github.com/halimiqi/bilibili_video_craw/assets/39412839/842b9f43-2d40-48fa-9a16-b03f40290dea)
