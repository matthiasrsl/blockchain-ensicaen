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
        MainWindow.resize(1018, 333)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(20, 40, 851, 248))
        self.widget.setObjectName("widget")
        self.gridLayout = QtWidgets.QGridLayout(self.widget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.sendButton = QtWidgets.QPushButton(self.widget)
        self.sendButton.setObjectName("sendButton")
        self.gridLayout.addWidget(self.sendButton, 2, 0, 1, 1)
        self.createButton = QtWidgets.QPushButton(self.widget)
        self.createButton.setObjectName("createButton")
        self.gridLayout.addWidget(self.createButton, 2, 1, 1, 1)
        self.dataLabel = QtWidgets.QLabel(self.widget)
        self.dataLabel.setObjectName("dataLabel")
        self.gridLayout.addWidget(self.dataLabel, 0, 1, 1, 1)
        self.lineMessage = QtWidgets.QTextEdit(self.widget)
        self.lineMessage.setObjectName("lineMessage")
        self.gridLayout.addWidget(self.lineMessage, 1, 0, 1, 1)
        self.dataText = QtWidgets.QPlainTextEdit(self.widget)
        self.dataText.setObjectName("dataText")
        self.gridLayout.addWidget(self.dataText, 1, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1018, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.actionSendMessage = QtWidgets.QAction(MainWindow)
        self.actionSendMessage.setObjectName("actionSendMessage")

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        MainWindow.setProperty("enter", _translate("MainWindow", "Return"))
        self.sendButton.setText(_translate("MainWindow", "Send"))
        self.createButton.setText(_translate("MainWindow", "Create Block"))
        self.dataLabel.setText(_translate("MainWindow", "Data to insert in block"))
        self.label.setText(_translate("MainWindow", "Message to send"))
        self.actionSendMessage.setText(_translate("MainWindow", "SendMessage"))

