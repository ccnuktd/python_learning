import ip
import socket
import threading
import configparser

MAX_CONNECT_NUM = 5
BUFFER_SIZE = 1024


def handle_client(client_socket: socket):
    """
    client_socket获取接受的信息，并发送send_message，发送完成后关闭服务
    :param client_socket:
    :return: None
    """
    recv_msg = client_socket.recv(BUFFER_SIZE)

    print("[*] Received: %s\n" % recv_msg.decode())
    # 向客户端返回数据
    send_msg = b"Received your message: " + recv_msg
    client_socket.send(send_msg)

    client_socket.close()


def set_tcp_server(bind_ip: str, bind_port: int):
    """
    设置一个TCP服务器，返回服务器的socket
    :param bind_ip:
    :param bind_port:
    :return: socket
    """

    # AF_INET：使用标准的IPv4地址或主机名，SOCK_STREAM：说明这是一个TCP服务器
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((bind_ip, bind_port))
    # 设置最大连接数
    server.listen(MAX_CONNECT_NUM)
    print("[*] Listening on %s:%d, max connection number is %d.\n" % (bind_ip, bind_port, MAX_CONNECT_NUM))
    return server


if __name__ == '__main__':
    config_obj = configparser.ConfigParser()
    config_obj.read("./config.ini", encoding='utf-8')

    bind_ip = ip.get_host_ip()
    # 将字符串类型的port转换为int
    bind_port = int(config_obj['config']['port'])

    # 设置TCP服务器
    server = set_tcp_server(bind_ip, bind_port)

    try:
        while True:
            handle_socket, addr = server.accept()
            print("[*] Acception connection from ip %s, port is %d" % (addr[0], addr[1]))

            # 开线程处理客户端的请求
            client_handler = threading.Thread(target=handle_client, args=(handle_socket,))
            client_handler.start()
    except Exception as e:
        raise e
    finally:
        if 'handle_socket' in locals():
            handle_socket.close()
        server.close()

