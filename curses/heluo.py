# -*- coding:utf-8 -*-
import re
import sys
sys.path.append('..')
import paipan.heluo as heluo
import db.birthdb as birthdb

class PersonInfo(object):
    def __init__(self):
        self.name=''
        self.gender=1
        self.year=1983
        self.month=9
        self.day=2
        self.hour=13
        self.minute=15
        self.second=0
        pass
    def setName(self,name):
        self.name=name
        return self
    def setGender(self,gender):
        self.gender=(gender-1)%2+1
        return self
    def setBirthday(self,year,month,day,hour,minute,second):
        self.year=year
        self.month=(month-1)%12+1
        self.day=(day-1)%31+1
        self.hour=(hour-1)%24+1
        self.minute=(minute-1)%60+1
        self.second=(second-1)%60+1
        return self

class PersonManager(object):
    def __init__(self):
        self._db=birthdb.BirthDB()
    def iterPerson(self):
        for row in self._db.data(('name','gender','birthday')):
            name=row[0]
            if row[1]=='F':
                gender=2
            else:
                gender=1
            birthday=[int(x) for x in re.split(r'[- :]+',row[2])]
            yield PersonInfo().setName(name).setGender(gender).setBirthday(*birthday)

class HintManager(object):
    D_CHAR_GUA='卦'
    def __init__(self):
        self._heluo=heluo.HeLuoPaiPan()
    def setPerson(self,pinfo):
        self._heluo.setPerson(
                pinfo.gender,
                pinfo.year,
                pinfo.month,
                pinfo.day,
                pinfo.hour,
                pinfo.minute,
                pinfo.second)
        return self

    def getAgeFromYear(self,year):
        birthyear=self._heluo.getData('ShengNian')
        if (birthyear%2)!=(self._heluo.getData('ShengNianGan')%2):
            # born after LiChun
            age=year-birthyear+1
        else:
            # born before LiChun
            age=year-birthyear+2
        return age
    def getHint0(self,age):
        # DaYun
        infot=self._heluo.getDaTime(age)
        outs="/".join([str(x) for x in infot[0][0:3]])+"~"+"/".join([str(x) for x in infot[1][0:3]])+"\n"
        info=self._heluo.getDaYun(age)
        gua=self._heluo.getKouJue(info[0],0,"","")
        outs+=gua[0:gua.index(self.D_CHAR_GUA)]+self.D_CHAR_GUA
        outs+=self._heluo.getKouJue(info[0],info[1],"","\n")
        return outs
    def getHint1(self,age):
        # NianYun
        infot=self._heluo.getNianTime(age)
        outs="/".join([str(x) for x in infot[0][0:3]])+"~"+"/".join([str(x) for x in infot[1][0:3]])+"\n"
        info=self._heluo.getNianYun(age)
        gua=self._heluo.getKouJue(info[0],0,"","")
        outs+=gua[0:gua.index(self.D_CHAR_GUA)]+self.D_CHAR_GUA
        outs+=self._heluo.getKouJue(info[0],info[1],"","\n")
        return outs
    def getHint2(self,age,month):
        # YueYun
        infot=self._heluo.getYueTime(age,month)
        outs="/".join([str(x) for x in infot[0][0:3]])+"~"+"/".join([str(x) for x in infot[1][0:3]])+"\n"
        info=self._heluo.getYueYun(age,month)
        gua=self._heluo.getKouJue(info[0],0,"","")
        outs+=gua[0:gua.index(self.D_CHAR_GUA)]+self.D_CHAR_GUA
        outs+=self._heluo.getKouJue(info[0],info[1],"","\n")
        return outs
    def getHint3(self,age,month):
        # RiYun
        outs=""
        for daygroup in range(5):
            day=daygroup*6+1
            info=self._heluo.getRiYun(age,month,day)
            gua=self._heluo.getKouJue(info[0],0,"","")
            guachar=gua[0:gua.index(self.D_CHAR_GUA)]+self.D_CHAR_GUA
            for i in range(6):
                infot=self._heluo.getRiTime(age,month,day+i)
                outs+="/".join([str(x) for x in infot[0][0:3]])+"\n"
                info=self._heluo.getRiYun(age,month,day+i)
                outs+=guachar+self._heluo.getKouJue(info[0],info[1],"","\n")
        return outs

if __name__ == '__main__':
    ht=HintManager()
    pm=PersonManager()
    for p in pm.iterPerson():
        ht.setPerson(p)
        print p.name
        print ht.getHint1(ht.getAgeFromYear(2014))
