import sys
import socket
from threading import Thread

clients = {}
addresses = {}
names = []

HOST = '127.0.0.1'
PORT = 33000
lim = 1024
ADDR = (HOST, PORT)
SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
SERVER.bind(ADDR)

def connection():
    while True:
        client, client_address = SERVER.accept()
        print("{}:{} has connected.".format(client_address[0],client_address[1]))
        client.send(bytes("HI..."+
                          "Now type your name and press enter! note that your name can only have 5 letters", "utf8"))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()

def handle_client(client):
    name = client.recv(lim).decode("utf8")
    welcome = 'Welcome {}! if you ever want to quit, type quit to exit.'.format(name)
    client.send(bytes(welcome, "utf8"))
    msg = "{} has joined the chat!".format(name)
    broadcast(bytes(msg,"utf8"))
#    broadcast(bytes(name,"utf8"),">")
    clients[client] = name
    #names.append(clients[client])
    while True:
        msg = client.recv(lim)
        if msg != bytes('quit',"utf8"):
#            if msg == bytes(name,"utf8"):
#                send_names(bytes(name,"utf8"),">")
#            else:
#                broadcast(msg,name+": ")
            broadcast(msg,name+": ")
        else:
            client.send(bytes("quit","utf8"))
            client.close()
            del clients[client]
            broadcast(bytes("{} has eft the chat.".format(name),"utf8"))
            break

def broadcast(msg, prefix=""):
    for sock in clients:
        sock.send(bytes(prefix, "utf8")+msg)

#def send_names(name,prefix=">"):
#    for sock in clients:
#        sock.send(bytes(prefix, "utf8")+name)


if __name__ == "__main__":
    SERVER.listen(5)  # Listens for 5 connections at max.
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=connection)
    ACCEPT_THREAD.start()  # Starts the infinite loop.
    ACCEPT_THREAD.join()
    SERVER.close()


