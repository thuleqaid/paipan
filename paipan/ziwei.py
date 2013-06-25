class ZiWeiPaiPan(object):
	def __init__(self):
		super(ZiWeiPaiPan,self).__init__()
		self._data={}
		self._data['ShengNianGan']=10
		self._data['ShengNianZhi']=6
		self._data['ShengYueGan']=8
		self._data['ShengYueZhi']=8
		self._data['ShengRiGan']=6
		self._data['ShengRiZhi']=8
		self._data['ShengShiGan']=6
		self._data['ShengShiZhi']=6
		self._inputdata={}
		self._outputdata={}
		self._inputdata['ShengNianGan']=(1,2,3,4,5,6,7,8,9,10)
		self._inputdata['ShengNianZhi']=(1,2,3,4,5,6,7,8,9,10,11,12)
		self._inputdata['ShengYueGan']=(1,2,3,4,5,6,7,8,9,10)
		self._inputdata['ShengYueZhi']=(1,2,3,4,5,6,7,8,9,10,11,12)
		self._inputdata['ShengRiGan']=(1,2,3,4,5,6,7,8,9,10)
		self._inputdata['ShengRiZhi']=(1,2,3,4,5,6,7,8,9,10,11,12)
		self._inputdata['ShengShiGan']=(1,2,3,4,5,6,7,8,9,10)
		self._inputdata['ShengShiZhi']=(1,2,3,4,5,6,7,8,9,10,11,12)
		self.loadConfig('ziwei_rule.txt')

	def loadConfig(self,cfile):
		fh=open(cfile,'rU')
		target=''
		for line in fh.readlines():
			line=line.strip()
			if line.startswith('#'):
				pass
			elif line.startswith('Target:'):
				if target!='':
					self._inputdata[target]=tuple(int(x) for x in output.split(','))
					self._outputdata[target]={'params':tuple(input.split(',')),'data':tuple(int(x) for x in data.split(','))}
				target=line[7:]
			elif line.startswith('Input:'):
				input=line[6:]
			elif line.startswith('Output:'):
				output=line[7:]
			elif line.startswith('Data:'):
				data=''
			else:
				if data=='':
					data=line
				else:
					if data.endswith(','):
						data=data+line
					else:
						data=data+','+line
		if target!='':
			self._inputdata[target]=tuple(int(x) for x in output.split(','))
			self._outputdata[target]={'params':tuple(input.split(',')),'data':tuple(int(x) for x in data.split(','))}
		fh.close()

	def getData(self,datakey,defaultvalue=''):
		if datakey in self._inputdata:
			if datakey in self._outputdata:
				dindex=0
				for pkey in self._outputdata[datakey]['params']:
					dindex=dindex*len(self._inputdata[pkey])+self._inputdata[pkey].index(self.getData(pkey))
				return self._outputdata[datakey]['data'][dindex]
			else:
				return self._data[datakey]
		else:
			return defaultvalue

if __name__=='__main__':
	zw=ZiWeiPaiPan()
	print zw._outputdata
	print zw.getData('MingGong')