# --coding:utf8--
import logging
import binascii
import re

class AsciiTbl(object):
    BORDER_TL='┌'
    BORDER_TR='┐'
    BORDER_BL='└'
    BORDER_BR='┘'
    BORDER_H='─'
    BORDER_V='│'
    BORDER_HU='┴'
    BORDER_HD='┬'
    BORDER_VL='┤'
    BORDER_VR='├'
    BORDER_HV='┼'
    BORDER_S=' '
    def __init__(self,loglevel=logging.DEBUG,logfile=''):
        self._log=self._initLogger(loglevel,logfile)
        self._ignoreptn=None
        self.setShape(4,4,1,1)
        self.setBorder(self.__class__.BORDER_TL,self.__class__.BORDER_TR,
                       self.__class__.BORDER_BL,self.__class__.BORDER_BR,
                       self.__class__.BORDER_H,self.__class__.BORDER_V,
                       self.__class__.BORDER_HU,self.__class__.BORDER_HD,
                       self.__class__.BORDER_VL,self.__class__.BORDER_VR,
                       self.__class__.BORDER_HV,self.__class__.BORDER_S)
    def setIgnorePattern(self,pattern):
        self._ignoreptn=re.compile(pattern)
    def setBorder(self,topleft,topright,bottomleft,bottomright,hline,vline,hup,hdown,vleft,vright,cross,space):
        if self._checkBorderLen(space,topleft,topright,bottomleft,bottomright,hline,vline,hup,hdown,vleft,vright,cross):
            self._border={'tl':topleft,'tr':topright,
                          'bl':bottomleft,'br':bottomright,
                          'h':hline,'v':vline,
                          'hu':hup,'hd':hdown,
                          'vl':vleft,'vr':vright,
                          'hv':cross,'s':space}
            self._log.info("BorderChar:%s"%(repr(self._border)))
    def setShape(self,rows,cols,cellrows,cellcols):
        if rows<3 or cols<3 or cellrows<1 or cellcols<1:
            self._log.error("Shape Error:Rows[%d],Cols[%d],LinesInCell[%d],CharsInCell[%d]"%(rows,cols,cellrows,cellcols))
            return False
        else:
            self._log.info("Shape:Rows[%d],Cols[%d],LinesInCell[%d],CharsInCell[%d]"%(rows,cols,cellrows,cellcols))
            self._rows=rows
            self._cols=cols
            self._crows=cellrows
            self._ccols=cellcols
            return True
    def getShape(self):
        return ((self._rows,self._cols),(self._crows,self._ccols))
    def startOutput(self):
        self._sts_row1=0
        self._sts_row2=0
        self._sts_row3=0
    def getStatus(self):
        if self._sts_row2>0:
            if self._sts_row1==0 or self._sts_row1==self._rows-1:
                inputcnt=self._cols
            else:
                inputcnt=3
        else:
            if 1<self._sts_row1<self._rows-1:
                inputcnt=1
            else:
                inputcnt=0
        outs={'row':self._sts_row1,'inputcnt':inputcnt,'cellrow':self._sts_row2,'centerrow':self._sts_row3}
        return outs
    def nextLine(self,txtlist=(),align=True):
        sts=self.getStatus()
        if sts['row']>=0:
            self._updateStatus()
            if sts['inputcnt']<=1:
                return self._getHorizontalLine(sts['row'],txtlist,align)
            else:
                return self._getVerticalLine(sts['row'],txtlist,align)
        else:
            return ''
    def _updateStatus(self):
        if self._sts_row1>=self._rows:
            self._sts_row1=-1
        else:
            self._sts_row2+=1
            if 1<=self._sts_row1<self._rows-1:
                self._sts_row3+=1
            if self._sts_row2>self._crows:
                self._sts_row2=0
                self._sts_row1+=1
                if self._sts_row1>=self._rows-1:
                    self._sts_row3=0
        self._log.debug("Output Status:TableRow[%d],CellRow[%d],CenterRow[%d]"%(self._sts_row1,self._sts_row2,self._sts_row3))
    def _getVerticalLine(self,idx,txtlist=(),align=True):
        self._log.info("VerticalLine[%d]:%s"%(idx,repr(txtlist)))
        vline=''
        if 0<=idx<self._rows:
            if idx==0 or idx==self._rows-1:
                newtxtlist=self._alignTxt(txtlist,(self._ccols*2,)*self._cols,align)
                vline=self._border['v']
                for i in range(self._cols):
                    vline+=newtxtlist[i]
                    vline+=self._border['v']
            else:
                newtxtlist=self._alignTxt(txtlist,(self._ccols*2,(self._cols-2)*self._ccols*2+(self._cols-3)*self._len1,self._ccols*2),align)
                vline=self._border['v']
                vline+=newtxtlist[0]
                vline+=self._border['v']
                if len(newtxtlist)>1:
                    vline+=newtxtlist[1]
                else:
                    vline+=self._border['s']*((self._cols-2)*self._ccols*2+(self._cols-3)*self._len1)
                vline+=self._border['v']
                vline+=newtxtlist[2]
                vline+=self._border['v']
        return vline
    def _getHorizontalLine(self,idx,txtlist=(),align=True):
        self._log.info("HorizontalLine[%d]:%s"%(idx,repr(txtlist)))
        hline=''
        if 0<=idx<=self._rows:
            hcell=self._border['h']*(self._ccols*2/self._len1)
            if idx==0:
                hline=self._border['tl']
                for i in range(self._cols):
                    hline+=hcell
                    if i<self._cols-1:
                        hline+=self._border['hd']
                    else:
                        hline+=self._border['tr']
            elif idx==1:
                hline=self._border['vr']
                for i in range(self._cols):
                    hline+=hcell
                    if i<1:
                        hline+=self._border['hv']
                    elif i<self._cols-2:
                        hline+=self._border['hu']
                    elif i<self._cols-1:
                        hline+=self._border['hv']
                    else:
                        hline+=self._border['vl']
            elif idx==self._rows-1:
                hline=self._border['vr']
                for i in range(self._cols):
                    hline+=hcell
                    if i<1:
                        hline+=self._border['hv']
                    elif i<self._cols-2:
                        hline+=self._border['hd']
                    elif i<self._cols-1:
                        hline+=self._border['hv']
                    else:
                        hline+=self._border['vl']
            elif idx==self._rows:
                hline=self._border['bl']
                for i in range(self._cols):
                    hline+=hcell
                    if i<self._cols-1:
                        hline+=self._border['hu']
                    else:
                        hline+=self._border['br']
            else:
                newtxtlist=self._alignTxt(txtlist,((self._cols-2)*self._ccols*2+(self._cols-3)*self._len1,),align)
                hline=self._border['vr']
                hline+=hcell
                hline+=self._border['vl']
                if len(newtxtlist)<1:
                    hline+=self._border['s']*((self._cols-2)*self._ccols*2+(self._cols-3)*self._len1)
                else:
                    hline+=newtxtlist[0]
                hline+=self._border['vr']
                hline+=hcell
                hline+=self._border['vl']
        return hline
    def _checkBorderLen(self,space,*others):
        chlen=-1
        for ch in others:
            tmplen,tmpstr=self._textlen(ch)
            if tmplen<1:
                self._log.error("Border character's length is zero")
                return False
            elif chlen<0:
                chlen=tmplen
            elif chlen!=tmplen:
                self._log.error("Border character's length is not equal")
                return False
        self._len1=chlen
        self._len2,tmpstr=self._textlen(space)
        return True
    def _alignTxt(self,txtlist,maxlen,align=True):
        outlist=[]
        self._log.debug("AlignText--TextListCnt:%d,MaxLen:%s"%(len(txtlist),str(maxlen)))
        self._log.debug("AlignText--In Text List:%s"%(repr(tuple(txtlist))))
        maxidx=len(maxlen)
        maxlist=len(txtlist)
        for i in range(maxidx):
            if align: # adjust string and set empty string
                if maxlist>i:
                    txtlen,newtext=self._textlen(txtlist[i],maxlen[i])
                else:
                    txtlen=0
                    newtext=''
                if txtlen<maxlen[i]:
                    scnt=(maxlen[i]-txtlen)%self._len2
                    newtext+=' '*scnt
                    newtext+=self._border['s']*((maxlen[i]-txtlen-scnt)/self._len2)
            else: # set empty string only
                if maxlist>i and len(txtlist[i])>0:
                    newtext=txtlist[i]
                else:
                    txtlen=0
                    newtext=''
                    scnt=(maxlen[i]-txtlen)%self._len2
                    newtext+=' '*scnt
                    newtext+=self._border['s']*((maxlen[i]-txtlen-scnt)/self._len2)
            outlist.append(newtext)
        self._log.debug("AlignText--Out Text List:%s"%(repr(tuple(outlist))))
        return tuple(outlist)
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
    def _textlen(self,text,maxlen=0):
        # calculate text length (one japanese character = two ascii characters)
        self._log.debug("TextLen--Origin String:"+binascii.hexlify(text))
        outs=self._patternsplit(text,self._split1,self._split2)
        data=''
        currentlen=0
        flag=True
        for index,item in enumerate(outs):
            if item[0]==1:
                # split done by self._split1
                data+=item[1]
            else:
                if flag:
                    if len(item[1])>1:
                        ilen=2
                    else:
                        ilen=1
                    if currentlen+ilen>maxlen and maxlen>0:
                        flag=False
                    else:
                        currentlen+=ilen
                        data+=item[1]
        if not flag:
            self._log.debug("TextLen--Cutted String:"+binascii.hexlify(data))
        return currentlen,data
    def transposeText(self,txtlist):
        maxlen=3
        outs=['']*maxlen
        for txt in txtlist:
            prefix=''
            suffix=''
            tmpout=self._patternsplit(txt,self._split1,self._split2)
            index=0
            flag=False
            oindex=0
            while index<len(tmpout):
                if tmpout[index][0]==1:
                    if not flag:
                        prefix=tmpout[index][1]
                        index2=index+1
                        while index2<len(tmpout) and tmpout[index2][0]!=1:
                            index2+=1
                        else:
                            if index2<len(tmpout):
                                suffix=tmpout[index2][1]
                            else:
                                suffix=''
                        flag=True
                    else:
                        flag=False
                        prefix=''
                        suffix=''
                else:
                    if len(tmpout[index][1])<2:
                        if index<len(tmpout)-1:
                            if len(tmpout[index+1][1])<2:
                                data=tmpout[index][1]+tmpout[index+1][1]
                                index+=1
                            else:
                                data=tmpout[index][1]+' '
                        else:
                            data=tmpout[index][1]+' '
                    else:
                        data=tmpout[index][1]
                    outs[oindex]+=prefix+data+suffix
                    oindex+=1
                index+=1
            while oindex<maxlen:
                outs[oindex]+='  '
                oindex+=1
        return tuple(outs)
    def _patternsplit(self,data,*funclist):
        indata=[(-1,data)]
        for idx,func in enumerate(funclist):
            tmpout=[]
            for item in indata:
                if item[0]<0:
                    tmpout.extend(func(item[1]))
                else:
                    tmpout.append(item)
            indata=[]
            for item in tmpout:
                if item[0]==0:
                    indata.append((idx+1,item[1]))
                else:
                    indata.append(item)
        return tuple(indata)
    def _split1(self,data):
        outs=[]
        if self._ignoreptn:
            index=0
            for m in self._ignoreptn.finditer(data):
                if m.start()>index:
                    outs.append((-1,data[index:m.start()]))
                    outs.append((0,m.group(0)))
                elif m.start()==index:
                    outs.append((0,m.group(0)))
                index=m.end()
            if index<len(data):
                outs.append((-1,data[index:]))
        else:
            outs.append((-1,data))
        return tuple(outs)
    def _split2(self,data):
        outs=[]
        index=0
        while index<len(data):
            dlen,blen=self._utf8txtlen(data[index])
            outs.append((0,data[index:index+blen]))
            index+=blen
        return tuple(outs)
    def _utf8txtlen(self,bdata):
        idata=ord(bdata)
        if idata<=0x7f:
            dlen=1
            blen=1
        elif 0xc0<=idata<=0xdf:
            # 2 bytes character
            dlen=2
            blen=2
        elif 0xe0<=idata<=0xef:
            # 3 bytes character
            dlen=2
            blen=3
        elif 0xf0<=idata<=0xf7:
            # 4 bytes character
            dlen=2
            blen=4
        elif 0xf8<=idata<=0xfb:
            # 5 bytes character
            dlen=2
            blen=5
        elif 0xfc<=idata<=0xfd:
            # 6 bytes character
            dlen=2
            blen=6
        return dlen,blen

def output():
    ht=AsciiTbl(loglevel=logging.INFO)
    #ht.setBorder('[',']','[',']','-','|','-','-','|','|','+','　')
    #ht.setShape(4,4,2,2)
    ht.startOutput()
    outs=''
    while True:
        sts=ht.getStatus()
        if sts['row']<0:
            break
        elif sts['row']==1 and sts['cellrow']==1:
            instrs=('abcd','het','hetsahs')
        else:
            instrs=('abcd','het','hetsahs')
        line=ht.nextLine(instrs)
        outs+=line+"\n"
    print outs

if __name__ == '__main__':
    #output()
    ht=AsciiTbl(loglevel=logging.CRITICAL)
    ht.setIgnorePattern(r'<.+?>')
    text='<font>hte</font>挨拶<br>大事'
    print ht.transposeText((text,))
    outs=ht._patternsplit(text,ht._split1,ht._split2)
    for item in outs:
        print item[0],item[1]
