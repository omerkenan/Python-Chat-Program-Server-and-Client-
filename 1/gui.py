import sys
from PyQt5 import QtWidgets, QtGui, QtCore
import socket
from threading import Thread
import json

class sign_in_window(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.UI()

    def UI(self):
        self.sign_in_button = QtWidgets.QPushButton("sign in")
        self.sign_up_button = QtWidgets.QPushButton("sign up")
        self.name_and_surname_text = QtWidgets.QLineEdit(self)
        self.password = QtWidgets.QLineEdit(self)

        some_layout = QtWidgets.QHBoxLayout()
        some_layout.addWidget(self.name_and_surname_text)
        some_layout.addWidget(self.password)
        some_layout.addWidget(self.sign_up_button)
        some_layout.addWidget(self.sign_in_button)
        self.setLayout(some_layout)

        self.sign_up_button.clicked.connect(self.sign_up)
        self.sign_in_button.clicked.connect(self.sign_in)

    def sign_in(self):
        self.SW = Gui()
        self.SW.show()
        #print("its working")

    def sign_up(self):
        #print("awesome")
        pass

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

        self.users_list = QtWidgets.QTextEdit()
        self.users_list.setReadOnly(True)
        self.users_list.setFixedWidth(100)
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
        H_L2.addWidget(self.users_list)
    
        V_L = QtWidgets.QHBoxLayout()
        V_L.addLayout(H_L2)
        V_L.addLayout(H_L)
    
        self.setLayout(V_L)
        self.setWindowTitle('Your lovely massage app')
        self.setGeometry(500,500,500,500)
        self.b.clicked.connect(self.on_click)

        quit = QtWidgets.QAction("Quit", self)
        quit.triggered.connect(self.closeEvent)
    
    def on_click(self):
        msg = self.textBox.text()
        def send():
            textFormatted = '{:>80}'.format(msg)
            self.chat.append(textFormatted)
            self.textBox.setText("")
            self.client_socket.send(bytes(msg, "utf8"))
        send()
        self.textBox.setText("")

    def recieve(self):
        while True:
            try:
                msg = self.client_socket.recv(self.lim).decode("utf-8")
                if msg[:6] == "USERS!":
                    #self.listWidget1.clear()
                    list_string = msg[6:]
                    name_list = json.loads(list_string)
                    for name in name_list:
                        self.users_list.append(name)
                elif msg[-16:] == "joined the chat!":
                    self.client_socket.send(bytes("USERS?","utf-8"))
                elif msg[:7] == "Welcome":
                    global my_name
                    my_name = msg[7:-46]
                    self.chat.append(msg)
                elif msg[:5] == "HI...":
                    self.chat.append(msg)
                else:
                    msg_name = ""
                    for i in msg:
                        if i == ":":
                            break
                        else:
                            msg_name = msg_name + i
                    if my_name == msg_name:
                        textFormatted = '                               {}'.format(msg)
                        self.chat.append(textFormatted)
                    else:
                        self.chat.append(msg)
            except OSError:
                break

    def closeEvent(self, event):
        close = QtWidgets.QMessageBox()
        close.setText("You sure ???")
        close.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.Cancel)
        close = close.exec()
        if close == QtWidgets.QMessageBox.Yes:
            event.accept()
            self.client_socket.send(bytes("...quit...","utf-8"))
        else:
            event.ignore()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    MW = sign_in_window()
    MW.show()
    sys.exit(app.exec_())
