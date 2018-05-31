import sys
import socket
from threading import Thread
import json

clients = {}
addresses = {}
names = []

HOST = '127.0.0.1'
PORT = 33000
lim = 2048
ADDR = (HOST, PORT)
SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
SERVER.bind(ADDR)

def connection():
    while True:
        client, client_address = SERVER.accept()
        print("{}:{} has connected.".format(client_address[0],client_address[1])) 
        client.send(bytes("HI..."+
                          "Now type your name and press enter!", "utf-8"))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()

def handle_client(client):
    name = client.recv(lim).decode("utf-8")
    welcome = 'Welcome {}! if you ever want to quit, type quit to exit.'.format(name)
    client.send(bytes(welcome, "utf-8"))
    msg = "{} has joined the chat!".format(name)
    broadcast(bytes(msg,"utf-8"))
    clients[client] = name
    names.append(clients[client])
    while True:
        msg = client.recv(lim)
        if msg != bytes('quit',"utf-8"):
            if msg == bytes("USERS?","utf-8"):
                real_list = json.dumps(names)
                string_list = bytes("USERS!","utf-8") + bytes(real_list,"utf-8")
                broadcast(string_list)
            else:
                broadcast(msg,name + ": ")
        else:
            client.send(bytes("quit","utf-8"))
            client.close()
            del clients[client]
            broadcast(bytes("{} has eft the chat.".format(name),"utf-8"))
            break

def broadcast(msg, prefix=""):
    for sock in clients:
        sock.send(bytes(prefix, "utf-8")+msg)


if __name__ == "__main__":
    SERVER.listen(5)  # Listens for 5 connections at max.
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=connection)
    ACCEPT_THREAD.start()  # Starts the infinite loop.
    ACCEPT_THREAD.join()
    SERVER.close()


