# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GuiLayout.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_RobotController(object):
    def setupUi(self, RobotController):
        RobotController.setObjectName("RobotController")
        RobotController.resize(1335, 799)
        self.centralwidget = QtWidgets.QWidget(RobotController)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(40, 590, 191, 71))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(17)
        self.pushButton.setFont(font)
        self.pushButton.setAcceptDrops(False)
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(260, 590, 191, 71))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(17)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setAcceptDrops(False)
        self.pushButton_2.setObjectName("pushButton_2")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(50, 230, 391, 251))
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
        self.label.setObjectName("label")
        self.graphicsView = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView.setGeometry(QtCore.QRect(500, 60, 800, 600))
        self.graphicsView.setObjectName("graphicsView")
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(50, 120, 271, 31))
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

    def retranslateUi(self, RobotController):
        _translate = QtCore.QCoreApplication.translate
        RobotController.setWindowTitle(_translate("RobotController", "Robot Controller"))
        self.pushButton.setText(_translate("RobotController", "Connect"))
        self.pushButton_2.setText(_translate("RobotController", "Send"))
        self.label.setText(_translate("RobotController", "Information"))
        self.label_2.setText(_translate("RobotController", "Manual commands"))
