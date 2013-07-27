# -*- coding: utf-8 -*-
import sys
sys.path.append('..')
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import liuyaoframe_ui
import liuyaoppframe
import liuyaoresultframe
import db.liuyaodb as liuyaodb

class LiuyaoFrame(QFrame):
    def setupUi(self):
        self.ui=liuyaoframe_ui.Ui_LiuyaoFrame()
        self.ui.setupUi(self)
        self.pframe=liuyaoppframe.LiuyaoPPFrame()
        self.pframe.setupUi()
        self.pframe.setCbPaipan(self.cbPaipan)
        self.ui.tabWidget.addTab(self.pframe,u"排盘")
        # load database
        self.liuyaodb=liuyaodb.LiuyaoDB()
        for row in self.liuyaodb.data(('id','question',)):
            self.ui.listWidget.addItem("%d:%s"%(row[0],row[1]))
    def onCloseTab(self,tindex):
        if tindex>0:
            self.ui.tabWidget.removeTab(tindex)
    def onDbclkItem(self,item):
        txt=int(item.text().toUtf8().data().split(':')[0])
        row=self.liuyaodb.find('id',txt,('name','question','gua','guatime','analyze'))
        info={'id':txt,'name':row[0][0],'question':row[0][1],'method2':row[0][2],'datetime':row[0][3],'analyze':row[0][4]}
        rframe=liuyaoresultframe.LiuyaoResultFrame()
        rframe.setupUi()
        rframe.setData(False,info)
        rframe.setCbAdd(self.cbAddRecord)
        rframe.setCbUpdate(self.cbUpdateRecord)
        rframe.setCbDel(self.cbDelRecord)
        tindex=self.ui.tabWidget.addTab(rframe,str(txt))
        self.ui.tabWidget.setCurrentIndex(tindex)
    def cbPaipan(self,frame):
        info=frame.data()
        rframe=liuyaoresultframe.LiuyaoResultFrame()
        rframe.setupUi()
        rframe.setData(True,info)
        rframe.setCbAdd(self.cbAddRecord)
        rframe.setCbUpdate(self.cbUpdateRecord)
        rframe.setCbDel(self.cbDelRecord)
        tindex=self.ui.tabWidget.addTab(rframe,'test')
        self.ui.tabWidget.setCurrentIndex(tindex)
    def _collectInfo(self,frame):
        info=frame.data()
        name=info['name'].decode('utf8')
        question=info['question'].decode('utf8')
        analyze=info['analyze'].decode('utf8')
        return (name,question,info['gua'],info['guatime'],analyze)
    def cbAddRecord(self,frame):
        info=self._collectInfo(frame)
        self.liuyaodb.append(('name','question','gua','guatime','analyze'),(info,))
        newid=self.liuyaodb.getLastId()
        rows=self.liuyaodb.find('id',newid,('question',))
        self.ui.listWidget.addItem("%d:%s"%(newid,rows[0][0]))
        self.ui.tabWidget.setTabText(self.ui.tabWidget.currentIndex(),str(newid))
        return (True,newid)
    def cbUpdateRecord(self,frame):
        info=frame.data()
        rows=self.liuyaodb.find('id',info['id'],('id',))
        if len(rows)>0:
            self.liuyaodb.update(info['id'],name=info['name'],question=info['question'],analyze=info['analyze'])
            return True
        else:
            return False
    def cbDelRecord(self,frame):
        info=frame.data()
        rows=self.liuyaodb.find('id',info['id'],('id',))
        if len(rows)>0:
            self.liuyaodb.delete(info['id'])
            for i in range(self.ui.listWidget.count()):
                item=self.ui.listWidget.item(i)
                txt=int(item.text().toUtf8().data().split(':')[0])
                if txt==info['id']:
                    self.ui.listWidget.takeItem(i)
                    break
            return True
        else:
            return False
