import sys, socket, json
from PyQt5 import QtWidgets, QtGui, QtCore
from threading import Thread

class Gui(QtWidgets.QWidget):
	
    def __init__(self):
        super().__init__()
        HOST = "127.0.0.1"
        PORT = 33000
        self.LIM = 2048
        self.ADDR = (HOST, PORT)
        self.window()

    def window(self):
        self.messages = ""
        self.window_title = QtWidgets.QLabel("V-O CHAT PROGRAM")
        self.send_button = QtWidgets.QPushButton("Send")
        self.sign_in_button = QtWidgets.QPushButton("Sign in")
        self.user_list_widget = QtWidgets.QListWidget()
        print(vars(self.user_list_widget))
        self.user_list_widget.setWindowTitle("asdasd")
        self.user_list_widget.setMinimumWidth(self.user_list_widget.sizeHintForColumn(0)) #setFixedWidth(100)
        self.chat = QtWidgets.QTextEdit()
        self.chat.setReadOnly(True)
        self.message_textbox = QtWidgets.QLineEdit(self)
        self.nick_textbox = QtWidgets.QLineEdit("name")
        self.password_textbox = QtWidgets.QLineEdit("password")


        H_L = QtWidgets.QVBoxLayout()
        H_L.addWidget(self.window_title)
        H_L.addWidget(self.chat)
        H_L.addWidget(self.message_textbox)
        H_L.addWidget(self.send_button)
        H_L_2 = QtWidgets.QVBoxLayout()
        H_L_2.addWidget(self.user_list_widget)
        H_L_2.addWidget(self.nick_textbox)
        H_L_2.addWidget(self.password_textbox)
        H_L_2.addWidget(self.sign_in_button)
        last_layout = QtWidgets.QHBoxLayout()
        last_layout.addLayout(H_L_2)
        last_layout.addLayout(H_L)
        self.setLayout(last_layout)
        self.setWindowTitle('Your lovely massage app')
        self.send_button.clicked.connect(self.on_click)
        self.message_textbox.returnPressed.connect(self.on_click)
        self.sign_in_button.clicked.connect(self.sign_in)
        #self.sign_in_button.clicked.connect(self.recieve)
        quit = QtWidgets.QAction("Quit", self)
        quit.triggered.connect(self.closeEvent)
        #self.show()
    
    def sign_in(self):
        nick_name = self.nick_textbox.text()
        password = self.password_textbox.text()
        #nickname ve password icin gerekli "string" bazli kontroller yapilmali. ornegin bosluk veye tirnak var mi?
        self.connect_server()
        self.client_socket.send(bytes(self.nick_textbox.text() + "," +self.password_textbox.text(),"utf-8"))
        del nick_name, password

    def log_in(self):
        nick_name = self.nick_textbox.text()
        password = self.password_textbox.text()
        self.connect_server()
        self.client_socket.send(bytes(nick_name + "," + password, "utf-8"))

    def on_click(self):
        msg = self.message_textbox.text()
        self.client_socket.send(bytes(msg, "utf-8"))
        self.messages = self.messages + "\n" + "<p dir='rtl' style='color:red;width:100%;' >{}</p>".format(msg)
        self.chat.setHtml(self.messages)
        self.message_textbox.setText("")

    def recieve(self):
        while True:
            try:
                msg = self.client_socket.recv(self.LIM).decode("utf-8")
                if msg[:6] == "USERS!":
                    self.user_list_widget.clear()
                    list_string = msg[6:]
                    name_list = json.loads(list_string)
                    for name in name_list:
                        self.user_list_widget.addItem(name)
                elif msg == "joined the chat!":
                    self.client_socket.send(bytes("USERS?","utf-8"))
                else:
                    self.messages = self.messages + "\n" + "<p dir='ltr' style='color:blue;width:100%;' >{}</p>".format(msg)
                    #self.chat.setHtml(self.messages)
                    #self.chat.setHtml(self.chat.toHtml()+"<p dir='ltr' style='color:red;width:100%;' >"+msg+"</p>")
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
            self.client_socket.close()
        else:
            event.ignore()

    def connect_server(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(self.ADDR)
        Thread(target=self.recieve).start()


#    def thing(self):
#        while True:
#            self.chat.setHtml(self.messages)

app = QtWidgets.QApplication(sys.argv)
a_window = Gui()
#def thread():
#    while True:
#        a_window.chat.setHtml(a_window.thing_list)
a_window.show()
#thread()
sys.exit(app.exec_())
