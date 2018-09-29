from flask import Blueprint, send_file
from setting import AUDIO_FILE
from setting import AUDIO_IMG_FILE
from setting import CHAT_FILE
import os

getfile = Blueprint("getfile", __name__)


@getfile.route("/get_audio/<filename>")
def get_audio(filename):
    sendfile = os.path.join(AUDIO_FILE, filename)
    return send_file(sendfile)


@getfile.route("/get_image/<filename>")
def get_image(filename):
    sendfile = os.path.join(AUDIO_IMG_FILE, filename)
    return send_file(sendfile)


@getfile.route("/get_chat/<filename>")
def get_chat(filename):
    sendfile = os.path.join(CHAT_FILE, filename)
    return send_file(sendfile)