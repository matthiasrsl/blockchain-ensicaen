# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GuiStart.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(326, 251)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.goButton = QtWidgets.QPushButton(self.centralwidget)
        self.goButton.setGeometry(QtCore.QRect(50, 150, 89, 25))
        self.goButton.setObjectName("goButton")
        self.ipLine = QtWidgets.QLineEdit(self.centralwidget)
        self.ipLine.setGeometry(QtCore.QRect(50, 100, 141, 25))
        self.ipLine.setObjectName("ipLine")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(50, 30, 281, 51))
        self.label.setObjectName("label")
        self.firstButton = QtWidgets.QPushButton(self.centralwidget)
        self.firstButton.setGeometry(QtCore.QRect(150, 150, 89, 25))
        self.firstButton.setObjectName("firstButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 326, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.goButton.setText(_translate("MainWindow", "Go"))
        self.label.setText(_translate("MainWindow", "Your public IP"))
        self.firstButton.setText(_translate("MainWindow", "I\'m First"))

