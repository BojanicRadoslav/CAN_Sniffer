from PyQt5 import QtWidgets, QtCore, QtGui, uic
from PyQt5.QtGui import  QPixmap
import serial

encoding = "ASCII"
filtering_mode = "except"
addr_min = 0
addr_max = 0
baudrate = 0
filtering_enabled = False
filtering_base = "HEX"

try:
	f = open("encoding.txt", "r")
	encoding = f.read()
	print(encoding)
	f.close()
except:
	f = open("encoding.txt", "w")
	f.write("ASCII")
	f.close()
try:
	f = open("filtering_mode.txt", "r")
	filtering_mode = f.read()
	print(filtering_mode)
	f.close()

except:
	f = open("filtering_mode.txt", "w")
	f.write("except")
	f.close()

try:
	f = open("addr_min.txt", "r")
	addr_min = int(f.read())
	print(addr_max)
	f.close()

except:
	f = open("addr_min.txt", "w")
	f.write("0")
	f.close()

try:
	f = open("addr_max.txt", "r")
	addr_max = int(f.read())
	print(addr_max)
	f.close()
except:
	f = open("addr_max.txt", "w")
	f.write("0")
	f.close()

try:
	f = open("baudrate.txt", "r")
	baudrate = f.read()
	print(baudrate)
	f.close()
except:
	f = open("baudrate.txt", "w")
	f.write("5KBPS")
	f.close()

try:
	f = open("filtering_enabled.txt", "r")
	filtering_enabled_temp = int(f.read())
	if(filtering_enabled_temp == 1):
		filtering_enabled = True
	else:
		filtering_enabled = False

	print(filtering_enabled)
	f.close()
except:
	f = open("filtering_enabled.txt", "w")
	f.write("0")
	f.close()

try:
	f = open("filtering_base.txt", "r")
	filtering_base = f.read()
	print(filtering_base)
	f.close()
except:
	f = open("filtering_base.txt", "w")
	f.write("HEX")
	f.close()

