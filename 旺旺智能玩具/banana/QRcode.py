from uuid import uuid4
from setting import CREATE_QR_URL
from setting import DEVICE_CODE_PATH
from setting import MONGO_DB
import hashlib, time,os
import requests


def create_device_id(count=1):
    device_list = []
    for i in range(count):
        device_id = f"{uuid4()}{time.time()}"
        device_id_md5 = hashlib.md5(device_id.encode("utf8"))

        qr_code = device_id_md5.hexdigest()
        qr_url = f"{CREATE_QR_URL}{qr_code}"
        res = requests.get(qr_url)
        code_file = os.path.join(DEVICE_CODE_PATH,f"{qr_code}.jpg")

        with open(code_file, "wb") as f:
            f.write(res.content)

        device_list.append({"device_id":qr_code})



        # time.sleep(0.2)

    MONGO_DB.devices.insert_many(device_list)


create_device_id(5)