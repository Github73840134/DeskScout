from collections import namedtuple
__version__ = "1.0.1"
__build__ = "Latest"
__platform__ = "Stable"
class Comment:
	'''Add a comment.'''
	isComment = True
	visComment = __name__
	uuid = object()
class SCONDecodeError(Exception):
	pass
def verify(data,x=0,y=0):
	for i in data:
		if type(data[i]) == dict:
			verify(data[i],y=y+1)
		if i == '':
			raise SCONDecodeError("Extraneous ; found "+str(x) + "," + str(y))
def parse(text):
	__doc__ = '''The parser, Used internally'''
	result = {}
	tree = []
	comments = []
	parsed = result
	listmode = False
	mode = 0
	ldepth = 0
	name = ""
	value = ""
	string = False
	wastring = False
	waslist = False
	cw = ''
	comment = ''
	for i in range(0,len(text)):
		cw += text[i]
		if cw == '=' and string == False:
			mode = 1
			cw = ''
		elif cw == '"':
			if mode == 1:
				if string:
					wastring = True
				string = not string
				cw = ''
		elif cw == '\"':
			if string:
				value += '"'
				cw = ''
		elif cw == ',' and listmode:
			if value.isnumeric() and wastring == False:
				value = int(value)
			elif value.lower() == 'true':
				value = True
			elif value.lower() == 'false':
				value = False
			elif value.lower() == 'null':
				value = None
			if waslist == False:
				parsed.append(value)
			else:
				waslist = False
			value = ''
			cw = ''
			wastring = False
		elif cw == ";":
			if string:
				value += ';'
			else:
				if value.isnumeric():
					value = int(value)
				elif value.lower() == 'true':
					value = True
				elif value.lower() == 'false':
					value = False
				elif value.lower() == 'null':
					value = None
			if mode == 2:
				comments.append(comment)
				comment = ''
				mode = 0
				cw = ''
			elif listmode == False:
				parsed[name] = value
				name = ''
				value = ''
				mode = 0
				cw = ''
				wastring = False
				waslist = False
			else:
				name = ''
				value = ''
				mode = 0
				cw = ''
				listmode = False
				wastring = False
			if waslist:
				waslist = False
		elif cw == '\n':
			if string:
				value += '\n'
			cw = ''
		elif cw == '\t':
			if string:
				value += '\t'
			cw = ''
		
		elif cw == ' ':
			if string:
				value += ' '
			if mode == 2:
				comment += ' '
			cw = ''
		elif cw == '{' and mode == 0 and string == False:
			tree.append(parsed)
			parsed[name] = {}
			parsed = parsed[name]
			cw = ''
			name = ''
		elif cw == '}' and mode == 0 and string == False:
			parsed = tree[len(tree)-1]
			tree.pop(len(tree)-1)
			value = ''
			cw = ''
		elif cw == '[' and mode == 1 and string == False:
			tree.append(parsed)
			if type(tree[len(tree)-1]) == dict:
				parsed[name] = []
				parsed = parsed[name]
			if type(tree[len(tree)-1]) == list:
				parsed.append([])
				parsed = parsed[len(parsed)-1]
			listmode = True
			ldepth += 1
			cw = ''
			name = ''
		elif cw == ']' and mode == 1 and string == False:
			if value.isnumeric() and wastring == False:
				value = int(value)
			elif value.lower() == 'true':
				value = True
			elif value.lower() == 'false':
				value = False
			elif value.lower() == 'null':
				value = None
			if text[i-1] != ']':
				parsed.append(value)
			value = ''
			parsed = tree[len(tree)-1]
			tree.pop(len(tree)-1)
			cw = ''
			wastring = False
			if len(tree) != 0:
				if len(tree) > 1:
					if type(tree[ldepth-1]) == dict:
						value = ''
						name = ''		
			
			waslist = True
			ldepth -= 1
		elif cw == "#":
			mode = 2
			cw = ''
		elif cw.isascii():
			if mode == 0:
				name += cw
			if mode == 1:
				value += cw
			if mode == 2:
				comment += cw
			cw = ''
	f = namedtuple("result",['data','comments'])
	verify(result)
	return f(data=result,comments=comments)
def make(data,ind=0,comments=[]):
	made = ''
	for i in data:
		if 'isComment' in dir(i):
			if i.visComment == __name__:
				made += '\t'*ind+'#'+data[i] + ';\n' 
		elif type(data[i]) == int:
			made += '\t'*ind+i + '=' + str(data[i]) + ';\n'
		elif type(data[i]) == str:
			made += '\t'*ind+i + '="' + data[i] + '";\n'
		elif type(data[i]) == bool:
			made += '\t'*ind+i + '=' + str(data[i]).lower() + ';\n'
		elif data[i] == None:
			made += '\t'*ind+i + '=' + 'null;\n'
		elif type(data[i]) == float:
			made += '\t'*ind+i + '="' + data[i] + '";\n'
		elif type(data[i]) == dict:
			made += '\t'*ind+i+'{\n'+make(data[i],ind+1)+'\t'*ind+'}\n'
		elif type(data[i]) == list:
			made += '\t'*ind+i+'='+data[i].__repr__().replace("'",'"')+';\n'
	return made
def dumps(obj):
	'''Creates a SCON file from a dictionary.  
##### Attribute info:
* obj  
  * type: dict

Returns a SCON string'''
	return make(obj)
