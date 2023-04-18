# -*- coding: utf-8 -*-
# @Author: xiaocao
# @Date:   2023-04-18 16:43:10
# @Last Modified by:   xiaocao
# @Last Modified time: 2023-04-18 18:43:29


# 北大医院宁夏儿童医院


from requests import Session
from hospital.common import BaseRobot


class Robot(BaseRobot):

    def __init__(self, cnfs):
        # 模拟浏览器配置相关
        self.session = Session()
        self.session.headers.update(cnfs['headers'])
        cookies_dict = {cookie.split("=")[0]: cookie.split(
            "=")[1] for cookie in cnfs['cookies'].split("; ")}
        self.session.cookies.update(cookies_dict)
        # 医生id
        self.docCodes = cnfs['docCodes']

    def getDocterSched(self):
        # 推出可以挂号的医生排班id schId
        for docCode in self.docCodes:
            res = self.session.post(url="http://36.103.228.223:7070/visualizedPlatformtest/reservation/getDoctor", data={"requestStr": """{"account": "wechat", "password": "wechat2018", "param": {
                                    "docName": "", "depId": "40283c788004b6f2018370dee9047142", "patientFlow": "40283c7783c0003b0183c11921a91bc9", "hosCode": "10003", "startDate": "2023-04-18", "endDate": "2023-04-24", "isWithSchedule": "1", "isScheduleDoctor": "1"}}"""})
            OrderDocSources = res.json()
            for schedule in OrderDocSources['record'][0]['scheduleList']:
                if schedule['schState'] == '0':
                    yield schedule['schId']

    def getSchedSurplusCode(self, schId):
        # 根据排班查余号
        res = self.session.post(url="http://36.103.228.223:7070/visualizedPlatformtest/reservation/sysnoSchedule", data={
                                "requestStr": f"""{{"account":"wechat","password":"wechat2018","param":{{"scheduleid":"{schId}"}}}}"""})
        result = res.json()

        for section in result["data"]['section']:
            if section['segState'] != "1":
                yield {
                    "time": section['secCode'],
                    "docName": result["data"]['docName'],
                    "other_information": ''
                }
            else:
                print(section['secCode'], '没有号')

    def to_register(self):
        for schId in self.getDocterSched():
            yield from self.getSchedSurplusCode(schId)


if __name__ == "__main__":
    r = Robot
