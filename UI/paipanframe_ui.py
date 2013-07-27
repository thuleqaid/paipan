# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'paipanframe.ui'
#
# Created: Sat Jul 27 07:07:47 2013
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

class Ui_PaipanFrame(object):
    def setupUi(self, PaipanFrame):
        PaipanFrame.setObjectName(_fromUtf8("PaipanFrame"))
        PaipanFrame.resize(601, 412)
        PaipanFrame.setFrameShape(QtGui.QFrame.StyledPanel)
        PaipanFrame.setFrameShadow(QtGui.QFrame.Raised)
        self.gridLayout = QtGui.QGridLayout(PaipanFrame)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.groupBox_3 = QtGui.QGroupBox(PaipanFrame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(4)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_3.sizePolicy().hasHeightForWidth())
        self.groupBox_3.setSizePolicy(sizePolicy)
        self.groupBox_3.setTitle(_fromUtf8(""))
        self.groupBox_3.setObjectName(_fromUtf8("groupBox_3"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.groupBox_3)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.tabWidget = QtGui.QTabWidget(self.groupBox_3)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.horizontalLayout.addWidget(self.tabWidget)
        self.gridLayout.addWidget(self.groupBox_3, 0, 1, 3, 1)
        self.listWidget = QtGui.QListWidget(PaipanFrame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listWidget.sizePolicy().hasHeightForWidth())
        self.listWidget.setSizePolicy(sizePolicy)
        self.listWidget.setObjectName(_fromUtf8("listWidget"))
        self.gridLayout.addWidget(self.listWidget, 0, 0, 1, 1)
        self.groupBox = QtGui.QGroupBox(PaipanFrame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setTitle(_fromUtf8(""))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.verticalLayout = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.radio_time1 = QtGui.QRadioButton(self.groupBox)
        self.radio_time1.setChecked(True)
        self.radio_time1.setObjectName(_fromUtf8("radio_time1"))
        self.verticalLayout.addWidget(self.radio_time1)
        self.radio_time2 = QtGui.QRadioButton(self.groupBox)
        self.radio_time2.setObjectName(_fromUtf8("radio_time2"))
        self.verticalLayout.addWidget(self.radio_time2)
        self.radio_time3 = QtGui.QRadioButton(self.groupBox)
        self.radio_time3.setObjectName(_fromUtf8("radio_time3"))
        self.verticalLayout.addWidget(self.radio_time3)
        self.gridLayout.addWidget(self.groupBox, 1, 0, 1, 1)
        self.groupBox_2 = QtGui.QGroupBox(PaipanFrame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy)
        self.groupBox_2.setTitle(_fromUtf8(""))
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.radio_modeb = QtGui.QRadioButton(self.groupBox_2)
        self.radio_modeb.setObjectName(_fromUtf8("radio_modeb"))
        self.verticalLayout_2.addWidget(self.radio_modeb)
        self.radio_modeh = QtGui.QRadioButton(self.groupBox_2)
        self.radio_modeh.setChecked(True)
        self.radio_modeh.setObjectName(_fromUtf8("radio_modeh"))
        self.verticalLayout_2.addWidget(self.radio_modeh)
        self.radio_modez = QtGui.QRadioButton(self.groupBox_2)
        self.radio_modez.setObjectName(_fromUtf8("radio_modez"))
        self.verticalLayout_2.addWidget(self.radio_modez)
        self.gridLayout.addWidget(self.groupBox_2, 2, 0, 1, 1)

        self.retranslateUi(PaipanFrame)
        QtCore.QObject.connect(self.listWidget, QtCore.SIGNAL(_fromUtf8("itemClicked(QListWidgetItem*)")), PaipanFrame.onSelPerson)
        QtCore.QObject.connect(self.listWidget, QtCore.SIGNAL(_fromUtf8("itemDoubleClicked(QListWidgetItem*)")), PaipanFrame.onDbclkPerson)
        QtCore.QObject.connect(self.tabWidget, QtCore.SIGNAL(_fromUtf8("tabCloseRequested(int)")), PaipanFrame.onCloseTab)
        QtCore.QMetaObject.connectSlotsByName(PaipanFrame)

    def retranslateUi(self, PaipanFrame):
        PaipanFrame.setWindowTitle(_translate("PaipanFrame", "Frame", None))
        self.radio_time1.setText(_translate("PaipanFrame", "手表时", None))
        self.radio_time2.setText(_translate("PaipanFrame", "平太阳时", None))
        self.radio_time3.setText(_translate("PaipanFrame", "真太阳时", None))
        self.radio_modeb.setText(_translate("PaipanFrame", "八字", None))
        self.radio_modeh.setText(_translate("PaipanFrame", "河洛", None))
        self.radio_modez.setText(_translate("PaipanFrame", "紫微", None))

