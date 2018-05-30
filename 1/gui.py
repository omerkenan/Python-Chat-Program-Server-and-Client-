import sys
from PyQt5 import QtWidgets, QtGui, QtCore
#from PyQt5.QtWidgets import	*
import socket
from threading import Thread
import pickle

u = "USERS"
texts = "                     CHAT SPACE"

class Gui(QtWidgets.QWidget):
	
    def __init__(self):
        super().__init__()
        self.window()

    def window(self):
        self.l = QtWidgets.QLabel("                  V-O CHAT PROGRAM")
        self.b = QtWidgets.QPushButton("Enter")

        self.listWidget1 = QtWidgets.QListWidget()
        self.listWidget1.addItem(u) #u = osman gibi userlari ekleyecek fonk?
        self.listWidget2 = QtWidgets.QListWidget()
        self.listWidget2.addItem(texts)
        self.listWidget2.addItem('insert your name please')
        self.listWidget1.setFixedWidth(100)
        self.textBox = QtWidgets.QLineEdit(self)

#        HOST = input('Enter host: ')
#        PORT = input('Enter port: ')
#        if not PORT:
#            PORT = 33000
#        else:
#            PORT = int(PORT)
        HOST = "127.0.0.1"
        PORT = 33000
        self.lim = 1024
        ADDR = (HOST, PORT)
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(ADDR)       
        self.receive_thread = Thread(target=self.recieve)
        self.receive_thread.start()
        
        #H_L is horizontel layout and V_L is vertical layout
        H_L = QtWidgets.QVBoxLayout()
        H_L.addWidget(self.l)
        H_L.addWidget(self.listWidget2)
        H_L.addWidget(self.textBox)
        H_L.addWidget(self.b)
    
        V_L = QtWidgets.QHBoxLayout()
        V_L.addWidget(self.listWidget1)
        V_L.addLayout(H_L)
    
        self.setLayout(V_L)
        self.setWindowTitle('Your lovely massage app')
        self.b.clicked.connect(self.on_click)
        self.show()
    
    def on_click(self):
        msg = self.textBox.text()
        def send():
            self.textBox.setText("")
            self.client_socket.send(bytes(msg, "utf8"))
            if msg == "USERS?":
                self.client_socket.send(bytes(msg,"utf8"))
        send()
        self.textBox.setText("")

    def recieve(self):
        while True:
            try:
                msg = self.client_socket.recv(self.lim)
                if pickle.loads(msg[:6]) == "USERS!":
                    self.listWidget1.addItem(msg[6:])
                else:
                    self.listWidget2.addItem(msg.decode("utf-8")) 
            except OSError:
                break

    def ask_name(self):
        while True:
            try:
                question = "" 
                self.client_socket.send(bytes(name, "utf8"))
            except OSError:
                break

app = QtWidgets.QApplication(sys.argv)
a_window = Gui()
sys.exit(app.exec_())
