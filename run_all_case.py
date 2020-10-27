#!/usr/bin/python
# -*- coding: UTF-8 _*_

import time
import os
import sys
from common.Logs import Log
import pytest
from common import Shell
import allure
from common.emails import mail

RootDir = os.path.abspath('.')                  # 项目路径
AllureData = RootDir + "/report/allure_data/"   # 测试报告allure数据保存路径
AllureHtml = RootDir + "/report/allure_html/"   # 测试报告allure页面保存路径
Worker = 1                                      # 大于1开启多进程
Reruns = 1                                      # 错误重试次数

file = os.path.basename(sys.argv[0])
log = Log(file)
logger = log.Logger

def allur_environment(AllureData):
    '''
    生成environment.properties文件，在allure测试报告界面中显示环境变量
    :param session:
    :return:
    '''
    with open("{}/environment.properties".format(AllureData), "w") as f:
        f.write("browser=chrome\nbackend=staging\ndomain=http://baidu.com")     # FIXME 根据配置文件写入环境变量值

def pytest_main_param():
    """
        pytest.main([RootDir + '/test_case', "--alluredir", AllureData])
        pytest.main([RootDir + '/test_case','-q', "--alluredir", AllureData])  # 精简输出
        pytest.main([RootDir + '/test_case', '-n 4', "--alluredir", AllureData]) # 多进程
        pytest.main([RootDir + '/test_case', '-n 4', "--reruns", "2", "--alluredir", AllureData]) # 多进程 + 错误重试
        pytest.main([RootDir + '/test_case', '-n 4', "--reruns", "2", "-s","--alluredir", AllureData]) # 多进程 + 错误重试 + 输出多进程的print

    :return: pytest.main的执行参数列表
    """
    param = [RootDir + '/test_case']
    if Worker >1:
        param.append('-n')
        param.append(str(Worker))
    if Reruns >1:
        param.append('--reruns')
        param.append(str(Reruns))

    param.append("--alluredir")
    param.append(AllureData)

    return param

def main():
    try:
        print("开始测试")
        logger.info("==================================" + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + "===================================")
        pytest.main(pytest_main_param())
        allur_environment(AllureData)
        print("测试完成")
    except Exception as e:
        logger.error("测试执行失败！", e)
        print("测试执行失败！", e)

    try:
        shell = Shell.Shell()
        cmd = 'allure generate %s -o %s --clean' % (AllureData, AllureHtml)

        print("生成测试报告")
        shell.invoke(cmd)
        print("测试报告生成完毕")
    except Exception as e:
        print("测试报告生成失败，请重新执行", e)
        raise

    # time.sleep(5)
    # mail()

if __name__ == "__main__":
    main()