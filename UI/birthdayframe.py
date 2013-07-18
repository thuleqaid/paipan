# -*- coding: utf-8 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import birthdayframe_ui

class BirthdayFrame(QFrame):
    def setupUi(self):
        self.ui=birthdayframe_ui.Ui_BirthdayFrame()
        self.ui.setupUi(self)
        self._dirty=False
        self._funcadd=None
    def setCbAdd(self,func):
        self._funcadd=func
    def setData(self,**kwargs):
        self.ui.edit_name.setText(kwargs.get('name',''))
        gender=kwargs.get('gender',1)
        if gender%2==1:
            self.ui.radio_male.setChecked(True)
            self.ui.radio_female.setChecked(False)
        else:
            self.ui.radio_female.setChecked(True)
            self.ui.radio_male.setChecked(False)
        if ('birthday' in kwargs) and (len(kwargs['birthday'])>=6):
            birth=kwargs['birthday']
            self.ui.calendar.setSelectedDate(QDate(birth[0],birth[1],birth[2]))
            self.ui.time.setTime(QTime(birth[3],birth[4],birth[5]))
        else:
            self.ui.calendar.setSelectedDate(QDate())
            self.ui.time.setTime(QTime())
        self._dirty=False
        self.ui.btnAdd.setEnabled(False)
    def data(self):
        info={}
        info['name']=self.ui.edit_name.text().toUtf8().data()
        if self.ui.radio_male.isChecked():
            info['gender']=1
        else:
            info['gender']=2
        d=self.ui.calendar.selectedDate()
        t=self.ui.time.time()
        info['birthday']=(d.year(),d.month(),d.day(),t.hour(),t.minute(),t.second())
        return info
    def isDirty(self):
        return self._dirty
    def onNameChg(self,text):
        self._dirty=True
        if self.ui.edit_name.text():
            self.ui.btnAdd.setEnabled(True)
        else:
            self.ui.btnAdd.setEnabled(False)
    def onGenderToggled(self,flag):
        self._dirty=True
        if self.ui.edit_name.text():
            self.ui.btnAdd.setEnabled(True)
    def onDateChg(self):
        self._dirty=True
        if self.ui.edit_name.text():
            self.ui.btnAdd.setEnabled(True)
    def onTimeChg(self,time):
        self._dirty=True
        if self.ui.edit_name.text():
            self.ui.btnAdd.setEnabled(True)
    def onBtnAdd(self):
        self._dirty=False
        self.ui.btnAdd.setEnabled(False)
        if self._funcadd:
            self._funcadd(self)
