# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'birthdayframe.ui'
#
# Created: Thu Jul 18 21:00:13 2013
#      by: PyQt4 UI code generator 4.10.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_BirthdayFrame(object):
    def setupUi(self, BirthdayFrame):
        BirthdayFrame.setObjectName(_fromUtf8("BirthdayFrame"))
        BirthdayFrame.resize(260, 371)
        BirthdayFrame.setFrameShape(QtGui.QFrame.StyledPanel)
        BirthdayFrame.setFrameShadow(QtGui.QFrame.Raised)
        self.formLayout = QtGui.QFormLayout(BirthdayFrame)
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.ExpandingFieldsGrow)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label = QtGui.QLabel(BirthdayFrame)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)
        self.edit_name = QtGui.QLineEdit(BirthdayFrame)
        self.edit_name.setObjectName(_fromUtf8("edit_name"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.edit_name)
        self.groupBox = QtGui.QGroupBox(BirthdayFrame)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.groupBox)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.radio_male = QtGui.QRadioButton(self.groupBox)
        self.radio_male.setChecked(True)
        self.radio_male.setObjectName(_fromUtf8("radio_male"))
        self.horizontalLayout.addWidget(self.radio_male)
        self.radio_female = QtGui.QRadioButton(self.groupBox)
        self.radio_female.setObjectName(_fromUtf8("radio_female"))
        self.horizontalLayout.addWidget(self.radio_female)
        self.formLayout.setWidget(1, QtGui.QFormLayout.SpanningRole, self.groupBox)
        self.groupBox_2 = QtGui.QGroupBox(BirthdayFrame)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.verticalLayout = QtGui.QVBoxLayout(self.groupBox_2)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.calendar = QtGui.QCalendarWidget(self.groupBox_2)
        self.calendar.setObjectName(_fromUtf8("calendar"))
        self.verticalLayout.addWidget(self.calendar)
        self.time = QtGui.QTimeEdit(self.groupBox_2)
        self.time.setAlignment(QtCore.Qt.AlignCenter)
        self.time.setTime(QtCore.QTime(12, 0, 0))
        self.time.setObjectName(_fromUtf8("time"))
        self.verticalLayout.addWidget(self.time)
        self.formLayout.setWidget(2, QtGui.QFormLayout.SpanningRole, self.groupBox_2)
        self.groupBox_3 = QtGui.QGroupBox(BirthdayFrame)
        self.groupBox_3.setTitle(_fromUtf8(""))
        self.groupBox_3.setObjectName(_fromUtf8("groupBox_3"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.groupBox_3)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.btnNow = QtGui.QPushButton(self.groupBox_3)
        self.btnNow.setObjectName(_fromUtf8("btnNow"))
        self.horizontalLayout_2.addWidget(self.btnNow)
        self.btnAdd = QtGui.QPushButton(self.groupBox_3)
        self.btnAdd.setEnabled(False)
        self.btnAdd.setObjectName(_fromUtf8("btnAdd"))
        self.horizontalLayout_2.addWidget(self.btnAdd)
        self.formLayout.setWidget(3, QtGui.QFormLayout.SpanningRole, self.groupBox_3)
        self.label.setBuddy(self.edit_name)

        self.retranslateUi(BirthdayFrame)
        QtCore.QObject.connect(self.btnAdd, QtCore.SIGNAL(_fromUtf8("clicked()")), BirthdayFrame.onBtnAdd)
        QtCore.QObject.connect(self.time, QtCore.SIGNAL(_fromUtf8("timeChanged(QTime)")), BirthdayFrame.onTimeChg)
        QtCore.QObject.connect(self.calendar, QtCore.SIGNAL(_fromUtf8("selectionChanged()")), BirthdayFrame.onDateChg)
        QtCore.QObject.connect(self.radio_male, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), BirthdayFrame.onGenderToggled)
        QtCore.QObject.connect(self.radio_female, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), BirthdayFrame.onGenderToggled)
        QtCore.QObject.connect(self.edit_name, QtCore.SIGNAL(_fromUtf8("textChanged(QString)")), BirthdayFrame.onNameChg)
        QtCore.QObject.connect(self.btnNow, QtCore.SIGNAL(_fromUtf8("clicked()")), BirthdayFrame.onBtnNow)
        QtCore.QMetaObject.connectSlotsByName(BirthdayFrame)

    def retranslateUi(self, BirthdayFrame):
        BirthdayFrame.setWindowTitle(_translate("BirthdayFrame", "Frame", None))
        self.label.setText(_translate("BirthdayFrame", "Name", None))
        self.groupBox.setTitle(_translate("BirthdayFrame", "Gender", None))
        self.radio_male.setText(_translate("BirthdayFrame", "Male", None))
        self.radio_female.setText(_translate("BirthdayFrame", "Female", None))
        self.groupBox_2.setTitle(_translate("BirthdayFrame", "Birthday", None))
        self.time.setDisplayFormat(_translate("BirthdayFrame", "hh:mm", None))
        self.btnNow.setText(_translate("BirthdayFrame", "Current Time", None))
        self.btnAdd.setText(_translate("BirthdayFrame", "Add", None))

