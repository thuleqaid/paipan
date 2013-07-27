#-*- coding: utf-8 -*-
from datetime import datetime
import lunar

class LiuYaoPaiPan(object):
    Tbl_Gua={1:7,2:6,3:5,4:4,5:3,6:2,7:1,8:0}
    Tbl_ShiYing=(32,16,8,4,2,4,56)
    Tbl_WXGua=(0,0,1,4,4,2,3,3)# 0:Tu,1:Shui,2:Huo,3:Jin,4:Mu
    Tbl_WXZhi=(1,0,4,4,0,2,2,0,3,3,0,1)
    Tbl_ZhuangGua=((32,42,52,50,60,10),
                   (53,43,33,23,13,3),
                   (15,5,55,45,35,25),
                   (38,48,58,8,18,28),
                   (37,27,17,7,57,47),
                   (16,26,36,46,56,6),
                   (54,4,14,24,34,44),
                   (1,51,41,19,9,59))
    Str_LiuQin=(u'兄',u'官',u'孙',u'父',u'财')# index=(base_wx-target_wx)%5
    Str_LiuSheng=(u'青龙',u'朱雀',u'勾陈',u'滕蛇',u'白虎',u'玄武')
    Str_DiZhi=(u'子',u'丑',u'寅',u'卯',u'辰',u'巳',u'午',u'未',u'申',u'酉',u'戌',u'亥')
    Str_Others=(u'年',u'月',u'日',u'时',u'空',u'应')
    Str_Gua=(u'坤',u'艮',u'坎',u'巽',u'震',u'离',u'兑',u'乾')

    def __init__(self):
        self._lunar=lunar.Lunar()

    def getGuaNoFromNumber(self,num1,num2,num3):
        num1=(num1-1)%8+1
        num2=(num2-1)%8+1
        num3=(num3-1)%6+1
        return (num1,num2,num3)
    def getGuaNoFromTongQian(self,tongqian):
        if len(tongqian)<6:
            return ()
        gua=0
        yao=[]
        for i in range(6):
            gua=(gua<<1)+(tongqian[i]%2)
            if tongqian[i]%4 in (0,3):
                yao.append(i+1)
        for k,v in LiuYaoPaiPan.Tbl_Gua.items():
            if v==gua%8:
                gua1=k
            if v==gua/8:
                gua2=k
        return (gua1,gua2)+tuple(yao)
    def paipanGZ(self,yuezhi,rigan,rizhi,gua):
        # Gua
        gua1=LiuYaoPaiPan.Tbl_Gua[gua[0]]+LiuYaoPaiPan.Tbl_Gua[gua[1]]*8
        gua2=gua1
        for yao in gua[2:]:
            gua2=gua2^(1<<(6-yao))
        # KongWang
        kong=(rizhi+(10-rigan))%12+1
        self.setParams(YueZhi=yuezhi,
                       RiGan=rigan,
                       RiZhi=rizhi,
                       KongWang=(kong,kong+1),
                       Gua1=gua1,
                       Gua2=gua2)
        self.calcGua()
    def paipanNow(self,gua):
        dt=datetime.now()
        cal=(dt.year,dt.month,dt.day,dt.hour,dt.minute,dt.second)
        self.paipan(cal,gua)
    def paipan(self,cal,gua):
        info=self._lunar.transCal(cal)
        # Gua
        gua1=LiuYaoPaiPan.Tbl_Gua[gua[0]]+LiuYaoPaiPan.Tbl_Gua[gua[1]]*8
        gua2=gua1
        for yao in gua[2:]:
            gua2=gua2^(1<<(6-yao))
        # KongWang
        kong=13-(info[0][2]+9)/10*2
        self.setParams(NianGan=(info[0][0]-1)%10+1,
                       NianZhi=(info[0][0]-1)%12+1,
                       YueGan=(info[0][1]-1)%10+1,
                       YueZhi=(info[0][1]-1)%12+1,
                       RiGan=(info[0][2]-1)%10+1,
                       RiZhi=(info[0][2]-1)%12+1,
                       ShiGan=(info[0][3]-1)%10+1,
                       ShiZhi=(info[0][3]-1)%12+1,
                       KongWang=(kong,kong+1),
                       Gua1=gua1,
                       Gua2=gua2)
        self.calcGua()
    def display(self,fmt={}):
        sep=fmt.get('sep',' ')
        yangyao=fmt.get('yangyao','-----')
        yinyao=fmt.get('yinyao','-- --')
        dongyao=fmt.get('dongyao','x')
        jingyao=fmt.get('jingyao',' ')
        outs=''
        gua1=self.getData('Gua1')
        gua2=self.getData('Gua2')
        zg1=self.getData('ZhuangGua1')
        zg2=self.getData('ZhuangGua2')
        zg3=self.getData('ZhuangGua3')
        lq1=self.getData('LiuQin1')
        lq2=self.getData('LiuQin2')
        lq3=self.getData('LiuQin3')
        ls=self.getData('LiuShen')

        # flag for display bian-gua
        flg_up=(gua1%8)^(gua2%8)
        flg_dn=(gua1/8)^(gua2/8)

        # get liuqin set
        # calc gua-no(uppergua,lowergua,yao1,...)
        guano=''
        lqset=set(lq1)
        dyao=gua1^gua2
        index=5
        while dyao>0:
            if dyao%2!=0:
                lqset.add(lq2[index])
                guano=str(index+1)+guano
            index-=1
            dyao=dyao/2
        for k,v in LiuYaoPaiPan.Tbl_Gua.items():
            if v==gua1/8:
                guano=str(k)+guano
                break
        for k,v in LiuYaoPaiPan.Tbl_Gua.items():
            if v==gua1%8:
                guano=str(k)+guano
                break

        shiying=self.getData('ShiYing1')
        gong=self.getData('Gong1')
        gongwx=LiuYaoPaiPan.Tbl_WXGua[gong]
        zhi=self.getData('NianZhi')
        if zhi:
            outs+="%s%s%s "%(LiuYaoPaiPan.Str_DiZhi[zhi-1],LiuYaoPaiPan.Str_Others[0],LiuYaoPaiPan.Str_LiuQin[(gongwx-LiuYaoPaiPan.Tbl_WXZhi[zhi-1])%5])
        zhi=self.getData('YueZhi')
        outs+="%s%s%s "%(LiuYaoPaiPan.Str_DiZhi[zhi-1],LiuYaoPaiPan.Str_Others[1],LiuYaoPaiPan.Str_LiuQin[(gongwx-LiuYaoPaiPan.Tbl_WXZhi[zhi-1])%5])
        zhi=self.getData('RiZhi')
        outs+="%s%s%s "%(LiuYaoPaiPan.Str_DiZhi[zhi-1],LiuYaoPaiPan.Str_Others[2],LiuYaoPaiPan.Str_LiuQin[(gongwx-LiuYaoPaiPan.Tbl_WXZhi[zhi-1])%5])
        zhi=self.getData('ShiZhi')
        if zhi:
            outs+="%s%s%s "%(LiuYaoPaiPan.Str_DiZhi[zhi-1],LiuYaoPaiPan.Str_Others[3],LiuYaoPaiPan.Str_LiuQin[(gongwx-LiuYaoPaiPan.Tbl_WXZhi[zhi-1])%5])
        kong=self.getData('KongWang')
        outs+="%s:%s%s"%(LiuYaoPaiPan.Str_Others[4],LiuYaoPaiPan.Str_DiZhi[kong[0]-1],LiuYaoPaiPan.Str_DiZhi[kong[1]-1])
        outs+=" "+guano+"\n"
        for i in range(6):
            yao1=gua1&(1<<i)
            yao2=gua2&(1<<i)
            # Liu Sheng
            outs+="%s"%(LiuYaoPaiPan.Str_LiuSheng[ls[5-i]-1])+sep
            # Fu Chang
            if lq3[5-i] not in lqset:
                outs+="%s%s"%(LiuYaoPaiPan.Str_DiZhi[(zg3[5-i]-1)%12],LiuYaoPaiPan.Str_LiuQin[lq3[5-i]])
            else:
                if len(lqset)<5:
                    outs+="    "
            outs+=sep
            # Ben Gua
            if yao1>0:
                outs+=yangyao
            else:
                outs+=yinyao
            if ((gua1^gua2)&(1<<i))>0:
                outs+=dongyao
            else:
                outs+=jingyao
            outs+="%s%s"%(LiuYaoPaiPan.Str_DiZhi[(zg1[5-i]-1)%12],LiuYaoPaiPan.Str_LiuQin[lq1[5-i]])
            # ShiYing
            if shiying==6-i:
                outs+=LiuYaoPaiPan.Str_Gua[gong]
            elif shiying+3==6-i or shiying-3==6-i:
                outs+=LiuYaoPaiPan.Str_Others[5]
            else:
                outs+='  '
            # Bian Gua
            if (i<3 and flg_up>0) or (i>=3 and flg_dn>0):
                outs+=sep
                if yao2>0:
                    outs+=yangyao
                else:
                    outs+=yinyao
                outs+="%s%s"%(LiuYaoPaiPan.Str_DiZhi[(zg2[5-i]-1)%12],LiuYaoPaiPan.Str_LiuQin[lq2[5-i]])
            else:
                outs+=sep.rstrip()
            outs+="\n"
        return outs

    def calcGua(self):
        # LiuShen
        rtg=self.getData('RiGan')
        if rtg<5:
            rtg=(rtg-1)/2
        elif 5<=rtg<=6:
            rtg=rtg-3
        else:
            rtg=(rtg+1)/2
        self._data['LiuShen']=tuple(((x+rtg)%6+1 for x in range(6)))
        # ShiYing
        gua1=self.getData('Gua1')
        gua2=self.getData('Gua2')
        info=self.calcShiYing(gua1)
        self._data['ShiYing1']=info[0]
        self._data['Gong1']=info[1]
        info=self.calcShiYing(gua2)
        self._data['ShiYing2']=info[0]
        self._data['Gong2']=info[1]
        # ZhuangGua
        gong=self.getData('Gong1')
        gongwx=LiuYaoPaiPan.Tbl_WXGua[gong]
        info=self.calcZhuangGua(gongwx,gua1)
        self._data['ZhuangGua1']=tuple(info[0])
        self._data['LiuQin1']=tuple(info[1])
        info=self.calcZhuangGua(gongwx,gua2)
        self._data['ZhuangGua2']=tuple(info[0])
        self._data['LiuQin2']=tuple(info[1])
        info=self.calcZhuangGua(gongwx,gong*9)
        self._data['ZhuangGua3']=tuple(info[0])
        self._data['LiuQin3']=tuple(info[1])

    def calcZhuangGua(self,gongwx,gua):
        info=LiuYaoPaiPan.Tbl_ZhuangGua[gua/8][0:3]+LiuYaoPaiPan.Tbl_ZhuangGua[gua%8][3:]
        info2=[]
        for x in info:
            wx=LiuYaoPaiPan.Tbl_WXZhi[(x-1)%12]
            rel=(gongwx-wx)%5
            info2.append(rel)
        return (info,tuple(info2))

    def calcShiYing(self,gua):
        gua1=gua
        i=0
        while gua1%9!=0:
            gua1=gua1^LiuYaoPaiPan.Tbl_ShiYing[i]
            i+=1
        if i==0:
            i=6
        elif i>5:
            i=10-i
        return (i,gua1/9)

    def setParams(self,**kwargs):
        self.init_data()
        for k,v in kwargs.items():
            self._data[k]=v
    def init_data(self):
        self._data={}
    def getData(self,kword,dvalue=''):
        return self._data.get(kword,dvalue)

if __name__ == '__main__':
    ly=LiuYaoPaiPan()
    ly.paipanNow((2,2,1,3))
    fmt={'sep':' '}
    print ly.display(fmt)
