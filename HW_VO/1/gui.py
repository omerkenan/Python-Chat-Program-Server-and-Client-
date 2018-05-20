import sys
from PyQt5 import QtWidgets, QtGui, QtCore
#from PyQt5.QtWidgets import	*

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
		self.listWidget1.setFixedWidth(100)
		self.textBox = QtWidgets.QLineEdit(self)
		
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

		self.show()


app = QtWidgets.QApplication(sys.argv)
a_window = Gui()
sys.exit(app.exec_())