import logging

class RuleObjBase(object):
    def __init__(self,loglevel=logging.CRITICAL,logfile=''):
        self._log=self._initLogger(loglevel,logfile)
        self._initData()
    def addRules(self,*rules):
        for rule in rules:
            self._addRule(rule)
    def getIds(self):
        idlist1=set(self._getDefinedIds())
        idlist2=set(self._getCalculatableIds())
        return tuple(idlist1.union(idlist2))
    def getTags(self):
        tags=set()
        for idname in self.getIds():
            info=self.getTag(idname)
            if info[0]:
                tags=tags.union(info[1])
        return tuple(tags)
    def getIdsByTags(self,*tags):
        ids=set()
        for idname in self.getIds():
            for tagname in tags:
                if self.hasTagById(idname,tagname):
                    ids.add(idname)
                    break
        return tuple(ids)
    def hasTag(self,tagname):
        if tagname in self.getTags():
            return True
        else:
            return False
    def hasId(self,idname):
        if self.isIdDefined(idname) or self.isIdCalculatable(idname):
            return True
        else:
            return False
    def isIdCalculatable(self,idname):
        if idname in self._getCalculatableIds():
            return True
        else:
            return False
    def isIdDefined(self,idname):
        if idname in self._getDefinedIds():
            return True
        else:
            return False
    def hasTagById(self,idname,tagname):
        info=self.getTag(idname)
        if (info[0]) and (tagname in info[1]):
            return True
        else:
            return False
    def resetValues(self):
        self._resetValues()
    def setValues(self,forceflg,**pairs):
        self._log.debug("[SetValues] Force Flag:%s, K-V Pairs:%s"%(str(forceflg),repr(pairs)))
        successlist=[]
        faillist=[]
        uncertainlist={}
        for k,v in pairs.items():
            # set uncalculatable ids
            if (self.isIdDefined(k)) and (not self.isIdCalculatable(k)):
                self._setValue(k,v)
                successlist.append(k)
        for k,v in pairs.items():
            # set calculatable ids
            if self.isIdCalculatable(k):
                if forceflg:
                    # set value when forceflg=True
                    self._setValue(k,v)
                    successlist.append(k)
                else:
                    info=self.getValue(k)
                    if info[0]:
                        # all dependent ids are set
                        if info[1]==v:
                            successlist.append(k)
                        else:
                            faillist.append(k)
                    else:
                        uncertainlist[k]=v
        # Exception: an Id depend on other calculatable Ids
        cnt=1
        while cnt>0:
            cnt=0
            droplist=[]
            for k,v in uncertainlist.items():
                info=self.getValue(k)
                if info[0]:
                    droplist.append(k)
                    cnt+=1
                    if info[1]==v:
                        successlist.append(k)
                    else:
                        faillist.append(k)
            for k in droplist:
                del uncertainlist[k]
        # Set Uncertain k-v
        for k,v in uncertainlist.items():
            self._setValue(k,v)
        self._log.debug("[SetValues] Success:%s, Fail:%s, Doubt:%s"%(tuple(successlist),tuple(faillist),tuple(uncertainlist.keys())))
        return (tuple(successlist),tuple(faillist),tuple(uncertainlist.keys()))
    def getValue(self,idname):
        if self.hasId(idname):
            idv=self._getAttribute(idname,'_value')
            if idv[0]:
                self._setValue(idname,idv[1])
            return idv
        else:
            return (False,None)
    def getName(self,idname):
        if self.isIdDefined(idname):
            return self._getAttribute(idname,'PNAME')
        else:
            return (False,None)
    def getTag(self,idname):
        if self.isIdDefined(idname):
            return self._getAttribute(idname,'PTAGS')
        else:
            return (False,None)
    def getValueByIndex(self,idname,ididx):
        if self.isIdDefined(idname):
            info=self._getAttribute(idname,'PVALUES')
            if info[0]:
                if 0<=ididx<len(info[1]):
                    return (True,info[1][ididx])
                else:
                    return (False,True)
            else:
                return (False,False)
        else:
            return (False,None)
    def getIndexByValue(self,idname,idvalue):
        if self.isIdDefined(idname):
            info=self._getAttribute(idname,'PVALUES')
            if info[0]:
                if idvalue in info[1]:
                    return (True,info[1].index(idvalue))
                else:
                    return (False,True)
            else:
                return (False,False)
        else:
            return (False,None)
    def _initLogger(self,level,logfile):
        log=logging.getLogger(self.__class__.__name__)
        log.setLevel(level)
        ch=self._getLogHandler(logfile)
        formatter=logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        log.addHandler(ch)
        return log
    def _getLogHandler(self,logfile):
        if logfile:
            ch=logging.FileHandler(logfile)
        else:
            ch=logging.StreamHandler()
        return ch
    def _initData(self):
        pass
    def _resetValues(self):
        pass
    def _addRule(self,rule):
        pass
    def _getAttribute(self,idname,attrname):
        return (False,None)
    def _getDefinedIds(self):
        return ()
    def _getCalculatableIds(self):
        return ()
    def _setValue(self,idname,idvalue):
        pass

