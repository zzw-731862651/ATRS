from flask import Flask, request, jsonify,render_template
from setting import MONGO_DB
from setting import RET
from bson import ObjectId
from serv import get_file
from serv import content
from serv import devices
from serv import toys
from serv import friend
from serv import chat

app = Flask(__name__)

app.register_blueprint(get_file.getfile)
app.register_blueprint(content.cont)
app.register_blueprint(devices.devs)
app.register_blueprint(toys.toy)
app.register_blueprint(friend.fri)
app.register_blueprint(chat.cht)


@app.route('/')
def hello_world():
    return render_template("index.html")


@app.route('/login', methods=["POST"])
def login():
    """
    登陆验证
    :return: settings -> RET
    """
    RET["code"] = 1
    RET["msg"] = "用户名或密码错误"
    RET["data"] = {}

    username = request.form.get("username")
    password = request.form.get("password")

    user = MONGO_DB.users.find_one({"username": username, "password": password})

    if user:
        user["_id"] = str(user.get("_id"))
        RET["code"] = 0
        RET["msg"] = "欢迎登陆"
        RET["data"] = {"user_id": user.get("_id")}

    return jsonify(RET)


@app.route('/user_info', methods=["POST"])
def user_info():
    user_id = request.form.get("user_id")

    res = MONGO_DB.users.find_one({"_id": ObjectId(user_id)}, {"password": 0})
    if res:
        res["_id"] = str(res.get("_id"))

    RET["code"] = 0
    RET["msg"] = ""
    RET["data"] = res

    return jsonify(res)


@app.route('/reg', methods=["POST"])
def reg():
    # print('222')
    username = request.form.get("username")
    password = request.form.get("password")
    age = request.form.get("age")
    nickname = request.form.get("nickname")
    gender = request.form.get("gender")
    phone = request.form.get("phone")

    user_info = {

        "username": username,
        "password": password,
        "age": age,
        "nickname": nickname,
        "avatar": "girl.jpg" if gender == 2 else "boy.jpg",
        "gender": gender,
        "phone": phone
    }

    res = MONGO_DB.users.insert_one(user_info)
    # print('6666')
    user_id = str(res.inserted_id)

    return f"注册成功，{user_id}"


if __name__ == '__main__':
    app.run("0.0.0.0", 9527, debug=True)

#备注：
#登录用户名：zhao,密码123
#打开网页以后，先从芒果数据库中取出玩具id,放入输入框中，点击开机
#运行以后可以在浏览地地址栏输入http://192.168.11.31:9527/，运行程序(自己的ip)
#记得要更改index.html中的ip地址：
#注意：这里是两个进程，两条服务；
    # 所有的websocket在前端只能出现一次，出现第二次就被覆盖了；整个app,只能有一个。这是一个坑；
    # 在Myapp 的HBuilder文件中的index.html文件中也有一个mui.plus的地方，需要改ip地址；
    # 在 QRcode.py文件中运行一下，采集到二维码设备信息（就是获取到二维码，相当于生产了设备）
