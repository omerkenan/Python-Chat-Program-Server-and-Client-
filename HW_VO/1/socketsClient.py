import sys
import socket

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM) #our socket object

host = socket.gethostname()

port = 9999

s.connect((host, port)) #connection hostname on the port

msg = s.recv(2048) #2048 bytes message limit

s.close()

print(msg.decode('urf-8'))