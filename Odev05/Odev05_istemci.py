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
from PyQt5.QtWidgets import *
import queue
import time
from time import gmtime, strftime


class ReadThread (threading.Thread):
    def __init__(self, name, conn_socket, thread_queue, app):
        threading.Thread.__init__(self)
        self.name = name
        self.conn_socket = conn_socket
        self.nickname = ""
        self.thread_queue = thread_queue
        self.app = app

    def incoming_parser(self, data):
        if len(data) == 0:
            return

        parametre = " "
        split_data = data.split(" ")    
        query = split_data[0]
        parametre = split_data[1]


        if query == "TIN":
            return "TON"
    
        elif query == "PRV":
            self.thread_queue.put(parametre)
            return "OKP"

        elif query == "WRN":
            self.thread_queue.put(parametre)
            return "OKW"
        
        elif query == "GNL":
            self.thread_queue.put(parametre)
            return "OKG"
        
        else:
            return "ERR"
        
    def run(self):
        while True:
            data = self.conn_soc.recv(1024).decode()
            reponse = self.incoming_parser(data)            
            self.conn_soc.send(bytes(reponse, 'utf-8'))

class WriteThread (threading.Thread):
    def __init__(self, name, conn_socket, thread_queue):
        threading.Thread.__init__(self)
        self.name = name
        self.conn_socket = conn_socket
        self.thread_queue = thread_queue

    def run(self):
        while True:
            data = input("> ")
            self.thread_queue.put(data)
            self.conn_soc.send(bytes(data, 'utf-8'))

class ClientDialog(QDialog):
    def __init__(self, thread_queue):
        self.thread_queue = thread_queue        
        self.qt_app = QApplication(sys.argv)
        QDialog.__init__(self, None)                
        self.setWindowTitle("IRC Client")
        self.setMinimumSize(500, 200)        
        self.vbox = QVBoxLayout()       
        self.sender = QLineEdit("", self)        
        self.channel = QTextBrowser()       
        self.send_button = QPushButton('&Send')        
        self.send_button.clicked.connect(self.outgoing_parser)        
        self.vbox.addWidget(self.channel)
        self.vbox.addWidget(self.sender)
        self.vbox.addWidget(self.send_button)        
        self.timer = QTimer()
        self.timer.timeout.connect(self.updateText)        
        self.timer.start(10)        
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
        self.channel.append(data)

    def formatMessage(self, message, isLocal):
        result = strftime("%H:%M:%S", gmtime())
        result +=  " -Local-" if isLocal else " -Server-"
        return result + ": " + message


    def outgoing_parser(self):
        msg = str(self.sender.text())
        if len(msg) > 0:
            displayedMessage = self.formatMessage(msg, True)
            self.sender.clear()
            self.channel.append(displayedMessage)
            self.thread_queue.put(msg)

    def run(self):
        self.show()
        self.qt_app.exec_()

s = socket.socket()
host = sys.argv[1]
port = sys.argv[2]
s.connect((host,port))

sendQueue = queue.Queue()
app = ClientDialog(sendQueue)

rt = ReadThread("ReadThread", s, sendQueue, app)
rt.start()

wt = WriteThread("WriteThread", s, sendQueue)
wt.start()

app.run()

rt.join()
wt.join()
s.close()
