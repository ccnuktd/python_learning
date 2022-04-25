import socket


def get_host_ip():
    """
    查询本机ip地址
    :return: ip
    """
    socket_obj = None
    try:
        socket_obj = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # http协议端口
        socket_obj.connect(('8.8.8.8', 80))
        host_ip = socket_obj.getsockname()[0]
        # port = socket_obj.getsockname()[1]
    finally:
        socket_obj.close()

    return host_ip


if __name__ == '__main__':
    print(get_host_ip())
