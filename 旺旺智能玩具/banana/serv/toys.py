from flask import Blueprint, request, jsonify
from setting import MONGO_DB
from setting import RET
from bson import ObjectId

toy = Blueprint("toy", __name__)


@toy.route("/toy_list", methods=["POST"])
def toy_list():
    user_id = request.form.get("user_id")
    user_info = MONGO_DB.users.find_one({"_id": ObjectId(user_id)})
    bind_toy = user_info.get("bind_toy")
    bind_toy_id = []
    for toy_id in bind_toy:
        bind_toy_id.append(ObjectId(toy_id))

    toys_list = list(MONGO_DB.toys.find({"_id": {"$in": bind_toy_id}}))

    for index, item in enumerate(toys_list):
        toys_list[index]["_id"] = str(item.get("_id"))

    RET["code"] = 0
    RET["msg"] = ""
    RET["data"] = toys_list

    return jsonify(RET)


@toy.route("/device_toy_id", methods=["POST"])
def device_toy_id():
    RET["code"] = 0
    RET["msg"] = "开机成功"
    RET["data"] = {}

    device_id = request.form.get("device_id")

    if MONGO_DB.devices.find_one({"device_id": device_id}):
        toy_info = MONGO_DB.toys.find_one({"device_id": device_id})
        if toy_info:
            RET["data"]["toy_id"] = str(toy_info.get("_id"))
            RET["data"]["audio"] = "success.mp3"
            return jsonify(RET)
        else:
            RET["msg"] = "找小主人"
            RET["data"]["audio"] = "Nobind.mp3"
            return jsonify(RET)
    else:
        RET["msg"] = "联系玩具厂"
        RET["data"]["audio"] = "Nodevice.mp3"
        return jsonify(RET)


@toy.route("/toy_info", methods=["POST"])
def toy_info():
    toy_id = request.form.get("toy_id")
    toy = MONGO_DB.toys.find_one({"_id":ObjectId(toy_id)})

    toy["_id"] = str(toy.get("_id"))

    RET["code"] = 0
    RET["msg"] = ""
    RET["data"] = toy

    return jsonify(RET)