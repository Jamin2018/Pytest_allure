#!/usr/bin/python
# -*- coding: UTF-8 _*_

import pytest
import allure
import json
import requests
import urllib.parse

from common.ReadExcel import readExcel

file_path = './test_data/caseExcel.xlsx'
sheet_name = 'case'
readExcel = readExcel(file_path, sheet_name)
parametrize = readExcel.get_parametrize()
# 单个参数的情况

@pytest.mark.parametrize('parametrize', parametrize)
@allure.description("excel数据驱动 api 接口")
@allure.testcase("http://calapi.51jirili.com/config/common", "测试用例地址 👇")
class TestHyperx(object):

    def setParameters(self, parametrize):
        """
        set params
        :param case_name:
        :param path
        :param query
        :param method
        :return:
        """
        self.case_name = parametrize[0]
        self.path = parametrize[1]
        self.query = parametrize[2]
        self.method = parametrize[3]
        self.headers = json.loads(parametrize[4])

    def test_run(self, parametrize):
        self.setParameters(parametrize)
        self.checkResult()

    def checkResult(self):
        print(self.path)
        url1 = "?"
        new_url = url1 + self.query
        data1 = dict(urllib.parse.parse_qsl(
            urllib.parse.urlsplit(new_url).query))  # 将一个完整的URL中的name=&pwd=转换为{'name':'xxx','pwd':'bbb'}

        url = self.path
        if self.method == 'get':
            url = self.path + "?" + self.query
            res = requests.get(url, headers=self.headers)
            if res.status_code != 200:
                pass
                # assert False
        elif self.method == 'post':
            res = requests.post(url, data=data1, headers=self.headers)
            if res.status_code != 200:
                pass
                # assert False


if __name__ == '__main__':
    print(parametrize)
    print(len(parametrize))
