import os.path
import sys
import logging
import lunar
sys.path.append('..')
import tabledrv.ruleobj
import tabledrv.ruleparser

class ZiWeiPaiPan(object):
    def __init__(self,loglevel=logging.CRITICAL,logfile=''):
        self._log=self._initLogger(loglevel,logfile)
        self._rules=tabledrv.ruleobj.RuleObj()
        self._lunar=lunar.Lunar()
        dname=os.path.dirname(__file__)
        self.loadConfig(os.path.join(dname,'ziwei_rule.txt'))

    # public functions
    def paipan(self,gender,*cal):
        info=self._lunar.transCal(cal)
        self.setParams(
            XingBie=(gender-1)%2+1,
            LunarNianGan=(info[1][0]-1984)%10+1,
            LunarNianZhi=(info[1][0]-1984)%12+1,
            LunarYue=(info[1][1]+info[1][3]-1)%12+1,
            LunarShi=(info[0][3]-1)%12+1,
            LunarRi=info[1][2])

    def setParams(self,**kwargs):
        self._rules.resetValues()
        self._rules.setValues(False,**kwargs)

    def getRules(self):
        return self._rules

    # private functions
    def loadConfig(self,cfile,filecode='cp936'):
        self._log.info("[LoadConfig] File:%s"%(cfile,))
        rp=tabledrv.ruleparser.RuleParser()
        rp.parse(cfile,filecode)
        self._rules.addRules(*rp.results())

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

if __name__=='__main__':
    zw=ZiWeiPaiPan()
    zw.paipan(1,1983,9,2,12,47,0)
    rules=zw.getRules()
    sihua={}
    for id in sorted(rules.getIdsByTags('SiHua')):
        idv=rules.getValue(id)
        if idv[0]:
            sihua[idv[1]]=id
    outs=[[] for x in range(12)]
    for tag in ('Star0N','Star0S','Star1'):
        for id in sorted(rules.getIdsByTags(tag)):
            idv=rules.getValue(id)
            if idv[0]:
                if id in sihua:
                    outs[idv[1]-1].append(rules.getName(id)[1]+rules.getName(sihua[id])[1]
)
                else:
                    outs[idv[1]-1].append(rules.getName(id)[1])
    for idx,data in enumerate(outs):
        print "%02d %s"%(idx+1,','.join(data))
