from datetime import datetime
import lunar

class Bazi(object):
    Tbl_ChangGan=((10,   ),
                  (6,10,8),
                  (1,3,5 ),
                  (2,    ),
                  (5,2,10),
                  (3,7,5 ),
                  (4,6   ),
                  (6,4,2 ),
                  (7,9,5 ),
                  (8,    ),
                  (5,8,4 ),
                  (9,1   ))
    def __init__(self):
        self._lunar=lunar.Lunar()
    def setPerson(self,gender,cal):
        info=self._lunar.transCal(cal)
        self.setParams(
            XingBie=gender,
            ShengNianGan=(info[0][0]-1)%10+1,
            ShengNianZhi=(info[0][0]-1)%12+1,
            ShengYueGan=(info[0][1]-1)%10+1,
            ShengYueZhi=(info[0][1]-1)%12+1,
            ShengRiGan=(info[0][2]-1)%10+1,
            ShengRiZhi=(info[0][2]-1)%12+1,
            ShengShiGan=(info[0][3]-1)%10+1,
            ShengShiZhi=(info[0][3]-1)%12+1,
            )
    def getData(self,k,dv=''):
        return self._data.get(k,dv)
    def setParams(self,**kwargs):
        self.init_data()
        for k,v in kwargs.items():
            self._data[k]=v
    def init_data(self):
        self._data={}
if __name__=='__main__':
    bz=Bazi()
    cal=(2013,7,3,12,43,0)
    bz.setPerson(1,cal)
    print bz._data
    print("%2d      %2d      %2d      %2d"%(bz.getData('ShengNianGan'),bz.getData('ShengYueGan'),bz.getData('ShengRiGan'),bz.getData('ShengShiGan')))
    print("%2d      %2d      %2d      %2d"%(bz.getData('ShengNianZhi'),bz.getData('ShengYueZhi'),bz.getData('ShengRiZhi'),bz.getData('ShengShiZhi')))
    print("%-6s  %-6s  %-6s  %-6s"%(','.join([str(x) for x in Bazi.Tbl_ChangGan[bz.getData('ShengNianZhi')-1]]),
                                    ','.join([str(x) for x in Bazi.Tbl_ChangGan[bz.getData('ShengYueZhi')-1]]),
                                    ','.join([str(x) for x in Bazi.Tbl_ChangGan[bz.getData('ShengRiZhi')-1]]),
                                    ','.join([str(x) for x in Bazi.Tbl_ChangGan[bz.getData('ShengShiZhi')-1]])))
