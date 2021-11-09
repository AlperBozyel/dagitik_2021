# -*- coding: utf-8 -*-
"""
Created on Sat Nov  6 16:30:25 2021

@author: VV
"""

import sys
import socket
import threading
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import queue
import time

class ReadThread (threading.Thread):
    def __init__(self, name, csoc, threadQueue, app):
        threading.Thread.__
        self.csoc = csoc
        self.nickname = ""
        self.threadQueue = threadQueue
        self.app = app
        
    def incoming_parser(self, data):
        threadQueue.put(data)
        # 
        
    def run(self):
        data = csoc.recv(1024)
        self.incoming_parser(data)
                
    #...
        
class WriteThread (threading.Thread):
    def __init__(self, name, csoc, threadQueue):
        threading.Thread.__init__(self)
        self.name = name
        self.csoc = csoc
        self.threadQueue = threadQueue
        
    def run(self):
        threadQueue.get()
        
''' An example application for PyQt. Instantiate
and call the run method to run. '''        
class ClientDialog(QDialog):
    def __init__(self, threadQueue):
        self.threadQueue = threadQueue
# create a Qt application --- every PyQt app needs one
        self.qt_app = QApplication(sys.argv)
# Call the parent constructor on the current object
        QDialog.__init__(self, None)
# Set up the window
        self.setWindowTitle('IRC Client')
        self.setMinimumSize(500, 200)
# Add a vertical layout
        self.vbox = QVBoxLayout()
# The sender textbox
        self.sender = QLineEdit("", self)
# The channel region
        self.channel = QTextBrowser()
# The send button
        self.send_button = QPushButton('&Send')
# Connect the Go button to its callback
        self.send_button.clicked.connect(self.outgoing_parser)
# Add the controls to the vertical layout
        self.vbox.addWidget(self.channel)
        self.vbox.addWidget(self.sender)
        self.vbox.addWidget(self.send_button)
# start timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.updateText)
# update every 100 ms
        self.timer.start(10)
# Use the vertical layout for the current window
        self.setLayout(self.vbox)
        
    def updateText(self):
        if not self.screenQueue.empty():
            data = self.screenQueue.get()
            t = time.localtime()
            pt = "%02d:%02d:%02d" % (t.tm_hour, t.tm_min, t.tm_sec)
            self.channel.append(pt + " " + data)
        else:
            return
        
    def cprint(self, data):
        print("%s",data)
        self.channel.append(data)
        
    def outgoing_parser(self):
        print("Todo")
       
    def run(self):
        self.show()
        self.qt_app.exec_()
        
# connect to the server
s = socket.socket()
host = sys.argv[1]    # To do
port = sys.argv[2]
s.connect((host,port))
sendQueue = queue.Queue() #Queue
app = ClientDialog(sendQueue)
# start threads
rt = ReadThread("ReadThread", s, sendQueue, app)
rt.start()
wt = WriteThread("WriteThread", s, sendQueue)
wt.start()
app.run()
rt.join()
wt.join()
s.close()