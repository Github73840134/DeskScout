# DeskScout Service
# Author: Seth Edwards
# DeskScout service pulls information from clarity
import os,sys,json
os.chdir(os.path.dirname(__file__))
sys.path.append(os.path.join(os.getcwd(),'libs'))
sys.path.append(os.path.join(os.getcwd(),'mods'))

from bottle import route, run, template,request,post
import keyring,psutil, subprocess
from windows_toasts import Toast, ToastAudio, WindowsToaster,InteractableWindowsToaster,ToastDuration
from pathlib import Path
from win32more.Windows.Win32.Media.Audio import PlaySoundW, SND_FILENAME, SND_ASYNC, SND_PURGE
from win32more.Windows.Win32.Foundation import PWSTR
import time
import requests,_thread,json,logging
from tkinter import messagebox
import importlib
from importlib import util as imputil
class DeltaTimeFormatter(logging.Formatter):
	def format(self, record):
		record.delta = time.time()-ast
		return super().format(record)
handler = logging.StreamHandler(open(f"logs/service/{time.strftime("%Y-%m-%d-%H%M%S")}.log","w"))
LOGFORMAT = '+%(asctime)s [%(delta)s] %(name)s %(levelname)s: %(message)s'
fmt = DeltaTimeFormatter(LOGFORMAT)
handler.setFormatter(fmt)
logging.basicConfig(
					format='%(asctime)s [%(delta)s] %(levelname)-9s: %(message)s',
					datefmt='%Y-%m-%d %H:%M:%S',
					handlers=[handler],
					level=logging.INFO)
ast = time.time()
class log:
	notifier = logging.getLogger("notifier")
	main = logging.getLogger("main")
	gdp = logging.getLogger("gdp")
	serviceChecker = logging.getLogger("serverchecker")

	exts = logging.getLogger("exts")
	updater = logging.getLogger("updater")

	status = logging.getLogger("status")
	sync = logging.getLogger("deskscout_sync")
	nsync = logging.getLogger("nightscout_sync")

account = None
serviceConnected = False
serviceOffline = True
serviceDisconnectedAt = 0
attemptingConnection = False
intent = None
from mods import gdr
__version__ = "6"
__build__ = "18"
__channel__ = "developer"
__release__ = "alpha"
class Flags:
	USE_ALTERNATE_UPDATE_SERVER = False
	DISABLE_OVERLAY = False
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-fromDeskScoutPy",action="store_true")
parser.add_argument("-useAltUpdateServer",action="store_true")
parser.add_argument("-disableOverlay",action="store_true")
args = parser.parse_args(sys.argv[1:])
Flags.USE_ALTERNATE_UPDATE_SERVER = args.useAltUpdateServer
Flags.DISABLE_OVERLAY = args.disableOverlay

rec = None
if Flags.USE_ALTERNATE_UPDATE_SERVER:
	UPDATE_URL = json.load(open("../data/url_const.json"))['update.alt_host']
else:
	UPDATE_URL = json.load(open("../data/url_const.json"))['update.host']

try:
	log.main.info("Checking if service is already running")
	print("Checking if service is already running")
	resp = requests.get("http://127.0.0.1:49152/about")
	if args.fromDeskScoutPy:
		log.main.warning("Another service instance is currently running while invoked from launcher. We will quietly exit")
		exit(0)
	try:
		ver = json.loads(resp.text)
		if ver['build'] != __build__:
			log.main.warning("Another service instance of a different version is currently running")

			ans = messagebox.askyesno("DeskScout Service","An newer/older version of service is already running, would you like to stop the old service and start the new one?")
			if ans:
				log.main.info("Stopping old service")

				try:
					requests.get("http://127.0.0.1:49152/shutdown")
				except:
					pass
			else:
				log.main.info("Stopping this instance")

				p = psutil.Process(os.getpid())
				for proc in p.children(recursive=True):
					proc.kill()
				p.kill()
		else:
			log.main.warning("Another service instance is currently running")
			messagebox.showinfo("DeskScout Service","DeskScout service is already running, please stop your current instance before starting a new one")
			p = psutil.Process(os.getpid())
			for proc in p.children(recursive=True):
				proc.kill()
			p.kill()
	except:

		messagebox.showinfo("DeskScout Service","DeskScout service is already running, please stop your current instance before starting a new one")
		p = psutil.Process(os.getpid())
		for proc in p.children(recursive=True):
			proc.kill()
		p.kill()
	
except:
	logging.info("Service not running or is unresponsive")
from datetime import datetime, timedelta, timezone

def hours_to_utc_minute_timestamps(hours):
	"""
	Converts a duration of `hours` into a list of UTC timestamps (in seconds)
	for every minute, starting from the current UTC time.
	
	Args:
		hours (int or float): Number of hours to generate timestamps for.
	
	Returns:
		list: List of UNIX timestamps in seconds for each minute.
	"""
	now = datetime.now(timezone.utc)
	total_minutes = int(hours * 60)
	return [
		int((now + timedelta(minutes=i)).timestamp())
		for i in range(total_minutes + 1)
	]
def calculate_slope(data):
	times = [(t - data[0][0]).total_seconds() / 60 for t, _ in data]
	values = [g for _, g in data]
	
	# Simple linear regression (least squares)
	n = len(values)
	avg_x = sum(times) / n
	avg_y = sum(values) / n

	num = sum((times[i] - avg_x) * (values[i] - avg_y) for i in range(n))
	den = sum((times[i] - avg_x)**2 for i in range(n))
	
	slope = num / den if den != 0 else 0
	return slope  # units: mg/dL per minute

