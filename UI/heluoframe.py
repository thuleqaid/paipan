# -*- coding: utf-8 -*-
import sys
sys.path.append('..')
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import heluoframe_ui
import paipan.heluo as heluo

class HeluoFrame(QFrame):
    def setupUi(self):
        self.ui=heluoframe_ui.Ui_HeluoFrame()
        self.ui.setupUi(self)
        self.heluo=None
    def onSelectAge(self,item,col):
        if self.heluo:
            if item.parent():
                cc=item.childCount()
                if cc==12:
                    age=int(item.text(0).split(' ')[0])
                    self.updateNianYun(age)
                elif cc==5:
                    month=int(item.text(0).split(' ')[0])
                    age=int(item.parent().text(0).split(' ')[0])
                    self.updateYueYun(age,month)
                elif cc==0:
                    daygroup=item.parent().indexOfChild(item)
                    month=int(item.parent().text(0).split(' ')[0])
                    age=int(item.parent().parent().text(0).split(' ')[0])
                    self.updateRiYun(age,month,daygroup)
                elif cc in (6,9):
                    age=int(item.child(0).text(0).split(' ')[0])
                    self.updateDaYun(age)
            else:
                idx=self.ui.treeWidget.indexOfTopLevelItem(item)
                if idx==0:
                    self.updateXianTianYun()
                elif idx==1:
                    self.updateHouTianYun()
    def updateXianTianYun(self):
        strs=(u'天',u'地',u'元气',u'反')
        koujue=(u'坤反，主贫',
                u'艮反，多痈疽气塞',
                u'坎反，多聋闭不聪',
                u'巽反，多痼疾',
                u'震反，多跛',
                u'离反，多瞽目受病',
                u'兑反，多唇舌抬祸',
                u'乾反，主夭')
        info=self.heluo.getYuanQi()
        outs=''
        if info[0][0]>=0:
            outs+=strs[0].encode('utf8')+strs[2].encode('utf8')+"\n"
        if info[0][1]>=0:
            outs+=strs[0].encode('utf8')+strs[3].encode('utf8')+strs[2].encode('utf8')+"  "
            outs+=koujue[info[0][1]].encode('utf8')+"\n"
        if info[1][0]>=0:
            outs+=strs[1].encode('utf8')+strs[2].encode('utf8')+"\n"
        if info[1][1]>=0:
            outs+=strs[1].encode('utf8')+strs[3].encode('utf8')+strs[2].encode('utf8')+"  "
            outs+=koujue[info[1][1]].encode('utf8')+"\n"
        info=self.heluo.getXianTianYun()
        outs+=self.heluo.getKouJue(info[0],0,"","\n")
        self.ui.textEdit.setText(outs.decode('utf8'))
    def updateHouTianYun(self):
        info=self.heluo.getHouTianYun()
        outs=self.heluo.getKouJue(info[0],0,"","\n")
        self.ui.textEdit.setText(outs.decode('utf8'))
    def updateDaYun(self,age):
        info=self.heluo.getDaYun(age)
        outs=self.heluo.getKouJue(info[0],info[1],"","\n")
        self.ui.textEdit.setText(outs.decode('utf8'))
    def updateNianYun(self,age):
        infot=self.heluo.getNianTime(age)
        outs="/".join([str(x) for x in infot[0][0:3]])+"~"+"/".join([str(x) for x in infot[1][0:3]])+"\n"
        info=self.heluo.getNianYun(age)
        outs+=self.heluo.getKouJue(info[0],0,"","\n")
        outs+=self.heluo.getKouJue(info[0],info[1],"","\n")
        self.ui.textEdit.setText(outs.decode('utf8'))
    def updateYueYun(self,age,month):
        infot=self.heluo.getYueTime(age,month)
        outs="/".join([str(x) for x in infot[0][0:3]])+"~"+"/".join([str(x) for x in infot[1][0:3]])+"\n"
        info=self.heluo.getYueYun(age,month)
        outs+=self.heluo.getKouJue(info[0],0,"","\n")
        outs+=self.heluo.getKouJue(info[0],info[1],"","\n")
        self.ui.textEdit.setText(outs.decode('utf8'))
    def updateRiYun(self,age,month,daygroup):
        day=daygroup*6+1
        info=self.heluo.getRiYun(age,month,day)
        outs=self.heluo.getKouJue(info[0],0,"","\n")
        for i in range(6):
            infot=self.heluo.getRiTime(age,month,day+i)
            outs+="/".join([str(x) for x in infot[0][0:3]])+"\n"
            info=self.heluo.getRiYun(age,month,day+i)
            outs+=self.heluo.getKouJue(info[0],info[1],"","\n")
            self.ui.textEdit.setText(outs.decode('utf8'))
    def setupData(self,gender,year,month,day,hour,minute,second):
        self.heluo=heluo.HeLuoPaiPan()
        self.heluo.setPerson(gender,year,month,day,hour,minute,second)
        strs=(u'大运',u'岁',u'月',u'日')
        item=QTreeWidgetItem((u'先天',))
        self.ui.treeWidget.addTopLevelItem(item)
        agebase=1
        age=1
        for i in range(6):
            info=self.heluo.getDaYun(agebase)
            while True:
                info2=self.heluo.getDaYun(age)
                if info[0]*10+info[1]!=info2[0]*10+info2[1]:
                    itemy=QTreeWidgetItem(item,("%d~%d %s"%(agebase,age-1,strs[0]),))
                    for j in range(agebase,age):
                        itemy2=QTreeWidgetItem(itemy,("%d %s"%(j,strs[1]),))
                        for k in range(12):
                            itemm=QTreeWidgetItem(itemy2,("%d %s"%(k+1,strs[2]),))
                            for l in range(5):
                                itemd=QTreeWidgetItem(itemm,("%d~%d %s"%(l*6+1,l*6+6,strs[3]),))
                    agebase=age
                    break
                age+=1
        item=QTreeWidgetItem((u'后天',))
        self.ui.treeWidget.addTopLevelItem(item)
        for i in range(6):
            info=self.heluo.getDaYun(agebase)
            while True:
                info2=self.heluo.getDaYun(age)
                if info[0]*10+info[1]!=info2[0]*10+info2[1]:
                    itemy=QTreeWidgetItem(item,("%d~%d %s"%(agebase,age-1,strs[0]),))
                    for j in range(agebase,age):
                        itemy2=QTreeWidgetItem(itemy,("%d %s"%(j,strs[1]),))
                        for k in range(12):
                            itemm=QTreeWidgetItem(itemy2,("%d %s"%(k+1,strs[2]),))
                            for l in range(5):
                                itemd=QTreeWidgetItem(itemm,("%d~%d %s"%(l*6+1,l*6+6,strs[3]),))
                    agebase=age
                    break
                age+=1
