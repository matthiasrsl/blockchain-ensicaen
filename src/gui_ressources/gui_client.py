# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GuiClient.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets


# noinspection PyAttributeOutsideInit,PyAttributeOutsideInit,PyAttributeOutsideInit,PyAttributeOutsideInit,PyAttributeOutsideInit,PyAttributeOutsideInit,PyAttributeOutsideInit,PyAttributeOutsideInit,PyAttributeOutsideInit,PyAttributeOutsideInit,PyAttributeOutsideInit,PyAttributeOutsideInit,PyAttributeOutsideInit,PyAttributeOutsideInit,PyAttributeOutsideInit
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(941, 610)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.sendButton = QtWidgets.QPushButton(self.centralwidget)
        self.sendButton.setGeometry(QtCore.QRect(150, 230, 80, 25))
        self.sendButton.setObjectName("sendButton")
        self.lineMessage = QtWidgets.QTextEdit(self.centralwidget)
        self.lineMessage.setGeometry(QtCore.QRect(20, 80, 351, 121))
        self.lineMessage.setObjectName("lineMessage")
        self.dataText = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.dataText.setGeometry(QtCore.QRect(460, 80, 421, 121))
        self.dataText.setMinimumSize(QtCore.QSize(421, 121))
        self.dataText.setMaximumSize(QtCore.QSize(16777215, 121))
        self.dataText.setObjectName("dataText")
        self.createButton = QtWidgets.QPushButton(self.centralwidget)
        self.createButton.setGeometry(QtCore.QRect(610, 230, 111, 31))
        self.createButton.setObjectName("createButton")
        self.dataLabel = QtWidgets.QLabel(self.centralwidget)
        self.dataLabel.setGeometry(QtCore.QRect(460, 40, 401, 17))
        self.dataLabel.setMinimumSize(QtCore.QSize(401, 17))
        self.dataLabel.setMaximumSize(QtCore.QSize(16777215, 17))
        self.dataLabel.setObjectName("dataLabel")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 40, 301, 17))
        self.label.setObjectName("label")
        self.manuelBox = QtWidgets.QCheckBox(self.centralwidget)
        self.manuelBox.setGeometry(QtCore.QRect(700, 330, 92, 23))
        self.manuelBox.setObjectName("manuelBox")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(20, 300, 141, 17))
        self.label_2.setObjectName("label_2")
        self.acceptBox = QtWidgets.QDialogButtonBox(self.centralwidget)
        self.acceptBox.setEnabled(False)
        self.acceptBox.setGeometry(QtCore.QRect(650, 370, 169, 51))
        self.acceptBox.setOrientation(QtCore.Qt.Vertical)
        self.acceptBox.setStandardButtons(QtWidgets.QDialogButtonBox.No|QtWidgets.QDialogButtonBox.Yes)
        self.acceptBox.setCenterButtons(False)
        self.acceptBox.setObjectName("acceptBox")
        self.blockDisplayer = QtWidgets.QTextBrowser(self.centralwidget)
        self.blockDisplayer.setGeometry(QtCore.QRect(5, 330, 641, 192))
        self.blockDisplayer.setObjectName("blockDisplayer")
        self.hiddenRefreshButton = QtWidgets.QPushButton(self.centralwidget)
        self.hiddenRefreshButton.setGeometry(QtCore.QRect(30, 530, 16, 16))
        self.hiddenRefreshButton.setObjectName("hiddenRefreshButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 941, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.actionSendMessage = QtWidgets.QAction(MainWindow)
        self.actionSendMessage.setObjectName("actionSendMessage")

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Client"))
        MainWindow.setProperty("enter", _translate("MainWindow", "Return"))
        self.sendButton.setText(_translate("MainWindow", "Send"))
        self.createButton.setText(_translate("MainWindow", "Create Block"))
        self.dataLabel.setText(_translate("MainWindow", "Data to insert in block"))
        self.label.setText(_translate("MainWindow", "Message to send"))
        self.manuelBox.setText(_translate("MainWindow", "Manual"))
        self.label_2.setText(_translate("MainWindow", "Block recieved"))
        self.blockDisplayer.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">None</p></body></html>"))
        self.hiddenRefreshButton.setText(_translate("MainWindow", "PushButton"))
        self.actionSendMessage.setText(_translate("MainWindow", "SendMessage"))