def dump(obj,fp):
	'''Creates and writes a SCON file from a dictionary.  
##### Attribute info:
* obj
  * type: dict
* fp
  * type: builtin_function_or_method

Make sure that fp is writable.'''
	if not fp.writable:
		raise PermissionError("Make sure the file object is writeable")
	e = make(obj)
	fp.write(e)
	fp.close()
def loads(obj):
	'''Creates a dictonary from a SCON string.  
##### Attribute info:
* obj
  * type: str

Make sure that fp is readable.  
Return a namedtuple: `data` contains the parsed SCON file, `comments` contains the comments from the parsed SCON file.'''
	return parse(obj)
def load(fp):
	'''Creates a dictonary from a SCON file.  
##### Attribute info:
* fp
  * type: builtin_function_or_method

Make sure that fp is readable.  
Return a namedtuple: `data` contains the parsed SCON file, `comments` contains the comments from the parsed SCON file. '''
	if not fp.readable:
		raise PermissionError("Make sure the file object is readable")
	return parse(fp.read())
class Browse:
	
	'''Browse a SCON object like a POSIX file path.  
ex. ```/test/name.str```
#### File Naming
|Python Type|Extention|
|-----------|---------|
| str|.str|
| int|.int|
| bool|.bol|
| list|.lst|
| dict|None (sub-dictionaries represented as directories)'''
	def __init__(self,data):
		global bself
		bself = self
		if type(data) == str:
			self.tree = loads(data)
		else:
			verify(data)
			self.tree = data
		self.cwd = '/'
		self.ftree = {}
		self.prevdir = []
		self.directories = []
		self._listdir()
		self._link(self.tree)
	def _link(self,t,name='/'):
		for i in t:
			if type(t[i]) == int:
				self.ftree[name+i+'.int'] = i
			if type(t[i]) == str:
				self.ftree[name+i+'.str'] = i
			if type(t[i]) == bool:
				self.ftree[name+i+'.bol'] = i
			if type(t[i]) == list:
				self.ftree[name+i+'.lst'] = i
			if type(t[i]) == dict:			
				self._link(t[i],name+i+'/')
				
	def _listdir(self):
		def treemaker(t,o=[],name='/'):
			for i in t:
				if type(t[i]) == int:
					o.append(name+i+'.int')
				if type(t[i]) == str:
					o.append(name+i+'.str')
				if type(t[i]) == bool:
					o.append(name+i+'.bol')
				if type(t[i]) == list:
					o.append(name+i+'.lst')
				if type(t[i]) == dict:
					self.directories.append(name+i)				
					o.extend(treemaker(t[i],[],name+i+'/'))
			return o
		self.etree = treemaker(self.tree)
	def listdir(self,path=None):
		'''Views the current directory tree or the directory specified in `path`.  
* path
  * type: str  

Returns contents of current or specifified directory '''
		made = []
		if path == None:
			for i in self.etree:
				if self.cwd in i:
					made.append(i.strip(self.cwd))
		else:
			for i in self.etree:
				if path in i and i.strip(path) in made :
					made.append(i.strip(path))

		return made
	def chdir(self,path):

		if path[0] != '/':
			
			if self.cwd == '/':
				self.cwd = '/'+path
			else:
				self.cwd = '/'+self.cwd+'/'+path
		else:
			self.cwd = path
	def getcwd(self):
		'''Gets the current directory'''
		return self.cwd
	def find(self,path):
		'''Find value from a path in the dictonary.'''
		loc = self.etree.index(self.path)
		loc2 = self.etree[loc]
		data = loc2.split('/')
		dpath = self.tree
		ftypes = ['.str','.int','.lst','.bol']
		for i in data[1:]:
			if i == data[len(data)-1]:
				return dpath[self.ftree[path]]
			else:
				dpath = dpath[i]
	class open:
		'''Opens the value to be read or written to.  
**NOTE!**: Any changes made to the dictonary will not sync to the SCON file.  (This feature will be added soon.)
* Path
  * type: str

* Mode
  * type: str

Returns a class similar to the builtin function `open()`, the following methods are available.  
* write()
* read()
* close()'''
		writable = False
		readable = True
		closed = False
		name = ''
		def __init__(self,path,mode="r"):
			self = bself
			if mode == 'r':
				self.writable = False
				self.readable = True
				self.name = path
				self.closed = False
			if mode == 'w':
				self.writable = True
				self.readable = False
				self.closed = False
				self.name = path
			if mode == 'w+':
				self.writable = True
				self.readable = False
				self.closed = False
				self.name = path
			loc = self.etree.index(self.cwd+'/'+path)
			loc2 = self.etree[loc]
			data = loc2.split('/')
			self.dpath = self.tree
			for i in data[1:]:
				if i == data[len(data)-1]:
					self.floc = self.ftree[self.cwd+'/'+path]
					if mode == 'w+':
						self.dpath[self.floc] = ""
					break
				else:
					self.dpath = self.dpath[i]
		def read(self):
			self = bself
			'''Read a value.'''
			if self.readable:
				return self.dpath[self.floc]
			else:
				raise PermissionError("Operation Not Permitted")
		def write(self,data):
			self = bself
			'''Writes to the value.'''
			if self.writable:
				self.dpath[self.floc] += data
			else:
				raise PermissionError("Operation Not Permitted")
			
		
		