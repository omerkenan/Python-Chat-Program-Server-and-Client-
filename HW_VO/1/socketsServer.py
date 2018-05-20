import sys
import socket

serversocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

host = socket.gethostname()

port = 9999

serversocket.bind((host, port))

serversocket.listen(5)

while True:
    clientsocket,addr = serversocket.accept()

    print("Your ip is %s" % str(addr))

    msg = "Thanks for choosing us ^_^"
    clientsocket.send(msg.encode("urf-8"))
    clientsocket.close()