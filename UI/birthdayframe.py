# -*- coding: utf-8 -*-
import sys
sys.path.append('..')
import datetime
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import birthdayframe_ui
import db.solartime as solartime

class BirthdayFrame(QFrame):
    def setupUi(self):
        self.ui=birthdayframe_ui.Ui_BirthdayFrame()
        self.ui.setupUi(self)
        self._dirty=False
        self._funcadd=None
        self._funcupdate=None
        self._funcupdatetest=None
        self._funcdel=None
        self._timedb=solartime.SolarTimeDB()
        self._updateSelDateTime()
        for data in self._timedb.provinces():
            self.ui.combo_p.addItem(data[1],QVariant(data[0]))
    def setCbAdd(self,func):
        self._funcadd=func
    def setCbUpdate(self,functest,funcupdate):
        self._funcupdate=funcupdate
        self._funcupdatetest=functest
    def setCbDelete(self,func):
        self._funcdel=func
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
            n=datetime.datetime.now()
            self.ui.calendar.setSelectedDate(QDate(n.year,n.month,n.day))
            self.ui.time.setTime(QTime(n.hour,n.minute,n.second))
        loctype=kwargs.get('locationtype','U')
        if loctype=='C':
            self.ui.radio_lc.setChecked(True)
            cityid=int(kwargs.get('locationdata','1'))
            pid=self._timedb.province(cityid)
            for i in range(self.ui.combo_p.count()):
                item=self.ui.combo_p.itemData(i)
                if item.toInt()[0]==pid:
                    self.ui.combo_p.setCurrentIndex(i)
                    # self.onProvinceChg(i) will be called after here
                    for j in range(self.ui.combo_c.count()):
                        item=self.ui.combo_c.itemData(j)
                        if item.toList()[0].toInt()[0]==cityid:
                            self.ui.combo_c.setCurrentIndex(j)
                            break
                    else:
                        self.ui.combo_c.setCurrentIndex(0)
                    break
            else:
                self.ui.combo_p.setCurrentIndex(0)
                self.ui.combo_c.setCurrentIndex(0)
            self.ui.edit_lon.setText('120.0')
        elif loctype=='L':
            self.ui.radio_ll.setChecked(True)
            longitute=kwargs.get('locationdata','120.0')
            self.ui.edit_lon.setText(longitute)
        else:
            self.ui.radio_lu.setChecked(True)
            self.ui.edit_lon.setText('120.0')
        self._dirty=False
        if self._funcdel:
            self.ui.btnDelete.setEnabled(True)
        self._updateBtn()
        self._updateSelDateTime()
    def data(self):
        info={}
        info['name']=self.ui.edit_name.text().toUtf8().data()
        if self.ui.radio_male.isChecked():
            info['gender']=1
        else:
            info['gender']=2
        info['birthday']=self._getSelDateTime()
        if self.ui.radio_lu.isChecked():
            info['locationtype']='U'
        elif self.ui.radio_ll.isChecked():
            info['locationtype']='L'
            info['locationdata']=self.ui.edit_lon.text().toDouble()[0]
        elif self.ui.radio_lc.isChecked():
            info['locationtype']='C'
            index=self.ui.combo_c.currentIndex()
            if index>=0:
                info['locationdata']=self.ui.combo_c.itemData(index).toList()[0].toInt()[0]
            else:
                self._log.critical("City Index error. P(%d) C(%d)"%(self.ui.combo_p.currentIndex(),index))
                info['locationdata']=0
        return info
    def _getSelDateTime(self):
        d=self.ui.calendar.selectedDate()
        t=self.ui.time.time()
        return (d.year(),d.month(),d.day(),t.hour(),t.minute(),t.second())
    def _updateSelDateTime(self):
        info=self._getSelDateTime()
        self.ui.edit_time1.setText("%02d-%02d-%02d %02d:%02d:%02d"%info)
        if self.ui.radio_lu.isChecked():
            datediff=0
        elif self.ui.radio_ll.isChecked():
            lon=self.ui.edit_lon.text().toDouble()[0]
            datediff=int((lon-120)*4*60)
        elif self.ui.radio_lc.isChecked():
            index=self.ui.combo_c.currentIndex()
            if index>=0:
                datediff=self.ui.combo_c.itemData(index).toList()[1].toInt()[0]
            else:
                datediff=0
        dt2=datetime.datetime(*info)+datetime.timedelta(seconds=datediff)
        info2=(dt2.year,dt2.month,dt2.day,dt2.hour,dt2.minute,dt2.second)
        datediff=self._timedb.dateDiff(info[1],info[2])
        dt2=datetime.datetime(*info2)+datetime.timedelta(seconds=datediff)
        info3=(dt2.year,dt2.month,dt2.day,dt2.hour,dt2.minute,dt2.second)
        self.ui.edit_time2.setText("%02d-%02d-%02d %02d:%02d:%02d"%info2)
        self.ui.edit_time3.setText("%02d-%02d-%02d %02d:%02d:%02d"%info3)
    def _updateBtn(self):
        self.ui.btnAdd.setEnabled(False)
        self.ui.btnUpdate.setEnabled(False)
        if self.ui.edit_name.text():
            # name in not null
            if self.isDirty():
                self.ui.btnDelete.setEnabled(False)
                # data has been modified
                if self._funcupdate and self._funcupdatetest:
                    # functions for update exist
                    if self._funcupdatetest(self.ui.edit_name.text().toUtf8().data()):
                        # current data can be updated
                        self.ui.btnUpdate.setEnabled(True)
                    else:
                        self.ui.btnAdd.setEnabled(True)
                else:
                    if self._funcadd:
                        self.ui.btnAdd.setEnabled(True)
    def isDirty(self):
        return self._dirty
    def onNameChg(self,text):
        self._dirty=True
        self._updateBtn()
    def onGenderToggled(self,flag):
        self._dirty=True
        self._updateBtn()
    def onLocToggled(self,flag):
        self._dirty=True
        if self.ui.radio_lu.isChecked():
            self.ui.edit_lon.setEnabled(False)
            self.ui.combo_p.setEnabled(False)
            self.ui.combo_c.setEnabled(False)
        elif self.ui.radio_ll.isChecked():
            self.ui.edit_lon.setEnabled(True)
            self.ui.combo_p.setEnabled(False)
            self.ui.combo_c.setEnabled(False)
        elif self.ui.radio_lc.isChecked():
            self.ui.edit_lon.setEnabled(False)
            self.ui.combo_p.setEnabled(True)
            self.ui.combo_c.setEnabled(True)
        self._updateBtn()
        self._updateSelDateTime()
    def onDateChg(self):
        self._dirty=True
        self._updateBtn()
        self._updateSelDateTime()
    def onTimeChg(self,time):
        self._dirty=True
        self._updateBtn()
        self._updateSelDateTime()
    def onBtnAdd(self):
        self._dirty=False
        self._updateBtn()
        self._funcadd(self)
    def onBtnUpdate(self):
        self._dirty=False
        self._updateBtn()
        self._funcupdate(self)
    def onBtnDelete(self):
        self._funcdel(self)
        self._dirty=True
        self._updateBtn()
    def onBtnNow(self):
        n=datetime.datetime.now()
        self.ui.calendar.setSelectedDate(QDate(n.year,n.month,n.day))
        self.ui.time.setTime(QTime(n.hour,n.minute,n.second))
        self._dirty=True
        self._updateBtn()
    def onProvinceChg(self,index):
        # province change -> city change -> dirty flag
        pid=self.ui.combo_p.itemData(index).toInt()[0]
        self.ui.combo_c.clear()
        for data in self._timedb.cities(pid):
            self.ui.combo_c.addItem(data[1],QVariant.fromList((QVariant(data[0]),QVariant(data[2]))))
    def onCityChg(self,index):
        self._dirty=True
        self._updateBtn()
        self._updateSelDateTime()
    def onEditLonFinish(self):
        self._dirty=True
        self._updateBtn()
        self._updateSelDateTime()
