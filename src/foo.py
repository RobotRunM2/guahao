# -*- coding: utf-8 -*-
# @Author: xiaocao
# @Date:   2023-01-03 17:30:17
# @Last Modified by:   xiaocao
# @Last Modified time: 2023-01-03 17:46:59

import asyncio
import random


async def t1(num: int = None):
    print(f"这是第{num}个，开始执行")

    sleep_time = random.randint(10, 50) / 10
    await asyncio.sleep(sleep_time)
    print(f"这是第{num}个，执行结束")


async def t2():
    task = [asyncio.create_task(t1(i)) for i in range(10)]

    await asyncio.wait(task)


async def main():
    [await t2() for _ in range(10)]

if __name__ == '__main__':
    asyncio.run(main())
