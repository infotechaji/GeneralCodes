# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'g:\Ajith\Others\Ajith-self-instresed\QT-Learning\UIDesginer\Practising\BhavCopyDemo2.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(750, 552)
        self.GetBhavCopy = QtWidgets.QPushButton(Form)
        self.GetBhavCopy.setGeometry(QtCore.QRect(170, 370, 251, 41))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(170, 85, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(170, 85, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(170, 85, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        self.GetBhavCopy.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.GetBhavCopy.setFont(font)
        self.GetBhavCopy.setObjectName("GetBhavCopy")
        self.startdate_label = QtWidgets.QLabel(Form)
        self.startdate_label.setGeometry(QtCore.QRect(170, 73, 110, 30))
        self.startdate_label.setObjectName("startdate_label")
        self.comp_wise_radiobtn = QtWidgets.QRadioButton(Form)
        self.comp_wise_radiobtn.setGeometry(QtCore.QRect(320, 160, 161, 31))
        self.comp_wise_radiobtn.setObjectName("comp_wise_radiobtn")
        self.bvcp_type_label = QtWidgets.QLabel(Form)
        self.bvcp_type_label.setGeometry(QtCore.QRect(170, 160, 121, 41))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.bvcp_type_label.setFont(font)
        self.bvcp_type_label.setObjectName("bvcp_type_label")
        self.date_wise_radiobtn = QtWidgets.QRadioButton(Form)
        self.date_wise_radiobtn.setGeometry(QtCore.QRect(320, 180, 121, 31))
        self.date_wise_radiobtn.setObjectName("date_wise_radiobtn")
        self.enddate_edit = QtWidgets.QDateEdit(Form)
        self.enddate_edit.setGeometry(QtCore.QRect(310, 110, 110, 22))
        self.enddate_edit.setObjectName("enddate_edit")
        self.enddate_label = QtWidgets.QLabel(Form)
        self.enddate_label.setGeometry(QtCore.QRect(170, 112, 101, 21))
        self.enddate_label.setObjectName("enddate_label")
        self.startdate_edit = QtWidgets.QDateEdit(Form)
        self.startdate_edit.setGeometry(QtCore.QRect(310, 80, 110, 22))
        self.startdate_edit.setObjectName("startdate_edit")
        self.output_folder_label = QtWidgets.QLabel(Form)
        self.output_folder_label.setGeometry(QtCore.QRect(170, 230, 121, 41))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.output_folder_label.setFont(font)
        self.output_folder_label.setObjectName("output_folder_label")
        self.browse_btn = QtWidgets.QPushButton(Form)
        self.browse_btn.setGeometry(QtCore.QRect(570, 280, 75, 23))
        self.browse_btn.setObjectName("browse_btn")
        self.pathchooser_edit = QtWidgets.QLineEdit(Form)
        self.pathchooser_edit.setGeometry(QtCore.QRect(300, 240, 401, 20))
        self.pathchooser_edit.setObjectName("pathchooser_edit")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.GetBhavCopy.setText(_translate("Form", "Download Bhav Copy"))
        self.startdate_label.setText(_translate("Form", "Choose Start Date"))
        self.comp_wise_radiobtn.setText(_translate("Form", "Company wise files"))
        self.bvcp_type_label.setText(_translate("Form", "Bhav copy type"))
        self.date_wise_radiobtn.setText(_translate("Form", "Date wise files"))
        self.enddate_label.setText(_translate("Form", "Choose End Date"))
        self.output_folder_label.setText(_translate("Form", "Output Folder"))
        self.browse_btn.setText(_translate("Form", "Browse"))
