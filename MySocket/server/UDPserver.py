import threading

import ip
import socket
import configparser

BUFFER_SIZE = 1024


def send_message(client_socket: socket, recv_msg: bytes, addr: tuple):
    """
    打印recv_msg，并向addr发送send_message
    :param client_socket:
    :param recv_msg:
    :param addr:
    :return:
    """

    print("[*] Message: %s\n" % recv_msg.decode())
    # 向客户端返回数据
    send_msg = b"Received your message: " + recv_msg
    client_socket.sendto(send_msg, addr)


def set_udp_server(bind_ip: str, bind_port: int):
    """
    设置一个UDP服务器，返回服务器的socket
    :param bind_ip:
    :param bind_port:
    :return: socket
    """
    # AF_INET：使用标准的IPv4地址或主机名，SOCK_DGRAM：说明这是一个UDP服务器
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind((bind_ip, bind_port))

    return server


if __name__ == '__main__':
    config_obj = configparser.ConfigParser()
    config_obj.read("./config.ini", encoding='utf-8')

    bind_ip = ip.get_host_ip()
    # 将字符串类型的port转换为int
    bind_port = int(config_obj['config']['port'])

    # 设置UDP服务器
    server = set_udp_server(bind_ip, bind_port)

    try:
        while True:
            recv_msg, addr = server.recvfrom(BUFFER_SIZE)
            print("[*] Receive message from ip %s, port is %d\n" % (addr[0], addr[1]))

            # 新线程用于打印以及发送数据，可以改造成更复杂的逻辑
            client_handler = threading.Thread(target=send_message, args=(server, recv_msg, addr))
            client_handler.start()
    except Exception as e:
        raise e
    finally:
        server.close()
