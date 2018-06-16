import sys
import socket
import threading
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
        #for thread in threading.enumerate():
            #print(thread.name)

def handle_client(client):
    users_info = client.recv(lim).decode("utf-8").split(",")
    name = users_info[1]
#    welcome ='Welcome {}! if you ever want to quit, type quit to exit.'.format(name)
#    client.send(bytes(welcome, "utf-8"))
#    msg = "{} has joined the chat!".format(name)
#    broadcast(bytes(msg,"utf-8"))
    clients[client] = name
    names.append(clients[client])
    while True:
        msg = client.recv(lim)
        print(msg)
        a = msg.decode("utf-8")[:12] 
        print(a)
        if msg != bytes('...quit...',"utf-8"):
            if msg == bytes("USERS?","utf-8"):
                real_list = json.dumps(names)
                string_list = bytes("USERS!","utf-8") + bytes(real_list,"utf-8")
                broadcast(string_list)
            else:
                broadcast(bytes(name + ":","utf-8") + msg,exclude=client)
        else:
            #client.send(bytes("quit","utf-8"))
            for i in names:
                a = 0
                if i != clients[client]:
                    a += 1
                else:
                    del names[a]
            client.close()
            del clients[client]
            broadcast(bytes("{} has left the chat.".format(name),"utf-8"))
            real_list = json.dumps(names)
            string_list = bytes("USERS!","utf-8") + bytes(real_list,"utf-8")
            broadcast(string_list)
            break

def broadcast(msg, prefix="",exclude=False):
    for sock in clients:
        if (exclude!=sock):
            sock.send(bytes(prefix, "utf-8")+msg)

def people(people_file):
    pass

if __name__ == "__main__":
    SERVER.listen(5)  # Listens for 5 connections at max.
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=connection)
    ACCEPT_THREAD.start()  # Starts the infinite loop.
    ACCEPT_THREAD.join()
    SERVER.close()