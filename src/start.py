# -*- coding: utf-8 -*-
# @Author: xiaocao
# @Date:   2022-04-24 15:16:14
# @Last Modified by:   xiaocao
# @Last Modified time: 2023-04-19 08:57:56
'''
Author: wdjoys
Date: 2022-04-24 15:16:14
LastEditors: wdjoys
LastEditTime: 2022-07-19 09:52:57
FilePath: \guahao\src\start.py
Description: 

Copyright (c) 2022 by github/wdjoys, All Rights Reserved. 
'''


import itertools
import random
import time
from notification.wechat import send_notification
from config.settings import ROBOTS
import string


def instantiate_all_hospital_robots():
    """
    实例化所有采集器
    """
    robots = []
    all_chars = string.ascii_letters

    for robot_str in ROBOTS:
        u_name = ''.join(random.choice(all_chars) for _ in range(8))

        exec_str = f"""from {robot_str['ROBOT_PATH']} import Robot as {u_name}
from config.settings import {robot_str['CNFS']}
robot = {u_name}({robot_str['CNFS']})
robots.append(robot)"""
        exec(exec_str)

    return robots


def all_hospital_register(robots):
    """尝试所有医院执行挂号
    """

    resources = [robot.to_register() for robot in robots]
    return itertools.chain(*resources)


def run():

    print('程序开始运行...', 1,)
    # 实例化所有采集机器人
    robots = instantiate_all_hospital_robots()

    # 定义变量记录执行次数
    i = 0

    while True:

        [send_notification(time=regist_result['time'], docName=regist_result["docName"], other_information=regist_result['other_information'])
         for regist_result in all_hospital_register(robots)]

        i += 1

        # 180次 也就是 1800秒打印一次日志
        if i % 180 == 0 or i == 1:
            print(f'已经完成{i}次检查，sleep...',)
        # 间隔10执行一次
        time.sleep(10)


if __name__ == '__main__':
    run()
