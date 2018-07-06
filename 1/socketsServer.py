import sys, socket, json
from threading import Thread
#from mysql_dbconfig import read_db_config
#from mysql.connector import MySQLConnection, Error

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
        broadcast(bytes("joined the chat!", "utf-8"))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()

def handle_client(client):
    info = client.recv(lim).decode("utf-8").split(",")
    name = info[0]
    password = info[1]
#    insert_into_db(name, password)
    print(name)
    clients[client] = name
    names.append(clients[client])
    while True:
        msg = client.recv(lim)
        print(msg)
        if msg == bytes("USERS?","utf-8"):
                real_list = json.dumps(names)
                string_list = bytes("USERS!","utf-8") + bytes(real_list,"utf-8")
                broadcast(string_list)
        elif msg == bytes("quit", "utf-8"):
            client.send(bytes("quit","utf-8"))
            client.close()
            del clients[client]
            broadcast(bytes("{} has left the chat.".format(name),"utf-8"))
            break
        else:
            broadcast(msg, name + ": ", exclude=client)

def broadcast(msg, prefix="",exclude = False):
    for sock in clients:
        if (exclude!=sock):
            sock.send(bytes(prefix, "utf-8")+msg)


#def insert_into_db(nick,password):
#    query = "INSERT INTO info(nick,password) " \
#            "VALUES (%s,%s)"
#    args = (nick,password)
#    
#    try:
#        db_config = read_db_config()
#        conn = MySQLConnection(**db_config)
#        cursor = conn.cursor()
#        cursor.execute(query, args)
#        if cursor.lastrowid:
#            print('last insert id', cursor.lastrowid)
#        else:
#            print('last insert id not found')
#        conn.commit
#    except Error as e:
#        print('Error: ',e)
#    finally:
#        cursor.close()
#        conn.close()

if __name__ == "__main__":
    SERVER.listen(5)  # Listens for 5 connections at max.
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=connection)
    ACCEPT_THREAD.start()  # Starts the infinite loop.
    ACCEPT_THREAD.join()
    SERVER.close()