def predict_glucose(current_value, slope, minutes_ahead=20):
	return current_value + slope * minutes_ahead
def urgent_low_soon_alert(glucose_data, threshold=55, horizon=20):
	slope = calculate_slope(glucose_data)
	current_glucose = glucose_data[-1][1]
	predicted = predict_glucose(current_glucose, slope, horizon)
	
	print(f"Slope: {slope:.2f} mg/dL/min, Predicted in {horizon} min: {predicted:.1f} mg/dL")
	
	return predicted <= threshold
silence = {
	"urgentLow":None,
	"urgentLowSoon":None,
	"low":None,
	"high":None,
	"risingFast":None,
	"fallingFast":None,
}
notified = {
	"urgentLow":False,
	"urgentLowSoon":False,
	"low":False,
	"high":False,
	"risingFast":False,
	"fallingFast":False,
}
currentAlarmState = None
serverStatusInit = False
recordQueue = []
serviceOffline = True
GlucoseDataProvider = None
activeAlert = None
class SDK:
	gdp = None
toaster = InteractableWindowsToaster('DeskScout')
def sdkResolver(sdk_id):
	sdkmanifest = json.load(open("../data/sdk.json"))
	try:
		return f"../{sdkmanifest[sdk_id]['path']}"
	except KeyError:
		return None
def loadGlucoseDataProvider():
	global GlucoseDataProvider
	log.exts.info("Loading glucose data provider")
	try:
		settings = json.load(open("../data/settings.json"))
		if not settings['gdp']:
			log.exts.warning("No glucose data provider was selected")

			return
		spec = imputil.spec_from_file_location("GlucoseDataProviderX", f"../data/extensions/{settings['gdp']}/__init__.py")
		
		GlucoseDataProviderX = imputil.module_from_spec(spec)
		# Register the module in sys.modules (optional but good practice)
		# Execute the module code
		spec.loader.exec_module(GlucoseDataProviderX)
		GlucoseDataProvider = GlucoseDataProviderX.__gdp__()
		GlucoseDataProvider.__manifest__ = json.load(open(f"../data/extensions/{settings['gdp']}/manifest.json"))
		spec = imputil.spec_from_file_location("GlucoseDataProviderSDK", sdkResolver(GlucoseDataProvider.__manifest__['sdk']))
		print(sdkResolver(GlucoseDataProvider.__manifest__['sdk']))
		SDK.gdp = imputil.module_from_spec(spec)
		# Register the module in sys.modules (optional but good practice)
		# Execute the module code
		spec.loader.exec_module(SDK.gdp)
		log.exts.info("Glucouse data provider load")

	except Exception as e:
		log.exts.error(f"GDP failed to load {str(e)}")
		newToast = Toast()
		newToast.text_fields = ['Issue with Glucose Data Provider', 'Glucose data provider failed to initialize.']
		newToast.audio = ToastAudio(Path(os.path.abspath(os.path.join(os.getcwd(),'../assets/sounds/generic.wav'))),silent=True)
		PlaySoundW(PWSTR(os.path.join(os.getcwd(),'../assets/sounds/attention.wav')), None, SND_FILENAME | SND_ASYNC)
		toaster.clear_toasts()
		toaster.show_toast(newToast)
def serverstatus():
	global serviceOffline,serviceConnected,serviceDisconnectedAt,account,serverStatusInit
	while True:
		try:
			resp = GlucoseDataProvider.getState()
			log.serviceChecker.debug(f"GDP state {resp}")
			if resp != SDK.gdp.State.SERVICE_ONLINE:
				if not serviceOffline:
					log.serviceChecker.warning(f"Service is offline: '{GlucoseDataProvider.__manifest__["serviceName"]}'")
					serviceOffline = True
					serviceDisconnectedAt = time.time()

					if serviceConnected:
						serviceDisconnectedAt = 0
						if bulb:
							bulb.title = "DeskScout\nApplication Offline"

						newToast = Toast()
						newToast.text_fields = [f'{GlucoseDataProvider.__manifest__["serviceName"]} Unreachable', 'DeskScout cannot provide alerts']
						newToast.audio = ToastAudio(Path(os.path.abspath(os.path.join(os.getcwd(),'../assets/sounds/attention.wav'))),silent=True)
						PlaySoundW(PWSTR(os.path.join(os.getcwd(),'../assets/sounds/attention.wav')), None, SND_FILENAME | SND_ASYNC)
						serviceConnected = False
						toaster.show_toast(newToast)
				else:
					if time.time()-serviceDisconnectedAt > 59:
						log.gdp.warning(f"Service is offline: '{GlucoseDataProvider.__manifest__["serviceName"]}'")
						if bulb:
							bulb.title = "DeskScout\nApplication Offline"

						newToast = Toast()
						newToast.text_fields = [f'{GlucoseDataProvider.__manifest__["serviceName"]} Unreachable', 'DeskScout cannot provide alerts']
						newToast.audio = ToastAudio(Path(os.path.abspath(os.path.join(os.getcwd(),'../assets/sounds/attention.wav'))),silent=True)
						PlaySoundW(PWSTR(os.path.join(os.getcwd(),'../assets/sounds/attention.wav')), None, SND_FILENAME | SND_ASYNC)
						toaster.show_toast(newToast)
						serviceDisconnectedAt = time.time()
			else:
				if serviceOffline:
					log.serviceChecker.info(f"Service is online: '{GlucoseDataProvider.__manifest__["serviceName"]}'")
					newToast = Toast()
					serviceOffline = False 
					serviceDisconnectedAt = 0
					if not attemptingConnection:
						_thread.start_new_thread(attemptConnect,())
		except Exception as e :
			log.serviceChecker.error(f"Service is offline due to an exception: {str(e)}")
			if not serviceOffline:
				serviceOffline = True
				serviceDisconnectedAt = time.time()

				if serviceConnected:
					serviceDisconnectedAt = 0
					newToast = Toast()
					if bulb:
						bulb.title = "DeskScout\nApplication Offline"

					newToast.text_fields = [f'{GlucoseDataProvider.__manifest__["serviceName"]} Unreachable', 'DeskScout cannot provide alerts']

					newToast.audio = ToastAudio(Path(os.path.abspath(os.path.join(os.getcwd(),'../assets/sounds/attention.wav'))),silent=True)
					PlaySoundW(PWSTR(os.path.join(os.getcwd(),'../assets/sounds/attention.wav')), None, SND_FILENAME | SND_ASYNC)
					serviceConnected = False
					toaster.clear_toasts()
					toaster.show_toast(newToast)
			else:
				if time.time()-serviceDisconnectedAt > 59:
					newToast = Toast()
					newToast.text_fields = [f'{GlucoseDataProvider.__manifest__["serviceName"]} Unreachable', 'DeskScout cannot provide alerts']

					if bulb:
						bulb.title = "DeskScout\nApplication Offline"

					newToast.audio = ToastAudio(Path(os.path.abspath(os.path.join(os.getcwd(),'../assets/sounds/attention.wav'))),silent=True)
					PlaySoundW(PWSTR(os.path.join(os.getcwd(),'../assets/sounds/attention.wav')), None, SND_FILENAME | SND_ASYNC)
					toaster.clear_toasts()
					
					toaster.show_toast(newToast)
					serviceDisconnectedAt = time.time()
		time.sleep(1)
		serverStatusInit = True

