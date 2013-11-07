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
        self._rules.resetValues()
        if len(cal)>=6:
            info=self._lunar.transCal(cal)
            self.setParams(
                XingBie=(gender-1)%2+1,
                LunarNianGan=(info[1][0]-1984)%10+1,
                LunarNianZhi=(info[1][0]-1984)%12+1,
                LunarYue=(info[1][1]+info[1][3]-1)%12+1,
                LunarShi=(info[0][3]-1)%12+1,
                LunarRi=info[1][2],
                SiHuaNianGan=(info[1][0]-1984)%10+1)

    def setParams(self,**kwargs):
        self._rules.setValues(False,**kwargs)

    def getRules(self):
        return self._rules

    def getStar(self,*tags):
        outs=[[] for x in range(12)]
        for tag in tags:
            for id in sorted(self._rules.getIdsByTags(tag)):
                idv=self._rules.getValue(id)
                if idv[0]:
                    outs[idv[1]-1].append(id)
        return tuple(outs)

    def getSihua(self):
        sihua={}
        for id in sorted(self._rules.getIdsByTags('SiHua')):
            idv=self._rules.getValue(id)
            sihua[idv[1]]=id
        return sihua

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

def output():
    import asciitbl
    ht=asciitbl.AsciiTbl(loglevel=logging.CRITICAL)
    ht.setShape(4,4,4,4)
    ht.setIgnorePattern(r'<.+?>')
    ht.startOutput()
    zw=ZiWeiPaiPan()
    zw.paipan(1,1983,9,2,12,47,0)
    #zw.paipan(1)
    #zw.setParams(ZiWei=1)
    rules=zw.getRules()
    sihua=zw.getSihua()
    stars=zw.getStar('Star0N','Star0S','Star1')
    #stars=zw.getStar('Star0N','Star0S')
    outs=[]
    for i in range(len(stars)):
        tmpout=[]
        for j,id in enumerate(stars[i]):
            if id in sihua:
                tmpout.append(rules.getName(id)[1]+rules.getName(sihua[id])[1])
            else:
                tmpout.append(rules.getName(id)[1])
            #tmpout.append(rules.getName(id)[1])
        outs.append(ht.transposeText(tmpout))
    outstr=''
    while True:
        sts=ht.getStatus()
        if sts['row']<0:
            break
        elif sts['row']==0:
            if sts['cellrow']>len(outs[5]) or sts['cellrow']<=0:
                str1=''
            else:
                str1=outs[5][sts['cellrow']-1]
            if sts['cellrow']>len(outs[6]) or sts['cellrow']<=0:
                str2=''
            else:
                str2=outs[6][sts['cellrow']-1]
            if sts['cellrow']>len(outs[7]) or sts['cellrow']<=0:
                str3=''
            else:
                str3=outs[7][sts['cellrow']-1]
            if sts['cellrow']>len(outs[8]) or sts['cellrow']<=0:
                str4=''
            else:
                str4=outs[8][sts['cellrow']-1]
            instrs=(str1,str2,str3,str4)
        elif sts['row']==1:
            if sts['cellrow']>len(outs[4]) or sts['cellrow']<=0:
                str1=''
            else:
                str1=outs[4][sts['cellrow']-1]
            str2=''
            if sts['cellrow']>len(outs[9]) or sts['cellrow']<=0:
                str3=''
            else:
                str3=outs[9][sts['cellrow']-1]
            instrs=(str1,str2,str3)
        elif sts['row']==2:
            if sts['cellrow']>len(outs[3]) or sts['cellrow']<=0:
                str1=''
            else:
                str1=outs[3][sts['cellrow']-1]
            str2=''
            if sts['cellrow']>len(outs[10]) or sts['cellrow']<=0:
                str3=''
            else:
                str3=outs[10][sts['cellrow']-1]
            instrs=(str1,str2,str3)
        elif sts['row']==3:
            if sts['cellrow']>len(outs[2]) or sts['cellrow']<=0:
                str1=''
            else:
                str1=outs[2][sts['cellrow']-1]
            if sts['cellrow']>len(outs[1]) or sts['cellrow']<=0:
                str2=''
            else:
                str2=outs[1][sts['cellrow']-1]
            if sts['cellrow']>len(outs[0]) or sts['cellrow']<=0:
                str3=''
            else:
                str3=outs[0][sts['cellrow']-1]
            if sts['cellrow']>len(outs[-1]) or sts['cellrow']<=0:
                str4=''
            else:
                str4=outs[-1][sts['cellrow']-1]
            instrs=(str1,str2,str3,str4)
        else:
            instrs=()
        line=ht.nextLine(instrs)
        outstr+=line+"\n"
    print outstr
if __name__=='__main__':
    output()
