# -*- coding: utf-8 -*-
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import heluoframe
import birthdayframe
import liuyaoppframe
import paipanframe

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

class TestBirthdayFrame(QDialog):
    def __init__(self,parent=None):
        super(TestBirthdayFrame,self).__init__(parent)
        layout=QVBoxLayout()
        frame=birthdayframe.BirthdayFrame()
        frame.setupUi()
        frame.setCbAdd(self.printdata)
        frame.setData(name='uat',gender=10,birthday=(1983,9,2,13,15,0))
        layout.addWidget(frame)
        self.setLayout(layout)
        self.resize(640,480)
    def printdata(self,frame):
        info=frame.data()
        outs=''
        outs+=info['name']+"\n"
        if info['gender']==1:
            outs+="Male\n"
        else:
            outs+="Female\n"
        outs+="%d-%d-%d %d:%d:%d"%info['birthday']
        print outs

class TestLiuyaoPPFrame(QDialog):
    def __init__(self,parent=None):
        super(TestLiuyaoPPFrame,self).__init__(parent)
        layout=QVBoxLayout()
        frame=liuyaoppframe.LiuyaoPPFrame()
        frame.setupUi()
        frame.setCbPaipan(self.printdata)
        layout.addWidget(frame)
        self.setLayout(layout)
        self.resize(640,480)
    def printdata(self,frame):
        info=frame.data()
        print info

class TestPaipanFrame(QDialog):
    def __init__(self,parent=None):
        super(TestPaipanFrame,self).__init__(parent)
        frame=paipanframe.PaipanFrame()
        frame.setupUi()
        layout=QVBoxLayout()
        layout.addWidget(frame)
        self.setLayout(layout)
        self.resize(640,480)

if __name__ == '__main__':
    app=QApplication(sys.argv)
    #form=TestHeLuoFrame()
    #form=TestBirthdayFrame()
    form=TestLiuyaoPPFrame()
    #form=TestPaipanFrame()
    form.show()
    app.exec_()
