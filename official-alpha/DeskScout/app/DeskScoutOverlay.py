import sys,os
os.chdir(os.path.dirname(__file__))
sys.path.insert(0,os.path.join(os.getcwd(), "libs"))
sys.path.append(os.path.join(os.getcwd(), "mods"))
import winreg
import time
import requests
import json
class InvalidRequest(Exception):
	pass
class ServerLost(Exception):
	pass
SERVICE_URL = "http://127.0.0.1:49152"
def getOverlaySettings():
	return json.load(open('../data/overlay/setup.json'))
def getSetting(path):
	#Gets setting from path
	try:
		#Send a POST request to the settings endpoint
		resp = requests.post("http://127.0.0.1:49152/settings",data={"action":"get","path":path},timeout=10)
		data = json.loads(resp.text)
		if data['status'] == "OK":
			return data['data']
		else:
			return InvalidRequest()
	except:
		return ServerLost()

def get_game_name(appid):

	url = "https://store.steampowered.com/api/appdetails"

	response = requests.get(url, params={
		"appids": appid
	})

	data = response.json()

	return data[str(appid)]["data"]["name"]

def checkSteamCache(appid):
	cache = json.load(open("../data/overlay/registry/internal.json"))
	if not f"steam_{appid}" in cache:
		print("Adding game to cache")
		try:
			cache[f"steam_{appid}"] = {
				"name":get_game_name(appid),
				"source":"steam"
			}
			json.dump(cache,open("../data/overlay/registry/internal.json","w+"))
			print("Game",cache[f'steam_{appid}'],"Added")
		except:
			pass
lastreading = 0
		
STEAM_KEY = r"Software\Valve\Steam"
def get_running_steam_game():
	try:
		key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, STEAM_KEY)

		appid, _ = winreg.QueryValueEx(key, "RunningAppID")

		# 0 means no game running
		if appid == 0:
			return None

		return appid

	except FileNotFoundError:
		return None
def OverlayController():
	global lastreading
	# Trigger the overlay if an alarmState is present
	resp = requests.get(SERVICE_URL+"/getAlarmStatus")
	data = json.loads(resp.text)
	if data['data'] != None:
		resp = requests.get(SERVICE_URL+"/getLatestReading")
		data = json.loads(resp.text)
		if data['status'] == "ok":
			import subprocess
			if data['data']['Timestamp']/1000 != lastreading:
				lastreading = data['data']["Timestamp"]/1000
				subprocess.run("pyw DeskScoutAlertOverlay.py")

while True:
	if getSetting("overlay"):
		settings = getOverlaySettings()
		if settings['sources']['steam']:
			try:
				appid = get_running_steam_game()
				
				if appid:
					try:
						checkSteamCache(appid)
					except:
						pass
					print("ALERTING")
					OverlayController()
				else:
					lastreading = 0
					print("No Steam game running")
			except:
				pass
		else:
			lastreading = 0

	else:
		lastreading = 0



	time.sleep(5)