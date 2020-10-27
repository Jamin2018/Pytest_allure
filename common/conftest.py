
def pytest_sessionfinish(session):
    '''
    在Pytest中，有一个hook函数叫作pytest_sessionfinish，根据官方文档的描述，这个函数是在整个测试完成后被调用的，我们可以在其内部实现我们自己的逻辑。

    生成文件在allure显示环境变量
    :param session:
    :return:
    '''
    print("pytest_sessionfinish")
    with open("{}/report/reportallure/environment.properties".format(session.config.rootdir), "w") as f:
        f.write("browser=chrome123\nbackend=staging\ndomain=http://baidu.com")     # FIXME 根据配置文件写入环境变量值