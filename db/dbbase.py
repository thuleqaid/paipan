import sqlite3
import os.path
import logging

class DBBase(object):
    def __init__(self,dbpath,logfile='',loglevel=logging.CRITICAL):
        super(DBBase,self).__init__()
        self._initloger(loglevel,logfile)
        self._dbpath=dbpath
        self._conn=sqlite3.connect(self._dbpath)
        self._cursor=self._conn.cursor()
        self.createTbl()
    def data(self,table,klist=None):
        if klist:
            stm="select %s from %s"%(','.join(klist),table)
        else:
            stm="select * from %s"%(table,)
        self._log.debug(stm)
        self._cursor.execute(stm)
        return tuple(self._cursor.fetchall())
    def createTbl(self):
        pass
    def append(self,table,cols,values):
        collist=','.join(cols)
        vlist=','.join(['?' for x in range(len(cols))])
        stm="insert into %s (%s) values(%s)"%(table,collist,vlist)
        self._log.debug(stm)
        self._cursor.executemany(stm,values)
        self._conn.commit()
    def find(self,table,col,value,klist=None):
        if isinstance(value,int) or isinstance(value,float):
            if klist:
                stm="select %s from %s where %s = %s" % (','.join(klist),table,col,str(value))
            else:
                stm="select * from %s where %s = %s" % (table,col,str(value))
        else:
            if klist:
                stm="select %s from %s where %s = '%s'" % (','.join(klist),table,col,value)
            else:
                stm="select * from %s where %s = '%s'" % (table,col,value)
        self._log.debug(stm)
        self._cursor.execute(stm)
        return tuple(self._cursor.fetchall())
    def delete(self,table,key,value):
        if isinstance(value,int) or isinstance(value,float):
            stm="delete from %s where %s = %s"%(table,key,str(value))
        else:
            stm="delete from %s where %s = '%s'"%(table,key,value)
        self._log.debug(stm)
        self._cursor.execute(stm)
        self._conn.commit()
    def _initloger(self,level,logfile):
        self._log=logging.getLogger(self.__class__.__name__)
        self._log.setLevel(level)
        ch=self._getLogHandler(logfile)
        formatter=logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        self._log.addHandler(ch)
    def _getLogHandler(self,logfile):
        if logfile:
            ch=logging.FileHandler(logfile)
        else:
            ch=logging.StreamHandler()
        return ch

class SingleTblDB(DBBase):
    def __init__(self,dbname,dbpath=os.path.dirname(__file__),logfile='',loglevel=logging.CRITICAL):
        super(SingleTblDB,self).__init__(os.path.join(dbpath,dbname),logfile,loglevel)
    def createTbl(self):
        self._table=''
        # create table self._table
        # commit
    def append(self,cols,values):
        return super(SingleTblDB,self).append(self._table,cols,values)
    def data(self,klist=None):
        return super(SingleTblDB,self).data(self._table,klist)
    def find(self,col,value,klist=None):
        return super(SingleTblDB,self).find(self._table,col,value,klist)
    def delete(self,col,value):
        return super(SingleTblDB,self).delete(self._table,col,value)

if __name__=='__main__':
    class DBTest(DBBase):
        def createTbl(self):
            self._cursor.execute("create table if not exists test(name TEXT,cnt INTEGER)")
            self._conn.commit()
    db=DBTest('test.db')
    db.append('test',('cnt','name'),((2,'abcd'),(3,'efg')))
    print db.data('test')
