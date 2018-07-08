import sys, socket, json
from PyQt5 import QtWidgets, QtGui, QtCore
from threading import Thread

class Gui(QtWidgets.QWidget):
	
    def __init__(self):
        super().__init__()
        self.window()

    def window(self):
        self.thing_list = ""
        self.l = QtWidgets.QLabel("                  V-O CHAT PROGRAM")
        self.b = QtWidgets.QPushButton("Enter")
        self.sign_in_button = QtWidgets.QPushButton("sign in")
        self.listWidget1 = QtWidgets.QListWidget()
        self.listWidget1.addItem("USERS") #u = osman gibi userlari ekleyecek fonk?
        self.chat = QtWidgets.QTextEdit()
        self.chat.setReadOnly(True)
        self.listWidget1.setFixedWidth(100)
        self.textBox = QtWidgets.QLineEdit(self)
        self.nick_box = QtWidgets.QLineEdit("name")
        self.password_box = QtWidgets.QLineEdit("password")
        self.nick_box = QtWidgets.QLineEdit("nick")
        self.password_box = QtWidgets.QLineEdit("password")

        HOST = "127.0.0.1"
        PORT = 33000
        self.lim = 2048
        ADDR = (HOST, PORT)
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(ADDR)
        self.receive_thread = Thread(target=self.recieve)
        self.receive_thread.start()
#        self.thing_thread = Thread(target = self.thing)
#        self.thing_thread.start()

        H_L = QtWidgets.QVBoxLayout()
        H_L.addWidget(self.l)
        H_L.addWidget(self.chat)
        H_L.addWidget(self.textBox)
        H_L.addWidget(self.b)
        H_L_2 = QtWidgets.QVBoxLayout()
        H_L_2.addWidget(self.nick_box)
        H_L_2.addWidget(self.password_box)
        H_L_2.addWidget(self.sign_in_button)
        V_L = QtWidgets.QVBoxLayout()
        V_L.addWidget(self.listWidget1)
        V_L.addLayout(H_L_2)
        last_layout = QtWidgets.QHBoxLayout()
        last_layout.addLayout(V_L)
        last_layout.addLayout(H_L)
        self.setLayout(last_layout)
 
        self.setWindowTitle('Your lovely massage app')
        self.b.clicked.connect(self.on_click)
        self.textBox.returnPressed.connect(self.on_click)
        self.sign_in_button.clicked.connect(self.sign_in)
        #self.sign_in_button.clicked.connect(self.recieve)
        quit = QtWidgets.QAction("Quit", self)
        quit.triggered.connect(self.closeEvent)
        #self.show()
    
    def sign_in(self):
        nick_name = self.nick_box.text()
        password = self.password_box.text()
        self.client_socket.send(bytes(nick_name + "," +password,"utf-8"))
        #self.client_socket.send(bytes(nick_name+","+password,"utf-8"))
        del nick_name, password
    
    def on_click(self):
        msg = self.textBox.text()
        self.client_socket.send(bytes(msg, "utf-8"))
        self.thing_list = self.thing_list + "\n" + "<p dir='rtl' style='color:red;width:100%;' >{}</p>".format(msg)
        self.chat.setHtml(self.thing_list)
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
                elif msg == "joined the chat!":
                    self.client_socket.send(bytes("USERS?","utf-8"))
                else:
                    self.thing_list = self.thing_list + "\n" + "<p dir='ltr' style='color:blue;width:100%;' >{}</p>".format(msg)
                    #self.chat.setHtml(self.thing_list)
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
        else:
            event.ignore()

#    def thing(self):
#        while True:
#            self.chat.setHtml(self.thing_list)

app = QtWidgets.QApplication(sys.argv)
a_window = Gui()
#def thread():
#    while True:
#        a_window.chat.setHtml(a_window.thing_list)
a_window.show()
#thread()
sys.exit(app.exec_())
