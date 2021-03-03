# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GuiClient.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1211, 892)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.sendButton = QtWidgets.QPushButton(self.centralwidget)
        self.sendButton.setGeometry(QtCore.QRect(390, 60, 80, 25))
        self.sendButton.setObjectName("sendButton")
        self.lineMessage = QtWidgets.QTextEdit(self.centralwidget)
        self.lineMessage.setGeometry(QtCore.QRect(10, 20, 351, 121))
        self.lineMessage.setObjectName("lineMessage")
        self.widget = QtWebEngineWidgets.QWebEngineView(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(40, 180, 601, 651))
        self.widget.setObjectName("widget")
        self.dataText = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.dataText.setGeometry(QtCore.QRect(740, 150, 421, 121))
        self.dataText.setObjectName("dataText")
        self.createButton = QtWidgets.QPushButton(self.centralwidget)
        self.createButton.setGeometry(QtCore.QRect(890, 300, 111, 31))
        self.createButton.setObjectName("createButton")
        self.dataLabel = QtWidgets.QLabel(self.centralwidget)
        self.dataLabel.setGeometry(QtCore.QRect(740, 110, 401, 17))
        self.dataLabel.setObjectName("dataLabel")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1211, 22))
        self.menubar.setObjectName("menubar")
        self.menuFIle = QtWidgets.QMenu(self.menubar)
        self.menuFIle.setObjectName("menuFIle")
        MainWindow.setMenuBar(self.menubar)
        self.actionSendMessage = QtWidgets.QAction(MainWindow)
        self.actionSendMessage.setObjectName("actionSendMessage")
        self.menubar.addAction(self.menuFIle.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        MainWindow.setProperty("enter", _translate("MainWindow", "Return"))
        self.sendButton.setText(_translate("MainWindow", "Send"))
        self.createButton.setText(_translate("MainWindow", "Create Block"))
        self.dataLabel.setText(_translate("MainWindow", "Data to insert in block"))
        self.menuFIle.setTitle(_translate("MainWindow", "FIle"))
        self.actionSendMessage.setText(_translate("MainWindow", "SendMessage"))

from PyQt5 import QtWebEngineWidgets
