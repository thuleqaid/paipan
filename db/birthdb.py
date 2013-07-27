import dbbase
import logging

class BirthDB(dbbase.SingleTblDB):
    def __init__(self,dbname='birth.db3',logfile='',loglevel=logging.CRITICAL):
        super(BirthDB,self).__init__(dbname,logfile=logfile,loglevel=loglevel)
    def createTbl(self):
        self._table='birthtbl'
        self._cursor.execute("""create table if not exists %s
                                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                 name TEXT UNIQUE NOT NULL,
                                 gender CHARACTER(1) NOT NULL,
                                 birthday CHARACTER(19) NOT NULL,
                                 locationtype CHARACTER(1),
                                 locationdata CHARACTER(9))"""%(self._table,))
        self._conn.commit()
    def update(self,id,**kwargs):
        stm="update %s set "%(self._table,)
        stm+=",".join(["%s = '%s'"%(x[0],x[1]) for x in kwargs.items()])
        stm+=" where id=%d"%(id,)
        self._log.debug(stm)
        self._cursor.execute(stm)
        self._conn.commit()
    def delete(self,id):
        return super(LiuyaoDB,self).delete('id',id)

if __name__=='__main__':
    db=BirthDB()
    db.append(('name','gender','birthday'),(('tianquan','M','1983-09-02 13:15:00'),
                                   ('tianyuwen','M','2013-07-03 13:03:00')))
    print db.data()
