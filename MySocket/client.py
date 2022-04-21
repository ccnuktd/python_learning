import socket
import sys

# 创建一个UTP报文
# 注意TCP的报文格式为SOCK_STREAM，UTP为SOCK_DGRAM
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 请求的ip地址，这是一个域名服务器
request_ip = '8.8.8.8'
port = 1111
server_address = (request_ip, port)
message = 'This is the message.  It will be repeated.'

sock.sendto(bytes(message.encode('utf-8')), server_address)


