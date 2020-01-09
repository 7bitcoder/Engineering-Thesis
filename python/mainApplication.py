# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'guiLayout.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from serialComunication import Commands
from datetime import datetime
from main import GestureRecognition
from PyQt5.QtCore import *
from torch import argmax
from time import time
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_RobotController(QObject):

    def closeNeuralNetworkThread(self):
        self.commands.disconnect()
        self.recognition.stop()
        self.recognition.wait()

    def setupUi(self, RobotController):
        RobotController.setObjectName("RobotController")
        RobotController.resize(1400, 700)

        RobotController.emergency.connect(self.emergencyStop)
        RobotController.network.connect(self.capture)

        self.centralwidget = QtWidgets.QWidget(RobotController)
        self.centralwidget.setObjectName("centralwidget")

        self.pushButton_5 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_5.setGeometry(QtCore.QRect(900, 48, 80, 60))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(15)
        self.pushButton_5.setFont(font)
        self.pushButton_5.setAcceptDrops(False)
        self.pushButton_5.setObjectName("pushButton_5")

        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(1200, 48, 80, 60))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(15)
        self.pushButton_4.setFont(font)
        self.pushButton_4.setAcceptDrops(False)
        self.pushButton_4.setObjectName("pushButton_4")

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
        self.fps.setGeometry(QtCore.QRect(700, 50, 100, 61))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.fps.setFont(font)
        self.fps.setLayoutDirection(QtCore.Qt.LeftToRight)

        self.capturing = QtWidgets.QLabel(self.centralwidget)
        self.capturing.setGeometry(QtCore.QRect(1000, 50, 200, 61))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.capturing.setFont(font)
        self.capturing.setLayoutDirection(QtCore.Qt.LeftToRight)

        self.network = QtWidgets.QLabel(self.centralwidget)
        self.network.setGeometry(QtCore.QRect(800, 50, 100, 61))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.network.setFont(font)
        self.network.setLayoutDirection(QtCore.Qt.LeftToRight)

        self.label.setObjectName("label")
        self.graphicsView = QtWidgets.QLabel(self.centralwidget)
        self.graphicsView.setGeometry(QtCore.QRect(700, 120, 640, 480))
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

        font.setPointSize(12)
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(490, 110, 200, 41))
        self.label_4.setFont(font)
        self.label_4.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_4.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.label_4.setObjectName("Capture probabilities")
        self.label_4.setText("Capture probabilities:")

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
        self.pushButton3.clicked.connect(self.emergencyStop)
        self.pushButton_4.clicked.connect(self.capture)

        self.gesturesLabels = []

        font = QtGui.QFont()
        font.setPointSize(10)

        self.print("Application started")
        self.comboBox.addItem("None", 1)
        offset = 30
        i = 0
        for val in self.commands.commands:
            self.comboBox.addItem(val.name, val.value)
            label_2 = QtWidgets.QLabel(self.centralwidget)
            label_2.setGeometry(QtCore.QRect(560, 150 + i * offset, 130, 41))
            label_2.setFont(font)
            label_2.setLayoutDirection(QtCore.Qt.LeftToRight)
            label_2.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
            label_2.setObjectName(val.name)
            label_2.setText(val.name)
            self.gesturesLabels.append(label_2)
            i += 1

        self.pushButton_2.clicked.connect(self.sendWrap)
        self.pushButton_5.clicked.connect(self.onNetwork)

        self.recognition = GestureRecognition(self.showFps)
        self.recognition.setTerminationEnabled(True)
        self.recognition.signals.result.connect(self.getRecognitionResult)

        self.finished = self.recognition.signals.finished
        self.gesturesCapturing = False
        self.netowkrProcess = True
        self.recognition.start()
        self.lastCompute = None
        self.frames = 0
        self.time = time()

    def retranslateUi(self, RobotController):
        _translate = QtCore.QCoreApplication.translate
        RobotController.setWindowTitle(_translate("RobotController", "Robot Controller"))
        self.pushButton.setText(_translate("RobotController", "Connect"))
        self.pushButton_2.setText(_translate("RobotController", "Send"))
        self.pushButton3.setText(_translate("RobotController", "Emergency stop"))
        self.pushButton_4.setText(_translate("RobotController", "OFF"))
        self.pushButton_5.setText(_translate("RobotController", "ON"))
        self.label.setText(_translate("RobotController", "Information"))
        self.fps.setText("Fps: 0")
        self.capturing.setText("Gesture capturing: ")
        self.label_2.setText(_translate("RobotController", "Manual commands"))
        self.network.setText(_translate("RobotController", "Network: "))

    def capture(self):
        self.gesturesCapturing = not self.gesturesCapturing
        if self.gesturesCapturing:
            self.pushButton_4.setText("ON")
        else:
            self.pushButton_4.setText("OFF")

    def onNetwork(self):
        self.netowkrProcess = not self.netowkrProcess
        if self.netowkrProcess:
            self.pushButton_5.setText("ON")
            self.recognition.disableNetwork = False
        else:
            self.pushButton_5.setText("OFF")
            self.recognition.disableNetwork = True

    def showFps(self, fps):
        self.fps.setText("Fps: {}".format(fps))

    def emergencyStop(self):
        self.commands.executeCommand(self.commands.commands.stopCommand)

    def connect(self):
        if self.connectionInProgress:
            return
        self.connectionInProgress = True
        if self.connectedToRobot:
            self.commands.disconnect()
        else:
            self.commands.run()

    def sendWrap(self):
        self.send()

    def send(self, recognized=None):
        try:
            if not self.connectedToRobot:
                self.print("Cannot send command, connection to robot is not established")
                return
            command = recognized
            if recognized is None:
                if self.comboBox.currentIndex() == 0:
                    pass
                else:
                    command = self.commands.commands(int(self.comboBox.currentData()))
                    self.comboBox.setCurrentIndex(0)
            if command == self.commands.commands.default:
                pass
            elif command == self.commands.commands.stopCommand:
                self.emergencyStop()
                self.print("Emergency stop")
            elif command.value < self.commands.commands.speedUp.value and self.commands.watchDog:  # acvive command not settings
                self.print("Cannot send command, one is already in execution: {}".format(
                    self.commands.watchDog[0].command.name))
            else:
                self.print(command.name)
                self.commands.executeCommand(command)
        except Exception as e:
            self.print(e)
        finally:
            pass

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
        image = QtGui.QImage(image, image.shape[1], image.shape[0], image.shape[1] * 3, QtGui.QImage.Format_RGB888)
        pix = QtGui.QPixmap(image)
        self.graphicsView.setPixmap(pix)
        self.frames += 1
        self.computeGesture(output)

    def computeGesture(self, output):
        index = argmax(output).item() + 1  # label
        if (not self.gesturesCapturing) or index == 1 or (not self.netowkrProcess) or index != self.lastCompute:
            self.time = time()
            self.frames = 0
        elif time() - self.time > 2 and self.frames > 15:
            command = self.commands.commands(index)
            self.print("Recognized: {}".format(command.name))
            self.send(command)
            self.time = time()
            self.frames = 0
        self.lastCompute = index


class MyWindow(QtWidgets.QMainWindow):
    emergency = pyqtSignal()
    network = pyqtSignal()

    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent=parent)

    def keyPressEvent(self, event):
        if type(event) == QtGui.QKeyEvent:
            if event.key() == QtCore.Qt.Key_Shift:
                self.emergency.emit()
            elif event.key() == QtCore.Qt.Key_Control:
                self.network.emit()


if __name__ == '__main__':
    import sys

    ui = Ui_RobotController()
    app = QtWidgets.QApplication(sys.argv)
    app.aboutToQuit.connect(ui.closeNeuralNetworkThread)
    window = MyWindow()
    ui.setupUi(window)
    window.show()
    sys.exit(app.exec_())
    """
    w = MyWindow()
    app = QtWidgets.QApplication(sys.argv)
    app.aboutToQuit.connect(w.closeNeuralNetworkThread)
    w.show()
    sys.exit(app.exec_())
    """
