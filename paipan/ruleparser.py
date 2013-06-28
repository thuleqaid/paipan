import ply.lex as lex
import ply.yacc as yacc
import logging

class RuleParser(object):
    # tokens
    reserved = (
            'TARGET','NAME','INPUT','OUTPUT','DATA','TAG')
    tokens = reserved + (
        'COMMENT','NUMBER','ID','SCONST',
        )

    # constructor
    def __init__(self,loglevel=logging.CRITICAL):
        self.initlog(loglevel)
        self._reserved_map={}
        for r in RuleParser.reserved:
            self._reserved_map[r.upper()] = r
        #self._lexer=lex.lex(module=self)
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
    def results(self):
        return tuple(self._result)

    # private functions
    def initlog(self,loglevel):
        self._log=logging.getLogger('RuleParser')
        self._log.setLevel(loglevel)
        ch=logging.StreamHandler()
        ch.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        self._log.addHandler(ch)
    def init(self):
        self._result=[]
    def initstate(self):
        self._pinfo={}
    def _parse(self,statements):
        self.initstate()
        yacc.parse(statements)
        #self._lexer.input(statements)
        #while True:
            #tok=self._lexer.token()
            #if not tok:
                #break
            #self._log.debug(tok)

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
        '''rulefile : item
                    | rulefile item'''
        self._result.append(self._pinfo)
        self._log.debug(repr(self._pinfo))
        self.initstate()
    def p_item(self,p):
        '''item : target
                | item name
                | item tag
                | item input
                | item output
                | item data
                | item COMMENT'''
        p[0]='PITEM'
    def p_target(self,p):
        '''target : TARGET ID'''
        p[0]='PTARGET'
        self._pinfo[p[0]]=p[2]
    def p_name(self,p):
        '''name : NAME SCONST'''
        p[0]='PNAME'
        self._pinfo[p[0]]=p[2]
    def p_tag(self,p):
        '''tag : TAG ids'''
        p[0]='PTAG'
        self._pinfo[p[0]]=self._pinfo[p[2]]
    def p_input(self,p):
        '''input : INPUT ids'''
        p[0]='PINPUT'
        self._pinfo[p[0]]=self._pinfo[p[2]]
    def p_output(self,p):
        '''output : OUTPUT numbers
                  | OUTPUT ids'''
        p[0]='POUTPUT'
        self._pinfo[p[0]]=self._pinfo[p[2]]
    def p_data(self,p):
        '''data : DATA numbers
                | DATA ids'''
        p[0]='PDATA'
        self._pinfo[p[0]]=self._pinfo[p[2]]
    def p_ids(self,p):
        '''ids : ID
               | ids ID'''
        p[0]='PIDS'
        if p[1]!='PIDS':
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

if __name__ == '__main__':
    rp=RuleParser(logging.DEBUG)
    rp.parse('ziwei_rule.txt','cp936')
    print rp.results()
