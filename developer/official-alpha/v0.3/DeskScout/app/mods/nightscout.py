# Nightscout API
import requests,json,urllib,datetime,time

logger = None
class Entry:
	def __init__(self,sgv,readingTime,trendArrow):
		self.sgv = sgv
		self.time = readingTime
		self.trend = trendArrow
	def makeNSEntry(self):
		return {
			"type":'sgv',
			"dateString":datetime.fromtimestamp(self.time, tz=datetime.timezone.utc),
			"date":self.time,
			"sgv":self.sgv,
			"direction":self.trend
		}
class NightScout:
	def __init__(self,url,token):
		self.url = url
		self.token = token
		self.server = None
	def connect(self):
		try:
			self.server.get(self.url+f"?token={self.token}")
		except:
			raise ConnectionError()
	def uploadEntry(self,entry):
		pass