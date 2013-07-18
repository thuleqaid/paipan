# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'birthdayframe.ui'
#
# Created by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_BirthdayFrame(object):
    def setupUi(self, BirthdayFrame):
        BirthdayFrame.setObjectName(_fromUtf8("BirthdayFrame"))
        BirthdayFrame.resize(292, 369)
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
        self.time.setTime(QtCore.QTime(12, 0, 0))
        self.time.setObjectName(_fromUtf8("time"))
        self.verticalLayout.addWidget(self.time)
        self.formLayout.setWidget(2, QtGui.QFormLayout.SpanningRole, self.groupBox_2)
        self.groupBox_3 = QtGui.QGroupBox(BirthdayFrame)
        self.groupBox_3.setObjectName(_fromUtf8("groupBox_3"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.groupBox_3)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
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
        QtCore.QMetaObject.connectSlotsByName(BirthdayFrame)

    def retranslateUi(self, BirthdayFrame):
        BirthdayFrame.setWindowTitle(QtGui.QApplication.translate("BirthdayFrame", "Frame", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("BirthdayFrame", "Name", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("BirthdayFrame", "Gender", None, QtGui.QApplication.UnicodeUTF8))
        self.radio_male.setText(QtGui.QApplication.translate("BirthdayFrame", "Male", None, QtGui.QApplication.UnicodeUTF8))
        self.radio_female.setText(QtGui.QApplication.translate("BirthdayFrame", "Female", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_2.setTitle(QtGui.QApplication.translate("BirthdayFrame", "Birthday", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_3.setTitle(QtGui.QApplication.translate("BirthdayFrame", "GroupBox", None, QtGui.QApplication.UnicodeUTF8))
        self.btnAdd.setText(QtGui.QApplication.translate("BirthdayFrame", "Add", None, QtGui.QApplication.UnicodeUTF8))

