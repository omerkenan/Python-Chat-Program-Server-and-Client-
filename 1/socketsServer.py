import sys, socket, json
from threading import Thread
import signal
import sys
from mysql_dbconfig import read_db_config
from mysql.connector import MySQLConnection, Error
from pprint import pprint

clients = {}
addresses = {}
names = []

HOST = '127.0.0.1'
PORT = 33000
lim = 2048
ADDR = (HOST, PORT)
SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
SOCKET.bind(ADDR)

def connection():
    while True:
        client, client_address = SOCKET.accept()
        print("{}:{} made connection request.".format(client_address[0],client_address[1])) 
        
        #broadcast(bytes("joined the chat!", "utf-8"))
        
        Thread(target=handle_client, args=(client,)).start()

def handle_client(client):
    info = client.recv(lim).decode("utf-8").split(",")
    name = info[0]
    password = info[1]

    db_first_or_create(name, password)

    print(name)
    clients[client] = name
    client.send(bytes("hiiiiii","utf-8"))
    names.append(clients[client])
    while True:
        try:     
            msg = client.recv(lim)
            print(msg)
            if msg == bytes("USERS?","utf-8"):
                real_list = json.dumps(names)
                string_list = bytes("USERS!","utf-8") + bytes(real_list,"utf-8")
                broadcast(string_list)
            if msg == bytes("...quit...", "utf-8"):
                client.send(bytes("...quit...","utf-8"))
                client.close()
                del clients[client]
                broadcast(bytes("{} has eft the chat.".format(name),"utf-8"))
                break
            else:
                broadcast(msg,name + ": ",exclude=client)
        except OSError:
            break

def broadcast(msg, prefix="",exclude = False):
    for sock in clients:
        if (exclude!=sock):
            sock.send(bytes(prefix, "utf-8")+msg)


def db_first_or_create(nick,password):
    db_config = read_db_config()
    conn = MySQLConnection(**db_config)
    cursor = conn.cursor(buffered=True)

    query1 = "SELECT password FROM info WHERE nick = '%s'" % (nick) 
    query2 = "INSERT INTO info (nick, password) VALUES (%s,%s)"

    cursor.execute(query1)
    data = cursor.fetchall()

    if(len(data)==1):
        if(data[2]==password):
            print(data)
            #login oldu
        else:
            print("boyle bir nick var ama parola yanlis")
            #boyle bir nick var ama parola yanlis
    elif(len(data)>1):
        print("beklenmedik hata")
    else:
        try:
            cursor.execute(query2,(nick,password))
            conn.commit()
            print(cursor.lastrowid)
        except:
            conn.rollback()
        

    # CREATE TABLE IF NOT EXISTS info(
    #    id INT NOT NULL AUTO_INCREMENT,
    #    nick VARCHAR(20) NOT NULL,
    #    password VARCHAR(20) NOT NULL,
    #    PRIMARY KEY ( id )
    # );

    cursor.close()
    conn.close()

def signal_handler(sig, frame):
        print('BYE BYE')
        SOCKET.close()
        sys.exit(0)
if __name__ == "__main__":

    SOCKET.listen(5)  # Listens for 5 connections at max.
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=connection)
    signal.signal(signal.SIGINT, signal_handler)
    ACCEPT_THREAD.start()  # Starts the infinite loop.
    ACCEPT_THREAD.join()
    SOCKET.close()


