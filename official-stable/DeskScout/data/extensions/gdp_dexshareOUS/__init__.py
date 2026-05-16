from mods.sdk.gdp import v1 as sdk
import time,re,json
from libs import requests
import requests
DEXCOM_TREND_DIRECTIONS: dict[str, int] = {
    "None": 0,  # unconfirmed
    "DoubleUp": 1,
    "SingleUp": 2,
    "FortyFiveUp": 3,
    "Flat": 4,
    "FortyFiveDown": 5,
    "SingleDown": 6,
    "DoubleDown": 7,
    "NotComputable": 8,  # unconfirmed
    "RateOutOfRange": 9,  # unconfirmed
}
TREND_DESCRIPTIONS: list[str] = [
    "",
    "rising quickly",
    "rising",
    "rising slightly",
    "steady",
    "falling slightly",
    "falling",
    "falling quickly",
    "unable to determine trend",
    "trend unavailable",
]
class GlucoseDataProvider():
	__manifest__ = None
	def __init__(self):
		self.authstate = sdk.AuthenticationState.UNAUTHED
		self.token = None
		self.last = 0
		self.last2 = 0

		self.reading = None
		self.cache = []
		self.state = None
	def setup(self):
		pass
	def login(self,username,password):
		# Username and password both need to be a string
		print("Share requesting authorization")
		resp = requests.post('https://shareous1.dexcom.com/ShareWebServices/Services/General/AuthenticatePublisherAccount',json={"accountName":username,'password':password,'applicationId':"d89443d2-327c-4a6f-89e5-496bbb0317db"})
		print("We have liftoff")
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
			if time.time()-self.last > 15:
				try:
					self._getAllReadings()
					self.last = time.time()
				except:
					pass
			return self.cache[0]
	def getState(self):
		if time.time()-self.last2 > 60:
			try:
				resp = requests.get("https://shareous1.dexcom.com/ShareWebServices/Services/General/AuthenticatePublisherAccount")
				print(resp.status_code)
				if resp.status_code == 405:
					self.state = sdk.State.SERVICE_ONLINE
					

				else:
					self.state = sdk.State.SERVICE_ISSUE
			except:
				self.state = sdk.State.SERVICE_UNREACHABLE
			self.last2 = time.time()
		return self.state

	def _getAllReadings(self):
		# Return multiple GlucoseReading objects
		#print("AUTHSTAT",self.authstate,self.token)
		if self.authstate == sdk.AuthenticationState.AUTHED:
			resp = requests.post("https://shareous1.dexcom.com/ShareWebServices/Services/Publisher/ReadPublisherLatestGlucoseValues",json={'sessionId':self.token,"minutes":int(86400/60),"maxCount":2880})
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
				#print(dummy.trend)
				dummy.trend_description = TREND_DESCRIPTIONS[DEXCOM_TREND_DIRECTIONS[reading["Trend"]]]
				dummy.timestamp = int(match.group("timestamp"))
				dummy.json = {"Timestamp":dummy.timestamp,"Value":dummy.value,"Trend":dummy.trend,"TrendDescription":dummy.trend_description}
				rlist.append(dummy)
			self.cache = rlist
	def getAllReadings(self):
		# Return multiple GlucoseReading objects
		#print("AUTHSTAT",self.authstate,self.token)
		if self.authstate == sdk.AuthenticationState.AUTHED:
			return self.cache
__gdp__ = GlucoseDataProvider
