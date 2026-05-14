import os,sys
os.chdir(os.path.dirname(__file__))
sys.path.insert(0,os.path.join(os.getcwd(), "libs"))
sys.path.append(os.path.join(os.getcwd(), "mods"))
from discordrp import Presence
import requests
import time

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
keys = json.load(open("../data/api_keys.json"))
client_id = keys['discord']  # Replace this with your own client id
presence = None
def formatDetails():
	preamble = ""
	glucose = ""
	trend = ""
	resp = requests.get(SERVICE_URL+"/getAlarmStatus")
	data = json.loads(resp.text)
	# Urgent Low Glucose
	dk = {
		"None":"",
		"urgentLow":"Urgent Low: ",
		"low":"Low Glucose: ",
		"high":"High Glucose: ",
		"risingFast":"Rising Fast: ",
		"fallingFast":"Falling Fast: ",
	}
	preamble = dk[str(data['data'])]
	resp = requests.get(SERVICE_URL+"/getLatestReading")
	data = json.loads(resp.text)
	print("glr",data)
	if data['status'] == "ok":
		glucose = f"{data['data']["Value"]}mg/dl ({round(data['data']["Value"]/18,1)} mmol/L)"
		trend = f"{data['data']["TrendDescription"]}"
	return (preamble+glucose+" and "+trend,f"Last Updated: {time.ctime(data['data']["Timestamp"]/1000)}")

def getIcon():
	resp = requests.get(SERVICE_URL+"/getAlarmStatus")
	data = json.loads(resp.text)
	print("trend",resp.text)
	return str(data['data']).lower()

presence = None
while True:
	while getSetting("drp"):
		if presence == None:
			try:
				presence = Presence(client_id)
				start_time = time.time()
			except Exception as e:
				print("Error",str(e))
		else:
			try:
				toptext,bottomtext = formatDetails()
				icon = getIcon()

				try:
					
					presence.set(
						{
							"state": bottomtext,
							"details": toptext,
							"timestamps": {"start": int(start_time)},
							"assets": {
								"large_image": "logo",  # Replace this with the key of one of your assets
								"small_image": getIcon(),  # Replace this with the key of one of your assets
							}
						}
					)
				except:
					presence = None
			except Exception as e:
				print("Gen Error",e)
		time.sleep(5)
	if presence:
		try:
			presence.close()
			
		except:
			pass
		presence = None
	time.sleep(5)