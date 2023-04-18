# -*- coding: utf-8 -*-
# @Author: xiaocao
# @Date:   2023-04-18 16:48:41
# @Last Modified by:   xiaocao
# @Last Modified time: 2023-04-18 21:54:47


import time


class BaseRobot:

    # 已经挂号的标记字典，用于避免段时间内重复提醒
    already_regist = {}

    def is_in_already_regist(self, resourceID) -> bool:
        """
        判断是否已经挂号，返回 True/False
        若没有挂号，则添加到已挂号列表
        添加到列表内的号源，5分钟后会过期

        Args:
            resourceID (_type_): _description_

        Returns:
            _type_: _description_
        """
        '''
        {
            "resourceID":"time"
        }

        '''

        current_time = time.time()

        # 180秒内不重复报警
        if resourceID in self.already_regist.keys() and current_time - self.already_regist[resourceID] < 300:
            return True
        self.already_regist[resourceID] = current_time
        return False

    def to_register(self):
        """执行挂号动作， yeild 出挂号结果
        """
        raise NotImplementedError
