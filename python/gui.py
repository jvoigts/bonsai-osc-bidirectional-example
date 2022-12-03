# -*- coding: utf-8 -*-
"""
Created on Dec.3 2022
@author: jvoigts
"""



import sys

from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from mainwindow import Ui_MainWindow

import random

import struct
import numpy as np
from numpy.random import randn


import sys
import time
import datetime


# osc stuff to get tracking data from bonsai
from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import BlockingOSCUDPServer
from pythonosc.udp_client import SimpleUDPClient

	
# in a separate thread we'll run a blocking OSC server
class OscInputMonitor(QObject):

	OscInputSignal = pyqtSignal(tuple)
	
	@pyqtSlot()
	def default_handler(sig, address, *args):
		#print(f"DEFAULT {address}: {args}")
		x=args[1]; # unpack Osc message
		sig.OscInputSignal.emit( (1,x) ) #<- send to main thread

	@pyqtSlot()
	def monitor_OscServer(self):
		dispatcher = Dispatcher()
		#dispatcher.map("/something/*", self.default_handler)
		decoratedhandler = lambda address, *args : self.default_handler(self.OscInputSignal, address, *args) #decorate function with ref to tracking signal so the thread can send stuff back
		dispatcher.set_default_handler(decoratedhandler)
		server = BlockingOSCUDPServer(("127.0.0.1", 1337), dispatcher)
		server.serve_forever()  # Blocks forever


class MainGui(QMainWindow):
	def __init__(self, parent=None):
		QWidget.__init__(self, parent)
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)
		self.initUI()
		
		# set up OSC server to receive messages from bonsai
		self.OscServer  = OscInputMonitor()
		self.thread = QThread(self)
		self.OscServer.OscInputSignal.connect(self.OscServer_callback)
		self.OscServer.moveToThread(self.thread)
		self.thread.started.connect(self.OscServer.monitor_OscServer)
		self.thread.start()
		print("started QThread")

		# set up OSC client, connect to bonsai instance
		# to send messages back
		self.OSCclient = SimpleUDPClient("127.0.0.1", 1338)  # Create client


	def sendRandomToBonsai(self):
		print("sending random number to bonsai")
		self.OSCclient.send_message("/127.0.0.1", np.random.rand(1)[0])  


	@pyqtSlot(tuple)
	def OscServer_callback(self, InputData):
		#print(InputData);
		self.ui.label_in.setText(str(InputData[1]))

	def initUI(self):    
		self.ui.pushButton_out.clicked.connect(self.sendRandomToBonsai)


if __name__ == "__main__":
	app = QApplication(sys.argv)
	myapp = MainGui()
	myapp.show()
	sys.exit(app.exec())



