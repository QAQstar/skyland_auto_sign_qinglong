#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
File: auto_sign.py(森空岛签到)
Author: Zerolouis
cron: 0 50 5 * * *
new Env('森空岛签到');
Update: 2023/9/19
"""
import json
import logging
import os
import time

import requests
import notify

skyland_tokens = os.getenv('SKYLAND_TOKEN')

SIGN_URL = "https://zonai.skland.com/api/v1/game/attendance"
SUCCESS_CODE = 0
# 休眠三秒继续其他账号签到
SLEEP_TIME = 3

# 打印当前时间
print("当前时间为：" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

app_code = '4ca99fa6b56cc2ba'

def do_sign(token):
    """
    进行签到
    """
    # 准备签到信息
    configs = cookie_line.split("&")
    uid = configs[0].strip()
    signing_cookie = configs[1].strip()
    headers = {
        "user-agent": "Skland/1.0.1 (com.hypergryph.skland; build:100001014; Android 33; ) Okhttp/4.11.0",
        "cred": signing_cookie,
        "vName": "1.0.1",
        "vCode": "100001014",
        'Accept-Encoding': 'gzip',
        'Connection': 'close',
        "dId": "de9759a5afaa634f",
        "platform": "1"
    }
    data = {
        "uid": str(uid),
        "gameId": 1
    }

    # 签到请求
    sign_response = requests.post(headers=headers, url=SIGN_URL, data=data)

    # 检验返回是否为json格式
    try:
        sign_response_json = json.loads(sign_response.text)
    except:
        print(sign_response.text)
        print("返回结果非json格式，请检查...")
        time.sleep(SLEEP_TIME)
        sys.exit()

    # 如果为json则解析
    code = sign_response_json.get("code")
    message = sign_response_json.get("message")
    data = sign_response_json.get("data")

    # 返回成功的话，打印详细信息
    if code == SUCCESS_CODE:
        print("签到成功")
        awards = sign_response_json.get("data").get("awards")
        for award in awards:
            print("签到获得的奖励ID为：" + award.get("resource").get("id"))
            print("此次签到获得了" + str(award.get("count")) + "单位的" + award.get("resource").get("name") + "(" + award.get(
                "resource").get("type") + ")")
            print("奖励类型为：" + award.get("type"))
    else:
        print(sign_response_json)
        print("签到失败，请检查以上信息...")


def main():
    token_list = skyland_tokens.split(';')
    if len(token_list) != 0:
        print("已读取" + str(len(token_list)) + "个token")
        time.sleep(SLEEP_TIME)
        for token in token_list:
            do_sign(token)
        print('签到结束！')


if __name__ == "__main__":
    main()
