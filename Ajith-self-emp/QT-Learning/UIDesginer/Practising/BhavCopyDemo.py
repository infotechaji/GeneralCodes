# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'BhavCopyDemo.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(581, 381)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.startdate = QtWidgets.QDateEdit(self.centralwidget)
        self.startdate.setGeometry(QtCore.QRect(200, 40, 110, 22))
        self.startdate.setObjectName("startdate")
        self.enddate = QtWidgets.QDateEdit(self.centralwidget)
        self.enddate.setGeometry(QtCore.QRect(200, 80, 110, 22))
        self.enddate.setObjectName("enddate")
        
        self.GetBhavCopy = QtWidgets.QPushButton(self.centralwidget)
        self.GetBhavCopy.setGeometry(QtCore.QRect(200, 210, 111, 41))
        self.GetBhavCopy.setObjectName("GetBhavCopy")
        
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(76, 43, 110, 30))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(76, 82, 101, 21))
        self.label_2.setObjectName("label_2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 581, 21))
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
        self.GetBhavCopy.setText(_translate("MainWindow", "Get Bhav Copy"))
        self.label.setText(_translate("MainWindow", "Choose Start Date"))
        self.label_2.setText(_translate("MainWindow", "Choose End Date"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
