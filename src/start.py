'''
Author: wdjoys
Date: 2022-04-23 12:36:07
LastEditors: wdjoys
LastEditTime: 2022-04-23 16:02:27
FilePath: \guahao\src\start.py
Description: 

Copyright (c) 2022 by github/wdjoys, All Rights Reserved. 
'''

import random
from hospital.bjdxdyyy import Robot as Robot_BJDXDYYY
from settings import ROBOTS
import string

all_chars = string.ascii_letters + string.digits


def run():

    for robot in ROBOTS:
        u_name = ''.join(random.choice(all_chars) for x in range(8))
        'hospital.bjdxdyyy.Robot',
        "from hospital.bjdxdyyy import Robot as Robot_BJDXDYYY"
        robot = eval(robot)
        robot.run()

    robots = []
    robots.append(Robot_BJDXDYYY())
