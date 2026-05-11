import json
class Mode:
	init = 0
	merge = 1
	delete = 2
	rw = 3
class Template:
	def __init__(self,mode):
		self.mode = mode
		self.data = {}
		self.header = {
			"type":None,
			"version":None,
			"fn":None
		}
		self.actions = {
			"ktd":[],
			"la":[]
		}
		if self.mode == Mode.init:
			self.header['type'] = "init"
		elif self.mode == Mode.merge:
			self.header['type'] = "merge"
	def addKey(self,key):
		self.data[key] = None
	def addPair(self,key,value):
		self.data[key] = value
	def editPair(self,key,value):
		if key in self.data:
			self.data[key] = value
		else:
			raise KeyError(key)
	def setVersion(self,v):
		self.header['version']
	def build(self,fn):
		scon.dump({"header":self.header,"actions":self.actions,"data":self.data},open(fn,"w+"))
	def addHeaderAtrribute(self,name,value):
		self.header[name] = value
	def definePrefName(self,fn):
		self.header['prefname'] = fn
	def addKeyToDelete(self,key):
		self.actions['ktd'].append(key)
	def addKeyToIgnore(self,key):
		self.actions['la'].append(key)
def reader(fn,directory="",override=False):
	pkg = json.load(open(fn))
	if override:
		pkg['header']['type'] = override
	if pkg['header']['type'] == "init":
		file = open(directory+pkg['header']['prefname'],"w+")
		file.write(json.dumps(pkg['data']))
		file.close()
		return True
	elif pkg["header"]['type'] == "merge":
		oldpref = json.load(open(directory+pkg['header']['prefname']))
		for i in pkg['actions']['ktd']:
			oldpref.pop(i)
		for i in pkg['data']:
			if i in oldpref and i in pkg['actions']['la']:
				continue
			oldpref[i] = pkg['data'][i]
		json.dump(oldpref,open(directory+pkg['header']['prefname'],'w+'))
		return True