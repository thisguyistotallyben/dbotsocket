import sys
import socket
import json
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import *


class DBotClient(QtWidgets.QMainWindow):
    def __init__(self):
        # formalities
        super().__init__()

        # window variables
        self.title = 'Discord Bot Client'
        self.left = 10
        self.top = 10
        self.width = 650
        self.height = 500

        # other variables
        self.bots = {}

        # setup
        self.setupWindow()
        self.setupWidgets()
        self.setupLayouts()
        self.build()

        # show
        self.show()

    def setupWindow(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

    def setupWidgets(self):
        self.widgets = {}

        # define
        self.widgets['main'] = QWidget()
        self.widgets['connserver'] = QPushButton('Connect to server')
        self.widgets['botlistbutt'] = QPushButton('Get list of bots')

        # connect
        self.widgets['connserver'].clicked.connect(self.connect_server)
        self.widgets['botlistbutt'].clicked.connect(self.botlistsig)

    def setupLayouts(self):
        self.layouts = {}

        # define
        self.layouts['main'] = QGridLayout()

    def build(self):
        # build main layout
        mainl = self.layouts['main']
        mainl.addWidget(self.widgets['connserver'], 0, 0)
        mainl.addWidget(self.widgets['botlistbutt'], 0, 1)


        self.widgets['main'].setLayout(mainl)

        self.setCentralWidget(self.widgets['main'])

    # ## ACTIONS AND SIGNALS## #

    def connect_server(self):
        HOST = '10.0.0.7'
        PORT = 50042
        self.sock = socket.create_connection((HOST, PORT))

    def botlistsig(self):
        # send
        self.sock.sendall(str('botlist').encode())

        # receive
        data = self.sock.recv(1024)

        # process
        print('Received', data.decode())
        self.bots = json.loads(data.decode())

# QT IT UP
app = QApplication(sys.argv)

# initalize classes
win = DBotClient()

# execute, clean up, and exit
sys.exit(app.exec_())


'''
# HOST = 'localhost'
HOST = '10.0.0.7'
PORT = 50042

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    while True:

        mess = input('message: ')
        s.sendall(str.encode(mess))
        data = s.recv(1024)
        print('Received', data.decode())
        print('')
'''
