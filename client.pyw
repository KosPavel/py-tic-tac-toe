from PyQt5 import QtWidgets
from socket import *
import socket
import sys
import pickle

class TicTakToe(QtWidgets.QMainWindow):

	def __init__(self):
		super().__init__()
		self.initUI()
		self.symbol = ''
		self.field = ['u', 'u', 'u', 'u', 'u', 'u', 'u', 'u', 'u', '']

	def initUI(self):

		self.window = QtWidgets.QWidget()
		self.window.setWindowTitle("Крестики-нолики")
		self.window.resize(280,200)

		self.btn1 = QtWidgets.QPushButton()
		self.btn2 = QtWidgets.QPushButton()
		self.btn3 = QtWidgets.QPushButton()
		self.btn4 = QtWidgets.QPushButton()
		self.btn5 = QtWidgets.QPushButton()
		self.btn6 = QtWidgets.QPushButton()
		self.btn7 = QtWidgets.QPushButton()
		self.btn8 = QtWidgets.QPushButton()
		self.btn9 = QtWidgets.QPushButton()

		self.btn1.setEnabled(False)
		self.btn2.setEnabled(False)
		self.btn3.setEnabled(False)
		self.btn4.setEnabled(False)
		self.btn5.setEnabled(False)
		self.btn6.setEnabled(False)
		self.btn7.setEnabled(False)
		self.btn8.setEnabled(False)
		self.btn9.setEnabled(False)

		self.btnConnect = QtWidgets.QPushButton()
		self.btnConnect.setText('connect')
		self.btnConnect.clicked.connect(self.connect)

		self.textIP = QtWidgets.QTextEdit()
		self.textPORT = QtWidgets.QTextEdit()

		self.textIP.setText('<center>Enter IP</center>')
		self.textPORT.setText('<center>8000</center>')

		self.gameStatus = QtWidgets.QLabel()
		self.gameStatus.setText('<center></center>')
		
		self.btn1.clicked.connect(self.pushbtn)
		self.btn2.clicked.connect(self.pushbtn)
		self.btn3.clicked.connect(self.pushbtn)
		self.btn4.clicked.connect(self.pushbtn)
		self.btn5.clicked.connect(self.pushbtn)
		self.btn6.clicked.connect(self.pushbtn)
		self.btn7.clicked.connect(self.pushbtn)
		self.btn8.clicked.connect(self.pushbtn)
		self.btn9.clicked.connect(self.pushbtn)

		self.hbox0 = QtWidgets.QHBoxLayout()
		self.hbox0.addWidget(self.textIP)
		self.hbox0.addWidget(self.textPORT)
		self.hbox0.addWidget(self.btnConnect)

		self.hbox1 = QtWidgets.QHBoxLayout()
		self.hbox1.addWidget(self.gameStatus)

		self.hbox2 = QtWidgets.QHBoxLayout()
		self.hbox2.addWidget(self.btn1)
		self.hbox2.addWidget(self.btn2)
		self.hbox2.addWidget(self.btn3)

		self.hbox3 = QtWidgets.QHBoxLayout()
		self.hbox3.addWidget(self.btn4)
		self.hbox3.addWidget(self.btn5)
		self.hbox3.addWidget(self.btn6)

		self.hbox4 = QtWidgets.QHBoxLayout()
		self.hbox4.addWidget(self.btn7)
		self.hbox4.addWidget(self.btn8)
		self.hbox4.addWidget(self.btn9)

		self.vbox = QtWidgets.QVBoxLayout()
		self.vbox.addStretch(1)

		self.vbox.addLayout(self.hbox0)
		self.vbox.addLayout(self.hbox1)
		self.vbox.addLayout(self.hbox2)
		self.vbox.addLayout(self.hbox3)
		self.vbox.addLayout(self.hbox4)

		self.window.setLayout(self.vbox)
		self.window.show()

	def connect(self):
		try:
			for i in range(9):
				self.field[i] = 'u'
			self.field[9] = ''
			self.btn1.setText("")
			self.btn2.setText("")
			self.btn3.setText("")
			self.btn4.setText("")
			self.btn5.setText("")
			self.btn6.setText("")
			self.btn7.setText("")
			self.btn8.setText("")
			self.btn9.setText("")
			host = self.textIP.toPlainText()
			port = int(self.textPORT.toPlainText())
			address = (host, port)
			self.sock = socket.socket(AF_INET, SOCK_STREAM)
			self.sock.connect(address)
			self.btnConnect.setText('Connected')
			self.btnConnect.setEnabled(False)
			self.getinfo()
		except:
			self.gameStatus.setText('<center>connection error</center>')
			self.btnConnect.setEnabled(True)
			self.btnConnect.setText('connect')

	def getinfo(self): #получение игрового символа
		info = (self.sock.recv(1024)).decode('utf-8')
		if info == '1':
			self.symbol = 'X'
			self.gameStatus.setText('<center>you are X, your turn!</center>')
			self.btn1.setEnabled(True)
			self.btn2.setEnabled(True)
			self.btn3.setEnabled(True)
			self.btn4.setEnabled(True)
			self.btn5.setEnabled(True)
			self.btn6.setEnabled(True)
			self.btn7.setEnabled(True)
			self.btn8.setEnabled(True)
			self.btn9.setEnabled(True)
		elif info == '2':
			self.symbol = 'O'
			self.gameStatus.setText('<center>you are O, your turn!</center>')
			self.reseivedata()
		# self.gameStatus.setText('<center>you are'  + self.symbol + ' </center>')

	def pushbtn(self):
		sender = self.sender() #определяется нажатая кнопка
		sender.setText(self.symbol)
		sender.setEnabled(False)
		self.senddata()

	def senddata(self):
		self.packdata() #считываем данные с поля
		pickleddata = pickle.dumps(self.field)
		self.sock.send(pickleddata)
		self.reseivedata()

	#тут ошибка: происходит перезапись кнопок, нажатых соперником на себя
	def packdata(self):
		if self.symbol == 'X':
			if not self.btn1.isEnabled() and (self.field[0] != '2'):
				self.field[0] = '1'
			if not self.btn2.isEnabled() and (self.field[1] != '2'):
				self.field[1] = '1'
			if not self.btn3.isEnabled() and (self.field[2] != '2'):
				self.field[2] = '1'
			if not self.btn4.isEnabled() and (self.field[3] != '2'):
				self.field[3] = '1'
			if not self.btn5.isEnabled() and (self.field[4] != '2'):
				self.field[4] = '1'
			if not self.btn6.isEnabled() and (self.field[5] != '2'):
				self.field[5] = '1'
			if not self.btn7.isEnabled() and (self.field[6] != '2'):
				self.field[6] = '1'
			if not self.btn8.isEnabled() and (self.field[7] != '2'):
				self.field[7] = '1'
			if not self.btn9.isEnabled() and (self.field[8] != '2'):
				self.field[8] = '1'
		elif self.symbol == 'O':
			if not self.btn1.isEnabled() and (self.field[0] != '1'):
				self.field[0] = '2'
			if not self.btn2.isEnabled() and (self.field[1] != '1'):
				self.field[1] = '2'
			if not self.btn3.isEnabled() and (self.field[2] != '1'):
				self.field[2] = '2'
			if not self.btn4.isEnabled() and (self.field[3] != '1'):
				self.field[3] = '2'
			if not self.btn5.isEnabled() and (self.field[4] != '1'):
				self.field[4] = '2'
			if not self.btn6.isEnabled() and (self.field[5] != '1'):
				self.field[5] = '2'
			if not self.btn7.isEnabled() and (self.field[6] != '1'):
				self.field[6] = '2'
			if not self.btn8.isEnabled() and (self.field[7] != '1'):
				self.field[7] = '2'
			if not self.btn9.isEnabled() and (self.field[8] != '1'):
				self.field[8] = '2'

	def reseivedata(self):
		self.gameStatus.setText('<center>you are ' + self.symbol + ', wait for your turn! </center>')
		# кнопки отключены на период ожидания
		self.btn1.setEnabled(False)
		self.btn2.setEnabled(False)
		self.btn3.setEnabled(False)
		self.btn4.setEnabled(False)
		self.btn5.setEnabled(False)
		self.btn6.setEnabled(False)
		self.btn7.setEnabled(False)
		self.btn8.setEnabled(False)
		self.btn9.setEnabled(False)

		pickleddata = self.sock.recv(1024)
		data = pickle.loads(pickleddata)

		#конец игры / учёт хода соперника
		for i in range(10):
			self.field[i] = data[i]

		#как сделать ссылку на метод? чтобы ввести цикл и уменьшить код
		if self.field[0] == 'u':
			self.btn1.setEnabled(True)
		elif self.field[0] == '1':
			self.btn1.setText('X')
		elif self.field[0] == '2':
			self.btn1.setText('O')
		if self.field[1] == 'u':
			self.btn2.setEnabled(True)
		elif self.field[1] == '1':
			self.btn2.setText('X')
		elif self.field[1] == '2':
			self.btn2.setText('O')
		if self.field[2] == 'u':
			self.btn3.setEnabled(True)
		elif self.field[2] == '1':
			self.btn3.setText('X')
		elif self.field[2] == '2':
			self.btn3.setText('O')
		if self.field[3] == 'u':
			self.btn4.setEnabled(True)
		elif self.field[3] == '1':
			self.btn4.setText('X')
		elif self.field[3] == '2':
			self.btn4.setText('O')
		if self.field[4] == 'u':
			self.btn5.setEnabled(True)
		elif self.field[4] == '1':
			self.btn5.setText('X')
		elif self.field[4] == '2':
			self.btn5.setText('O')
		if self.field[5] == 'u':
			self.btn6.setEnabled(True)
		elif self.field[5] == '1':
			self.btn6.setText('X')
		elif self.field[5] == '2':
			self.btn6.setText('O')
		if self.field[6] == 'u':
			self.btn7.setEnabled(True)
		elif self.field[6] == '1':
			self.btn7.setText('X')
		elif self.field[6] == '2':
			self.btn7.setText('O')
		if self.field[7] == 'u':
			self.btn8.setEnabled(True)
		elif self.field[7] == '1':
			self.btn8.setText('X')
		elif self.field[7] == '2':
			self.btn8.setText('O')
		if self.field[8] == 'u':
			self.btn9.setEnabled(True)
		elif self.field[8] == '1':
			self.btn9.setText('X')
		elif self.field[8] == '2':
			self.btn9.setText('O')

		self.gameStatus.setText('<center>your turn, ' + self.symbol + '!</center>')

		print(self.field) #для отладки
		self.checkEndGame()

	def checkEndGame(self):
		if self.field[9] == self.symbol:
			print(self.field[9]) #для отладки
			self.gameStatus.setText('<center>you win!</center>')
			self.btnConnect.setEnabled(True)
			self.btnConnect.setText('connect')
			self.btn1.setEnabled(False)
			self.btn2.setEnabled(False)
			self.btn3.setEnabled(False)
			self.btn4.setEnabled(False)
			self.btn5.setEnabled(False)
			self.btn6.setEnabled(False)
			self.btn7.setEnabled(False)
			self.btn8.setEnabled(False)
			self.btn9.setEnabled(False)
			self.sock.close()
		elif (self.field[9] != self.symbol) and (self.field[9] != 'd') and (self.field[9] != ''):
			self.gameStatus.setText('<center>you lost!</center>')
			self.btnConnect.setEnabled(True)
			self.btnConnect.setText('connect')
			self.btn1.setEnabled(False)
			self.btn2.setEnabled(False)
			self.btn3.setEnabled(False)
			self.btn4.setEnabled(False)
			self.btn5.setEnabled(False)
			self.btn6.setEnabled(False)
			self.btn7.setEnabled(False)
			self.btn8.setEnabled(False)
			self.btn9.setEnabled(False)
			self.sock.close()
		elif self.field[9] == 'd':
			self.gameStatus.setText('<center>draw!</center>')
			self.btnConnect.setEnabled(True)
			self.btnConnect.setText('connect')
			self.sock.close()


if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	game = TicTakToe()
	sys.exit(app.exec_())