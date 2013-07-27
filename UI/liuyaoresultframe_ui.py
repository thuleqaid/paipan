# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'liuyaoresultframe.ui'
#
# Created: Sat Jul 27 08:13:03 2013
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

class Ui_LiuyaoResultFrame(object):
    def setupUi(self, LiuyaoResultFrame):
        LiuyaoResultFrame.setObjectName(_fromUtf8("LiuyaoResultFrame"))
        LiuyaoResultFrame.resize(281, 516)
        LiuyaoResultFrame.setFrameShape(QtGui.QFrame.StyledPanel)
        LiuyaoResultFrame.setFrameShadow(QtGui.QFrame.Raised)
        self.gridLayout = QtGui.QGridLayout(LiuyaoResultFrame)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(LiuyaoResultFrame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.edit_name = QtGui.QLineEdit(LiuyaoResultFrame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.edit_name.sizePolicy().hasHeightForWidth())
        self.edit_name.setSizePolicy(sizePolicy)
        self.edit_name.setObjectName(_fromUtf8("edit_name"))
        self.gridLayout.addWidget(self.edit_name, 0, 1, 1, 1)
        self.text_gua = QtGui.QTextEdit(LiuyaoResultFrame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(4)
        sizePolicy.setHeightForWidth(self.text_gua.sizePolicy().hasHeightForWidth())
        self.text_gua.setSizePolicy(sizePolicy)
        self.text_gua.setReadOnly(True)
        self.text_gua.setObjectName(_fromUtf8("text_gua"))
        self.gridLayout.addWidget(self.text_gua, 2, 0, 1, 2)
        self.label_2 = QtGui.QLabel(LiuyaoResultFrame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.text_analyze = QtGui.QPlainTextEdit(LiuyaoResultFrame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.text_analyze.sizePolicy().hasHeightForWidth())
        self.text_analyze.setSizePolicy(sizePolicy)
        self.text_analyze.setObjectName(_fromUtf8("text_analyze"))
        self.gridLayout.addWidget(self.text_analyze, 3, 0, 1, 2)
        self.edit_question = QtGui.QLineEdit(LiuyaoResultFrame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.edit_question.sizePolicy().hasHeightForWidth())
        self.edit_question.setSizePolicy(sizePolicy)
        self.edit_question.setObjectName(_fromUtf8("edit_question"))
        self.gridLayout.addWidget(self.edit_question, 1, 1, 1, 1)
        self.groupBox = QtGui.QGroupBox(LiuyaoResultFrame)
        self.groupBox.setTitle(_fromUtf8(""))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.groupBox)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.btn_add = QtGui.QPushButton(self.groupBox)
        self.btn_add.setEnabled(False)
        self.btn_add.setObjectName(_fromUtf8("btn_add"))
        self.horizontalLayout.addWidget(self.btn_add)
        self.btn_update = QtGui.QPushButton(self.groupBox)
        self.btn_update.setEnabled(False)
        self.btn_update.setObjectName(_fromUtf8("btn_update"))
        self.horizontalLayout.addWidget(self.btn_update)
        self.btn_del = QtGui.QPushButton(self.groupBox)
        self.btn_del.setEnabled(False)
        self.btn_del.setObjectName(_fromUtf8("btn_del"))
        self.horizontalLayout.addWidget(self.btn_del)
        self.gridLayout.addWidget(self.groupBox, 4, 0, 1, 2)
        self.label.setBuddy(self.edit_name)
        self.label_2.setBuddy(self.edit_question)

        self.retranslateUi(LiuyaoResultFrame)
        QtCore.QObject.connect(self.btn_add, QtCore.SIGNAL(_fromUtf8("clicked()")), LiuyaoResultFrame.onBtnAdd)
        QtCore.QObject.connect(self.btn_update, QtCore.SIGNAL(_fromUtf8("clicked()")), LiuyaoResultFrame.onBtnUpdate)
        QtCore.QObject.connect(self.btn_del, QtCore.SIGNAL(_fromUtf8("clicked()")), LiuyaoResultFrame.onBtnDelete)
        QtCore.QObject.connect(self.text_analyze, QtCore.SIGNAL(_fromUtf8("textChanged()")), LiuyaoResultFrame.onModified)
        QtCore.QObject.connect(self.edit_name, QtCore.SIGNAL(_fromUtf8("textChanged(QString)")), LiuyaoResultFrame.onModified)
        QtCore.QObject.connect(self.edit_question, QtCore.SIGNAL(_fromUtf8("textChanged(QString)")), LiuyaoResultFrame.onModified)
        QtCore.QMetaObject.connectSlotsByName(LiuyaoResultFrame)

    def retranslateUi(self, LiuyaoResultFrame):
        LiuyaoResultFrame.setWindowTitle(_translate("LiuyaoResultFrame", "Frame", None))
        self.label.setText(_translate("LiuyaoResultFrame", "求测人", None))
        self.label_2.setText(_translate("LiuyaoResultFrame", "占事", None))
        self.btn_add.setText(_translate("LiuyaoResultFrame", "新增记录", None))
        self.btn_update.setText(_translate("LiuyaoResultFrame", "更新记录", None))
        self.btn_del.setText(_translate("LiuyaoResultFrame", "删除记录", None))

