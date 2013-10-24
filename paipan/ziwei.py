import os.path
import logging
import ruleparser
import lunar

class ZiWeiPaiPan(object):
    def __init__(self,loglevel=logging.DEBUG,logfile=''):
        self._log=self._initLogger(loglevel,logfile)
        dname=os.path.dirname(__file__)
        self.loadConfig(os.path.join(dname,'ziwei_rule.txt'))

    # public functions
    def setParams(self,**kwargs):
        self.init_data()
        for k,v in kwargs.items():
            self._data[k]=v
            self._log.debug("[SetParams] SetData:key=%s,value=%s"%(k,v))
        dv=''
        for target in self._outputdata.keys():
            self._log.debug("[SetParams] CalcData:key=%s"%(target,))
            targetv=self.calcData(target,dv)
            if targetv!=dv:
                self._data[target]=targetv
                self._log.debug("[SetParams] CalcData:key=%s,value=%s"%(target,self._data[target]))
            else:
                self._log.debug("[SetParams] CalcData:key(%s) cannot be calculated"%(target,))
        self._log.info("[SetParams] Data:%s"%(repr(self._data),))

    def getData(self,datakey,defaultvalue=''):
        if datakey in self._data:
            return self._data[datakey]
        else:
            return defaultvalue

    # private functions
    def init_data(self):
        self._data={}

    def init_const(self):
        self._inputdata={}
        self._inputdata['LunarNianGan']=(1,2,3,4,5,6,7,8,9,10)
        self._inputdata['LunarNianZhi']=(1,2,3,4,5,6,7,8,9,10,11,12)
        self._inputdata['LunarYue']=(1,2,3,4,5,6,7,8,9,10,11,12)
        self._inputdata['LunarRi']=(1,2,3,4,5,6,7,8,9,10,
                                    11,12,13,14,15,16,17,18,19,20,
                                    21,22,23,24,25,26,27,28,29,30)
        self._inputdata['LunarShi']=(1,2,3,4,5,6,7,8,9,10,11,12)
        self._inputdata['XingBie']=(1,2)
        self._outputdata={}

    def loadConfig(self,cfile,filecode='cp936'):
        self._log.info("[LoadConfig] File:%s"%(cfile,))
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
        self._log.debug("[CalcData] key=%s"%(datakey,))
        if datakey in self._inputdata:
            if datakey in self._data:
                self._log.debug("[CalcData] key=%s,value=%s"%(datakey,self._data[datakey]))
                return self._data[datakey]
            elif datakey in self._outputdata:
                dindex=0
                dv=''
                for pkey in self._outputdata[datakey]['params']:
                    pkeyv=self.calcData(pkey,dv)
                    if pkeyv==dv:
                        self._log.warn("[CalcData] key(%s) depends on an unknown key(%s)"%(datakey,pkey))
                        return defaultvalue
                    dindex=dindex*len(self._inputdata[pkey])+self._inputdata[pkey].index(pkeyv)
                self._log.debug("[CalcData] key=%s,value=%s"%(datakey,self._outputdata[datakey]['data'][dindex]))
                return self._outputdata[datakey]['data'][dindex]
            else:
                self._log.warn("[CalcData] key(%s) is not set"%(datakey,))
                return defaultvalue
        else:
            self._log.errror("[CalcData] key(%s) is out of range"%(datakey,))
            return defaultvalue
    def _initLogger(self,level,logfile=''):
        log=logging.getLogger(self.__class__.__name__)
        log.setLevel(level)
        ch=self._getLogHandler(logfile)
        formatter=logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        log.addHandler(ch)
        return log
    def _getLogHandler(self,logfile=''):
        if logfile:
            ch=logging.FileHandler(logfile)
        else:
            ch=logging.StreamHandler()
        return ch

def paipan(gender,*cal):
    zw=ZiWeiPaiPan(logging.INFO)
    l=lunar.Lunar()
    info=l.transCal(cal)
    zw.setParams(
        XingBie=gender,
        LunarNianGan=(info[1][0]-1984)%10+1,
        LunarNianZhi=(info[1][0]-1984)%12+1,
        LunarYue=(info[1][1]+info[1][3]-1)%12+1,
        LunarShi=(info[0][3]-1)%12+1,
        LunarRi=info[1][2])
    outs={}
    for k,v in sorted(zw._data.iteritems()):
        if k in zw._outputdata:
            if zw._outputdata[k]['tag'] not in outs:
                outs[zw._outputdata[k]['tag']]=[]
            outs[zw._outputdata[k]['tag']].append((k,zw._outputdata[k]['name'],v))
    #for k,v in sorted(outs.iteritems()):
        #print k
        #for vi in sorted(v,key=lambda v:v[2]):
            #print "\t","\t".join([str(x) for x in vi[1:]])

if __name__=='__main__':
    paipan(1,1983,9,2,12,47,0)
