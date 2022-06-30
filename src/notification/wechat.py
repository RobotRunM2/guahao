'''
Author: wdjoys
Date: 2022-04-23 12:37:27
LastEditors: wdjoys
LastEditTime: 2022-06-30 08:20:12
FilePath: \guahao\src\notification\wechat.py
Description: 

Copyright (c) 2022 by github/wdjoys, All Rights Reserved. 
'''


from config.settings import WECHAT_TOKEN
from requests import post


def send_notification(time, docName, other_information):
    url = f"https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={WECHAT_TOKEN}"

    msg_template = {
        "msgtype": "markdown",
        "markdown": {
            "content": f"""⏱ 号源状态监测提醒：发现<font color=\"warning\">{docName}</font>医生，在<font color=\"warning\">{time}</font>有最新号源状态。

> 费用：<font color=\"comment\">{other_information['amount']}</font>
> 等级：<font color=\"comment\">{other_information['registLevel']}</font>
> 状态：<font color=\"comment\">{other_information['message']}</font>

前往支付：[点击这里]({other_information['payUrl']})"""
        }
    }

    post(url, json=msg_template)


if __name__ == '__main__':
    send_notification(1, 2, {'registLevel': 1, 'amount': 2, 'resourceMemo': 3})
