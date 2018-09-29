from flask import Blueprint, request, jsonify
from setting import MONGO_DB
from setting import RET
from bson import ObjectId

devs = Blueprint("devs", __name__)


@devs.route("/yanzheng_qr", methods=["POST"])
def yanzheng_qr():
    device_id = request.form.get("device_id")
    if MONGO_DB.devices.find_one({"device_id": device_id}):
        # 查询该玩具是不是已被用户绑定
        toy_info = MONGO_DB.toys.find_one({"device_id": device_id})
        # 未绑定开启绑定逻辑
        if not toy_info:
            RET["code"] = 0
            RET["msg"] = "感谢购买本公司产品"
            RET["data"] = {}

        # 如果被绑定加好友逻辑开启
        if toy_info:
            RET["code"] = 1
            RET["msg"] = "添加好友"
            RET["data"] = {"toy_id":str(toy_info.get("_id"))}

    else:
        RET["code"] = 2
        RET["msg"] = "你个大傻X，我们只识别我们自己的设备，快去买正版！"
        RET["data"] = {}

    return jsonify(RET)


@devs.route("/bind_toy", methods=["POST"])
def bind_toy():
    chat_window = MONGO_DB.chat.insert_one({})
    chat_id = chat_window.inserted_id

    user_id = request.form.get("user_id")
    print(user_id)
    res = MONGO_DB.users.find_one({"_id": ObjectId(user_id)})
    print(res)

    device_id = request.form.get("device_id")
    toy_name = request.form.get("toy_name")
    baby_name = request.form.get("baby_name")
    remark = request.form.get("remark")
    gender = request.form.get("gender")

    # 聊天id = chat_window.inserted_id

    toy_info = {
        "device_id": device_id,
        "toy_name": toy_name,
        "baby_name": baby_name,
        "gender": gender,
        "avatar": "boy.jpg" if gender == 1 else "girl.jpg",
        # 绑定用户
        "bind_user": str(res.get("_id")),
        # 第一个好友
        "friend_list": [{
            "friend_id": str(res.get("_id")),
            "friend_name": res.get("nickname"),
            "friend_remark": remark,
            "friend_avatar": res.get("avatar"),
            "friend_chat": str(chat_id),
            "user_type":"user"
        }]
    }

    toy_res = MONGO_DB.toys.insert_one(toy_info)

    if res.get("friend_list"):
        res["bind_toy"].append(str(toy_res.inserted_id))
        res["friend_list"].append({
            "friend_id": str(toy_res.inserted_id),
            "friend_name": toy_name,
            "friend_remark": baby_name,
            "friend_avatar": toy_info.get("avatar"),
            "friend_chat": str(chat_id),
            "user_type":"toy"
        })
    else:
        res["bind_toy"] = [str(toy_res.inserted_id)]
        res["friend_list"] = [{
            "friend_id": str(toy_res.inserted_id),
            "friend_name": toy_name,
            "friend_remark": baby_name,
            "friend_avatar": toy_info.get("avatar"),
            "friend_chat": str(chat_id),
            "user_type": "toy"
        }]

    MONGO_DB.users.update_one({"_id": ObjectId(user_id)}, {"$set": res})

    MONGO_DB.chat.update_one({"_id": chat_id},
                             {"$set":
                                  {"user_list":
                                       [str(toy_res.inserted_id),
                                        str(res.get("_id"))]}})

    RET["code"] = 0
    RET["msg"] = "绑定成功"
    RET["data"] = {}

    return jsonify(RET)
