import socket


def udp_test():
    """
    用来测试udp服务器的客户端请求
    :return:
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # 请求的ip地址，这是一个域名服务器
    request_ip = '192.168.43.118'
    port = 10003
    server_address = (request_ip, port)
    message = "This is the message"

    sock.sendto(message.encode('utf-8'), server_address)
    data, _ = sock.recvfrom(1024)
    print(data.decode())


def tcp_test():
    """
    用来测试tcp服务器的客户端请求
    :return:
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 请求的ip地址，这是一个域名服务器
    request_ip = '192.168.43.118'
    port = 10003
    server_address = (request_ip, port)

    # 连接tcp服务器
    sock.connect(server_address)

    message = "This is the message"
    sock.send(message.encode('utf-8'))
    data = sock.recv(1024)
    print(data.decode())


if __name__ == '__main__':
    tcp_test()
    # udp_test()
