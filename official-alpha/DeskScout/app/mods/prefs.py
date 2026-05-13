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
			"prefname":None
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
import json


def path_matches(path, path_list):
    return path in path_list


def delete_nested_key(obj, path):
    """
    Deletes a nested key from a dict using a path list.
    Example:
        ['a', 'b', 'c']
    deletes:
        obj['a']['b']['c']
    """

    current = obj

    # Traverse to parent
    for key in path[:-1]:
        if key not in current or not isinstance(current[key], dict):
            return
        current = current[key]

    # Delete final key
    current.pop(path[-1], None)


def merge_dict(old, new, leave_alone_paths, delete_paths, current_path=None):
    if current_path is None:
        current_path = []

    for key, value in new.items():
        path = current_path + [key]

        # Skip keys marked leave-alone
        if path_matches(path, leave_alone_paths):
            continue

        # Recursive merge
        if (
            isinstance(value, dict)
            and key in old
            and isinstance(old[key], dict)
        ):
            merge_dict(
                old[key],
                value,
                leave_alone_paths,
                delete_paths,
                path
            )
        else:
            old[key] = value


def reader(fn, directory="", override=False):

    pkg = json.load(open(fn))

    if override:
        pkg['header']['type'] = override

    if pkg['header']['type'] == "init":

        with open(directory + pkg['header']['prefname'], "w+") as file:
            json.dump(pkg['data'], file)

        return True

    elif pkg["header"]['type'] == "merge":

        with open(directory + pkg['header']['prefname']) as f:
            oldpref = json.load(f)

        # Convert paths
        leave_alone_paths = [
            p.split('/')
            for p in pkg['actions']['la']
        ]

        delete_paths = [
            p.split('/')
            for p in pkg['actions']['ktd']
        ]

        # Delete nested keys
        for path in delete_paths:
            delete_nested_key(oldpref, path)

        # Merge data
        merge_dict(
            oldpref,
            pkg['data'],
            leave_alone_paths,
            delete_paths
        )

        with open(directory + pkg['header']['prefname'], 'w+') as f:
            json.dump(oldpref, f)

        return True