nametable = {
	"urgentLow":"Urgent Low",
	"urgentLowSoon":"Urgent Low Soon",
	"low":"Low",
	"high":"High",
	"risingFast":"Rising Fast",
	"fallingFast":"Falling Fast silenced",

}
def cap(num,_max):
	if num > _max:
		return _max
	return num
def notificationRespone(activatedEventArgs):
	resp = activatedEventArgs.arguments.split(".")
	settings = json.load(open("../data/settings.json"))

	if resp[0] == "silence":
		silence[resp[1]] = time.time()
		PlaySoundW(None, None, SND_PURGE)
		toast = Toast([f"{nametable[resp[1]]} Alert Silenced",f"You will not recieve another alert for {settings['notify'][resp[1]]['silence']/60} minutes"])
		toast.audio = ToastAudio(Path(""),silent=True)
		toaster.show_toast(toast)
		PlaySoundW(PWSTR('../assets/sounds/generic.wav'), None, SND_FILENAME | SND_ASYNC)

def remove_duplicates(items):
	seen = set()
	unique = []
	for item in items:
		if item not in seen:
			seen.add(item)
			unique.append(item)
	return unique
def nightscoutUplodader():
	nut = -1
	from mods import nightscout
	while True:
		settings = json.load(open("../data/settings.json"))

		if settings['ns']['enabled']:
			ns = nightscout.NightScout()
			if settings['ns']['delay'] == 0:
				pass
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
def recordAccessHandler():
	# Nope for now
	log.sync.info(f"Starting sync thread")
	lastSync = 0
	grec = None
	records = []
	log.sync.info(f"Sync thread started")

	while True:
		time.sleep(15)
		log.sync.info("Sync process started")
		try:
			settings = json.load(open("../data/settings.json"))
		except:
			log.sync.error("Failed to load settings")
			continue
		records = []

		if GlucoseDataProvider:
			if serviceConnected and not serviceOffline:
				if os.path.exists(os.path.abspath("../data/glucose.gdr")):
					try:
						if settings['gdrState'] != 1:
							log.sync.warning("Sync process failed, glucose data record not setup")

							continue
						log.sync.info("Loading large glucose record file")
						grec = gdr.RecordAccess(os.path.abspath("../data/glucose.gdr"))
							
					except Exception as e:
						grec = None
						rec = None
						log.sync.error(f"Error while loading large glucose record file {str(e)}")
						log.sync.warning("Sync process failed")
						time.sleep(5)
						continue

					try:
						print("Retreiving last record time")
						x = grec.getLastRecordTime()
						reading = GlucoseDataProvider.getLatestGlucoseReading()
						print("LASTRT",x,int(reading.timestamp))
						if x:
							if x < int(reading.timestamp):
								print("Syncing",x,reading.timestamp)
								log.sync.info("Data available to sync, gathering data")
								time.sleep(5)
								records1 = GlucoseDataProvider.getAllReadings()
								for i in records1:
									if int(i.timestamp) > x:
										records.append(i)
							
							else:
								log.sync.info("No data available to sync")
								log.sync.info("Sync process complete")
								records = []
						else:
							records1 = GlucoseDataProvider.getAllReadings()
							for i in records1:
								if i.timestamp > x:
									records.append(i)
						records.reverse()
						log.sync.info(f"Found {len(records)} data points to sync,writing data")

						print("Data Collected, Writing",len(records))

						for i in records:
							#print(i)
			
							#print("rec",time.localtime(i.timestamp),time.strftime('%Y%m%d',time.localtime(i.timestamp)))
							
							grec.writeRecord(i.timestamp,i.value,DEXCOM_TREND_DIRECTIONS[i.trend])
							if not (f"{time.strftime('%Y-%m-%d',time.localtime(i.timestamp/1000))}.gdr" in os.listdir("../data/glucose/daily")):
								rec = gdr.createRecordFile(f"../data/glucose/daily/{time.strftime('%Y-%m-%d',time.localtime(i.timestamp/1000))}.gdr")
							rec = gdr.RecordAccess(f"../data/glucose/daily/{time.strftime('%Y-%m-%d',time.localtime(i.timestamp/1000))}.gdr")
							rec.writeRecord(i.timestamp,i.value,DEXCOM_TREND_DIRECTIONS[i.trend])
							rec.file.close()
						log.sync.info("Sync complete")

					except Exception as e:
						log.sync.error(f"Sync failed with exception {str(e)}")

			else:
				log.sync.warning("Sync failed, glucose data provider is offline")
			for i in recordQueue:
				if i[0] == "delete":
					ts = hours_to_utc_minute_timestamps(i[1])
					for i in ts:
						print("del",rec.deleteRecordByTime(ts))
					i[2] = True
		else:
			log.sync.warning("Sync failed, glucose data provider is not availiable")




