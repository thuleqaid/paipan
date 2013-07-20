import os.path
import logging
import dbbase

class SolarTimeDB(dbbase.DBBase):
    def __init__(self,dbname='difftime.db3',dbpath=os.path.dirname(__file__),logfile='',loglevel=logging.CRITICAL):
        super(SolarTimeDB,self).__init__(os.path.join(dbpath,dbname),logfile,loglevel)
    def createTbl(self):
        stm="create table if not exists dfdate (month INTERER NOT NULL,day INTEGER NOT NULL,diff INTEGER NOT NULL)"
        self._log.debug(stm)
        self._cursor.execute(stm)
        stm="""create table if not exists province
               (id INTEGER PRIMARY KEY AUTOINCREMENT,
                province TEXT NOT NULL)"""
        self._log.debug(stm)
        self._cursor.execute(stm)
        stm="""create table if not exists dfcity
               (id INTEGER PRIMARY KEY AUTOINCREMENT,
                province INTEGER NOT NULL,
                city TEXT NOT NULL,
                lon REAL,
                lat REAL,
                diff INTEGER NOT NULL,
                FOREIGN KEY(province) REFERENCES province(id))"""
        self._log.debug(stm)
        self._cursor.execute(stm)
        self._conn.commit()
    def provinces(self):
        stm="select id,province from province"
        self._log.debug(stm)
        self._cursor.execute(stm)
        return tuple(self._cursor.fetchall())
    def province(self,cityid,defaultvalue=-1):
        data=self.find('dfcity','id',int(cityid),('province',))
        if len(data)>0:
            return data[0][0]
        else:
            return defaultvalue
    def cities(self,provinceid):
        return self.find('dfcity','province',provinceid,('id','city','diff'))
    def dateDiff(self,month,day):
        stm="select diff from dfdate where month=%d and day=%d"%(int(month),int(day))
        self._log.debug(stm)
        self._cursor.execute(stm)
        return self._cursor.fetchone()[0]
    def cityDiff(self,cityid,defaultvalue=-1):
        stm="select diff from dfcity where id=%d"%(int(cityid),)
        self._log.debug(stm)
        self._cursor.execute(stm)
        data=self._cursor.fetchone()
        if data:
            return data[0]
        else:
            return defaultvalue

def loadDiffTime_Date(filename,sdb):
    info=[]
    fh=open(filename,'rU')
    line=fh.readline()
    for line in fh.readlines():
        line=line.strip()
        parts=[int(x) for x in line.split(',')]
        info.append(tuple(parts))
    fh.close()
    sdb.append('dfdate',('month','day','diff'),info)
def loadDiffTime_City(filename,sdb):
    info=[]
    fh=open(filename,'rU')
    line=fh.readline()
    for line in fh.readlines():
        line=line.strip()
        line=line.decode('utf8')
        parts=line.split(',')
        if len(parts)>4:
            if parts[0]:
                if len(info)>0:
                    sdb.append('dfcity',('province','city','lon','lat','diff'),info)
                    info=[]
                sdb.append('province',('province',),((parts[0],),))
                pid=sdb.find('province','province',parts[0],('id',))[0][0]
            info.append((pid,parts[1],float(parts[2]),float(parts[3]),int(parts[4])))
    sdb.append('dfcity',('province','city','lon','lat','diff'),info)
    fh.close()

if __name__=='__main__':
    curpath=os.path.dirname(__file__)
    dtdate='../ref/difftime_date.txt'
    dtcity='../ref/difftime_city.txt'
    sdb=SolarTimeDB('difftime.db3',loglevel=logging.DEBUG)
    loadDiffTime_Date(os.path.join(curpath,dtdate),sdb)
    loadDiffTime_City(os.path.join(curpath,dtcity),sdb)

