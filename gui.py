import sys
from PyQt5 import QtWidgets, QtGui, QtCore
#from PyQt5.QtWidgets import	*

u = "users"
texts = "texts"
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

		self.listWidget1 = QtWidgets.QListWidget()
		self.listWidget1.addItem(u) #u = osman gibi userlari ekleyecek fonk?
		self.listWidget2 = QtWidgets.QListWidget()
		self.listWidget2.addItem(texts)
		self.textBox = QtWidgets.QLineEdit(self)


		vertical_layout = QtWidgets.QVBoxLayout()
		vertical_layout.addStretch()
		vertical_layout.addWidget(self.listWidget2)
		vertical_layout.addWidget(self.textBox)
		vertical_layout.addStretch()

		
		horizontal_layout = QtWidgets.QHBoxLayout()
		horizontal_layout.addStretch()
		horizontal_layout.addLayout(vertical_layout)
		horizontal_layout.addWidget(self.listWidget1)
		horizontal_layout.addStretch()

		self.setLayout(vertical_layout)
		self.setWindowTitle('Your lovely massage app')

		self.show()


app = QtWidgets.QApplication(sys.argv)
a_window = Gui()
sys.exit(app.exec_())