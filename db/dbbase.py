import sqlite3
import os.path

class DBBase(object):
    def __init__(self,dbpath):
        super(DBBase,self).__init__()
        self._dbpath=dbpath
        self._conn=sqlite3.connect(self._dbpath)
        self._cursor=self._conn.cursor()
        self.createTbl()
    def data(self,table,klist=None):
        if klist:
            self._cursor.execute("select %s from %s"%(','.join(klist),table))
        else:
            self._cursor.execute("select * from %s"%(table,))
        return tuple(self._cursor.fetchall())
    def createTbl(self):
        pass
    def append(self,table,cols,values):
        collist=','.join(cols)
        vlist=','.join(['?' for x in range(len(cols))])
        stm="insert into %s (%s) values(%s)"%(table,collist,vlist)
        self._cursor.executemany(stm,values)
        self._conn.commit()

class SingleTblDB(DBBase):
    def __init__(self,dbname,dbpath=os.path.dirname(__file__)):
        super(SingleTblDB,self).__init__(os.path.join(dbpath,dbname))
    def createTbl(self):
        self._table=''
        # create table self._table
        # commit
    def append(self,cols,values):
        super(SingleTblDB,self).append(self._table,cols,values)
    def data(self,klist=None):
        return super(SingleTblDB,self).data(self._table,klist)

if __name__=='__main__':
    class DBTest(DBBase):
        def createTbl(self):
            self._cursor.execute("create table if not exists test(name TEXT,cnt INTEGER)")
            self._conn.commit()
    db=DBTest('test.db')
    db.append('test',('cnt','name'),((2,'abcd'),(3,'efg')))
    print db.data('test')
