import sys
from PyQt5 import QtWidgets, QtGui, QtCore
#from PyQt5.QtWidgets import	*
import socket

u = "USERS"
texts = "                     CHAT SPACE"

class Gui(QtWidgets.QWidget):
	
    def __init__(self):
        super().__init__()
        #self.top = 10
        #self.left = 10
        #self.widht = 400
        #self.height = 330
        self.window()
    
    def window(self):
        #self.setGeometry(self.left, self.top, self.width, self.height)
        self.l = QtWidgets.QLabel("                  V-O CHAT PROGRAM")
        self.b = QtWidgets.QPushButton("Enter")
    
        self.listWidget1 = QtWidgets.QListWidget()
        self.listWidget1.addItem(u) #u = osman gibi userlari ekleyecek fonk?
        self.listWidget2 = QtWidgets.QListWidget()
        self.listWidget2.addItem(texts)
        self.listWidget2.addItem('insert your name please')
        self.listWidget1.setFixedWidth(100)
        self.textBox = QtWidgets.QLineEdit(self)
        
        action = QtWidgets.QAction(self)
        action.setShortcut(QtGui.QKeySequence("W"))
        self.connect(action, QtCore.SIGNAL("activated()"), self.pushButtonForward, QtCore.SLOT("animateClick()"))
        self.addAction(action)

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
    
#    def bind(self):
#        try:
#            s.bind((host, port))
#        except socket.error as e:
#            listWidget2.addItem(str(e))
    def on_click(self): # this and on_enter function will be unnecessary we should  put these in the send function
        textboxValue = self.textBox.text()
        self.listWidget2.addItem(textboxValue)
        self.textBox.setText("")

    def on_enter(self): # this one needs some pyqt knowledge the idea is when you press enter key it sould trigger our button
        textboxValue = self.textBox.text()

    def recieve(self):  # it puts massages into the listWidget2
        while True:
            try:
                msg = client_socket.recv(lim).decode("utf8")
                self.listWidget2.addItem(msg)
            except OSError:
                break

    def send(evsent): # problem is i couldnt make the program stop
        msg = self.textBox.text()
        self.textBox.setText("")
        client_socket.send(bytes(msg, "utf8"))
        if msg == "{quit}":
            client_socket.close()
            #?????sys.exit(app.exec_())

#try:
#    s.bind((host, port))
#except socket.error as e:
#    print(str(e))
#
#s.listen(5)
#
#def threaded_client(conn):
#    conn.send(str.encode("Hi, type your info\n"))
#
#    while True:
#        data = conn.recv(2048)
#        reply = 'server output: '+ data.decode('utf-8')
#        if not data:
#            break
#        conn.sendall(str.encode(reply))
#    conn.close()
#
#while True:
#    conn, addr = s.accept()
#    print('connected to: '+addr[0]+':'+str(addr[1]))
#    start_new_thread(threaded_client, (conn,))


app = QtWidgets.QApplication(sys.argv)
a_window = Gui()
sys.exit(app.exec_())
