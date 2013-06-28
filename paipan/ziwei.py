import ruleparser
import lunar

class ZiWeiPaiPan(object):
    def __init__(self):
        self.loadConfig('ziwei_rule.txt')

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
        self._inputdata['ShengRi']=(1,2,3,4,5,6,7,8,9,10,
                                    11,12,13,14,15,16,17,18,19,20,
                                    21,22,23,24,25,26,27,28,29,30)
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

def paipan(*cal):
    zw=ZiWeiPaiPan()
    l=lunar.Lunar()
    info=l.transCal(cal)
    zw.setParams(
        ShengNianGan=(info[0][0]-1)%10+1,
        ShengNianZhi=(info[0][0]-1)%12+1,
        ShengYueGan=(info[0][1]-1)%10+1,
        ShengYueZhi=(info[0][1]-1)%12+1,
        ShengRiGan=(info[0][2]-1)%10+1,
        ShengRiZhi=(info[0][2]-1)%12+1,
        ShengShiGan=(info[0][3]-1)%10+1,
        ShengShiZhi=(info[0][3]-1)%12+1,
        ShengRi=info[1][2])
    for k,v in sorted(zw._data.iteritems()):
        if (k in zw._outputdata) and ('Star0' in zw._outputdata[k]['tag']):
            print k,v

if __name__=='__main__':
    paipan(1983,9,2,12,47,0)
