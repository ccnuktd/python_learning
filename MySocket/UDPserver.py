# UDPserver.py

# UDP版本
import socket
import get_ip
import configparser

config = configparser.ConfigParser()
config.read("./config.ini", encoding='utf-8')

port = int(config.items('config')[0][1])
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind((get_ip.get_host_ip(), port))
num = 0
while True:

    msg, addr = server.recvfrom(1024)
    msg = msg.decode("utf-8")
    if not msg:
        break
    num = num + 1
    print(msg, num)

    server.sendto(bytes("收到!".encode('utf-8')), addr)

server.close()
