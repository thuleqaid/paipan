# -*- coding: utf-8 -*-
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import heluoframe

class TestHeLuoFrame(QDialog):
    def __init__(self,parent=None):
        super(TestHeLuoFrame,self).__init__(parent)
        layout=QVBoxLayout()
        frame=heluoframe.HeluoFrame()
        frame.setupUi()
        frame.setupData(1,2013,7,3,12,45,0)
        layout.addWidget(frame)
        self.setLayout(layout)
        self.resize(640,480)

if __name__ == '__main__':
    app=QApplication(sys.argv)
    form=TestHeLuoFrame()
    form.show()
    app.exec_()
