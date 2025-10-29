# Resource identifier
import json
class Resource:
	rtype = 0
	rvalue = None
class ResourceProvider:
	def __init__(self):
		pass
	def get(self, rid):
		pass
class ResourceTable(ResourceProvider):
	def __init__(self,rf_path):
		self.rtable = json.load(open(rf_path))
	def get(self, rid):
		return super().get(rid)