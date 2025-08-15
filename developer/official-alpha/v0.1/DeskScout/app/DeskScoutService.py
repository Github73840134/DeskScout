#DeskScout service pulls information from clarity
import os,sys,json
os.chdir(os.path.dirname(__file__))
sys.path.append(os.path.join(os.getcwd(),'libs'))
from bottle import route, run, template,request,post
from pydexcom import Dexcom
import keyring,psutil, subprocess
from windows_toasts import Toast, ToastAudio, WindowsToaster,InteractableWindowsToaster,ToastDuration
from pathlib import Path
from win32more.Windows.Win32.Media.Audio import PlaySoundW, SND_FILENAME, SND_ASYNC, SND_PURGE
from win32more.Windows.Win32.Foundation import PWSTR
import time
import requests,_thread
account = None
serviceConnected = False
serviceDisconnectedAt = 0
__version__ = "1"
__build__ = 1
__channel__ = "developer"
__release__ = "alpha"
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

serviceOffline = True
toaster = InteractableWindowsToaster('DeskScout')

def serverstatus():
	global serviceOffline,serviceConnected,serviceDisconnectedAt,account
	while True:
		try:
			resp = requests.get("https://share2.dexcom.com/ShareWebServices/Services/General/AuthenticatePublisherAccount",timeout=5)
			if resp.status_code != 405:
				if not serviceOffline:
					serviceOffline = True
					serviceDisconnectedAt = time.time()

					if serviceConnected:
						serviceDisconnectedAt = 0
						newToast = Toast()
						newToast.text_fields = ['Dexcom Share Unreachable', 'DeskScout cannot provide alerts']
						newToast.audio = ToastAudio(Path(os.path.abspath(os.path.join(os.getcwd(),'../assets/sounds/attention.wav'))),silent=True)
						PlaySoundW(PWSTR(os.path.join(os.getcwd(),'../assets/sounds/attention.wav')), None, SND_FILENAME | SND_ASYNC)
						serviceConnected = False
						toaster.show_toast(newToast)
				else:
					if time.time()-serviceDisconnectedAt > 10:
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
		except:
			print("ERTS")
			if not serviceOffline:
				serviceOffline = True
				serviceDisconnectedAt = time.time()

				if serviceConnected:
					serviceDisconnectedAt = 0
					newToast = Toast()
					newToast.text_fields = ['Dexcom Share Unreachable', 'DeskScout cannot provide alerts']
					newToast.audio = ToastAudio(Path(os.path.abspath(os.path.join(os.getcwd(),'../assets/sounds/attention.wav'))),silent=True)
					PlaySoundW(PWSTR(os.path.join(os.getcwd(),'../assets/sounds/attention.wav')), None, SND_FILENAME | SND_ASYNC)
					serviceConnected = False
					toaster.clear_toasts()
					toaster.show_toast(newToast)
			else:
				if time.time()-serviceDisconnectedAt > 10:
					newToast = Toast()
					newToast.text_fields = ['Dexcom Share Unreachable', 'DeskScout cannot provide alerts']
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
def notificationRespone(activatedEventArgs):
	resp = activatedEventArgs.arguments.split(".")
	settings = json.load(open("../data/settings.json"))

	if resp[0] == "silence":
		silence[resp[1]] = time.time()
		PlaySoundW(None, None, SND_PURGE)
		toast = Toast([f"{nametable[resp[1]]} Alert Silenced",f"You will not recieve another alert for {settings['notify'][resp[1]]['silence']/60} minutes"])
		toaster.show_toast(toast)
		PlaySoundW(PWSTR('../assets/sounds/generic.wav'), None, SND_FILENAME | SND_ASYNC)



def notificationRunner():
	import re
	last = None
	while True:
		time.sleep(1)
		if account and serviceConnected and not serviceOffline:
			settings = json.load(open("../data/settings.json"))
			if settings['enableNotify']:
				if account:
					reading = account.get_latest_glucose_reading()
					#Check for urgent low
					if settings['notify']['urgentLow']['enabled']:
						if reading.datetime.time() == last:
							continue
						else:
							last = reading.datetime.time()
						if reading.value <= settings['notify']['urgentLow']['level']:
							if silence['urgentLow']:
								if time.time()-silence['urgentLow'] >= settings['notify']['urgentLow']['silence']:
									silence['urgentLow'] = None
							if silence['urgentLow'] == None:
								newToast = Toast(['DeskScout',"Urgent Low Glucose",f"Your glucose is {reading.value} mg/dl"],duration=ToastDuration.Long)
								newToast.AddAction(ToastButton('OK', 'silence.urgentLow'))
								newToast.on_activated = notificationRespone
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
									silence['low'] = None
							if silence['low'] == None:
								newToast = Toast(['DeskScout',"High Glucose",f"Your glucose is {reading.value} mg/dl"],duration=ToastDuration.Long)
								newToast.AddAction(ToastButton('OK', 'silence.high'))
								newToast.on_activated = notificationRespone
								toaster.show_toast(newToast)
								notified['high'] = True
								if settings['notify']['high']['soundOn']:
									PlaySoundW(PWSTR(settings['notify']['high']['sound']), None, SND_FILENAME)
						else:
							silence['high'] = None
					
					
		

	
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
@route('/authenticate')
def auth():
	global account,serviceConnected
	settings = json.load(open("../data/settings.json"))
	pw = keyring.get_password("com.sedwards.deskscout",settings['username'])
	try:
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
newToast = Toast()
newToast.text_fields = ['DeskScout is Starting', 'Glucose alerts should be available soon.']
newToast.audio = ToastAudio(Path(os.path.abspath(os.path.join(os.getcwd(),'../assets/sounds/generic.wav'))),silent=True)
PlaySoundW(PWSTR(os.path.join(os.getcwd(),'../assets/sounds/generic.wav')), None, SND_FILENAME | SND_ASYNC)
toaster.clear_toasts()
toaster.show_toast(newToast)
_thread.start_new_thread(serverstatus,())
_thread.start_new_thread(notificationRunner,())

run(host='127.0.0.1', port=49152)
