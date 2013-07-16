# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'heluoframe.ui'
#
# Created: Mon Jul 15 19:27:15 2013
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

class Ui_HeluoFrame(object):
    def setupUi(self, HeluoFrame):
        HeluoFrame.setObjectName(_fromUtf8("HeluoFrame"))
        HeluoFrame.resize(482, 355)
        HeluoFrame.setFrameShape(QtGui.QFrame.StyledPanel)
        HeluoFrame.setFrameShadow(QtGui.QFrame.Raised)
        self.horizontalLayout = QtGui.QHBoxLayout(HeluoFrame)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.treeWidget = QtGui.QTreeWidget(HeluoFrame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.treeWidget.sizePolicy().hasHeightForWidth())
        self.treeWidget.setSizePolicy(sizePolicy)
        self.treeWidget.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.treeWidget.setObjectName(_fromUtf8("treeWidget"))
        self.horizontalLayout.addWidget(self.treeWidget)
        self.textEdit = QtGui.QTextEdit(HeluoFrame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textEdit.sizePolicy().hasHeightForWidth())
        self.textEdit.setSizePolicy(sizePolicy)
        self.textEdit.setUndoRedoEnabled(False)
        self.textEdit.setReadOnly(True)
        self.textEdit.setObjectName(_fromUtf8("textEdit"))
        self.horizontalLayout.addWidget(self.textEdit)

        self.retranslateUi(HeluoFrame)
        QtCore.QObject.connect(self.treeWidget, QtCore.SIGNAL(_fromUtf8("itemClicked(QTreeWidgetItem*,int)")), HeluoFrame.onSelectAge)
        QtCore.QMetaObject.connectSlotsByName(HeluoFrame)

    def retranslateUi(self, HeluoFrame):
        HeluoFrame.setWindowTitle(_translate("HeluoFrame", "Frame", None))
        self.treeWidget.headerItem().setText(0, _translate("HeluoFrame", "运势", None))

