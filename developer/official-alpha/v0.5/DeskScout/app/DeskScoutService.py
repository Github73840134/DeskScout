# DeskScout Service
# Author: Seth Edwards
#DeskScout service pulls information from clarity
import os,sys,json
os.chdir(os.path.dirname(__file__))
sys.path.append(os.path.join(os.getcwd(),'libs'))
sys.path.append(os.path.join(os.getcwd(),'mods'))

from bottle import route, run, template,request,post
from pydexcom import Dexcom
import pydexcom
import keyring,psutil, subprocess
from windows_toasts import Toast, ToastAudio, WindowsToaster,InteractableWindowsToaster,ToastDuration
from pathlib import Path
from win32more.Windows.Win32.Media.Audio import PlaySoundW, SND_FILENAME, SND_ASYNC, SND_PURGE
from win32more.Windows.Win32.Foundation import PWSTR
import time
import requests,_thread,json,logging
from tkinter import messagebox
class DeltaTimeFormatter(logging.Formatter):
	def format(self, record):
		record.delta = time.time()-ast
		return super().format(record)
handler = logging.StreamHandler(open("netlogs/service.log","w"))
LOGFORMAT = '+%(asctime)s [%(delta)s] %(name)s %(levelname)s: %(message)s'
fmt = DeltaTimeFormatter(LOGFORMAT)
handler.setFormatter(fmt)
logging.basicConfig(
					format='%(asctime)s [%(delta)s] %(levelname)-9s: %(message)s',
					datefmt='%Y-%m-%d %H:%M:%S',
					handlers=[handler],
					level=logging.DEBUG)
ast = time.time()
class netlog:
	notifier = logging.getLogger("notifier")
	main = logging.getLogger("main")
	status = logging.getLogger("status")
	sync = logging.getLogger("deskscout_sync")
	nsync = logging.getLogger("nightscout_sync")
account = None
serviceConnected = False
serviceDisconnectedAt = 0
from mods import gdr
__version__ = "4"
__build__ = 13
__channel__ = "developer"
__release__ = "alpha"
rec = None
try:
	

	print("Checking if service is already running")
	resp = requests.get("http://127.0.0.1:49152/about")
	if len(sys.argv) > 1:
		if sys.argv[1] == "fromDeskscoutPy":
			exit(0)
	try:
		ver = json.loads(resp.text)
		if ver['build'] != __build__:
			ans = messagebox.askyesno("DeskScout Service","An newer/older version of service is already running, would you like to stop the old service and start the new one?")
			if ans:
				try:
					requests.get("http://127.0.0.1:49152/shutdown")
				except:
					pass
			else:
				p = psutil.Process(os.getpid())
				for proc in p.children(recursive=True):
					proc.kill()
				p.kill()
		else:
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
	pass
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
recordQueue = []
serviceOffline = True
toaster = InteractableWindowsToaster('DeskScout')

