import itertools
import ply.lex as lex
import ply.yacc as yacc
import logging

class RuleParser(object):
    # tokens
    reserved = (
            'TARGET',
            'DEFINE','CALCULATE',
            'NAME',
            'TAG',
            'INPUT',
            'FORMULA',
            'DATA',
            'VALUES',
            'DEFAULT',
            'VALUE','INDEX')
    tokens = reserved + (
        'COMMENT','NUMBER','ID','SCONST',
        )

    # constructor
    def __init__(self,loglevel=logging.CRITICAL,logfile=''):
        self._log=self.initLogger(loglevel,logfile)
        self._reserved_map={}
        for r in RuleParser.reserved:
            self._reserved_map[r.upper()] = r
        lex.lex(module=self)
        yacc.yacc(module=self)

    # public functions
    def parse(self,fname,encode):
        # load rule file
        fh=open(fname,'rU')
        lines=[]
        for line in fh.readlines():
            lines.append(line.strip().decode(encode).encode('utf8'))
        fh.close()
        self.init()
        self._parse("\n".join(lines))
        self._checkRules()
    def results(self):
        return tuple(self._result)

    # private functions
    def _checkRules(self):
        infod={}
        infoc={}
        for item in self._result:
            if 'PTARGETD' in item:
                # TARGET DEFINE
                id=item['PTARGETD']
                # check duplicated:
                if id in infod:
                    self._log.error("Rule Error:Duplicate:%s"%(str(item),))
                    continue
                # check default value
                dindex=-1
                if 'PDEFAULTV' in item:
                    if item['PDEFAULTV'] in item['PVALUES']:
                        dindex=item['PVALUES'].index(item['PDEFAULTV'])
                    else:
                        self._log.error("Rule Error:Default Value:%s"%(str(item),))
                        continue
                if 'PDEFAULTI' in item:
                    if 0<=item['PDEFAULTI']<len(item['PVALUES']):
                        if dindex>=0:
                            if dindex==item['PDEFAULTI']:
                                self._log.warning("Rule Warn:Double Default:%s"%(str(item),))
                            else:
                                self._log.error("Rule Error:Double Default:%s"%(str(item),))
                                continue
                        dindex=item['PDEFAULTI']
                    else:
                        self._log.error("Rule Error:Default Index:%s"%(str(item),))
                        continue
                infod[id]=item
            elif 'PTARGETC' in item:
                # TARGET CALCULATE
                id=item['PTARGETC']
                # check duplicated:
                if id in infoc:
                    self._log.error("Rule Error:Duplicate:%s"%(str(item),))
                # Exclusive:formula,data index,data value
                dcnt=0
                for k in ('PFORMULA','PDATAI','PDATAV'):
                    if k in item:
                        dcnt+=1
                if dcnt<1:
                    self._log.error("Rule Error:No calculation:%s"%(str(item),))
                    continue
                if dcnt>1:
                    self._log.error("Rule Error:Multiple calculations:%s"%(str(item),))
                    continue
                infoc[id]=item
        droplist=[]
        uncertainlist={}
        # check PDATAV and PDATAI
        for k,v in infoc.items():
            if 'PDATAV' in v:
                # input ids must be defined
                mincnt=1
                for id in v['PINPUT']:
                    if id not in infod:
                        self._log.error("Rule Error:No dependencies:%s"%(str(v),))
                        droplist.append(k)
                        break
                    mincnt*=len(infod[id]['PVALUES'])
                else:
                    # all input ids are defined
                    # check count of values
                    if len(v['PDATAV'])<mincnt:
                        self._log.error("Rule Error:Data not enough:%s"%(str(v),))
                        droplist.append(k)
                    else:
                        if k in infod:
                            # check values
                            for i in range(mincnt):
                                if v['PDATAV'][i] in infod[k]['PVALUES']:
                                    pass
                                else:
                                    self._log.error("Rule Error:Data out of range:%s"%(str(v),))
                                    droplist.append(k)
                                    break
            elif 'PDATAI' in v:
                # target id must be defined
                if k not in infod:
                    self._log.error("Rule Error:Target not defined:%s"%(str(v),))
                    droplist.append(k)
                else:
                    # input ids must be defined
                    mincnt=1
                    for id in v['PINPUT']:
                        if id not in infod:
                            self._log.error("Rule Error:No dependencies:%s"%(str(v),))
                            droplist.append(k)
                            break
                        mincnt*=len(infod[id]['PVALUES'])
                    else:
                        # all input ids are defined
                        # check count of values
                        if len(v['PDATAI'])<mincnt:
                            self._log.error("Rule Error:Data not enough:%s"%(str(v),))
                            droplist.append(k)
                        else:
                            # check index
                            for i in range(mincnt):
                                if 0<=v['PDATAI'][i]<len(infod[k]['PVALUES']):
                                    pass
                                else:
                                    self._log.error("Rule Error:Data out of range:%s"%(str(v),))
                                    droplist.append(k)
                                    break
        # split PFORMULA into 3 parts(ok,ng,uncertain)
        for k,v in infoc.items():
            if 'PFORMULA' in v:
                # input ids must be defined or can be calculated
                for id in v['PINPUT']:
                    if id in infod:
                        pass
                    elif id in infoc:
                        if ('PDATAI' in infoc[id]) or ('PDATAV' in infoc[id]):
                            if id in droplist:
                                self._log.error("Rule Error:No dependencies:%s"%(str(v),))
                                droplist.append(k)
                        else: # 'PFORMULA'
                            if k not in uncertainlist:
                                uncertainlist[k]=[]
                            uncertainlist[k].append(id)
                    else:
                        # unknown input id
                        self._log.error("Rule Error:No dependencies:%s"%(str(v),))
                        droplist.append(k)
        # find ok PFORMULA from uncertainlist
        cnt=1
        while cnt>0:
            cnt=0
            for k,v in infoc.items():
                if k in uncertainlist:
                    for id in uncertainlist[k]:
                        if (id not in uncertainlist) and (id not in droplist):
                            uncertainlist[k].remove(id)
                    if len(uncertainlist[k])<1:
                        cnt+=1
                        del uncertainlist[k]
        for k in droplist:
            del infoc[k]
        for k in uncertainlist.keys():
            self._log.error("Rule Error:Loop dependent:%s[%s]"%(k,str(uncertainlist[k]),))
            del infoc[k]
        droplist=[]
        for k,v in infoc.items():
            if ('PFORMULA' in v) and (k in infod):
                # defined formula target
                # check whether all possible calculation results are in range
                inputs=[]
                for id in v['PINPUT']:
                    if id not in infod:
                        break
                    else:
                        inputs.append(infod[id]['PVALUES'])
                else:
                    formula=v['PFORMULA']
                    # all input ids are defined
                    for comb in itertools.product(*inputs):
                        inputp={}
                        for idi in range(len(v['PINPUT'])):
                            inputp[v['PINPUT'][idi]]=comb[idi]
                        ret=eval(formula.format(**inputp))
                        if ret not in infod[k]['PVALUES']:
                            self._log.error("Rule Error:Possible result out of range:%s=%s[%s]"%(k,str(ret),str(inputp)))
                            droplist.append(k)
                            break
        for k in droplist:
            del infoc[k]
        for item in self._result:
            if 'PTARGETD' in item:
                id=item['PTARGETD']
                if id not in infod:
                    self._log.debug("[CheckRule] Remove TargetDefine %s"%(id,))
                    self._result.remove(item)
            elif 'PTARGETC' in item:
                id=item['PTARGETC']
                if id not in infoc:
                    self._log.debug("[CheckRule] Remove TargetCalculate %s"%(id,))
                    self._result.remove(item)
        self._log.info("[CheckRule] Settable Key:%s"%(repr(infod.keys()),))
        self._log.info("[CheckRule] Calculatable Key:%s"%(repr(infoc.keys()),))
    def initLogger(self,level,logfile=''):
        log=logging.getLogger(self.__class__.__name__)
        log.setLevel(level)
        ch=self.getLogHandler(logfile)
        formatter=logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        log.addHandler(ch)
        return log
    def getLogHandler(self,logfile):
        if logfile:
            ch=logging.FileHandler(logfile)
        else:
            ch=logging.StreamHandler()
        return ch
    def init(self):
        self._result=[]
    def initstate(self):
        self._pinfo={}
    def _parse(self,statements):
        self.initstate()
        yacc.parse(statements)

    # lexer
    def t_ID(self,t):
        r'[A-Za-z_][\w_]*'
        t.type = self._reserved_map.get(t.value.upper(),"ID")
        return t
    def t_COMMENT(self,t):
        r'\#.*'
        return t
    def t_NUMBER(self,t):
        r'\d+\.?\d*'
        t.value=int(t.value)
        return t
    def t_SCONST(self,t):
        r'".*?"'
        t.value=t.value[1:-1]
        return t
    def t_newline(self,t):
        r'\n+'
        t.lexer.lineno+=len(t.value)
    t_ignore  =': \t\x0c,'
    def t_error(self,t):
        self._log.critical("T_ERROR: %s" % repr(t.value[0]))
        t.lexer.skip(1)

    # parser
    def p_rulefile(self,p):
        '''rulefile : comments
                    | itemd
                    | itemc
                    | rulefile itemd
                    | rulefile itemc'''
        if self._pinfo:
            self._log.debug(repr(self._pinfo))
            for k in ('PNUMBERS','PIDS','PSTRINGS'):
                if k in self._pinfo:
                    del self._pinfo[k]
            self._result.append(self._pinfo)
        self.initstate()
    def p_comments(self,p):
        '''comments : COMMENT
                    | comments COMMENT'''
    def p_itemd(self,p):
        '''itemd : targetd
                | itemd name
                | itemd tag
                | itemd defaultv
                | itemd defaulti
                | itemd values
                | itemd comments'''
        p[0]='PITEMD'
    def p_targetd(self,p):
        '''targetd : TARGET DEFINE ID'''
        p[0]='PTARGETD'
        self._pinfo[p[0]]=p[3]
    def p_name(self,p):
        '''name : NAME SCONST'''
        p[0]='PNAME'
        self._pinfo[p[0]]=p[2]
    def p_tag(self,p):
        '''tag : TAG strings'''
        p[0]='PTAG'
        self._pinfo[p[0]]=self._pinfo[p[2]]
    def p_defaultv(self,p):
        '''defaultv : DEFAULT VALUE NUMBER
                    | DEFAULT VALUE SCONST'''
        p[0]='PDEFAULTV'
        self._pinfo[p[0]]=p[3]
    def p_defaulti(self,p):
        '''defaulti : DEFAULT INDEX NUMBER'''
        p[0]='PDEFAULTI'
        self._pinfo[p[0]]=p[3]
    def p_values(self,p):
        '''values : VALUES numbers
                  | VALUES strings'''
        p[0]='PVALUES'
        self._pinfo[p[0]]=self._pinfo[p[2]]
    def p_itemc(self,p):
        '''itemc : targetc
                | itemc input
                | itemc formula
                | itemc datai
                | itemc datav
                | itemc comments'''
        p[0]='PITEMC'
    def p_targetc(self,p):
        '''targetc : TARGET CALCULATE ID'''
        p[0]='PTARGETC'
        self._pinfo[p[0]]=p[3]
    def p_input(self,p):
        '''input : INPUT ids'''
        p[0]='PINPUT'
        self._pinfo[p[0]]=self._pinfo[p[2]]
    def p_formula(self,p):
        '''formula : FORMULA SCONST'''
        p[0]='PFORMULA'
        self._pinfo[p[0]]=p[2]
    def p_datai(self,p):
        '''datai : DATA INDEX numbers'''
        p[0]='PDATAI'
        self._pinfo[p[0]]=self._pinfo[p[3]]
    def p_datav(self,p):
        '''datav : DATA VALUE numbers
                 | DATA VALUE strings'''
        p[0]='PDATAV'
        self._pinfo[p[0]]=self._pinfo[p[3]]
    def p_ids(self,p):
        '''ids : ID
               | ids ID'''
        p[0]='PIDS'
        if p[1]!='PIDS':
            self._pinfo[p[0]]=[p[1],]
        else:
            self._pinfo[p[0]].append(p[2])
    def p_strings(self,p):
        '''strings : SCONST
                   | strings SCONST'''
        p[0]='PSTRINGS'
        if p[1]!='PSTRINGS':
            self._pinfo[p[0]]=[p[1],]
        else:
            self._pinfo[p[0]].append(p[2])
    def p_numbers(self,p):
        '''numbers : NUMBER
                   | numbers NUMBER'''
        p[0]='PNUMBERS'
        if p[1]!='PNUMBERS':
            self._pinfo[p[0]]=[p[1],]
        else:
            self._pinfo[p[0]].append(p[2])
    def p_error(self,p):
        self._log.critical("P_ERROR: "+str(p))

