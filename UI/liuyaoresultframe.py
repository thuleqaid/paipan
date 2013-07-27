# -*- coding: utf-8 -*-
import sys
sys.path.append('..')
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import liuyaoresultframe_ui
import paipan.liuyao as liuyao

class LiuyaoResultFrame(QFrame):
    def setupUi(self):
        self.ui=liuyaoresultframe_ui.Ui_LiuyaoResultFrame()
        self.ui.setupUi(self)
        self._liuyao=liuyao.LiuYaoPaiPan()
        self._funcadd=None
        self._funcupdate=None
        self._funcdel=None
        self._flgNew=True
        self._dirty=False
        self._recordid=-1
        self._recordgua='1,1'
        self._recordtime='1,1,1'
        self._recordname=''
        self._recordanalyze=''
    def updateBtn(self):
        if self._flgNew:
            self.ui.btn_update.setEnabled(False)
            self.ui.btn_del.setEnabled(False)
            if self._funcadd:
                if self.ui.edit_name.text() and self.ui.edit_question.text():
                    self.ui.btn_add.setEnabled(True)
                else:
                    self.ui.btn_add.setEnabled(False)
            else:
                self.ui.btn_add.setEnabled(False)
        else:
            self.ui.btn_add.setEnabled(False)
            if self._funcdel:
                self.ui.btn_del.setEnabled(True)
            else:
                self.ui.btn_del.setEnabled(False)
            if self._dirty and self._funcupdate:
                self.ui.btn_update.setEnabled(True)
            else:
                self.ui.btn_update.setEnabled(False)
    def setCbAdd(self,func):
        self._funcadd=func
        self.updateBtn()
    def setCbUpdate(self,func):
        self._funcupdate=func
        self.updateBtn()
    def setCbDel(self,func):
        self._funcdel=func
        self.updateBtn()
    def data(self):
        info={}
        info['id']=self._recordid
        info['gua']=self._recordgua
        info['guatime']=self._recordtime
        info['name']=self.ui.edit_name.text().toUtf8().data()
        info['question']=self.ui.edit_question.text().toUtf8().data()
        info['analyze']=self.ui.text_analyze.toPlainText().toUtf8().data()
        return info
    def setData(self,flgNew,info):
        self._flgNew=flgNew
        self._recordid=info.get('id',-1)
        self._recordtime=info.get('datetime','1,1,1')
        name=info.get('name','')
        if name=='':
            name=u"某人"
        question=info.get('question','')
        self.ui.edit_name.setText(name)
        self.ui.edit_question.setText(question)
        if 'method1' in info:
            guanumbers=[int(x) for x in info['method1'].split(',')]
            gua=self._liuyao.getGuaNoFromNumber(*guanumbers)
        elif 'method2' in info:
            gua=tuple([int(x) for x in info['method2'].split(',')])
        else: # 'method3'
            guanumbers=[int(x) for x in info['method3'].split(',')]
            gua=self._liuyao.getGuaNoFromTongQian(guanumbers)
        self._recordgua=",".join([str(x) for x in gua])
        dt=[int(x) for x in info['datetime'].split(',')]
        if len(dt)<6:
            self._liuyao.paipanGZ(dt[0],dt[1],dt[2],gua)
        else:
            self._liuyao.paipan(dt[0:6],gua)
        self.ui.text_gua.setText(self._liuyao.display())
        self.ui.text_analyze.setPlainText(info.get('analyze',''))
        self._dirty=False
        self.updateBtn()
    def onBtnAdd(self):
        ret=self._funcadd(self)
        if ret[0]:
            self._flgNew=False
            self._dirty=False
            self._recordid=ret[1]
            self.updateBtn()
    def onBtnUpdate(self):
        ret=self._funcupdate(self)
        if ret:
            self._dirty=False
            self.updateBtn()
    def onBtnDelete(self):
        ret=self._funcdel(self)
        if ret:
            self._flgNew=True
            self._dirty=False
            self.updateBtn()
    def onModified(self):
        self._dirty=True
        self.updateBtn()
