from mods.sdk.gdp import v1 as sdk
import time,re,json
from libs import requests
import requests
class GlucoseDataProvider():
	__manifest__ = None
	def __init__(self):
		self.authstate = sdk.AuthenticationState.UNAUTHED
		self.token = None
	def setup(self):
		pass
	def login(self,username,password):
		# Username and password both need to be a string
		print("Starting")
		resp = requests.post('https://shareous1.dexcom.com/ShareWebServices/Services/General/AuthenticatePublisherAccount',json={"accountName":username,'password':password,'applicationId':"d89443d2-327c-4a6f-89e5-496bbb0317db"})
		print(resp.status_code,resp.text)
		if resp.status_code == 200:
			resp = requests.post('https://shareous1.dexcom.com/ShareWebServices/Services/General/LoginPublisherAccountById',json={"accountId":eval(resp.text),'password':password,'applicationId':"d89443d2-327c-4a6f-89e5-496bbb0317db"})
			if resp.status_code == 200:
				self.authstate = sdk.AuthenticationState.AUTHED
				self.token = eval(resp.text)
			elif resp.status_code == 500:
				self.authstate = sdk.AuthenticationState.INVALID_CREDENTIALS

		elif resp.status_code == 500:
			self.authstate = sdk.AuthenticationState.INVALID_CREDENTIALS

		return
	def getAuthStatus(self):
		# Must return one of the states described in the AuthenticationState Class
		return self.authstate
	def getLatestGlucoseReading(self):
		# Return a GlucoseReading object
		#print("AUTHSTAT",self.authstate,self.token)
		if self.authstate == sdk.AuthenticationState.AUTHED:
			resp = requests.post("https://share2.dexcom.com/ShareWebServices/Services/Publisher/ReadPublisherLatestGlucoseValues",json={'sessionId':self.token,"minutes":5,"maxCount":1})
			print(resp.text)
			reading = json.loads(resp.text)[0]
			#print(resp.status_code,reading)
			match = re.match(
				r"Date\((?P<timestamp>\d+)(?P<timezone>[+-]\d{4})\)",
				reading["DT"],
			)
			dummy = sdk.GlucoseReading()

			dummy.value = reading["Value"]
			dummy.trend = reading["Trend"]
			dummy.trend_description = "steady"
			dummy.timestamp = int(match.group("timestamp")) / 1000.0
			dummy.json = {"Timestamp":dummy.timestamp,"Value":dummy.value,"Trend":dummy.trend,"TrendDescription":dummy.trend_description}
			return dummy
	def getState(self):
		try:
			resp = requests.get("https://share2.dexcom.com/ShareWebServices/Services/General/AuthenticatePublisherAccount")
			print(resp.status_code)
			if resp.status_code == 405:
				return sdk.State.SERVICE_ONLINE
			else:
				return sdk.State.SERVICE_ISSUE
		except:
			return sdk.State.SERVICE_UNREACHABLE
	def getAllReadings(self):
		# Return multiple GlucoseReading objects
		#print("AUTHSTAT",self.authstate,self.token)
		if self.authstate == sdk.AuthenticationState.AUTHED:
			resp = requests.post("https://share2.dexcom.com/ShareWebServices/Services/Publisher/ReadPublisherLatestGlucoseValues",json={'sessionId':self.token,"minutes":int(86400/60),"maxCount":2880})
			print(resp.text)
			readings = json.loads(resp.text)
			
			rlist = []
			for reading in readings:
				match = re.match(
					r"Date\((?P<timestamp>\d+)(?P<timezone>[+-]\d{4})\)",
					reading["DT"],
				)
				dummy = sdk.GlucoseReading()

				dummy.value = reading["Value"]
				dummy.trend = reading["Trend"]
				dummy.trend_description = "steady"
				dummy.timestamp = int(match.group("timestamp")) / 1000.0
				dummy.json = {"Timestamp":dummy.timestamp,"Value":dummy.value,"Trend":dummy.trend,"TrendDescription":dummy.trend_description}
				rlist.append(dummy)
			print(rlist)
			return rlist
__gdp__ = GlucoseDataProvider