def notificationRunner():
	global rec,currentAlarmState,settings
	import re
	last = None
	def checkForUrgentLow():
		if settings['notify']['urgentLow']['enabled']:

			if reading.value <= settings['notify']['urgentLow']['level']:
				currentAlarmState = "urgentLow"
				if silence['urgentLow']:
					if time.time()-silence['urgentLow'] >= settings['notify']['urgentLow']['silence']:
						silence['urgentLow'] = None
				if silence['urgentLow'] == None:
					newToast = Toast(['DeskScout',"Urgent Low Glucose",f"Your glucose is {reading.value} mg/dl"],duration=ToastDuration.Long)
					newToast.AddAction(ToastButton('OK', 'silence.urgentLow'))
					newToast.on_activated = notificationRespone
					newToast.audio = ToastAudio(Path(os.path.abspath(os.path.join(os.getcwd(),'../assets/sounds/attention.wav'))),silent=True)
					toaster.clear_toasts()
					toaster.show_toast(newToast)
					notified['urgentLow'] = True
					if settings['notify']['urgentLow']['soundOn']:
						PlaySoundW(PWSTR(settings['notify']['urgentLow']['sound']), None, SND_FILENAME)
				return True
						
			else:
				silence['urgentLow'] = None
		return False
	f = str({})
	while True:
		time.sleep(5)
		
		
		if not GlucoseDataProvider:
			continue
		if GlucoseDataProvider.getAuthStatus() == SDK.gdp.AuthenticationState.AUTHED and serviceConnected and not serviceOffline:
			log.notifier.info("Checking glucose")
			try:
				settings = json.load(open("../data/settings.json"))
			except:
				log.notifier.warning("Couldn't load settings,stopped")
				continue
			if str(settings) != f:
				f = str(settings)
				last = 0


			
			try:
				reading = GlucoseDataProvider.getLatestGlucoseReading()
			except:
				continue
			lost = None
			if not reading:
				log.notifier.info("No reading available")
				print("No Data Available")
				continue
			glucose = reading.value
			if not settings["useMGDL"]:
				glucose = round(glucose/18,1)
			

			bulb.title = f"DeskScout\nYour glucose: {glucose}{'mg/dl' if settings['useMGDL'] else 'mmol/L'} {reading.trend_description}\nLast reading at: {time.ctime(reading.timestamp/1000)}"
			if settings['enableNotify']:
				if GlucoseDataProvider.getAuthStatus() == SDK.gdp.AuthenticationState.AUTHED and serviceConnected and not serviceOffline:

					reading = GlucoseDataProvider.getLatestGlucoseReading()
					#Check for urgent low
					if reading.timestamp == last:
						continue
					else:
						last = reading.timestamp
					if checkForUrgentLow() == False:
						if reading.value >= settings['notify']['low']['level'] and reading.value <= settings['notify']['high']['level']:
							currentAlarmState = None
						if settings['notify']['low']['enabled']:
							
							
							if reading.value <= settings['notify']['low']['level']:
								currentAlarmState = "low"
								if silence['low']:
									if time.time()-silence['low'] >= settings['notify']['low']['silence']:
										silence['low'] = None
								if silence['low'] == None:
									newToast = Toast(['DeskScout',"Low Glucose",f"Your glucose is {reading.value} mg/dl"],duration=ToastDuration.Long)
									newToast.AddAction(ToastButton('OK', 'silence.low'))
									newToast.on_activated = notificationRespone
									newToast.audio = ToastAudio(Path(os.path.abspath(os.path.join(os.getcwd(),'../assets/sounds/attention.wav'))),silent=True)
									toaster.show_toast(newToast)
									notified['low'] = True
									if settings['notify']['low']['soundOn']:
										PlaySoundW(PWSTR(settings['notify']['low']['sound']), None, SND_FILENAME)
							else:
								silence['low'] = None
					if settings['notify']['high']['enabled']:
						
						
						if reading.value >= settings['notify']['high']['level']:
							currentAlarmState = "high"
							if silence['high']:
								if time.time()-silence['high'] >= settings['notify']['high']['silence']:
									silence['high'] = None
							if silence['high'] == None:
								newToast = Toast(['DeskScout',"High Glucose",f"Your glucose is {reading.value} mg/dl"],duration=ToastDuration.Long)
								newToast.AddAction(ToastButton('OK', 'silence.high'))
								newToast.on_activated = notificationRespone
								newToast.audio = ToastAudio(Path(os.path.abspath(os.path.join(os.getcwd(),'../assets/sounds/attention.wav'))),silent=True)
								toaster.show_toast(newToast)
								notified['high'] = True
								if settings['notify']['high']['soundOn']:
									PlaySoundW(PWSTR(settings['notify']['high']['sound']), None, SND_FILENAME)
						else:
							silence['high'] = None
					if settings['notify']['fallingFast']['enabled']:
						if reading.value >= settings['notify']['fallingFast']['level']:
							#1,2,6,7
							if DEXCOM_TREND_DIRECTIONS[reading.trend] == (6 if settings['notify']['fallingFast']['arrow'] == 'one' else 7) :
								currentAlarmState = "fallingFast"

								if silence['fallingFast']:
									if time.time()-silence['fallingFast'] >= settings['notify']['fallingFast']['silence']:
										silence['fallingFast'] = None
								if silence['low'] == None:
									newToast = Toast(['DeskScout',f"Falling Fast-{reading.value if settings['useMGDL'] else round(reading.value/18,1)} {'mg/dl' if settings['useMGDL'] else 'mmol/L'}",f"Your glucose is falling fast at {'2-3 mg/dl' if settings['notify']['risingFast']['arrow']=="one" else '3+ mg/dl'}"],duration=ToastDuration.Long)
									newToast.AddAction(ToastButton('OK', 'silence.fallingFast'))
									newToast.on_activated = notificationRespone
									newToast.audio = ToastAudio(Path(os.path.abspath(os.path.join(os.getcwd(),'../assets/sounds/attention.wav'))),silent=True)
									toaster.show_toast(newToast)
									notified['fallingFast'] = True
									if settings['notify']['fallingFast']['soundOn']:
										PlaySoundW(PWSTR(settings['notify']['fallingFast']['sound']), None, SND_FILENAME)
					if settings['notify']['risingFast']['enabled']:
						if reading.value >= settings['notify']['risingFast']['level']:
							if DEXCOM_TREND_DIRECTIONS[reading.trend] == (2 if settings['notify']['risingFast']['arrow'] == 'one' else 1) :
								currentAlarmState = "risingFast"
								
								if silence['risingFast']:
									if time.time()-silence['risingFast'] >= settings['notify']['risingFast']['silence']:
										silence['risingFast'] = None
								if silence['low'] == None:
									newToast = Toast(['DeskScout',f"Rising Fast - {reading.value if settings['useMGDL'] else round(reading.value/18,1)} {'mg/dl' if settings['useMGDL'] else 'mmol/L'}",f"Your glucose is rising fast at {'2-3 mg/dl' if settings['notify']['risingFast']['arrow']=="one" else '3+ mg/dl'}"],duration=ToastDuration.Long)
									newToast.AddAction(ToastButton('OK', 'silence.risingFast'))
									newToast.on_activated = notificationRespone
									newToast.audio = ToastAudio(Path(os.path.abspath(os.path.join(os.getcwd(),'../assets/sounds/attention.wav'))),silent=True)
									toaster.show_toast(newToast)
									notified['fallingFast'] = True
									if settings['notify']['fallingFast']['soundOn']:
										PlaySoundW(PWSTR(settings['notify']['risingFast']['sound']), None, SND_FILENAME)
					
