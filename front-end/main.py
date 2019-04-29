#!/usr/bin/env python
# -*- coding: utf-8 -*-
######################################################################
#                           DEPENDENCES
######################################################################
# from fbs_runtime.application_context import ApplicationContext
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtCore, QtGui, QtWidgets, uic

from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QPoint
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QMessageBox, QFileDialog

# from functools import partial
import cv2 
import socket
import sys
import json
import requests


#  Colector of data
global data

# Setting default value to 0
global sexo
global edad
global presion
global colesterol
global azucar
global ecg
global rcm
global angina
global depresion
global vasos
global dolor
global thal
global pico


qtCreatorFile = "main.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

# #To allow only int
# self.onlyInt = QIntValidator()
# self.LineEdit.setValidator(self.onlyInt)


# number = self.ui.number_lineEdit.text()
# try:
#     number = int(number)
# except Exception:
#     QtGui.QMessageBox.about(self, 'Error','Input can only be a number')
#     pass


class MessageDialog(QMessageBox):
	def __init__(self, msg_type, message):
		super(MessageDialog, self).__init__()
		# self.window_name = window_name
		self.message = message
		self.setText(message)
		self.msg_type = msg_type
		self.message_type()
		self.center()


	def center(self):
		frame_gm = self.frameGeometry()
		screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
		center_point = QApplication.desktop().screenGeometry(screen).center()
		frame_gm.moveCenter(center_point)
		self.move(frame_gm.topLeft())


	def message_type(self):

		if  "info" == self.msg_type.lower():
			self.setIcon(QMessageBox.Information)
			self.setWindowTitle("Mensaje informativo")

			return True

		if  "alert" == self.msg_type.lower():
			self.setIcon(QMessageBox.Critical)
			self.setWindowTitle("Mensaje crítico")

			return True

		if  "warn" == self.msg_type.lower():
			self.setIcon(QMessageBox.Warning)
			self.setWindowTitle("Mensaje de advertencia")

			return True

		if  "quest" == self.msg_type.lower():
			self.setIcon(QMessageBox.Question)
			self.setWindowTitle("Mensaje de dudas")

			return True
			


class CheckableComboBox(QtWidgets.QComboBox):
	def __init__(self):
		super(CheckableComboBox, self).__init__()
		self.view().pressed.connect(self.handle_item_pressed)
		self.setModel(QtGui.QStandardItemModel(self))
	
	def handle_item_pressed(self, index):
		item = self.model().itemFromIndex(index)

		if item.checkState() == QtCore.Qt.Checked:
			item.setCheckState(QtCore.Qt.Unchecked)
		else:
			item.setCheckState(QtCore.Qt.Checked)