class RuleObj(RuleObjBase):
    def __init__(self,loglevel=logging.CRITICAL,logfile=''):
        super(RuleObj,self).__init__(loglevel,logfile)
    def _initData(self):
        self._data={'defined':{},'calculatable':{},'values':{}}
    def _addRule(self,rule):
        if 'PTARGETD' in rule:
            id=rule['PTARGETD']
            name=rule.get('PNAME','')
            tags=rule.get('PTAG',())
            values=rule['PVALUES']
            if 'PDEFAULTV' in rule:
                dv=rule['PDEFAULTV']
            else:
                dv=values[rule.get('PDEFAULTI',0)]
            self._data['defined'][id]={}
            self._data['defined'][id]['PNAME']=name
            self._data['defined'][id]['PTAGS']=tags
            self._data['defined'][id]['PVALUES']=values
            self._data['defined'][id]['PDEFAULTV']=dv
            if id not in self._data['values']:
                self._data['values'][id]=[False,None]
            self._log.debug("[AddRule] %s:%s"%(id,repr(self._data['defined'][id])))
        elif 'PTARGETC' in rule:
            id=rule['PTARGETC']
            self._data['calculatable'][id]={}
            self._data['calculatable'][id]['PINPUT']=rule['PINPUT']
            for cate in ('PFORMULA','PDATAI','PDATAV'):
                if cate in rule:
                    self._data['calculatable'][id][cate]=rule[cate]
                    break
            if id not in self._data['values']:
                self._data['values'][id]=[False,None]
            self._log.debug("[AddRule] %s:%s"%(id,repr(self._data['calculatable'][id])))
    def _getAttribute(self,idname,attrname):
        self._log.debug("[GetAttr] get id[%s] attr[%s]"%(idname,attrname))
        if attrname=='_value':
            if self._data['values'][idname][0]:
                self._log.debug("[GetAttr] get id[%s] attr[%s] value[%s]"%(idname,attrname,repr(self._data['values'][idname][1])))
                return (True,self._data['values'][idname][1])
            else:
                if idname in self._data['calculatable']:
                    if 'PFORMULA' in self._data['calculatable'][idname]:
                        vflg=True
                        inpd={}
                        for inp in self._data['calculatable'][idname]['PINPUT']:
                            inpv=self.getValue(inp)
                            if not inpv[0]:
                                vflg=False
                            if inpv[1] is None:
                                return (False,None)
                            #inpd[inp]=str(self.getIndexByValue(inp,inpv[1])[1])
                            inpd[inp]=str(inpv[1])
                        ans=eval(self._data['calculatable'][idname]['PFORMULA'].format(**inpd))
                        if vflg:
                            self._setValue(idname,ans)
                            self._log.debug("[GetAttr] get id[%s] attr[%s] value[%s]"%(idname,attrname,repr(ans)))
                        else:
                            self._log.debug("[GetAttr] get id[%s] attr[%s] value[%s](calculated by default values)"%(idname,attrname,repr(ans)))
                        return (vflg,ans)
                    elif 'PDATAI' in self._data['calculatable'][idname]:
                        vflg=True
                        ans=0
                        for inp in self._data['calculatable'][idname]['PINPUT']:
                            inpv=self.getValue(inp)
                            if not inpv[0]:
                                vflg=False
                            if inpv[1] is None:
                                return (False,None)
                            tmpa=self._data['defined'][inp]['PVALUES']
                            ans=ans*len(tmpa)+tmpa.index(inpv[1])
                        ans=self._data['calculatable'][idname]['PDATAI'][ans]
                        ans=self._data['defined'][idname]['PVALUES'][ans]
                        if vflg:
                            self._setValue(idname,ans)
                            self._log.debug("[GetAttr] get id[%s] attr[%s] value[%s]"%(idname,attrname,repr(ans)))
                        else:
                            self._log.debug("[GetAttr] get id[%s] attr[%s] value[%s](calculated by default values)"%(idname,attrname,repr(ans)))
                        return (vflg,ans)
                    elif 'PDATAV' in self._data['calculatable'][idname]:
                        vflg=True
                        ans=0
                        for inp in self._data['calculatable'][idname]['PINPUT']:
                            inpv=self.getValue(inp)
                            if not inpv[0]:
                                vflg=False
                            if inpv[1] is None:
                                return (False,None)
                            tmpa=self._data['defined'][inp]['PVALUES']
                            ans=ans*len(tmpa)+tmpa.index(inpv[1])
                        ans=self._data['calculatable'][idname]['PDATAV'][ans]
                        if vflg:
                            self._setValue(idname,ans)
                            self._log.debug("[GetAttr] get id[%s] attr[%s] value[%s]"%(idname,attrname,repr(ans)))
                        else:
                            self._log.debug("[GetAttr] get id[%s] attr[%s] value[%s](calculated by default values)"%(idname,attrname,repr(ans)))
                        return (vflg,ans)
                else:
                    self._log.debug("[GetAttr] get id[%s] attr[%s] default value[%s]"%(idname,attrname,repr(self._data['defined'][idname]['PDEFAULTV'])))
                    return (False,self._data['defined'][idname]['PDEFAULTV'])
        else:
            for cate in ('defined','calculatable'):
                if idname in self._data[cate] and attrname in self._data[cate][idname]:
                    return (True,self._data[cate][idname][attrname])
            else:
                return (False,False)
    def _getDefinedIds(self):
        return sorted(self._data['defined'].iterkeys())
    def _getCalculatableIds(self):
        return sorted(self._data['calculatable'].iterkeys())
    def _setValue(self,idname,idvalue):
        if idvalue!=self._data['values'][idname][1]:
            if self.hasTagById(idname,'VOLATILE'):
                self._data['values'][idname][0]=False    # value valid
            else:
                self._data['values'][idname][0]=True    # value valid
            self._data['values'][idname][1]=idvalue # set value
            self._log.debug("[SetValue] %s:%s"%(idname,repr(idvalue)))
    def _resetValues(self):
        for key in self._data['values'].keys():
            self._data['values'][key]=[False,None]
