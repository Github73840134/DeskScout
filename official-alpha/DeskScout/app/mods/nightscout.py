# Owl thingy access device
import requests,json,urllib,time,datetime as dt
from datetime import datetime
logger = None
class Entry:
	def __init__(self,sgv,readingTime,trendArrow):
		self.sgv = sgv
		self.time = readingTime
		self.trend = trendArrow
	def makeNSEntry(self):
		return {
			"type":'sgv',
			"dateString":str(datetime.fromtimestamp(self.time, tz=dt.timezone.utc)),
			"date":self.time*1000,
			"sgv":self.sgv,
			"direction":self.trend,
			"scaled":self.sgv,
			"noise":1,
			"rssi":30,
			"filtered":self.sgv*100000,
			"unfiltered":self.sgv*100000,
			"device":"deskscout-ns-uploader"

		}
class NightScout:
	def __init__(self,url,token):
		self.url = url
		self.token = token
		self.server = requests.Session()
	def connect(self):
		try:
			resp = self.server.get(self.url+f"/api/v1/status.json?token={self.token}")
		except:
			raise ConnectionError()
	def checkToken(self):
		try:
			resp = self.server.get(self.url+f"/api/v1/status.json?token={self.token}")
			if resp.status_code == 200:
				return 2
			if resp.status_code == 403:
				return 1
			if resp.status_code == 201:
				return 0
		except:
			raise ConnectionError()
	def uploadEntry(self,entry:Entry):
		resp = self.server.post(self.url+f"/api/v1/entries?token={self.token}",json=entry.makeNSEntry())
		print(resp.text)
	def getLastEntryTime(self):
		resp = self.server.get(self.url+f"/api/v1/entries/current.json?token={self.token}")
		print(resp.text)
		data = json.loads(resp.text)[0]
		return int(data['date'])

