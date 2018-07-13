import sys, socket, json
from threading import Thread
from mysql_dbconfig import read_db_config
from mysql.connector import MySQLConnection, Error


db_config = read_db_config()
conn = MySQLConnection(**db_config)
cursor = conn.cursor(buffered=True)
 
clients = {}
addresses = {}
names = []

HOST = '127.0.0.1'
PORT = 33000
lim = 2048
ADDR = (HOST, PORT)
SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
SERVER.bind(ADDR)

def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#    server_socket.setsockopt(socket.MYSOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(10)

server()

