from concurrent.futures import ThreadPoolExecutor
from win11toast import toast
import shutil
import socket
import requests
import os

# 禁用代理
os.environ["no_proxy"] = "*"


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # 这里不需要连接到任何服务器
        s.connect(("114.114.114.114", 80))
        IP = s.getsockname()[0]
    finally:
        s.close()
    return IP


def save_image_from_web(url, filename):
    # 发送GET请求
    response = requests.get(url, stream=True)

    # 确保请求成功
    if response.status_code == 200:
        with open(filename, "wb") as file:
            response.raw.decode_content = True
            shutil.copyfileobj(response.raw, file)


def getHitokoto():
    response = requests.get("https://v1.hitokoto.cn/")
    data = response.json()
    hitokoto = data["hitokoto"]
    return hitokoto


def getHitokotoImage():
    with ThreadPoolExecutor(max_workers=2) as executor:
        # 并行提交两个任务
        future_image = executor.submit(save_image_from_web, image_url, image_src)
        future_hitokoto = executor.submit(getHitokoto)

        # 等待结果
        hitokoto = future_hitokoto.result()
        future_image.result()  # 确保图片已经保存

        return hitokoto


if __name__ == "__main__":
    # 变量配置区 # 使用前先配置
    login_IP = "http://10.31.0.10/"
    not_sign_in_title = "上网登录页"
    result_return = 'result":1,'
    sign_parameter = f""
    signed_in_title = "注销页"

    success_icon = {
        "src": "C:\\sbXiaoYuanWang\\ico\\success.png",
        "placement": "appLogoOverride",
    }
    false_icon = {
        "src": "C:\\sbXiaoYuanWang\\ico\\warning.png",
        "placement": "appLogoOverride",
    }
    unknown_icon = {
        "src": "C:\\sbXiaoYuanWang\\ico\\question.png",
        "placement": "appLogoOverride",
    }
    image_url = "https://t.mwm.moe/pc"
    image_src = "C:\\sbXiaoYuanWang\\tmp.png"
    image = {
        "src": image_src,
        "placement": "hero",
    }

    try:
        r = requests.get(login_IP, timeout=1)
        req = r.text
    except:
        req = "False"
    if signed_in_title in req:
        toast(getHitokotoImage(), "设备已登录", icon=success_icon, image=image)
        # os.remove(image_src)
        os._exit(0)

    elif not_sign_in_title in req:
        r = requests.get(sign_parameter, timeout=1)
        req = r.text
        if result_return in req:
            toast(getHitokotoImage(), "登录成功", icon=success_icon, image=image)
            # os.remove(image_src)
            os._exit(0)
        else:
            toast(
                "校园网登录失败",
                "校园网状态",
                icon=false_icon,
            )
            os._exit(0)

    else:
        toast(
            "校园网状态异常",
            "校园网状态",
            icon=unknown_icon,
        )
        os._exit(0)