def serverstatus():
	global serviceOffline,serviceConnected,serviceDisconnectedAt,account
	while True:
		try:
			netlog.status.info(f"Requesting url: https://share2.dexcom.com/ShareWebServices/Services/General/AuthenticatePublisherAccount")
			resp = requests.get("https://share2.dexcom.com/ShareWebServices/Services/General/AuthenticatePublisherAccount",timeout=5)
			if resp.status_code != 405:
				if not serviceOffline:
					serviceOffline = True
					serviceDisconnectedAt = time.time()

					if serviceConnected:
						serviceDisconnectedAt = 0
						if bulb:
							bulb.title = "DeskScout\nApplication Offline"

						newToast = Toast()
						newToast.text_fields = ['Dexcom Share Unreachable', 'DeskScout cannot provide alerts']
						newToast.audio = ToastAudio(Path(os.path.abspath(os.path.join(os.getcwd(),'../assets/sounds/attention.wav'))),silent=True)
						PlaySoundW(PWSTR(os.path.join(os.getcwd(),'../assets/sounds/attention.wav')), None, SND_FILENAME | SND_ASYNC)
						serviceConnected = False
						toaster.show_toast(newToast)
				else:
					if time.time()-serviceDisconnectedAt > 59:
						if bulb:
							bulb.title = "DeskScout\nApplication Offline"

						newToast = Toast()
						newToast.text_fields = ['Dexcom Share Unreachable', 'DeskScout cannot provide alerts']
						newToast.audio = ToastAudio(Path(os.path.abspath(os.path.join(os.getcwd(),'../assets/sounds/attention.wav'))),silent=True)
						PlaySoundW(PWSTR(os.path.join(os.getcwd(),'../assets/sounds/attention.wav')), None, SND_FILENAME | SND_ASYNC)
						toaster.show_toast(newToast)
						serviceDisconnectedAt = time.time()
			else:
				if serviceOffline:
					account = None
					newToast = Toast()
					serviceDisconnectedAt = time.time()
					serviceOffline = False 
					serviceDisconnectedAt = 0
					_thread.start_new_thread(attemptConnect,())
		except:
			print("ERTS")
			if not serviceOffline:
				serviceOffline = True
				serviceDisconnectedAt = time.time()

				if serviceConnected:
					serviceDisconnectedAt = 0
					newToast = Toast()
					if bulb:
						bulb.title = "DeskScout\nApplication Offline"

					newToast.text_fields = ['Dexcom Share Unreachable', 'DeskScout cannot provide alerts']
					newToast.audio = ToastAudio(Path(os.path.abspath(os.path.join(os.getcwd(),'../assets/sounds/attention.wav'))),silent=True)
					PlaySoundW(PWSTR(os.path.join(os.getcwd(),'../assets/sounds/attention.wav')), None, SND_FILENAME | SND_ASYNC)
					serviceConnected = False
					toaster.clear_toasts()
					toaster.show_toast(newToast)
			else:
				if time.time()-serviceDisconnectedAt > 59:
					newToast = Toast()
					newToast.text_fields = ['Dexcom Share Unreachable', 'DeskScout cannot provide alerts']
					if bulb:
						bulb.title = "DeskScout\nApplication Offline"

					newToast.audio = ToastAudio(Path(os.path.abspath(os.path.join(os.getcwd(),'../assets/sounds/attention.wav'))),silent=True)
					PlaySoundW(PWSTR(os.path.join(os.getcwd(),'../assets/sounds/attention.wav')), None, SND_FILENAME | SND_ASYNC)
					toaster.clear_toasts()
					
					toaster.show_toast(newToast)
					serviceDisconnectedAt = time.time()
		time.sleep(1)

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

def recordAccessHandler():
	lastSync = 0
	grec = None
	while True:
		time.sleep(5)
		settings = json.load(open("../data/settings.json"))

		if account:
			if os.path.exists(os.path.abspath("../data/glucose.gdr")):
				try:
					if settings['gdrState'] != 1:
						continue
					if grec == None:
						grec = gdr.RecordAccess(os.path.abspath("../data/glucose.gdr"))
						
				except Exception as e:
					grec = None
					rec = None
					print("ER",e)
					time.sleep(5)
					continue

				try:
					x = grec.getLastRecordTime()
					reading = account.get_latest_glucose_reading()
					print(x,reading.datetime.timestamp()*1000)
					if x:
						if x < int(reading.datetime.timestamp()*1000):
							print("Syncing")
							if int((int(reading.datetime.timestamp())-(x/1000))/60) != 4:
								records = account.get_glucose_readings(cap(int((int(reading.datetime.timestamp())-(x/1000))/60),1140),cap(int(int((int(reading.datetime.timestamp())-(x/1000))/60)/5),288))
							else:
								records = account.get_glucose_readings(5,1)
						else:
							print("No Sync needed")
							records = []
					else:
						records = account.get_glucose_readings(1440,288)
					records.reverse()
					records = remove_duplicates(records)
					for i in records:
						print("rec",time.localtime(i.datetime.timestamp()/1000),i.datetime.strftime('%Y%m%d'))
						
						grec.writeRecord(i.datetime.timestamp()*1000,i.value,i.trend)
						if not (f"{i.datetime.strftime('%Y-%m-%d')}.gdr" in os.listdir("../data/glucose/daily")):
							rec = gdr.createRecordFile(f"../data/glucose/daily/{i.datetime.strftime('%Y-%m-%d')}.gdr")
						rec = gdr.RecordAccess(f"../data/glucose/daily/{i.datetime.strftime('%Y-%m-%d')}.gdr")
						rec.writeRecord(i.datetime.timestamp()*1000,i.value,i.trend)
						rec.file.close()

				except Exception as e:
					print("Sync failed",e)
			for i in recordQueue:
				if i[0] == "delete":
					ts = hours_to_utc_minute_timestamps(i[1])
					for i in ts:
						print("del",rec.deleteRecordByTime(ts))
					i[2] = True
			


