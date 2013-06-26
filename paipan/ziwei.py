import ruleparser

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

if __name__=='__main__':
    zw=ZiWeiPaiPan()
    zw.setParams(
        ShengNianGan=10,
        ShengNianZhi=6,
        ShengYueGan=8,
        ShengYueZhi=8,
        ShengRiGan=6,
        ShengRiZhi=8,
        ShengShiGan=6,
        ShengShiZhi=6)
    print zw._outputdata
    print zw.getData('MingGong')
