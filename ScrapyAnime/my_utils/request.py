from threading import Thread
from fake_useragent import UserAgent
import utils
import requests
import json

root_path = '../pictures/'
ua = UserAgent()


class WorkThread(Thread):
    """
    request请求的线程调用
    """
    def __init__(self, desc, message):
        super(WorkThread, self).__init__()
        self.desc = desc
        self.message = message

    def run(self):
        self.result = download_picture(self.desc, self.message)

    def get_result(self):
        return self.result


def request_get_download(url, pic_name):
    """
    通过url下载图片，并按照pic_name保存
    :param url:
    :param pic_name:
    :return:
    """
    # 伪造随机请求头
    headers = {
        "UserAgent": ua.random  # 随机取出一个UserAgent
    }
    try:
        # 发送get请求
        response = requests.get(url, headers=headers, timeout=10)
        # 检查图片是否完整
        if response.status_code == 200:
            if 'Content-Length' in response.headers:
                if len(response.content) == int(response.headers['Content-Length']):
                    utils.save_file(response, pic_name)
                    return True
            elif 'Transfer-Encoding' in response.headers:
                utils.save_file(response, pic_name)
                return True
        else:
            return False
    except (TimeoutError, IOError):
        return False


def get_pic_name(url):
    """
    获取url中图片名称[最后15个字母为图片名称]
    :param url:
    :return: str
    """
    return url[-15:]


def get_img_url(r18, tags):
    """
    api: https://api.lolicon.app/setu/v2
    获取图片url
    :return: url or None
    """
    # 构造get请求头
    api = "https://api.lolicon.app/setu/v2?r18=" + str(r18)
    for tag in tags:
        api += "&" + tag

    try:
        # 伪造随机请求头
        headers = {
            "UserAgent": ua.random  # 随机取出一个UserAgent
        }
        # 发送get请求
        response = requests.get(api, headers=headers, timeout=3)
        # 获取图片链接
        if response.status_code == 200:
            content = json.loads(response.content)
            url = content["data"][0]["urls"]["original"]
            print("图片链接: " + url)
            return url
        else:
            return None
    except TimeoutError:
        return None


def download_picture(r18, tags):
    """
    通过给定的r18和tags描述下载图片，返回图片名称
    :param r18:
    :param tags:
    :return:
    """
    pic_num = 1
    while True:
        url = get_img_url(r18, tags)
        pic_name = get_pic_name(url)
        if url is not None and request_get_download(url, pic_name):
            print(pic_name + " downloaded!")
            break
        else:
            print("第" + str(pic_num) + "此请求的图片损坏")
            pic_num += 1
    return pic_name


if __name__ == "__main__":
    r18 = 2
    diff_tags = [["白丝"], ["女仆"], ["黑丝"], ["萝莉"], ["少女"], ["贫乳"], ["傲娇"], ["可爱"], ["妹妹"], ["姐姐"]]
    pic_num = 1
    try:
        while True:
            tags = diff_tags[pic_num % 10]
            r18 = (r18 * pic_num) % 3
            download_picture(r18, tags)
            pic_num += 1
    except KeyboardInterrupt:
        print("爬取总数：" + str(pic_num))