updateStatus = {
	"status":"ready",
	"result":"ok",
	"isUpToDate":True,
	"progress":0,
	"manifest":None
}
def updateDownloadThread():
	log.updater.info("Update download requested")
	print("Update Download Thread started")
	updateStatus['status'] = "dc"
	log.updater.info("Checking download version")

	print("Checking download version")
	try:
		
		
		resp = requests.get(f"{UPDATE_URL}/information.json")
	except Exception as e:
		log.updater.error(f"Failed to check latest version: {str(e)}")
		updateStatus['status'] = 'ready'
		updateStatus['result'] = "dc_failed"
		return
	try:
		myversioninfo = json.load(open('versioninfo.json'))
		versioninfo = json.loads(resp.text)
	except Exception as e:
		log.updater.error(f"Failed to check latest version: {str(e)}")
		updateStatus['status'] = 'ready'
		updateStatus['result'] = "dc_failed"
		return
	try:
		latest = versioninfo['upgradeLock'][sys.platform]['official-alpha'][str(myversioninfo['app'])]
	except Exception as e:
		log.updater.error(f"Failed to check latest version: {str(e)}")
		updateStatus['status'] = 'ready'
		updateStatus['result'] = "dc_failed"
		return
	try:
		if latest == myversioninfo['client']:
			updateStatus["isUpToDate"] = True
			updateStatus['result'] = "update_not_needed"
			updateStatus['status'] = 'ready'
			print("Up to date")
			log.updater.info("Update not needed")
		else:
			print("Preparing update download")
			log.updater.info(f"Preparing update download")
			updateStatus["isUpToDate"] = False
			updateStatus["manifest"] = versioninfo['build'][sys.platform][str(latest)]
			updateStatus["manifest"]['build'] = latest
			updateStatus['result'] = "ok"
			updateStatus['status'] = 'dr'
			try:
				log.updater.info("Requesting download")
				from urllib import request
				resp = requests.get(versioninfo['build'][sys.platform][str(latest)]['url'])

			except Exception as e:
				log.updater.error(f"Download request failed: {str(e)}")

				updateStatus['status'] = "ready"
				updateStatus['result'] = "dr_failed"
				print("DRQ failed")
				return
			try:
				updateStatus['status'] = 'download'
				log.updater.info("Downloading update")
				update = bytes(resp.content)
				total = len(update)
				print("TD",total)
				consumed = 0
				file = open("../data/.update.zip",'wb+')
				from itertools import batched
				import io
				chunk_size = 8

				# batched yields tuples of integers (the byte values)
				# so we join them back into bytes objects
				chunks = [bytes(chunk) for chunk in batched(update, chunk_size)]
				for i in chunks:
					#print("Writing",file.tell())
					#log.updater.info(f"Downloading {file.tell()+1}/{total} bytes")
					updateStatus['status'] = 'download'

					file.write(i)

					updateStatus['progress'] = int((file.tell()/total)*100)
				file.close()

				os.rename("../data/.update.zip","../data/update.zip")
				updateStatus['status'] = 'ready'
				updateStatus['result'] = "installReady"
				print("Download Complete")
				log.updater.info("Download Complete")
				newToast = Toast(['DeskScout',"Update Downloaded","DeskScout will install updates on next launch."])
				newToast.audio = ToastAudio(Path(os.path.abspath(os.path.join(os.getcwd(),'../assets/sounds/attention.wav'))),silent=True)
				toaster.show_toast(newToast)
				PlaySoundW(PWSTR(os.path.abspath("../assets/sounds/generic.wav")), None, SND_FILENAME)
			except Exception as e:
				updateStatus['status'] = "ready"
				updateStatus['result'] = "download_failed"
				print("Download Failed",e)
				log.updater.error(f"Download failed: {str(e)}")

				return
	except Exception as e:
		log.updater.error(f"Failed to update: {str(e)}")
		updateStatus['status'] = 'ready'
		updateStatus['result'] = "download_failed"
		return


			