class Settings_Form(QtWidgets.QMainWindow):
	def __init__(self, ser):
		super(Settings_Form, self).__init__() # Call the inherited classes __init__ method
		uic.loadUi('settings.ui', self) # Load the .ui file
		self.show() # Show the GUI

		self.serial = serial.Serial()
		self.serial = ser

		self.cancel_button.clicked.connect(self.cancel_click)
		self.encoding_button.clicked.connect(self.encoding_click)
		self.filtering_button.clicked.connect(self.filtering_click)
		self.accept_button.clicked.connect(self.accept_click)
		self.filtering_enable_button.clicked.connect(self.filtering_enable_click)
		self.base_button.clicked.connect(self.filtering_base_click)

		self.encoding_button.setText(encoding)
		if(filtering_enabled):
			self.filtering_enable_button.setText("Filtering on")
		else:
			self.filtering_enable_button.setText("Filtering off")

		self.base_button.setText(filtering_base)
		if(filtering_base == "DEC"):
			self.id_max.setText(str(addr_max))
			self.id_min.setText(str(addr_min))
		else:
			self.id_max.setText(str(hex(addr_max)).upper())
			self.id_min.setText(str(hex(addr_min)).upper())

		if(filtering_mode == "except"):
			self.filtering_button.setText("All except")
		else:
			self.filtering_button.setText("All between")

		index = self.comboBox.findText(baudrate, QtCore.Qt.MatchFixedString)
		if index >= 0:
			self.comboBox.setCurrentIndex(index)

		if(filtering_enabled == False):

			self.filtering_button.setEnabled(False) #na pocetku je iskljucen filtering kao i svi njegovi buttoni i text inputi
			self.id_max.setReadOnly(True)
			self.id_min.setReadOnly(True)
			self.base_button.setEnabled(False)

		self.encoding = encoding
		self.baudrate = baudrate
		self.filtering_mode = filtering_mode
		self.filtering_enabled =filtering_enabled
		self.filtering_base = filtering_base

	def filtering_enable_click(self):
		if(self.filtering_enabled == False):
			self.filtering_enabled = True
			self.filtering_enable_button.setText("Filtering on")

			self.filtering_button.setEnabled(True)
			self.id_max.setReadOnly(False)
			self.id_min.setReadOnly(False)
			self.base_button.setEnabled(True)

		else:
			self.filtering_enabled = False
			self.filtering_enable_button.setText("Filtering off")

			self.filtering_button.setEnabled(False)
			self.id_max.setReadOnly(True)
			self.id_min.setReadOnly(True)
			self.base_button.setEnabled(False)
			

	def filtering_base_click(self):
		self.temp = self.id_max.text()
		if(self.temp == ""):
			self.id_max.setText("0")

		self.temp = self.id_min.text()
		if(self.temp == ""):
			self.id_min.setText("0")

		if(self.filtering_base == "HEX"):
			self.filtering_base = "DEC"
			self.base_button.setText("DEC")

			self.temp = self.id_max.text()

			if(len(self.temp) == 4):
				self.temp = self.temp[2:4]
			else:
				self.temp = self.temp[2:5]
			print(self.temp)
			self.temp = int(self.temp, 16)
			self.id_max.setText(str(self.temp))

			self.temp = self.id_min.text()
			if(len(self.temp) == 4):
				self.temp = self.temp[2:4]
			else:
				self.temp = self.temp[2:5]
			#self.temp = self.temp[2:4]
			self.temp = int(self.temp, 16)
			self.id_min.setText(str(self.temp))


		else:
			self.filtering_base = "HEX"
			self.base_button.setText("HEX")

			self.temp = self.id_min.text()
			self.temp = int(self.temp)
			self.temp = hex(self.temp)
			self.temp = self.temp.upper()
			self.id_min.setText(self.temp)

			self.temp = self.id_max.text()
			self.temp = int(self.temp)
			self.temp = hex(self.temp)
			self.temp = self.temp.upper()
			self.id_max.setText(self.temp)

	def accept_click(self):
		global encoding
		global addr_max
		global addr_min
		global filtering_mode
		global baudrate
		global filtering_base
		global filtering_enabled

		encoding = self.encoding
		addr_max = self.id_max.text()
		addr_min = self.id_min.text()
		filtering_mode = self.filtering_mode
		baudrate = self.comboBox.currentText()
		filtering_enabled = self.filtering_enabled
		filtering_base = self.filtering_base

		try:
			self.serial.write(baudrate.encode())
		except:
			pass

		if(filtering_enabled):
			if(filtering_base == "HEX"):
				if(len(addr_max) == 4):
					addr_max = addr_max[2:4]
				else:
					addr_max = addr_max[2:5]

				if(len(addr_min) == 4):
					addr_min = addr_min[2:4]
				else:
					addr_min = addr_min[2:5]
				addr_max = int(addr_max, 16)
				addr_min = int(addr_min, 16)

			else:
				addr_max = int(addr_max)
				addr_min = int(addr_min)

		try:
			f = open("encoding.txt", "w")
			f.write(encoding)
			f.close()
		except:
			pass

		try:
			f = open("addr_max.txt", "w")

			f.write(str(int(addr_max)))
			f.close()
		except:
			pass

		try:
			f = open("addr_min.txt", "w")
			f.write(str(int(addr_min)))
			f.close()
		except:
			pass

		try:
			f = open("baudrate.txt", "w")
			f.write(baudrate)
			f.close()
		except:
			pass

		try:
			f = open("filtering_base.txt", "w")
			f.write(filtering_base)
			f.close()
		except:
			pass

		try:
			f = open("filtering_mode.txt", "w")
			f.write(filtering_mode)
			f.close()
		except:
			pass

		try:
			f = open("filtering_enabled.txt", "w")
			a = 0
			if(filtering_enabled):
				a = 1
			else:
				a = 0
			f.write(str(a))
			f.close()
		except:
			pass




		self.close()



	def filtering_click(self):
		if(self.filtering_mode == "except"):
			self.filtering_mode = "between"
			self.filtering_button.setText("All between")
		else:
			self.filtering_mode = "except"
			self.filtering_button.setText("All except")

	def encoding_click(self):
		if(self.encoding == "ASCII"):
			self.encoding = "HEX"
			self.encoding_button.setText("HEX")
		else:
			self.encoding = "ASCII"
			self.encoding_button.setText("ASCII")

	def cancel_click(self):
		self.close()