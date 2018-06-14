import sys
from PyQt5 import QtWidgets, QtGui, QtCore
import socket
from threading import Thread
import json

HOST = "127.0.0.1"
PORT = 33000
lim = 1024
ADDR = (HOST, PORT)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(ADDR)

class sign_in_window(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.UI()

    def UI(self):
        self.sign_in_button = QtWidgets.QPushButton("sign in")
        self.sign_up_button = QtWidgets.QPushButton("sign up")
        self.label1 = QtWidgets.QLabel("Name And Surname")
        self.label2 = QtWidgets.QLabel("Nickname")
        self.label3 = QtWidgets.QLabel("Password")
        self.name_and_surname = QtWidgets.QLineEdit(self)
        self.nick_name = QtWidgets.QLineEdit(self)
        self.password = QtWidgets.QLineEdit(self)

        hor1_box = QtWidgets.QHBoxLayout()
        hor1_box.addWidget(self.label1)
        hor1_box.addWidget(self.name_and_surname)

        hor2_box = QtWidgets.QHBoxLayout()
        hor2_box.addWidget(self.label2)
        hor2_box.addWidget(self.nick_name)

        hor3_box = QtWidgets.QHBoxLayout()
        hor3_box.addWidget(self.label3)
        hor3_box.addWidget(self.password)

        hor_box = QtWidgets.QHBoxLayout()
        hor_box.addWidget(self.sign_up_button)
        hor_box.addWidget(self.sign_in_button)

        ver_layout = QtWidgets.QVBoxLayout()
        ver_layout.addStretch()
        ver_layout.addLayout(hor1_box)
        ver_layout.addLayout(hor2_box)
        ver_layout.addLayout(hor3_box)
        ver_layout.addLayout(hor_box)
        ver_layout.addStretch()
        self.setLayout(ver_layout)

        self.sign_up_button.clicked.connect(self.sign_up)
        self.sign_in_button.clicked.connect(self.sign_in)

    def sign_in(self):
        self.SW = Gui()
        self.SW.show()

    def sign_up(self):
        name_text = self.name_and_surname.text()
        nick_name_text = self.nick_name.text()
        password_text = self.password.text()
        client_socket.send(bytes(name_text+","+nick_name_text+","+password_text, "utf8"))
        self.SW = Gui(name_text,nick_name_text,password_text)
        self.SW.show()

u = "USERS"
texts = "                     CHAT SPACE"

class Gui(QtWidgets.QWidget):
	
    def __init__(self, a, b, c):
        super().__init__()
        self.name = a
        self.passwd = c
        self.nick = b
        self.window()

    def window(self):
        self.l = QtWidgets.QLabel("                               V-O CHAT PROGRAM")
        self.l2 = QtWidgets.QLabel("       USERS")
        self.b = QtWidgets.QPushButton("Enter")
        print(self.name, self.nick, self.passwd)
        self.users_list = QtWidgets.QTextEdit()
        self.users_list.setReadOnly(True)
        self.users_list.setFixedWidth(100)
        self.textBox = QtWidgets.QLineEdit(self)
        self.textBox.returnPressed.connect(self.on_click)
        self.chat = QtWidgets.QTextEdit()
        self.chat.setReadOnly(True)
        self.chat.setText(texts)
        self.chat.setText('insert your name please')
        self.htmlChat = '''
                <p style='color:red;width:100%;' dir='rtl'>bu yazi sagdan sola</p>
                <p style='color:blue;width:100%;' dir='ltr'>bu yazi soldan saga</p>
                '''
        self.chat.setHtml(self.htmlChat)

#        HOST = input('Enter host: ')
#        PORT = input('Enter port: ')
#        if not PORT:
#            PORT = 33000
#        else:
#            PORT = int(PORT)
#        HOST = "127.0.0.1"
#        PORT = 33000
#        self.lim = 1024
#        ADDR = (HOST, PORT)
#        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#        self.client_socket.connect(ADDR)
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
            self.htmlChat2 = """<p style='color:red;width:100%;' dir='rtl'> {}</p>""".format(msg)
            self.chat.append(self.htmlChat2)
            self.textBox.setText("")
            client_socket.send(bytes(msg, "utf8"))
        send()
        self.textBox.setText("")

    def recieve(self):
        while True:
            try:
                msg = client_socket.recv(lim).decode("utf-8")
                if msg[:6] == "USERS!":
                    #self.listWidget1.clear()
                    list_string = msg[6:]
                    name_list = json.loads(list_string)
                    for name in name_list:
                        self.users_list.append(name)
                elif msg[-16:] == "joined the chat!":
                    client_socket.send(bytes("USERS?","utf-8"))
                    self.chat.append(msg)
                else:
                    self.htmlChat1 = """<p style='color:blue;width:100%;' dir='ltr'> {}</p>""".format(msg)
                    self.chat.append(self.htmlChat1)
            except OSError:
                break

    def closeEvent(self, event):
        close = QtWidgets.QMessageBox()
        close.setText("You sure ???")
        close.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.Cancel)
        close = close.exec()
        if close == QtWidgets.QMessageBox.Yes:
            event.accept()
            client_socket.send(bytes("...quit...","utf-8"))
        else:
            event.ignore()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    MW = sign_in_window()
    MW.show()
    sys.exit(app.exec_())
