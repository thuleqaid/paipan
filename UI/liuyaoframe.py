# -*- coding: utf-8 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import liuyaoframe_ui
import liuyaoppframe
import liuyaoresultframe

class LiuyaoFrame(QFrame):
    def setupUi(self):
        self.ui=liuyaoframe_ui.Ui_LiuyaoFrame()
        self.ui.setupUi(self)
        self.pframe=liuyaoppframe.LiuyaoPPFrame()
        self.pframe.setupUi()
        self.pframe.setCbPaipan(self.cbPaipan)
        self.ui.tabWidget.addTab(self.pframe,u"排盘")
    def onCloseTab(self,tindex):
        if tindex>0:
            self.ui.tabWidget.removeTab(tindex)
    def onDbclkItem(self,item):
        pass
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
    def cbAddRecord(self,frame):
        return True
    def cbUpdateRecord(self,frame):
        return True
    def cbDelRecord(self,frame):
        return True
