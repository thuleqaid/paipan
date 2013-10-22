import dbbase
import logging

class LiuyaoDB(dbbase.SingleTblDB):
    def __init__(self,dbname='liuyao.db3',logfile='',loglevel=logging.CRITICAL):
        super(LiuyaoDB,self).__init__(dbname,logfile=logfile,loglevel=loglevel)
    def createTbl(self):
        self._table='liuyaotbl'
        self._cursor.execute("""create table if not exists %s
                                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                 name TEXT NOT NULL,
                                 question TEXT NOT NULL,
                                 gua CHARACTER(30) NOT NULL,
                                 guatime CHARACTER(20) NOT NULL,
                                 analyze TEXT DEFAULT "")"""%(self._table,))
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
    def getLastId(self):
        stm="select max(id) from %s"%(self._table,)
        self._log.debug(stm)
        self._cursor.execute(stm)
        return self._cursor.fetchall()[0][0]

if __name__=='__main__':
    db=LiuyaoDB()
    db.append(('name','question','gua','guatime'),(('tianquan','q1','1,3,2,3,4','2013,7,27,15,9,55'),
                                   ('tianyuwen','q2','4,7,1,2','9,4,8')))
    print db.data()
