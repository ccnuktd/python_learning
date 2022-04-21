import socket
import sys

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ('192.168.43.185', 1111)
message = 'This is the message.  It will be repeated.'

sock.sendto(bytes(message.encode('utf-8')), server_address)

#
# data, server = sock.recvfrom(4096)
# print(data.decode("utf-8"))
# sock.close()