def notificationRunner():
	global rec
	import re
	last = None
	while True:
		time.sleep(1)
		if account and serviceConnected and not serviceOffline:
			settings = json.load(open("../data/settings.json"))
			
			try:
				netlog.notifier.info(f"Requesting url {pydexcom.const.DEXCOM_BASE_URL}")
				reading = account.get_latest_glucose_reading()
			except:
				continue
			lost = None
			if not reading:
				print("No Data Available")
				continue
			glucose = reading.value
			if not settings["useMGDL"]:
				glucose = round(glucose/18,1)

			bulb.title = f"DeskScout\nYour glucose: {glucose}{'mg/dl' if settings['useMGDL'] else 'mmol/L'} {reading.trend_description}\nLast reading at: {reading.datetime.ctime()}"
			if settings['enableNotify']:
				if account:
					netlog.notifier.info(f"Requesting url {pydexcom.const.DEXCOM_BASE_URL}")

					reading = account.get_latest_glucose_reading()
					#Check for urgent low
					if reading.datetime.timestamp() == last:
						continue
					else:
						last = reading.datetime.timestamp()
					if settings['notify']['urgentLow']['enabled']:
	
						if reading.value <= settings['notify']['urgentLow']['level']:
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
						else:
							silence['urgentLow'] = None
					if settings['notify']['low']['enabled']:
								
								
						if reading.value <= settings['notify']['low']['level']:
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
							if reading.trend_arrow == (6 if settings['notify']['fallingFast']['arrow'] == 'one' else 7) :
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
							if reading.trend == (2 if settings['notify']['risingFast']['arrow'] == 'one' else 1) :
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
					
		

	
import ctypes
from windows_toasts import InteractableWindowsToaster, Toast, ToastActivatedEventArgs, ToastButton


@route('/')
def index():
	return "OK"
@route('/shutdown')
def index():
	PlaySoundW(PWSTR(os.path.join(os.getcwd(),'../assets/sounds/shutdown.wav')), None, SND_FILENAME)
	p = psutil.Process(os.getpid())
	for proc in p.children(recursive=True):
		proc.kill()
	p.kill()
	exit(0)
@route('/factoryReset')
def index():
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
	global account,serviceConnected
	settings = json.load(open("../data/settings.json"))
	pw = keyring.get_password("com.sedwards.deskscout",settings['username'])
	try:
		netlog.main.info(f"Requesting url:{pydexcom.DEXCOM_AUTHENTICATE_ENDPOINT}")
		account = Dexcom(username=settings['username'],password=pw)
		if not serviceConnected:
			
			serviceConnected = True
			newToast = Toast()
			newToast.text_fields = ['Dexcom Share Connected', 'DeskScout is now receiving data and is able to provide alerts.']
			newToast.audio = ToastAudio(Path(os.path.abspath(os.path.join(os.getcwd(),'../assets/sounds/attention.wav'))),silent=True)
			PlaySoundW(PWSTR(os.path.join(os.getcwd(),'../assets/sounds/connected.wav')), None, SND_FILENAME | SND_ASYNC)
			toaster.clear_toasts()
			
			toaster.show_toast(newToast)
		print("LOGIN")
		import time
		return json.dumps({"status":"ok"})
	except:
		print("NAXC")
		bulb.title = "DeskScout"

		serviceConnected = False

		account = None
		return json.dumps({"status":"error"})
