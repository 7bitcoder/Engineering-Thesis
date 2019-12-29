# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'guiLayout.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from comunication import Commands
from datetime import datetime
from main import GestureRecognition, Signals
from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtCore import *
import time
import sys
from PyQt5.QtWidgets import QDialog, QApplication


class Ui_RobotController(QObject):

    def closeNeuralNetworkThread(self):
        self.commands.disconnect()
        self.recognition.stop()
        self.recognition.wait()

    def setupUi(self, RobotController):
        RobotController.setObjectName("RobotController")
        RobotController.resize(1400, 700)
        self.centralwidget = QtWidgets.QWidget(RobotController)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(50, 590, 191, 71))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(17)
        self.pushButton.setFont(font)
        self.pushButton.setAcceptDrops(False)
        self.pushButton.setObjectName("pushButton")

        self.pushButton3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton3.setGeometry(QtCore.QRect(300, 590, 250, 71))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(17)
        self.pushButton3.setFont(font)
        self.pushButton3.setAcceptDrops(False)
        self.pushButton3.setObjectName("pushButton3")

        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(260, 110, 191, 71))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(17)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setAcceptDrops(False)
        self.pushButton_2.setObjectName("pushButton_2")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(50, 230, 500, 280))
        font = QtGui.QFont()
        font.setFamily("Lato")
        font.setPointSize(9)
        self.textBrowser.setFont(font)
        self.textBrowser.setObjectName("textBrowser")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(60, 160, 381, 61))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label.setFont(font)
        self.label.setLayoutDirection(QtCore.Qt.LeftToRight)

        self.fps = QtWidgets.QLabel(self.centralwidget)
        self.fps.setGeometry(QtCore.QRect(700, 50, 381, 61))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.fps.setFont(font)
        self.fps.setLayoutDirection(QtCore.Qt.LeftToRight)

        self.label.setObjectName("label")
        self.graphicsView = QtWidgets.QLabel(self.centralwidget)
        self.graphicsView.setGeometry(QtCore.QRect(700, 60, 800, 600))
        self.graphicsView.setObjectName("graphicsView")
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(50, 120, 150, 31))
        self.comboBox.setObjectName("comboBox")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(60, 60, 381, 41))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label_2.setFont(font)
        self.label_2.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_2.setObjectName("label_2")
        RobotController.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(RobotController)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1335, 26))
        self.menubar.setObjectName("menubar")
        RobotController.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(RobotController)
        self.statusbar.setObjectName("statusbar")
        RobotController.setStatusBar(self.statusbar)

        self.retranslateUi(RobotController)
        QtCore.QMetaObject.connectSlotsByName(RobotController)

        self.commands = Commands()
        self.commands.signals.print.connect(self.print)
        self.commands.signals.lock.connect(self.unlock)
        self.commands.ble.signals.print.connect(self.print)
        self.commands.ble.signals.lock.connect(self.unlock)

        self.connectedToRobot = False
        self.connectionInProgress = False
        self.pushButton.clicked.connect(self.connect)
        self.print("Application started")
        self.comboBox.addItem("None")
        for val in self.commands.commands:
            self.comboBox.addItem(val.name, )

        self.pushButton_2.clicked.connect(self.send)

        self.recognition = GestureRecognition(self.showFps)
        self.recognition.setTerminationEnabled(True)
        self.recognition.signals.result.connect(self.getRecognitionResult)

        self.finished = self.recognition.signals.finished

        self.recognition.start()

    def retranslateUi(self, RobotController):
        _translate = QtCore.QCoreApplication.translate
        RobotController.setWindowTitle(_translate("RobotController", "Robot Controller"))
        self.pushButton.setText(_translate("RobotController", "Connect"))
        self.pushButton_2.setText(_translate("RobotController", "Send"))
        self.pushButton3.setText(_translate("RobotController", "Emergency stop"))
        self.label.setText(_translate("RobotController", "Information"))
        self.fps.setText("Fps: 0")
        self.label_2.setText(_translate("RobotController", "Manual commands"))

    def showFps(self, fps):
        self.fps.setText("Fps: {}".format(fps))

    def connect(self):
        if self.connectionInProgress:
            return
        self.connectionInProgress = True
        if self.connectedToRobot:
            self.commands.disconnect()
        else:
            self.commands.run()

    def send(self):
        if not self.connectedToRobot:
            self.print("Cannot send command, connection to robot is not established")
            return
        if self.comboBox.currentIndex() == 0:
            pass
        else:
            command = self.commands.commands(self.comboBox.currentIndex())
            self.commands.executeCommand(command)
            self.comboBox.setCurrentIndex(0)

    def print(self, str):
        dt = datetime.now().time()
        sec = dt.microsecond / 1000000
        string = "{}:{:02d}:{:05.2f}".format(dt.hour, dt.minute, dt.second + sec)
        self.textBrowser.append("[{}] {}".format(string, str))
        self.textBrowser.verticalScrollBar().setValue(self.textBrowser.verticalScrollBar().maximum())

    def unlock(self, unlock):
        if unlock == 1:
            self.connectedToRobot = True
            self.pushButton.setText("Disconnect")
            self.connectionInProgress = False
        elif unlock == 2:
            self.connectedToRobot = False
            self.connectionInProgress = False
            self.pushButton.setText("Connect")

    def getRecognitionResult(self, image, output):
        height, width, byteValue = image.shape
        image = QtGui.QImage(image, image.shape[1], image.shape[0], image.shape[1] * 3, QtGui.QImage.Format_RGB888)
        pix = QtGui.QPixmap(image)
        self.graphicsView.setPixmap(pix)


if __name__ == '__main__':
    import sys

    ui = Ui_RobotController()
    app = QtWidgets.QApplication(sys.argv)
    app.aboutToQuit.connect(ui.closeNeuralNetworkThread)
    window = QtWidgets.QMainWindow()
    ui.setupUi(window)
    window.show()
    sys.exit(app.exec_())
