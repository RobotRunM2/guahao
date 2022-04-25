'''
Author: wdjoys
Date: 2022-04-23 12:36:07
LastEditors: wdjoys
LastEditTime: 2022-04-24 17:52:41
FilePath: \guahao\src\start.py
Description:

Copyright (c) 2022 by github/wdjoys, All Rights Reserved.
'''

import itertools
import random
import time
from hospital.bjdxdyyy import Robot as Robot_BJDXDYYY
from notification.wechat import send_notification
from settings import ROBOTS
import string


def instantiate_all_hospital_robots():
    '''
    实例化所有采集器
    '''
    robots = []
    all_chars = string.ascii_letters

    for robot_str in ROBOTS:
        u_name = ''.join(random.choice(all_chars) for x in range(8))

        exec_str = f"""from {robot_str['ROBOT_PATH']} import Robot as {u_name}
from settings import {robot_str['CNFS']}
robot = {u_name}({robot_str['CNFS']})
robots.append(robot)"""
        exec(exec_str)

    return robots


def get_hospital_resource_all(robots):
    '''
    获取所有医院的号源
    '''
    resources = []
    for robot in robots:
        resources.append(robot.get_hospital_resource())
    return itertools.chain(*resources)


def run():
    robots = instantiate_all_hospital_robots()

    already_notification = []
    i = 0
    while True:
        resources = get_hospital_resource_all(robots)
        for r in resources:
            if r["enable"] and r['docName']+r['time'] not in already_notification:
                send_notification(r['time'], r['docName'],
                                  r['other_information'])
                already_notification.append(r['docName']+r['time'])
        i += 1
        print(f'完成{i}次检查sleep...')
        time.sleep(10)


if __name__ == '__main__':
    run()
