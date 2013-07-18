# -*- coding: utf-8 -*-
import datetime
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import liuyaoppframe_ui

class LiuyaoPPFrame(QFrame):
    def setupUi(self):
        self.ui=liuyaoppframe_ui.Ui_LiuyaoPPFrame()
        self.ui.setupUi(self)
        self._funcpp=None
    def setCbPaipan(self,func):
        self._funcpp=func
    def data(self):
        info={}
        info['name']=self.ui.edit_name.text().toUtf8().data()
        info['question']=self.ui.edit_question.text().toUtf8().data()
        if self.ui.radio_number.isChecked():
            info['method1']="%d,%d,%d"%(self.ui.edit_mtd11.text().toInt()[0], self.ui.edit_mtd12.text().toInt()[0], self.ui.edit_mtd13.text().toInt()[0])
        elif self.ui.radio_gua.isChecked():
            info['method2']="%d"%(self.ui.edit_mtd2.text().toInt()[0])
        else:
            info['method3']="%d,%d,%d,%d,%d,%d"%(self.ui.edit_mtd31.text().toInt()[0], self.ui.edit_mtd32.text().toInt()[0], self.ui.edit_mtd33.text().toInt()[0], self.ui.edit_mtd34.text().toInt()[0], self.ui.edit_mtd35.text().toInt()[0], self.ui.edit_mtd36.text().toInt()[0])
        d=self.ui.calendar.selectedDate()
        t=self.ui.time.time()
        info['datetime']=(d.year(),d.month(),d.day(),t.hour(),t.minute(),t.second())
        return info
    def onMethodToggled(self,flag):
        if self.ui.radio_number.isChecked():
            self.ui.edit_mtd11.setEnabled(True)
            self.ui.edit_mtd12.setEnabled(True)
            self.ui.edit_mtd13.setEnabled(True)
        else:
            self.ui.edit_mtd11.setEnabled(False)
            self.ui.edit_mtd12.setEnabled(False)
            self.ui.edit_mtd13.setEnabled(False)
        if self.ui.radio_gua.isChecked():
            self.ui.edit_mtd2.setEnabled(True)
        else:
            self.ui.edit_mtd2.setEnabled(False)
        if self.ui.radio_coin.isChecked():
            self.ui.edit_mtd31.setEnabled(True)
            self.ui.edit_mtd32.setEnabled(True)
            self.ui.edit_mtd33.setEnabled(True)
            self.ui.edit_mtd34.setEnabled(True)
            self.ui.edit_mtd35.setEnabled(True)
            self.ui.edit_mtd36.setEnabled(True)
        else:
            self.ui.edit_mtd31.setEnabled(False)
            self.ui.edit_mtd32.setEnabled(False)
            self.ui.edit_mtd33.setEnabled(False)
            self.ui.edit_mtd34.setEnabled(False)
            self.ui.edit_mtd35.setEnabled(False)
            self.ui.edit_mtd36.setEnabled(False)
    def onBtnPaipan(self):
        if self._funcpp:
            self._funcpp(self)
    def onBtnNow(self):
        n=datetime.datetime.now()
        self.ui.calendar.setSelectedDate(QDate(n.year,n.month,n.day))
        self.ui.time.setTime(QTime(n.hour,n.minute,n.second))
