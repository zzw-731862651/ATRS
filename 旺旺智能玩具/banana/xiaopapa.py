import requests
import json
import os
from setting import XMLY_URL
from setting import AUDIO_FILE
from setting import AUDIO_IMG_FILE
from setting import MONGO_DB
from uuid import uuid4

content_url = "/ertong/424529/13667674"    #一千零一夜歌曲列表，审查元素，点击箭头审查就可以看到
category = "erge"

pid = content_url.rsplit("/", 1)[-1]

xiaopapa_url = XMLY_URL + pid + ".json"

content = requests.get(xiaopapa_url)

content_dict = json.loads(content.content.decode("utf8"))

play_path = content_dict.get("play_path")
cover_url = content_dict.get("cover_url")

intro = content_dict.get("intro")
nickname = content_dict.get("nickname")
title = content_dict.get("title")

file_name = f"{uuid4()}"
audio = f"{file_name}.mp3"
image = f"{file_name}.jpg"

audio_file = requests.get(play_path).content
with open(os.path.join(AUDIO_FILE, audio), "wb") as f:
    f.write(audio_file)

image_file = requests.get(cover_url).content
with open(os.path.join(AUDIO_IMG_FILE, image), "wb") as f:
    f.write(image_file)

content_db = {
    "title": title,
    "nickname": nickname,
    "avatar": image,
    "audio": audio,
    "intro": intro,
    "category":category,
    "play_count": 0
}

MONGO_DB.sources.insert_one(content_db)