def updateCheckThread():
	log.updater.info("Update check requested")
	if "update.zip" in os.listdir("../data"):
		log.updater.info("Found install media")

		if updateStatus['status'] == "ready":
			log.updater.info("Install ready")

			updateStatus['status'] = 'ready'
			updateStatus['result'] = "installReady"
			return
	updateStatus['status'] = "cfu"
	try:
		log.updater.info("Checking for update")

		resp = requests.get(f"{UPDATE_URL}/information.json?time={time.time()}")
	except Exception as e:
		updateStatus['status'] = 'ready'
		updateStatus['result'] = "cfu_failed"
		log.updater.error(f"Checking for update failed with {str(e)}")

		return
	myversioninfo = json.load(open('versioninfo.json'))
	versioninfo = json.loads(resp.text)
	print(versioninfo)
	latest = versioninfo['upgradeLock'][sys.platform]['official-alpha'][str(myversioninfo['app'])]
	log.updater.info(f"Latest version is {latest} current installed {myversioninfo['app']}")
	if latest == myversioninfo['app']:
		updateStatus["isUpToDate"] = True
		updateStatus['result'] = "ok"
		updateStatus['status'] = 'ready'
		updateStatus['vinfo'] = versioninfo
		print("Up to date")
		log.updater.info("Up to date")


	else:
		if updateStatus['isUpToDate']:
			newToast = Toast(['DeskScout',"Update Available",f"{versioninfo['build'][sys.platform][str(latest)]['name']} is available"])
			newToast.audio = ToastAudio(Path(os.path.abspath(os.path.join(os.getcwd(),'../assets/sounds/attention.wav'))),silent=True)
			toaster.show_toast(newToast)
			PlaySoundW(PWSTR(os.path.abspath("../assets/sounds/update_available.wav")), None, SND_FILENAME | SND_ASYNC)
		log.updater.info(f"Update available to: {latest}")

		updateStatus["isUpToDate"] = False
		updateStatus["manifest"] = versioninfo['build'][sys.platform][str(latest)]
		
		updateStatus["manifest"]['build'] = latest
		json.dump(updateStatus["manifest"],open("updatemanifest.json",'w+'))
		updateStatus['result'] = "ok"
		updateStatus['status'] = 'ready'
		updateStatus['vinfo'] = versioninfo

		print("Update avialable")
	
	
import ctypes
from windows_toasts import InteractableWindowsToaster, Toast, ToastActivatedEventArgs, ToastButton


@route('/')
def index():
	return "OK"
@route('/shutdown')
def index():
	log.main.info("Shutdown requested via external")
	PlaySoundW(PWSTR(os.path.join(os.getcwd(),'../assets/sounds/shutdown.wav')), None, SND_FILENAME)
	p = psutil.Process(os.getpid())
	for proc in p.children(recursive=True):
		proc.kill()
	p.kill()
	exit(0)
@route('/clearUpdateStatusError')
def ccus():
	if updateStatus['result'] in ['cfu_error',"download_error"]:
		updateStatus['result'] = "ok"
	return "ok"
@route('/checkForUpdate')
def runCFU():
	log.main.info("Update check requested")

	_thread.start_new_thread(updateCheckThread,())
	return "ok"
@route('/downloadUpdate')
def runDU():
	log.main.info("Update download requested")

	_thread.start_new_thread(updateDownloadThread,())
	return "ok"
@route('/getUpdateStatus')
def getUpdateStatus():
	return json.dumps(updateStatus)
@route('/factoryReset')
def index():
	log.main.warning("Factory Reset is a Deprecated method")

	global bulb,account,serviceConnected
	import shutil
	account = None
	serviceConnected = False
	shutil.copy("../data/default_settings.json","../data/settings.json")
	
	shutil.rmtree("../data/glucose/")
	os.mkdir("../data/glucose")
	os.mkdir("../data/glucose/daily")

	
	bulb.title = "DeskScout"
	return json.dumps({"status":"ok"})

