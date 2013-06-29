import lunar
import ruleparser

class HeLuoPaiPan(object):
    def __init__(self):
        self._lunar=lunar.Lunar()
        self.loadConfig('heluo_rule.txt')

    def setPerson(self,gender,*cal):
        info=self._lunar.transCal(cal)
        self.setParams(
            XingBie=gender,
            ShengNian=cal[0],
            ShengNianGan=(info[0][0]-1)%10+1,
            ShengNianZhi=(info[0][0]-1)%12+1,
            ShengYueGan=(info[0][1]-1)%10+1,
            ShengYueZhi=(info[0][1]-1)%12+1,
            ShengRiGan=(info[0][2]-1)%10+1,
            ShengRiZhi=(info[0][2]-1)%12+1,
            ShengShiGan=(info[0][3]-1)%10+1,
            ShengShiZhi=(info[0][3]-1)%12+1,
            )
        # calculate tianshu and dishu
        tianshu=self.getData('NianGanTianShu')+ \
                self.getData('NianZhiTianShu')+ \
                self.getData('YueGanTianShu')+ \
                self.getData('YueZhiTianShu')+ \
                self.getData('RiGanTianShu')+ \
                self.getData('RiZhiTianShu')+ \
                self.getData('ShiGanTianShu')+ \
                self.getData('ShiZhiTianShu')
        if tianshu>25:
            tianshu-=25
        if tianshu%10==0:
            tianshu/=10
        else:
            tianshu%=10
        dishu=self.getData('NianGanDiShu')+ \
              self.getData('NianZhiDiShu')+ \
              self.getData('YueGanDiShu')+ \
              self.getData('YueZhiDiShu')+ \
              self.getData('RiGanDiShu')+ \
              self.getData('RiZhiDiShu')+ \
              self.getData('ShiGanDiShu')+ \
              self.getData('ShiZhiDiShu')
        if dishu>30:
            dishu-=30
        if dishu%10==0:
            dishu/=10
        else:
            dishu%=10
        if tianshu==5 or dishu==5:
            if ((cal[0]-1984)%10+1)==self.getData('ShengNianGan'):
                yuan=int((cal[0]-1864)/60)%3
            else:
                yuan=int((cal[0]-1-1864)/60)%3
            if yuan==0:
                if self.getData('XingBie')==1:
                    if tianshu==5:
                        tianshu=8
                    if dishu==5:
                        dishu=8
                else:
                    if tianshu==5:
                        tianshu=2
                    if dishu==5:
                        dishu=2
            elif yuan==2:
                if self.getData('XingBie')==1:
                    if tianshu==5:
                        tianshu=9
                    if dishu==5:
                        dishu=9
                else:
                    if tianshu==5:
                        tianshu=7
                    if dishu==5:
                        dishu=7
            else:
                if self.getData('NanNv') in (1,2):
                    if tianshu==5:
                        tianshu=8
                    if dishu==5:
                        dishu=8
                else:
                    if tianshu==5:
                        tianshu=2
                    if dishu==5:
                        dishu=2
        # calculate gua of tianshu and dishu
        tbl_gua={1:2,2:0,3:4,4:3,6:7,7:6,8:1,9:5}
        tiangua=tbl_gua[tianshu]
        digua=tbl_gua[dishu]
        # calculate xian tian gua
        if self.getData('NanNv') in (1,2):
            gua1=digua*8+tiangua
        else:
            gua1=tiangua*8+digua
        # identify yuan tang
        yaocnt,yaosts=self.getBitSts(gua1,6)
        shizhi=self.getData('ShengShiZhi')
        if shizhi<=6:
            yinyang=1
        else:
            yinyang=0
            shizhi-=6
            yaocnt=6-yaocnt
        if 1<=yaocnt<=3:
            if shizhi<=yaocnt*2:
                if shizhi>yaocnt:
                    shizhi-=yaocnt
                for i in range(6):
                    if yaosts[i]==yinyang:
                        shizhi-=1
                    if shizhi<=0:
                        yuantang=i+1
                        break
            else:
                shzhi-=yaocnt*2
                for i in range(6):
                    if yaosts[i]!=yinyang:
                        shizhi-=1
                    if shizhi<=0:
                        yuantang=i+1
                        break
        elif 4<=yaocnt<=5:
            if shizhi<=yaocnt:
                for i in range(6):
                    if yaosts[i]==yinyang:
                        shizhi-=1
                    if shizhi<=0:
                        yuantang=i+1
                        break
            else:
                shizhi-=yaocnt
                for i in range(6):
                    if yaosts[i]!=yinyang:
                        shizhi-=1
                    if shizhi<=0:
                        yuangtang=i+1
                        break
        else:
            if gua1==63:
                if self.getData('XingBie')==1:
                    if yinyang==1:
                        if shizhi>3:
                            yuantang=shizhi-3
                        else:
                            yuantang=shizhi
                    else:
                        if shizhi>3:
                            yuantang=shizhi
                        else:
                            yuantang=shizhi+3
                else:
                    jieqi=self._lunar.getJieqiIndex(cal)
                    if 10<=jieqi[1]<22:
                        if yinyang==1:
                            if shizhi>3:
                                yuantang=shizhi-3
                            else:
                                yuantang=shizhi
                        else:
                            if shizhi>3:
                                yuantang=shizhi
                            else:
                                yuantang=shizhi+3
                    else:
                        if yinyang==1:
                            if shizhi>3:
                                yuantang=10-shizhi
                            else:
                                yuantang=7-shizhi
                        else:
                            if shizhi>3:
                                yuantang=7-shizhi
                            else:
                                yuantang=4-shizhi
            else:
                if self.getData('XingBie')==2:
                    if yinyang==1:
                        if shizhi>3:
                            yuantang=shizhi-3
                        else:
                            yuantang=shizhi
                    else:
                        if shizhi>3:
                            yuantang=shizhi
                        else:
                            yuantang=shizhi+3
                else:
                    jieqi=self._lunar.getJieqiIndex(cal)
                    if 10<=jieqi[1]<22:
                        if yinyang==1:
                            if shizhi>3:
                                yuantang=10-shizhi
                            else:
                                yuantang=7-shizhi
                        else:
                            if shizhi>3:
                                yuantang=7-shizhi
                            else:
                                yuantang=4-shizhi
                    else:
                        if yinyang==1:
                            if shizhi>3:
                                yuantang=shizhi-3
                            else:
                                yuantang=shizhi
                        else:
                            if shizhi>3:
                                yuantang=shizhi
                            else:
                                yuantang=shizhi+3
        self._data['Gua1']=gua1
        self._data['YuanTang1']=yuantang
        # calculate hou tian gua
        gua2=gua1^(1<<(6-yuantang))
        if yuantang>3:
            yuantang-=3
        else:
            yuantang+=3
        # ToDo: hou tian gua exception for gua 10,18 and 34
        self._data['Gua2']=gua2
        self._data['YuanTang2']=yuantang

    def getNianTime(self,age):
        if ((self.getData('ShengNian')-1984)%10+1)==self.getData('ShengNianGan'):
            year=self.getData('ShengNian')+age-1
        else:
            year=self.getData('ShengNian')-1+age-1
        outs=[]
        outs.append(self._lunar.getJieQiTime(year,1))
        outs.append(self._lunar.getJieQiTime(year+1,1))
        return tuple(outs)

    def getYueTime(self,age,month):
        if ((self.getData('ShengNian')-1984)%10+1)==self.getData('ShengNianGan'):
            year=self.getData('ShengNian')+age-1
        else:
            year=self.getData('ShengNian')-1+age-1
        index=month*2-1
        outs=[]
        outs.append(self._lunar.getJieQiTime(year,index))
        if index>22:
            outs.append(self._lunar.getJieQiTime(year+1,1))
        else:
            outs.append(self._lunar.getJieQiTime(year,index+2))
        return tuple(outs)

    def getRiTime(self,age,month,day):
        if ((self.getData('ShengNian')-1984)%10+1)==self.getData('ShengNianGan'):
            year=self.getData('ShengNian')+age-1
        else:
            year=self.getData('ShengNian')-1+age-1
        index=month*2-1
        outs=[]
        tempout=list(self._lunar.getJieQiTime(year,index))
        if day!=1:
            tempout[3]=0
            tempout[4]=0
            tempout[5]=0
        days=self._lunar.getDays(tempout[0],tempout[1])
        if tempout[2]+day-1>days:
            tempout[1]+=1
            if tempout[1]>12:
                tempout[0]+=1
                tempout[1]=1
            tempout[2]=tempout[2]+day-1-days
        else:
            tempout[2]=tempout[2]+day-1
        outs.append(tuple(tempout))
        tempout[3]=23
        tempout[4]=59
        tempout[5]=59
        outs.append(tuple(tempout))
        return tuple(outs)

    def getNianYun(self,age):
        agecnt=age
        # decide whether xian tian gua or hou tian gua?
        gua=self.getData('Gua1')
        yuantang=self.getData('YuanTang1')
        yaocnt,yaosts=self.getBitSts(gua,6)
        if 36+yaocnt*3<agecnt:
            agecnt=agecnt-36-yaocnt*3
            gua=self.getData('Gua2')
            yuantang=self.getData('YuanTang2')
            yaocnt,yaosts=self.getBitSts(gua,6)
            if 36+yaocnt*3<agecnt:
                return ()
        # decide yao
        for i in range(6):
            index=i+yuantang
            if index>6:
                index-=6
            if agecnt<=6+3*yaosts[index-1]:
                break
            else:
                agecnt=agecnt-6-3*yaosts[index-1]
        # get liu nian gua
        if yaosts[index-1]==0:
            index-=1
            while agecnt>0:
                index+=1
                if index>6:
                    index=1
                gua=gua^(1<<(6-index))
                agecnt-=1
            yuantang=index
        else:
            yinyang=(self.getData('ShengNianGan')+(age-agecnt))%2
            if yinyang!=1:
                gua=gua^(1<<(6-index))
            agecnt-=1
            yuantang=index
            if agecnt>0:
                if index>3:
                    gua=gua^(1<<(9-index))
                    yuantang-=3
                else:
                    gua=gua^(1<<(3-index))
                    yuantang+=3
                agecnt-=1
                index-=1
                while agecnt>0:
                    index+=1
                    if index>6:
                        index=1
                    gua=gua^(1<<(6-index))
                    agecnt-=1
                    yuantang=index
        return (gua,yuantang)

    def getYueYun(self,age,month):
        gua,yao=self.getNianYun(age)
        for i in range((month+1)/2):
            yao+=1
            if yao>6:
                yao-=6
            gua=gua^(1<<(6-yao))
        if month%2==0:
            if yao>3:
                yao-=3
            else:
                yao+=3
            gua=gua^(1<<(6-yao))
        return (gua,yao)

    def getRiYun(self,age,month,day):
        gua,yao=self.getYueYun(age,month)
        yao=yao+1+(day-1)/6
        if yao>6:
            yao-=6
        gua=gua^(1<<(6-yao))
        yao=(day-1)%6+1
        return (gua,yao)

    def getBitSts(self,data,dlen):
        gua=data
        yaosts=[0 for i in range(dlen)]
        yaocnt=0
        for i in range(dlen):
            if gua%2>0:
                yaosts[dlen-1-i]=1
                yaocnt+=1
            gua=gua/2
        return yaocnt,tuple(yaosts)

    # public functions
    def setParams(self,**kwargs):
        self.init_data()
        for k,v in kwargs.items():
            self._data[k]=v

        for target in self._outputdata.keys():
            self._data[target]=self.calcData(target)

    def getData(self,datakey,defaultvalue=''):
        if datakey in self._data:
            return self._data[datakey]
        else:
            return defaultvalue

    # private functions
    def init_data(self):
        self._data={}
        self._data['ShengNianGan']=-1
        self._data['ShengNianZhi']=-1
        self._data['ShengYueGan']=-1
        self._data['ShengYueZhi']=-1
        self._data['ShengRiGan']=-1
        self._data['ShengRiZhi']=-1
        self._data['ShengShiGan']=-1
        self._data['ShengShiZhi']=-1
        self._data['XingBie']=1

    def init_const(self):
        self._inputdata={}
        self._inputdata['ShengNianGan']=(1,2,3,4,5,6,7,8,9,10)
        self._inputdata['ShengNianZhi']=(1,2,3,4,5,6,7,8,9,10,11,12)
        self._inputdata['ShengYueGan']=(1,2,3,4,5,6,7,8,9,10)
        self._inputdata['ShengYueZhi']=(1,2,3,4,5,6,7,8,9,10,11,12)
        self._inputdata['ShengRiGan']=(1,2,3,4,5,6,7,8,9,10)
        self._inputdata['ShengRiZhi']=(1,2,3,4,5,6,7,8,9,10,11,12)
        self._inputdata['ShengShiGan']=(1,2,3,4,5,6,7,8,9,10)
        self._inputdata['ShengShiZhi']=(1,2,3,4,5,6,7,8,9,10,11,12)
        self._inputdata['XingBie']=(1,2)
        self._outputdata={}

    def loadConfig(self,cfile,filecode='cp936'):
        self.init_const()
        rp=ruleparser.RuleParser()
        rp.parse(cfile,filecode)
        res=rp.results()
        for r in res:
            target=r['PTARGET']
            self._inputdata[target]=tuple(r['POUTPUT'])
            self._outputdata[target]={'name':r.get('PNAME',''),'params':tuple(r['PINPUT']),'data':tuple(r['PDATA'])}
            if 'PTAG' in r:
                self._outputdata[target]['tag']=tuple(r['PTAG'])
            else:
                self._outputdata[target]['tag']=()

    def calcData(self,datakey,defaultvalue=''):
        if datakey in self._inputdata:
            if datakey in self._data:
                return self._data[datakey]
            elif datakey in self._outputdata:
                dindex=0
                for pkey in self._outputdata[datakey]['params']:
                    dindex=dindex*len(self._inputdata[pkey])+self._inputdata[pkey].index(self.calcData(pkey))
                return self._outputdata[datakey]['data'][dindex]
            else:
                return defaultvalue
        else:
            return defaultvalue
if __name__ == '__main__':
    h=HeLuoPaiPan()
    h.setPerson(1,1983,9,2,13,15,0)
    print h.getNianYun(27),h.getNianTime(27)
    for i in range(12):
        print "\t",h.getYueYun(27,i+1),h.getYueTime(27,i+1)
        for j in range(30):
            print "\t\t",h.getRiYun(27,i+1,j+1),h.getRiTime(27,i+1,j+1)