class DeskGUI(QMainWindow, Ui_MainWindow, QtWidgets.QComboBox):

	def __init__(self):
		super().__init__()
		self.init_ui()
		
		# self.setWindowFlags(QtCore.Qt.CustomizeWindowHint)
		# 	self.setStyleSheet("background-color: rgb(52, 152, 219);")

		self.setFixedSize(self.size());		

		# Set Checboxes
		# self.checkBoxConnect.setEnabled(False)

	def init_ui(self):
		self.setupUi(self)
		self.statusBar().showMessage('Ready')
		# self.event_filter(QMainWindo)

		# self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

		# Set Buttons		
		## Push button send
		    
		self.pushButtonMandarSintomas.clicked.connect(self.button_send_data_on_click)
		# self.pushButtonMandarSintomas.clicked.connect(self.button_send_on_click)
		
		## Push Button to close the app
		# self.pushButtonClose.setStyleSheet('background-color:rgb(192, 57, 43);color:#000000;')
		# self.push btn_close_clicked
		# self.btn_close.clicked.connect(self.btn_close_clicked)
		self.pushButtonClose.clicked.connect(self.close)

		
		# Settig default values
		# self.lineEditEdad.text()
		# self.lineEditPresion.text()
		# self.lineEditColesterol.text()
		# self.lineEditAzucar.text()
		# self.lineEditRCM.text()
		# self.lineEditDepresionST.text()


		# data_line = self.ui.lineEdit.displayText()


		## Push button search

		## Push button connect
		self.setFixedSize(self.size());	
		self.center()
		self.show()

		self.start = QPoint(0, 0)
		self.pressing = False
	

	def mouse_press_event(self, event):
		self.start = self.map_to_global(event.pos())
		self.pressing = True


	def mouse_move_event(self, event):
		if self.pressing:
			self.end = self.map_to_global(event.pos())
			self.movement = self.end - self.start
			self.parent.setGeometry(self.mapToGlobal(self.movement).x(),
			self.parent.width(),
			self.parent.height())
			
			self.start = self.end


	def mouse_release_event(self, QMouseEvent):
		self.pressing = False


	def btn_close_clicked(self):
		self.parent.close()
	
	def btn_max_clicked(self):
		self.parent.showMaximized()

	def btn_min_clicked(self):
		self.parent.showMinimized()


	# Button action 
	@pyqtSlot()
	def button_send_on_click(self):
		self.send_json()
	
	# Button action 
	@pyqtSlot()
	def button_send_data_on_click(self):
		self.send_json()
	
	def resize_event(self, event):
		super(DeskGUI, self).resizeEvent(event)


	def center(self):
		frame_gm = self.frameGeometry()
		screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
		center_point = QApplication.desktop().screenGeometry(screen).center()
		frame_gm.moveCenter(center_point)
		self.move(frame_gm.topLeft())


	def browse_image(self):
		file_name = QFileDialog.getOpenFileName(self, 'Open File', 'c\\', 'Images files (*.jpg *.png')
		image_path = file_name[0]

		# Reading image with opencv
		image = cv2.imread(image_path)

		# Change color space BGR to RGB
		image = cv2.cvtColor

		# Copy of the original image
		copy_image = image.copy()
	


		pix_map = QPixmap(image_path)

	
	def cv2imageQ(self, img):
		img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
		img = Image.fromarray(img)
		return img


	def send_json(self):

		data = []

		sexo = 0.00
		edad = 0.00
		presion = 0.00
		colesterol = 0.00
		azucar = 0.00
		ecg = 0.00
		rcm = 0.00
		angina = 0.00
		depresion = 0.00
		vasos = 0.00
		dolor = 0.00
		thal = 0.00
		pico = 0.00

		# Convert values to float
		# Setting default value to 0
		# sexo = float(1)
		# edad = float(self.lineEditEdad.text().toInt())
		# presion = float(self.lineEditPresion.text().toInt())
		# colesterol = float(self.lineEditColesterol.text().toInt())
		# azucar = float(self.lineEditAzucar.text().toInt())
		# ecg = float(1)
		# rcm = float(self.lineEditRCM.text().toInt())
		# angina = float(1)
		# depresion = float(self.lineEditDepresionST.text().toInt())
		# vasos = float(1)
		# dolor = float(1)
		# thal = float(1)
		
		data.append(sexo)
		data.append(edad)
		data.append(presion)
		data.append(colesterol)
		data.append(azucar)
		data.append(ecg)
		data.append(rcm)
		data.append(angina)
		data.append(depresion)
		data.append(vasos)
		data.append(dolor)
		data.append(thal)
		data.append(pico)

		# msg = MessageDialog(msg_type='alert',message='Problema al mandar la información')
		# msg.exec()
		print("[INFO] Data to send: " + str(data[0]), str(data[1]), \
			str(data[2]), str(data[3]), str(data[4]), str(data[5]), \
				str(data[6]), str(data[7]), str(data[8]), str(data[9]),\
					 str(data[10]), str(data[10]), str(data[11]), str(data[12]))
		
		
		print("[INFO] Sending JSON...\n")

		url = 'http://127.0.0.1:5000/heart_cancer_predict'

		payload ={
			"data": [[data[0],data[0],data[0],data[0],data[0],data[0],data[0],\
				data[0],data[0],data[0],data[0],data[0],data[0],data[0],data[0], \
					data[0],data[0],data[0],data[0],data[0],data[0]]]
		}

		headers = {'content-type': 'application/json'}

		response = requests.post(url, data=json.dumps(payload), headers=headers)

		print(response)

		
	
	
	# @classmethod
	def check_internet(self):
		for timeout in [1,5,10,15]:
			try:
				print("[INFO] checking internet connection...\n")
				socket.setdefaulttimeout(timeout)
				host = socket.gethostbyname("www.google.com")
				s = socket.create_connection((host, 80), 2)
				s.close()
				print("[INFO] internet on.\n")
				
				# Setting On Checkbox
				self.checkBoxConnect.setEnabled(True)

				self.checkbox2.toggled.connect(self.checkbox1.setEnabled)
				return True

			except e:
				print(e)
				print("[ERROR] internet off\n")
				# Setting Off Checkbox
				self.checkBoxConnect.setEnabled(False)

		return False





if __name__ == "__main__":
	Qapp = QApplication(sys.argv)
	app = DeskGUI()
	# screen_resolution = Qapp.desktop().screenGeometry()
	# width, height = screen_resolution.width(), screen_resolution.height()

	# print("Width value: " + str(width))
	# print("Height value: " + str(height))
	sys.exit(Qapp.exec())