@route('/authenticate')
def auth():

	log.main.info("Authentication requested")

	global account,serviceConnected,serviceOffline
	

	settings = json.load(open("../data/settings.json"))
	pw = keyring.get_password("com.sedwards.deskscout",settings['username'])
	try:
		if GlucoseDataProvider.getAuthStatus() != 0x03:
			GlucoseDataProvider.login(settings['username'],pw)
		if GlucoseDataProvider.getAuthStatus() == 0x03:
			
			serviceConnected = True
			serviceOffline = False
			newToast = Toast()
			newToast.text_fields = [f'{GlucoseDataProvider.__manifest__['serviceName']} Connected', 'DeskScout is now receiving data and is able to provide alerts.']
			newToast.audio = ToastAudio(Path(os.path.abspath(os.path.join(os.getcwd(),'../assets/sounds/attention.wav'))),silent=True)
			PlaySoundW(PWSTR(os.path.join(os.getcwd(),'../assets/sounds/connected.wav')), None, SND_FILENAME | SND_ASYNC)
			toaster.clear_toasts()
			
			toaster.show_toast(newToast)
			log.gdp.info(f"Service is authenticated {GlucoseDataProvider.__manifest__['serviceName']}")
		log.main.info("Authentication successful")
		import time
		return json.dumps({"status":"ok"})
	except Exception as e:
		print("NAXC",e)
		bulb.title = "DeskScout"

		serviceConnected = False

		account = None
		return json.dumps({"status":"error"})
@route('/getStatus')
def getStatus():
	global serviceConnected,serviceDisconnectedAt
	if serviceOffline and serviceConnected:
		newToast = Toast()
		newToast.text_fields = [f'{GlucoseDataProvider.__manifest__['serviceName']} Disconnected', 'DeskScout cannot provide alerts']
		newToast.audio = ToastAudio(Path(os.path.abspath(os.path.join(os.getcwd(),'../assets/sounds/attention.wav'))),silent=True)
		PlaySoundW(PWSTR(os.path.join(os.getcwd(),'../assets/sounds/attention.wav')), None, SND_FILENAME | SND_ASYNC)
		serviceConnected = False
		loginState = 'offline'
		toaster.clear_toasts()

		toaster.show_toast(newToast)
		return json.dumps({"status":"ok","login_state":"offline"})
	if serviceOffline and serviceDisconnectedAt == 0:
		newToast = Toast()
		newToast.text_fields = [f'{GlucoseDataProvider.__manifest__['serviceName']} Disconnected', 'DeskScout cannot provide alerts']
		newToast.audio = ToastAudio(Path(os.path.abspath(os.path.join(os.getcwd(),'../assets/sounds/attention.wav'))),silent=True)
		
		serviceConnected = False
		loginState = False
		toaster.clear_toasts()
		PlaySoundW(PWSTR(os.path.join(os.getcwd(),'../assets/sounds/attention.wav')), None, SND_FILENAME | SND_ASYNC)
		toaster.show_toast(newToast)
		serviceDisconnectedAt = time.time()
		return json.dumps({"status":"ok","login_state":"offline"})


	try:
		settings = json.load(open("../data/settings.json"))
		pw = keyring.get_password("com.sedwards.deskscout",settings['username'])
		
		if GlucoseDataProvider.getAuthStatus() == SDK.gdp.AuthenticationState.AUTHED:
			loginState = True
		elif pw == "":
			loginState = 'unknown'
			serviceConnected = False

		else:
			loginState = False


	except:
		pw = keyring.get_password("com.sedwards.deskscout",settings['username'])
		if pw == "":
			loginState = 'unknown'
			serviceConnected = False
		else:
			loginState = False
			if serviceOffline:
				loginState = "offline"


	try:
		
		return json.dumps({"status":"ok","login_state":loginState })
	except:
		return json.dumps({"status":"ok","login_state":"unknown"})
@route('/getAlarmStatus')
def getAlarmStatus():
	return json.dumps({"status":"ok","data":currentAlarmState})

@route('/getLatestReading')
def getLReading():
	global serviceConnected
	try:
		data = GlucoseDataProvider.getLatestGlucoseReading()
		if data:
			return json.dumps({"status":"ok","data":data.json})
	except Exception as e:
		log.gdp.error(f"Error while getting glucose {str(e)}")
		if serviceConnected:
			toaster = WindowsToaster('DeskScout')
			newToast = Toast()
			newToast.text_fields = ['Dexcom Share Disconnected', 'DeskScout cannot provide alerts']
			newToast.audio = ToastAudio(Path(os.path.abspath(os.path.join(os.getcwd(),'../assets/sounds/attention.wav'))),silent=True)
			PlaySoundW(PWSTR(os.path.join(os.getcwd(),'../assets/sounds/attention.wav')), None, SND_FILENAME | SND_ASYNC)
		serviceConnected = False
		return json.dumps({"status":"Error"})
@route('/setupGDP')
def initializeGDP():
	log.main.info("GDP setup requested")
	GlucoseDataProvider.setup()
	log.main.info("GDP complete")

	return json.dumps({"status":"ok"})
@route('/getCurrentReading')
def getCReading():
	data = GlucoseDataProvider.getLatestGlucoseReading()
	if data:
		return json.dumps({"status":"ok","data":data.json})
@route('/putIntent',method=["POST"])
def putIntent():
	global intent
	log.main.info("Application intent set")

	intent = request.forms['intent']
	return json.dumps({"status":"ok"})
@route('/getIntent')
def getIntent():
	global intent
	

	if intent:
		ix = intent
		intent = None
		log.main.info("Application intent retrieved")
		return json.dumps({"status":"ok","data":ix})
	
	else:
		return json.dumps({"status":"ok","data":None})


@route('/deleteRecords',method=["POST"])
def deleteRecords(self):
	data = request.forms
	if data['hours'] != "all":
		recordQueue.append(["delete_hours",data['hours'],0])
		while recordQueue[len(recordQueue)][2] == 0:
			pass
		return json.dumps({"status":"done"})
