from flask import Flask, request
from geventwebsocket.websocket import WebSocket
from geventwebsocket.handler import WebSocketHandler
from gevent.pywsgi import WSGIServer
import json, os
from uuid import uuid4
from setting import CHAT_FILE
from setting import MONGO_DB
from utils import baidu_ai
from utils import chat_redis
import time
from bson import ObjectId
from serv import content

app = Flask(__name__)

user_socket_dict = {}


@app.route("/toy/<tid>")
def toy(tid):
    user_socket = request.environ.get("wsgi.websocket")  # type:WebSocket
    if user_socket:
        user_socket_dict[tid] = user_socket
        # { uid : websocket}
        print(user_socket_dict)

    file_name = ""
    to_user = ""
    while True:
        msg = user_socket.receive()
        if type(msg) == bytearray:
            file_name = f"{uuid4()}.wav"
            file_path = os.path.join(CHAT_FILE, file_name)
            with open(file_path, "wb") as f:
                f.write(msg)
        else:
            msg_dict = json.loads(msg)
            to_user = msg_dict.get("to_user")
            msg_type = msg_dict.get("msg_type")
            user_type = msg_dict.get("user_type")

        if to_user and file_name:
            other_user_socket = user_socket_dict.get(to_user)
            if msg_type == "ai":
                q = baidu_ai.audio2text(file_path)
                print(q)
                ret = baidu_ai.my_nlp(q, tid)
                other_user_socket.send(json.dumps(ret))
            else:
                if user_type == "toy":
                    res = MONGO_DB.toys.find_one({"_id": ObjectId(to_user)})
                    fri = [i.get("friend_remark") for i in res.get("friend_list") if i.get("friend_id") == tid][0]
                    msg_file_name = baidu_ai.text2audio(f"你有来自{fri}的消息")
                    send_str = {
                        "code": 0,
                        "from_user": tid,
                        "msg_type": "chat",
                        "user_type": "toy",
                        "data": msg_file_name
                    }
                else:
                    send_str = {
                        "code": 0,
                        "from_user": tid,
                        "msg_type": "chat",
                        "data": file_name
                    }

                if other_user_socket:
                    chat_redis.save_msg(tid, to_user)
                    other_user_socket.send(json.dumps(send_str))
                else:
                    chat_redis.save_msg(tid, to_user)

                _add_chat(tid, to_user, file_name)

            to_user = ""
            file_name = ""


@app.route("/app/<uid>")
def user_app(uid):
    user_socket = request.environ.get("wsgi.websocket")  # type:WebSocket
    if user_socket:
        user_socket_dict[uid] = user_socket
        # { uid : websocket}
        print(user_socket_dict)

    file_name = ""
    to_user = ""

    while True:  # 手机听歌 把歌曲发送给 玩具 1.将文件直接发送给玩具 2.将当前听的歌曲名称或ID发送到玩具
        msg = user_socket.receive()  # 1.{to_user}
        if type(msg) == bytearray:
            file_name = f"{uuid4()}.amr"
            file_path = os.path.join(CHAT_FILE, file_name)
            print(msg)
            with open(file_path, "wb") as f:
                f.write(msg)

            os.system(f"ffmpeg -i {file_path} {file_path}.mp3")

        else:
            msg_dict = json.loads(msg)
            to_user = msg_dict.get("to_user")
            # {
            #     to_user: 123456
            #     音乐的id:12345678 # 音乐名称：987654321
            # }

            if msg_dict.get("msg_type") == "music":
                other_user_socket = user_socket_dict.get(to_user)
                send_str = {
                    "code": 0,
                    "from_user": uid,
                    "msg_type": "music",
                    "data": msg_dict.get("data")
                }
                other_user_socket.send(json.dumps(send_str))
                to_user = ""

            # res = content._content_one(content_id)
        if file_name and to_user:
            res = MONGO_DB.toys.find_one({"_id": ObjectId(to_user)})
            fri = [i.get("friend_remark") for i in res.get("friend_list") if i.get("friend_id") == uid][0]
            msg_file_name = baidu_ai.text2audio(f"你有来自{fri}的消息")

            other_user_socket = user_socket_dict.get(to_user)
            send_str = {
                "code": 0,
                "from_user": uid,
                "msg_type": "chat",
                "data": msg_file_name
            }

            if other_user_socket:
                chat_redis.save_msg(uid, to_user)
                other_user_socket.send(json.dumps(send_str))
            else:
                chat_redis.save_msg(uid, to_user)

            _add_chat(uid, to_user, f"{file_name}.mp3")
            file_name = ""
            to_user = ""


def _add_chat(sender, to_user, msg):
    chat_window = MONGO_DB.chat.find_one({"user_list": {"$all": [sender, to_user]}})
    if not chat_window.get("chat_list"):
        chat_window["chat_list"] = [{
            "sender": sender,
            "msg": msg,
            "updated_at": time.time(),
        }]
        res = MONGO_DB.chat.update_one({"_id": ObjectId(chat_window.get("_id"))}, {"$set": chat_window})
    else:
        chat = {
            "sender": sender,
            "msg": msg,
            "updated_at": time.time(),
        }
        res = MONGO_DB.chat.update_one({"_id": ObjectId(chat_window.get("_id"))}, {"$push": {"chat_list": chat}})

    return res


if __name__ == '__main__':
    http_serv = WSGIServer(("0.0.0.0", 9528), app, handler_class=WebSocketHandler)
    http_serv.serve_forever()

#备注：
#登录用户名：zhao,密码123
#打开网页以后，先从芒果数据库中取出玩具id,放入输入框中，点击开机
#运行以后可以在浏览地地址栏输入http://192.168.11.31:9527/，运行程序(自己的ip)
#记得要更改index.html中的ip地址：
#注意：这里是两个进程，两条服务；
    # 所有的websocket在前端只能出现一次，出现第二次就被覆盖了；整个app,只能有一个。这是一个坑；
    # 在Myapp 的HBuilder文件中的index.html文件中也有一个mui.plus的地方，需要改ip地址；
    # 在 QRcode.py文件中运行一下，采集到二维码设备信息（就是获取到二维码，相当于生产了设备）