from .. import const
from .. import types
import os
import json
from mods import gdr
from libs import requests

def getSetting(path):
	#Gets setting from path
	try:
		#Send a POST request to the settings endpoint
		resp = requests.post(const.Service.Url.settingsEndpoint,data={"action":"get","path":path},timeout=10)
		data = json.loads(resp.text)
		if data['status'] == "OK":
			return data['data']
		else:
			raise const.Service.InvalidRequest()
	except:
		raise const.Service.NotAvailable()
def changeSetting(path,value):
	# Changes a setting at path to value
	try:
		#Send a POST request to the settings endpoint
		resp = requests.post(const.Service.Url.settingsEndpoint,data={"action":"set","path":path,"value":str(value)},timeout=10)
		data = json.loads(resp.text)
		if data['status'] == "ok":
			return const.Service.Status.Success
		elif data['status'] == "key":
			return const.Service.Status.InvalidParameter
	except:
		return const.Service.Status.CommandFailed