@route("/reloadExts")
def reloadExtensions():
	loadGlucoseDataProvider()
	return json.dumps({"status":"ok","data":{}})
@route("/initializeGDR")
def inadgr():
	log.main.info("Glucose data record initialization requested")

	if not "glucose.gdr" in os.listdir("../data"):
		gdr.createRecordFile("../data/glucose.gdr")
		log.main.info("Glucose data record initialized")
	else:
		log.main.warning("Glucose data record already exists")



	return json.dumps({"status":"ok","data":{}})
@route("/extInfo")
def getExtInfo():
	result = []
	exts = os.listdir("../data/extensions")
	for ext in exts:
		if os.path.exists(f"../data/extensions/{ext}/manifest.json"):
			try:
				result.append(json.load(open(f"../data/extensions/{ext}/manifest.json")))
			except:
				pass
	return json.dumps({"status":"ok","data":result})
@route('/settings',method=["POST"])
def updateSettings():
	data = request.forms
	
	
	if data['action'] == 'get':
		settings = json.load(open("../data/settings.json"))
		path = "settings"
		for _ in data['path'].split("/"): path += f'["{_}"]'
		try:
			res = eval(path)
			return json.dumps({
				"status":"OK",
				"data":res
			})
		except:
			return json.dumps({"status":"Error"})
	if data['action'] == 'set':
		settings = json.load(open("../data/settings.json"))
		path = "settings"
		log.main.info(f"Setting at path {data['path']} requested change")
		for _ in data['path'].split("/"): path += f'["{_}"]'
		path += f"= {data['value']}"
		
		try:
			exec(path)
			json.dump(settings,open("../data/settings.json",'w+'))
			return json.dumps({
				"status":"OK"
			})
		except Exception as e:
			print(e,path)
			log.main.warning(f"Setting at path {data['path']} failed to change {str(e)}")

			return json.dumps({"status":"Error"})
@route("/about")
def about():
	return json.dumps({
		"version":__version__,
		"build":__build__,
		"channel":__channel__,
		"release":__release__
		
	})
bulb = None
log.main.info("Starting Service")
newToast = Toast()
newToast.text_fields = ['DeskScout is starting', 'Glucose alerts should be available soon.']
newToast.audio = ToastAudio(Path(os.path.abspath(os.path.join(os.getcwd(),'../assets/sounds/generic.wav'))),silent=True)
PlaySoundW(PWSTR(os.path.join(os.getcwd(),'../assets/sounds/generic.wav')), None, SND_FILENAME | SND_ASYNC)
toaster.clear_toasts()
toaster.show_toast(newToast)
try:
	log.main.info("Loading the glucose provier")
	loadGlucoseDataProvider()
except:
	newToast = Toast()
	newToast.text_fields = ['Issue with Glucose Data Provider', 'Glucose data provider failed to initialize.']
	newToast.audio = ToastAudio(Path(os.path.abspath(os.path.join(os.getcwd(),'../assets/sounds/generic.wav'))),silent=True)
	PlaySoundW(PWSTR(os.path.join(os.getcwd(),'../assets/sounds/attention.wav')), None, SND_FILENAME | SND_ASYNC)
	toaster.clear_toasts()
	toaster.show_toast(newToast)
log.main.info("Starting server status checker")
_thread.start_new_thread(serverstatus,())
log.main.info("Starting server notification host")
_thread.start_new_thread(notificationRunner,())
log.main.info("Starting server record access handler")
_thread.start_new_thread(recordAccessHandler,())

def runtime(internal):
	global bulb
	bulb = internal
	internal.visible = True
	print(internal)
	import subprocess
	if not Flags.DISABLE_OVERLAY:
		log.main.info("Starting overlay service")

		subprocess.Popen("py DeskScoutOverlay.py",shell=True)
		subprocess.Popen("py DeskScout-DiscordRichPresence.py",shell=True)

	run(host='127.0.0.1', port=49152)
	bulb.stop()
from PIL import Image
from pystray import Icon, Menu as menu, MenuItem as item
state = False
def attemptConnect():
	global account,serviceConnected,attemptingConnection
	log.main.info("attemptConnect: Requesting re-authenticaton")

	attemptingConnection = True
	import time
	try:
		requests.get("http://127.0.0.1:49152/authenticate",timeout=300)
		log.main.info("attemptConnect: Request sent")
	except Exception as e:
		attemptingConnection = False
		log.main.warning("attemptConnect: Failed to request authentication")
		raise e

def shutdown(icon, item):
	log.main.info("Shutdown invoked via tray icon")
	PlaySoundW(PWSTR(os.path.join(os.getcwd(),'../assets/sounds/shutdown.wav')), None, SND_FILENAME)
	log.main.info("Exiting")

	p = psutil.Process(os.getpid())
	for proc in p.children(recursive=True):
		proc.kill()
	p.kill()
	exit(0)
def restart(icon, item):
	log.main.info("Restart invoked via tray icon")
	subprocess.Popen("pyw restart.py",shell=True,start_new_session=True)
	bulb.visible = False

def openbackup(icon,item):
	pass

icon = Icon(
	'DeskScout',
	icon=Image.open("../assets/icons/logo/03.png"),
	
	menu=menu(
		item(
		'Refresh Connections',
		lambda icon,item:attemptConnect()),
		item(
		'Refresh Data Provider',
		lambda icon,item:loadGlucoseDataProvider()),
		item(
		'Restart Service',
		restart),
		item(
		'Shutdown Deskscout',
		shutdown),
	),
	title="DeskScout"
	)

icon.run(runtime)