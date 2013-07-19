import dbbase

class BirthDB(dbbase.SingleTblDB):
    def __init__(self,dbname='birth.db3'):
        super(BirthDB,self).__init__(dbname)
    def createTbl(self):
        self._table='birthtbl'
        self._cursor.execute("""create table if not exists %s
                                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                 name TEXT,
                                 birthday TEXT)"""%(self._table,))
        self._conn.commit()

if __name__=='__main__':
    db=BirthDB()
    db.append(('name','birthday'),(('tianquan','1983-09-02 13:15:00'),
                                   ('tianyuwen','2013-07-03 13:03:00')))
    print db.data()
