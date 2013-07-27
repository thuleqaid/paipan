# -*- coding: utf-8 -*-
import sys
sys.path.append('..')
import re
import datetime
import logging
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import paipanframe_ui
import birthdayframe
import heluoframe
import db.birthdb as birthdb
import db.solartime as solartime

class PaipanFrame(QFrame):
    def setupUi(self):
        self.ui=paipanframe_ui.Ui_PaipanFrame()
        self.ui.setupUi(self)
        # add a tab for birthday frame
        self.bframe=birthdayframe.BirthdayFrame()
        self.bframe.setupUi()
        self.bframe.setCbAdd(self.addPerson)
        self.bframe.setCbUpdate(self.hasPerson,self.updatePerson)
        self.bframe.setCbDelete(self.delPerson)
        self.ui.tabWidget.addTab(self.bframe,u'生日')
        # load birthday database
        self.birth=birthdb.BirthDB()
        for row in self.birth.data(('name',)):
            self.ui.listWidget.addItem(row[0])
        self.timedb=solartime.SolarTimeDB()
    def _collectPersonInfo(self,frame):
        info=frame.data()
        birthday="%d-%d-%d %d:%d:%d"%info['birthday']
        name=info['name'].decode('utf8')
        if info['gender']==1:
            gender='M'
        else:
            gender='F'
        locationtype=info.get('locationtype','U')
        if locationtype=='L':
            locationdata=str(info.get('locationdata',120.0))
        elif locationtype=='C':
            locationdata=str(info.get('locationdata',-1))
        else:
            locationtype='U'
            locationdata=''
        return (name,gender,birthday,locationtype,locationdata)
    def addPerson(self,frame):
        info=self._collectPersonInfo(frame)
        name=info[0]
        if len(self.birth.find('name',name))<=0:
            # name must be unique
            self.birth.append(('name','gender','birthday','locationtype','locationdata'),(info,))
            self.ui.listWidget.addItem(name)
    def hasPerson(self,name):
        for i in range(self.ui.listWidget.count()):
            item=self.ui.listWidget.item(i)
            if item.text().toUtf8().data()==name:
                break
        else:
            return False
        return True
    def updatePerson(self,frame):
        info=self._collectPersonInfo(frame)
        name=info[0]
        rows=self.birth.find('name',name,('id',))
        if len(rows)>0:
            pid=rows[0][0]
            self.birth.update(pid,gender=info[1],birthday=info[2],locationtype=info[3],locationdata=info[4])
    def delPerson(self,frame):
        info=self._collectPersonInfo(frame)
        name=info[0]
        rows=self.birth.find('name',name,('id',))
        if len(rows)>0:
            pid=rows[0][0]
            self.birth.delete(pid)
            self.ui.listWidget.takeItem(self.ui.listWidget.currentRow())
    def _fetchdata(self,item):
        name=item.text().toUtf8().data().decode('utf8')
        row=self.birth.find('name',name,('name','gender','birthday','locationtype','locationdata'))[0]
        name=row[0]
        if row[1]=='F':
            gender=2
        else:
            gender=1
        birthday=[int(x) for x in re.split(r'[- :]+',row[2])]
        return (name,gender,tuple(birthday),row[-2],row[-1])
    def onSelPerson(self,item):
        name,gender,birthday,ltype,ldata=self._fetchdata(item)
        self.bframe.setData(name=name,gender=gender,birthday=birthday,locationtype=ltype,locationdata=ldata)
    def onDbclkPerson(self,item):
        name,gender,birthday,ltype,ldata=self._fetchdata(item)
        if self.ui.radio_modeb.isChecked():
            ppmode='B'
        elif self.ui.radio_modeh.isChecked():
            ppmode='H'
        elif self.ui.radio_modez.isChecked():
            ppmode='Z'
        if self.ui.radio_time1.isChecked():
            timemode=1
        elif self.ui.radio_time2.isChecked():
            timemode=2
        elif self.ui.radio_time3.isChecked():
            timemode=3
        tabname=ppmode+str(timemode)+name
        for i in range(self.ui.tabWidget.count()-1):
            if tabname==self.ui.tabWidget.tabText(i+1).toUtf8().data().decode('utf8'):
                # selected person's tab exists and switch to that tab
                self.ui.tabWidget.setCurrentIndex(i+1)
                break
        else:
            # selected person's tab not exists
            # calculate time according to time mode
            if timemode>1:
                # CityAdj Time
                info=tuple(birthday)
                if ltype=='C':
                    datediff=self.timedb.cityDiff(int(ldata),0)
                elif ltype=='L':
                    datediff=int((float(ldata)-120)*4*60)
                else:
                    datediff=0
                dt2=datetime.datetime(*info)+datetime.timedelta(seconds=datediff)
                info2=(dt2.year,dt2.month,dt2.day,dt2.hour,dt2.minute,dt2.second)
                if timemode>2:
                    # SolarAdj Time
                    datediff=self.timedb.dateDiff(info[1],info[2])
                    dt2=datetime.datetime(*info2)+datetime.timedelta(seconds=datediff)
                    birthday=(dt2.year,dt2.month,dt2.day,dt2.hour,dt2.minute,dt2.second)
                else:
                    birthday=tuple(info2)
            if ppmode=='B':
                # BaZi PaiPan
                pass
            elif ppmode=='H':
                # HeLuo PaiPan
                hframe=heluoframe.HeluoFrame()
                hframe.setupUi()
                hframe.setupData(gender,*birthday)
                tabindex=self.ui.tabWidget.addTab(hframe,tabname)
                self.ui.tabWidget.setCurrentIndex(tabindex)
            elif ppmode=='Z':
                # ZiWei PaiPan
                pass
    def onCloseTab(self,index):
        if index>0:
            # the first tab(birthday frame) cannot be closed
            self.ui.tabWidget.removeTab(index)

