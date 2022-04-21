import functools
import sys
import os
import time


def get_time_path(path='./'):
    """
    生成path路径的txt日志文件，默认生成在当前目录
    :return: 路径字符串
    """

    def get_local_time_str():
        """
        获取日志名称
        :return:
        """
        loca_time = time.localtime()
        return "logfile_" + str(loca_time.tm_year) + "_" + str(loca_time.tm_mon) + "_" + str(loca_time.tm_mday)

    return path + get_local_time_str() + '.txt'


def log(func):
    """
    用来装饰一类没有参数的函数，打印异常日志
    :param func: 被装饰函数
    :return: 装饰后的函数
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as e:
            with open(get_time_path(), mode='a', encoding='utf-8') as f:
                path = os.path.abspath(sys.modules[func.__module__].__file__)
                f.write(f"error log,path=[{path}],error=[{e}]\n")

    return wrapper
