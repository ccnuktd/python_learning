import os
import random

root_path = "pictures/"


def get_file_path(file_name):
    """
    通过文件名称获取文件路径
    :param file_name:
    :return:
    """
    return root_path + file_name


def save_file(response, file_name):
    """
    将response中的图片以文件形式保存
    :param response:
    :param path:
    :param file_name:
    :return:
    """
    try:
        with open(root_path + file_name, 'wb') as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
            f.close()
    except IOError as e:
        raise e


def get_random_picture():
    """
    从图片目录随机选取一个图，返回文件名
    :return: str
    """
    file_list = os.listdir(root_path)
    if len(file_list) == 0:
        raise IndexError
    random_file = random.choice(file_list)
    # print(random_file)
    return random_file
