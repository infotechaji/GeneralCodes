# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ImageSwapping.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
import os

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.testImage1 = QtWidgets.QLabel(self.centralwidget)
        self.testImage1.setGeometry(QtCore.QRect(0, 0, 791, 501))
        self.testImage1.setText("")
        # self.testImage1.setPixmap(QtGui.QPixmap("../../../../../Images/Lord/Lord_muruga.jpg"))
        img_path = 'G:\Ajith\Images\Lord'
        image_name= 'Lord_muruga1.jpg'
        self.testImage1.setPixmap(QtGui.QPixmap(os.path.join(img_path,image_name)))
        self.testImage1.setScaledContents(True)
        self.testImage1.setObjectName("testImage1")
        self.muruga1 = QtWidgets.QPushButton(self.centralwidget)
        self.muruga1.setGeometry(QtCore.QRect(0, 500, 251, 51))
        self.muruga1.setObjectName("muruga1")
        self.muruga2 = QtWidgets.QPushButton(self.centralwidget)
        self.muruga2.setGeometry(QtCore.QRect(250, 500, 271, 51))
        self.muruga2.setObjectName("muruga2")
        self.muruga3 = QtWidgets.QPushButton(self.centralwidget)
        self.muruga3.setGeometry(QtCore.QRect(520, 500, 251, 51))
        self.muruga3.setObjectName("muruga3")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
        self.muruga1.clicked.connect(lambda: self.disp_muruga(image_name= 'Lord_muruga1.jpg'))
        self.muruga2.clicked.connect(lambda: self.disp_muruga(image_name= 'Lord_muruga2.jpg'))
        self.muruga3.clicked.connect(lambda: self.disp_muruga(image_name= 'Lord_muruga3.jpg'))

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.muruga1.setText(_translate("MainWindow", "MurugaWithValli"))
        self.muruga2.setText(_translate("MainWindow", "MalaysiaMurugar"))
        self.muruga3.setText(_translate("MainWindow", "MuruganFamilyStatue"))
    def disp_muruga(self,image_name):
        # self.testImage1.setPixmap(QtGui.QPixmap("../../../../../Images/Lord/Lord_muruga.jpg"))
        img_path = 'G:\Ajith\Images\Lord'
        self.testImage1.setPixmap(QtGui.QPixmap(os.path.join(img_path,image_name)))
        self.testImage1.setScaledContents(True)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
