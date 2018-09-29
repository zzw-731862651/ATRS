import pymongo
import os
import redis


# 数据库配置
client = pymongo.MongoClient(host="127.0.0.1", port=27017)
MONGO_DB = client["zhineng"]
REDIS_DB = redis.Redis(host="127.0.0.1",port=6379,db=5)


#
RET = {
    "code": 0,  # 1 大帅比 2 密码错 3 用户名不存在 4
    "msg": "欢迎登陆",
    "data": {}
}

XMLY_URL = "http://m.ximalaya.com/tracks/"    #这个地址是分享以后，分享-->展开获取声音链接---->微电台--->进去审查元素，播放就出来了

CREATE_QR_URL = "http://qr.liantu.com/api.php?text="

# 文件目录

AUDIO_FILE = os.path.join(os.path.dirname(__file__), "audio")
AUDIO_IMG_FILE = os.path.join(os.path.dirname(__file__), "audio_img")
DEVICE_CODE_PATH = os.path.join(os.path.dirname(__file__), "device_code")
CHAT_FILE = os.path.join(os.path.dirname(__file__), "chat")

# 百度ai配置
APP_ID = '11793791'
API_KEY = 'iaTErc4r5GXNT56tYnlVtVtk'
SECRET_KEY = '24P7ImcU7kEaOmoBxDy9giNe6evkYca4'
SPEECH = {
    "spd": 4,
    'vol': 7,
    "pit": 6,   #这里调低了点
    "per": 4
}

#图灵配置：
TL_URL = "http://openapi.tuling123.com/openapi/api/v2"
TL_DATA = {
    # 请求的类型 0 文本 1 图片 2 音频
    "reqType": 0,
    # // 输入信息(必要参数)
    "perception": {
        # 文本信息
        "inputText": {
            # 问题
            "text": "北京未来七天，天气怎么样"
        }
    },
    # 用户必要信息
    "userInfo": {
        # 图灵机器人的apikey
        "apiKey": "8fc493d348704ba4af5413e67e6fc90b",
        # 用户唯一标识
        "userId": "zilong"
    }
}