@route('/getStatus')
def getStatus():
	global serviceConnected,serviceDisconnectedAt
	
	if serviceOffline and serviceConnected:
		newToast = Toast()
		newToast.text_fields = ['Dexcom Share Disconnected', 'DeskScout cannot provide alerts']
		newToast.audio = ToastAudio(Path(os.path.abspath(os.path.join(os.getcwd(),'../assets/sounds/attention.wav'))),silent=True)
		PlaySoundW(PWSTR(os.path.join(os.getcwd(),'../assets/sounds/attention.wav')), None, SND_FILENAME | SND_ASYNC)
		serviceConnected = False
		loginState = 'offline'
		toaster.clear_toasts()

		toaster.show_toast(newToast)
		return json.dumps({"status":"ok","login_state":"offline"})
	if serviceOffline and serviceDisconnectedAt == 0:
		newToast = Toast()
		newToast.text_fields = ['Dexcom Share Disconnected', 'DeskScout cannot provide alerts']
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
		netlog.notifier.info(f"Requesting url {pydexcom.const.DEXCOM_AUTHENTICATE_ENDPOINT}")
		Dexcom(username=settings['username'],password=pw)
		if isinstance(account,Dexcom):
			loginState = True
		elif pw == "":
			loginState = 'unknown'
			serviceConnected = False

		else:
			loginState = False


	except:
		pw = keyring.get_password("com.sedwards.deskscout",settings['username'])
		print("PWW")
		if pw == "":
			print("LOGGED IN NO ")
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

@route('/getLatestReading')
def getLReading():
	global serviceConnected
	try:
		data = account.get_latest_glucose_reading()
		if data:
			return json.dumps({"status":"ok","data":data.json})
	except:
		if serviceConnected:
			toaster = WindowsToaster('DeskScout')
			newToast = Toast()
			newToast.text_fields = ['Dexcom Share Disconnected', 'DeskScout cannot provide alerts']
			newToast.audio = ToastAudio(Path(os.path.abspath(os.path.join(os.getcwd(),'../assets/sounds/attention.wav'))),silent=True)
			PlaySoundW(PWSTR(os.path.join(os.getcwd(),'../assets/sounds/attention.wav')), None, SND_FILENAME | SND_ASYNC)
		serviceConnected = False
		return json.dumps({"status":"Error"})

@route('/getCurrentReading')
def getCReading():
	data = account.get_current_glucose_reading()
	if data:
		return json.dumps({"status":"ok","data":data.json})
@route('/deleteRecords',method=["POST"])
def deleteRecords(self):
	data = request.forms
	if data['hours'] != "all":
		recordQueue.append(["delete_hours",data['hours'],0])
		while recordQueue[len(recordQueue)][2] == 0:
			pass
		return json.dumps({"status":"done"})

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
newToast = Toast()
newToast.text_fields = ['DeskScout is starting', 'Glucose alerts should be available soon.']
newToast.audio = ToastAudio(Path(os.path.abspath(os.path.join(os.getcwd(),'../assets/sounds/generic.wav'))),silent=True)
PlaySoundW(PWSTR(os.path.join(os.getcwd(),'../assets/sounds/generic.wav')), None, SND_FILENAME | SND_ASYNC)
toaster.clear_toasts()
toaster.show_toast(newToast)
_thread.start_new_thread(serverstatus,())
_thread.start_new_thread(notificationRunner,())
_thread.start_new_thread(recordAccessHandler,())

def runtime(internal):
	global bulb
	bulb = internal
	internal.visible = True
	print(internal)
	time.sleep(5)
	_thread.start_new_thread(attemptConnect,())
	run(host='127.0.0.1', port=49152)
	bulb.stop()
from PIL import Image
from pystray import Icon, Menu as menu, MenuItem as item
state = False
def attemptConnect():
	global account,serviceConnected
	import time
	time.sleep(5)
	requests.get("http://127.0.0.1:49152/authenticate")
def shutdown(icon, item):
	PlaySoundW(PWSTR(os.path.join(os.getcwd(),'../assets/sounds/shutdown.wav')), None, SND_FILENAME)

	p = psutil.Process(os.getpid())
	for proc in p.children(recursive=True):
		proc.kill()
	p.kill()
	exit(0)


def openbackup(icon,item):
	pass

icon = Icon(
	'DeskScout',
	icon=Image.open("../assets/icons/logo/03.png"),
	menu=menu(
		item(
		'Shutdown Deskscout',
		shutdown),
	),
	title="DeskScout"
	)

icon.run(runtime)