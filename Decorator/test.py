from mylog import log
import requests


@log
def func1():
    requests.post(url="https://sdf")


@log
def func2():
    return 1 / 0


if __name__ == '__main__':
    func1()
    func2()
