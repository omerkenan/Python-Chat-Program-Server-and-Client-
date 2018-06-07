import sys
from PyQt5 import QtWidgets, QtGui, QtCore
import socket
from threading import Thread
import json

u = "USERS"
texts = "                     CHAT SPACE"

class Gui(QtWidgets.QWidget):
	
    def __init__(self):
        super().__init__()
        self.window()

    def window(self):
        self.l = QtWidgets.QLabel("                               V-O CHAT PROGRAM")
        self.l2 = QtWidgets.QLabel("       USERS")
        self.b = QtWidgets.QPushButton("Enter")

        self.listWidget1 = QtWidgets.QListWidget()
        #u = osman gibi userlari ekleyecek fonk?
        #self.listWidget2 = QtWidgets.QListWidget()
        #self.listWidget2.addItem(texts)
        #self.listWidget2.addItem('insert your name please')
        self.listWidget1.setFixedWidth(100)
        self.textBox = QtWidgets.QLineEdit(self)
        self.textBox.returnPressed.connect(self.on_click)
        self.chat = QtWidgets.QTextEdit()
        self.chat.setReadOnly(True)
        self.chat.setText(texts)
        self.chat.setText('insert your name please')

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
        H_L.addWidget(self.chat)
        H_L.addWidget(self.textBox)
        H_L.addWidget(self.b)

        H_L2 = QtWidgets.QVBoxLayout()
        H_L2.addWidget(self.l2)
        H_L2.addWidget(self.listWidget1)
    
        V_L = QtWidgets.QHBoxLayout()
        V_L.addLayout(H_L2)
        V_L.addLayout(H_L)
    
        self.setLayout(V_L)
        self.setWindowTitle('Your lovely massage app')
        self.setGeometry(500,500,500,500)
        self.b.clicked.connect(self.on_click)
        self.show()
    
    def on_click(self):
        msg = self.textBox.text()
        def send():
            self.textBox.setText("")
            self.client_socket.send(bytes(msg, "utf8"))
        send()
        self.textBox.setText("")

    def recieve(self):
        while True:
            try:
                msg = self.client_socket.recv(self.lim).decode("utf-8")
                if msg[:6] == "USERS!":
                    self.listWidget1.clear()
                    list_string = msg[6:]
                    name_list = json.loads(list_string)
                    for name in name_list:
                        self.listWidget1.addItem(name)
                elif msg[-16:] == "joined the chat!":
                    self.client_socket.send(bytes("USERS?","utf-8"))
                else:
                    self.chat.append(msg)
            except OSError:
                break


app = QtWidgets.QApplication(sys.argv)
a_window = Gui()
sys.exit(app.exec_())
