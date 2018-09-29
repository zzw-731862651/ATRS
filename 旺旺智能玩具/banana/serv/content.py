from flask import Blueprint, jsonify,request
from bson import ObjectId
from setting import MONGO_DB
from setting import RET

cont = Blueprint("cont", __name__)


@cont.route("/content_list", methods=["POST"])
def content_list():
    res_list = list(MONGO_DB.sources.find({}))

    for index, item in enumerate(res_list):
        res_list[index]["_id"] = str(item.get("_id"))

    RET["code"] = 0
    RET["msg"] = ""
    RET["data"] = res_list

    return jsonify(RET)


@cont.route("/content_one", methods=["POST"])
def content_one():
    content_id = request.form.get("content_id")
    res = MONGO_DB.sources.find_one({"_id":ObjectId(content_id)})

    res["_id"] = str(res["_id"])

    RET["code"] = 0
    RET["msg"] = ""
    RET["data"] = res

    return jsonify(RET)


def _content_one(content_id):
    res = MONGO_DB.sources.find_one({"_id":ObjectId(content_id)})
    return res
