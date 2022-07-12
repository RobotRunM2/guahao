'''
Author: wdjoys
Date: 2022-04-24 15:16:14
LastEditors: wdjoys
LastEditTime: 2022-07-04 10:22:34
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
    robots = instantiate_all_hospital_robots()

    i = 0
    print('程序开始运行...',)
    while True:

        [send_notification(time=regist_result['time'], docName=regist_result["docName"], other_information=regist_result['other_information'])
         for regist_result in all_hospital_register(robots)]

        i += 1

        print(f'完成{i}次检查，sleep...',)
        time.sleep(10)


if __name__ == '__main__':
    run()
