from flask import Blueprint, request, jsonify
from setting import MONGO_DB
from setting import RET
from bson import ObjectId
from utils import chat_redis

cht = Blueprint("cht", __name__)


@cht.route("/chat_list", methods=["POST"])
def chat_list():
    user_id = request.form.get("user_id")
    friend_id = request.form.get("friend_id")
    print(friend_id)

    chat_window = MONGO_DB.chat.find_one({"user_list": {"$all": [user_id, friend_id]}})
    fri = MONGO_DB.toys.find_one({"_id": ObjectId(friend_id)})
    baby_name = fri.get("baby_name")
    cl = chat_window.get("chat_list")

    RET["code"] = 0
    RET["msg"] = baby_name
    RET["data"] = cl

    chat_redis.get_msg_one(friend_id, user_id)

    return jsonify(RET)


@cht.route("/get_msg", methods=["POST"])
def get_msg():
    user_id = request.form.get("user_id")
    sender = request.form.get("sender")
    # print(sender)
    if not sender:
        msg_dict = chat_redis.get_msg_list(user_id)
        sender = [i for i in msg_dict.keys() if msg_dict[i] != 0 and i != "count"]
        if sender:
            sender = sender[0]
            count = msg_dict[sender]
        # else:
        #     pass
            # filename= baidu_ai.text2audio("")
            # new_msg = [{sender:"",msg:filename}]

    else:
        count = chat_redis.get_user_msg_one(sender, user_id)

    chat_window = MONGO_DB.chat.find_one({"user_list": {"$all": [user_id, sender]}})
    new_msg = chat_window.get("chat_list")[-count:]  # type:list
    # filename= baidu_ai.text2audio("")
    # new_msg.insert(0,{
    #     "sender":sender,
    #     "msg":filename
    # })

    RET["code"] = 0
    RET["msg"] = ""
    RET["data"] = new_msg

    chat_redis.get_msg_one(sender, user_id)

    return jsonify(RET)


@cht.route("/get_msg_list", methods=["POST"])
def get_msg_list():
    user_id = request.form.get("user_id")
    user_msg_dict = chat_redis.get_msg_list(user_id)

    RET["code"] = 0
    RET["msg"] = ""
    RET["data"] = user_msg_dict

    return jsonify(RET)
