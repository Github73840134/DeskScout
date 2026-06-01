# DeskScout
# Putting you in glucose
# horrible slogan, it will be changed
# Anyways
__version__ = "1.2.5"
__build__ = "32"
supported_service = ["22","23","24","25","26"]
from tkinter import messagebox

import os, sys,json,_thread,time,logging,subprocess

def error(exception,value,tb):
	print("error",dir(exception))
	messagebox.showerror("DeskScout-Fatal Error",f"A fatal error occured\n{value}")
	exit(0)


ast = None
class ExcepthookHandler(logging.Handler):
	def emit(self, record):
		# Only trigger for critical/fatal logs
		if record.levelno >= logging.FATAL:
			exc_info = record.exc_info
			if exc_info:
				sys.excepthook(*exc_info)
			else:
				# No exception tuple in the log
				pass
os.chdir(os.path.dirname(__file__))
# Logger shit
class DeltaTimeFormatter(logging.Formatter):
	def format(self, record):
		record.delta = time.time()-ast
		return super().format(record)
handler = logging.StreamHandler(open("app_boot.log","w+"))

LOGFORMAT = '+%(asctime)s [%(delta)s] %(name)s %(levelname)s: %(message)s'
fmt = DeltaTimeFormatter(LOGFORMAT)
handler.setFormatter(fmt)
logging.basicConfig(
					format='%(asctime)s [%(delta)s] %(levelname)-9s: %(message)s',
					datefmt='%Y-%m-%d %H:%M:%S',
					handlers=[handler,ExcepthookHandler()],
					level=logging.INFO)
sys.excepthook = error
ast = time.time()
boot = logging.getLogger("boot")
app = logging.getLogger("app")
serviceworker = logging.getLogger("service")
fetcher = logging.getLogger("fetch")
ui = logging.getLogger("ui")


boot.info("Adding libs and mods folder to path")
sys.path.insert(0,os.path.join(os.getcwd(), "libs"))
sys.path.append(os.path.join(os.getcwd(), "mods"))
try:
	os.mkdir("../cache")
except:
	pass
boot.info("Starting imports")
import requests
boot.debug("Importing the hellscape that is win32more")
from win32more.winui3 import XamlApplication
from win32more.Microsoft.UI.Xaml import Window, FrameworkElement
from win32more.Microsoft.UI.Xaml.Media import MicaBackdrop,Imaging,FontFamily,CompositionTarget,VisualTreeHelper
from win32more.Microsoft.UI.Xaml.Markup import XamlReader
from win32more.Windows.UI.Xaml.Interop import TypeKind
from win32more.Windows.UI.Xaml import GridLength, GridLengthHelper, GridUnitType,DependencyObject,Thickness,Visibility
from win32more.Microsoft.UI.Xaml.Controls import InfoBar,Primitives,ToggleSplitButton,Border,ToggleSwitch,Page,HyperlinkButton,Button,CheckBox,ComboBox,NumberBox, ProgressRing,Image,PasswordBox,TextBlock,TextBox, Slider, StackPanel, NavigationView, Frame, NavigationViewItem, RowDefinition, Grid, GridView, GroupStyle, Canvas, ToolTip
from win32more.Windows.Foundation import PropertyValue,IPropertyValue,Uri
from win32more.Windows.Win32.System.WinRT import IInspectable
from win32more.Microsoft.UI.Windowing import AppWindow
from win32more.Microsoft.UI import WindowId
from win32more.Microsoft.UI.Xaml import DispatcherTimer
from win32more.Windows.Foundation import TimeSpan,MemoryBuffer
from win32more.Windows.UI import Colors
from win32more.Windows.UI.Xaml.Media import SolidColorBrush,TranslateTransform,ImageBrush,ImageSource, Stretch
from win32more.Microsoft.UI.Xaml.Media.Animation import Storyboard, DoubleAnimation
from win32more.Windows.UI.Xaml import Duration, DurationHelper
from win32more.Microsoft.UI.Xaml.Media.Animation import NavigationThemeTransition, TransitionCollection
from win32more.Windows.Win32.System.Registry import *
from win32more.Windows.Win32.Media.Audio import PlaySoundW, SND_FILENAME, SND_ASYNC, SND_PURGE
from win32more.Windows.Win32.Foundation import PWSTR
from win32more.Windows.Win32.System.Registry import (
	RegOpenKeyExW,
	RegQueryValueExW,
	RegCloseKey,
	HKEY_CURRENT_USER,
	HKEY,
	KEY_READ,
)
from win32more.Windows.Win32.UI.WindowsAndMessaging import (
	SetClassLongPtrW,
	LoadImageW,
	IMAGE_ICON,
	LR_LOADFROMFILE,
	GCLP_HICON,
	GCLP_HICONSM,
)
import ctypes
import ctypes
from ctypes import wintypes
import os
from tkinter import messagebox
import _thread
from PIL import Image as PImage,ImageDraw
def makeGraph(width,height,mintime,maxtime,low,high,history,units=True):
	def _map(x, in_min, in_max, out_min, out_max):
		return int((x-in_min) * (out_max-out_min) / (in_max-in_min) + out_min)
	img = PImage.new("RGB",(width,height))
	draw = ImageDraw.Draw(img)
	draw.rectangle((0,0,width,height),(255,255,255))
	draw.rectangle((int(width*0.08),int(height*0.05),int(width*0.08),int(height*0.95)),(0,0,0))
	draw.rectangle((int(width*0.08),int(height*0.95),int(width),int(height*0.95),),(0,0,0))
	for i in range(40,420,20):
		draw.text((int(width*0.04),_map(i,40,400,int(height*0.94),int(height*0.05))),str(i if units else round(i/18,1)),(0,0,0))
	
	if low:
		draw.text((int(width*0.01),_map(low,40,400,int(height*0.92),int(height*0.05))),str(low if units else round(low/18,1)),(255,0,0))
		for i in range(int(width*0.08),int(width),40):
			draw.rectangle((i,_map(low,40,400,int(height*0.94),int(height*0.05)),i+20,_map(low,40,400,int(height*0.94),int(height*0.05))),(255,0,0))
	if high:
		draw.text((int(width*0.01),_map(high,40,400,int(height*0.92),int(height*0.05))),str(high if units else round(high/18,1)),(255,200,0))

		for i in range(int(width*0.08),int(width),40):
			draw.rectangle((i,_map(high,40,400,int(height*0.94),int(height*0.05)),i+20,_map(high,40,400,int(height*0.94),int(height*0.05))),(255,200,0))
	for i in range(mintime,maxtime,3600):
		
		x = _map(i,mintime,maxtime,int(width*0.08),int(width))

		y = _map(i,int(width*0.08),int(width),mintime,maxtime)
		if x-int(width*0.05) > int(width*0.05):
		
			draw.text((x-int(width*0.05),int(height*0.96)),time.strftime("%I%p", time.localtime(i/1000)),(0,0,0))
	print(history[-1][0])
	if low:
		if history[-1][0] <= low:
			draw.rectangle((int(width*0.082),_map(low,40,400,int(height*0.94),int(height*0.05)),int(width),int(height*0.949)),(255,0,0))
	if high:
		if history[-1][0] >= high:
			draw.rectangle((int(width*0.082),int(height*0.05),int(width),_map(high,40,400,int(height*0.94),int(height*0.05))),(255,200,0))
	for i in history:
		x = _map(i[1],mintime,maxtime,int(width*0.085),int(width*0.98))
		if i == history[-1]:
			draw.circle((x,_map(i[0],40,400,int(height*0.94),int(height*0.05))),2,(0,0,0))
		else:
			draw.circle((x,_map(i[0],40,400,int(height*0.94),int(height*0.05))),2,(0,0,0))
		



	img.save("../data/glucose.png","PNG")

def custom_thread_hook(args):
	# Log the exception from a thread
	logger.fatal(f"Uncaught exception in thread {args.thread.name}",
					exc_info=(args.exc_type, args.exc_value, args.exc_traceback))

	# Still call default handler for full traceback
	sys.__excepthook__(args.exc_type, args.exc_value, args.exc_traceback)

user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32
EnumWindows = user32.EnumWindows
EnumWindowsProc = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)
GetWindowThreadProcessId = user32.GetWindowThreadProcessId
IsWindowVisible = user32.IsWindowVisible

def get_hwnds_by_pid(pid):
	hwnds = []

	@EnumWindowsProc
	def foreach_window(hwnd, lParam):
		if IsWindowVisible(hwnd):
			lpdw_process_id = wintypes.DWORD()
			GetWindowThreadProcessId(hwnd, ctypes.byref(lpdw_process_id))
			if lpdw_process_id.value == pid:
				hwnds.append(hwnd)
		return True

	EnumWindows(foreach_window, 0)
	return hwnds

# Example: Get HWNDs for current process


class RAFManager:
	def __init__(self):
		self._callbacks = []
		self._start_time = time.time()
		self._handler = None

	def request_animation_frame(self, callback,data={}):
		self._callbacks.append({
			"callback": callback,
			"start": time.time(),
			'data':data
		})
		if not self._handler:
			self._handler = CompositionTarget.add_Rendering(self._on_render)
		return len(self._callbacks)-1
	def cancel_animation_frame(self,i):
		self._callbacks.pop(i)
	def Respond(self,data={},cancel=False):
		return (data,cancel)
	def _on_render(self, sender, args):
		now = time.time()
		still_active = []

		for cb in self._callbacks:
			elapsed = (now - cb["start"]) * 1000  # ms
			response = cb["callback"](elapsed,cb['data'])
			cb['data'] = response[0]
			if response[1] == False:
				still_active.append(cb)

		self._callbacks = still_active
		if not self._callbacks:
			CompositionTarget.remove_Rendering(self._handler)
			self._handler = None
def is_dark_mode_enabled() -> bool:
	app.debug("Checking Dark Mode")
	sub_key = r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize"
	value_name = "AppsUseLightTheme"

	hkey = HKEY()
	# Open the registry key
	result = RegOpenKeyExW(HKEY_CURRENT_USER, sub_key, 0, KEY_READ, ctypes.byref(hkey))
	if result != 0:
		raise OSError("Failed to open registry key.")

	# Prepare a buffer for the DWORD value
	data = (ctypes.c_ubyte * 4)()
	data_size = ctypes.c_uint32(4)
	result = RegQueryValueExW(hkey, value_name, None, None, ctypes.cast(data, ctypes.POINTER(ctypes.c_ubyte)), ctypes.byref(data_size))
	RegCloseKey(hkey)

	if result != 0:
		raise OSError("Failed to read registry value.")

	# Convert bytes to integer (DWORD is 4 bytes)
	value = int.from_bytes(bytes(data), byteorder='little')
	return value == 0  # 0 means dark mode is enabled
def cap(number,_max):
	if number > _max:
		return _max
	return number
SERVICE_URL = "http://127.0.0.1:49152"
# Example usage
try:
	ctypes.WinDLL("Microsoft.WindowsAppRuntime.Bootstrap.dll")
	print("Runtime is installed.")
except Exception as e:
	print("Runtime missing!", e)
import socket
def check_internet_connection(host="8.8.8.8", port=53, timeout=3):
	"""
	Checks for an internet connection by trying to connect to a host.
	Args:
		host (str): The host to connect to (default: 8.8.8.8, Google's public DNS server).
		port (int): The port to connect to (default: 53, DNS port).
		timeout (int): Timeout in seconds for the connection attempt (default: 3).
	Returns:
		bool: True if a connection could be established, False otherwise.
	"""
	try:
		socket.setdefaulttimeout(timeout)
		socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
		return True
	except socket.error:
		return False

from win32more.Windows.UI.Xaml.Media import VisualTreeHelper
from win32more.Windows.UI.Xaml import DependencyObject

from win32more.Windows.UI.Xaml.Controls import Panel, ItemsControl
from win32more.Windows.UI.Xaml.Media import VisualTreeHelper
from win32more.Windows.UI.Xaml import DependencyObject

from win32more.Windows.UI.Xaml.Controls import ItemsControl
from win32more.Windows.UI.Xaml.Media import VisualTreeHelper
from win32more.Windows.UI.Xaml import DependencyObject

def getAllElements(root_element):
	all_elements = []

	def recurse(elem):
		if elem is None:
			return

		all_elements.append(elem)

		# Check if element has 'get_Children' method (for example in Panel or custom controls)
		get_children_method = getattr(elem, "get_Children", None)
		if callable(get_children_method):
			try:
				children_collection = get_children_method()
				# Assuming children_collection supports iteration
				for child in children_collection:
					recurse(child)
				return
			except Exception:
				pass

		# Try ItemsControl.Items
		try:
			items_control = elem.as_(ItemsControl)
			for item in items_control.Items:
				recurse(item)
			return
		except Exception:
			pass

		# Try Content property
		try:
			content = getattr(elem, "Content", None)
			if content is not None:
				recurse(content)
				return
		except Exception:
			pass

		# Fallback: VisualTreeHelper children
		try:
			dep_obj = elem.as_(DependencyObject)
			count = VisualTreeHelper.GetChildrenCount(dep_obj)
			for i in range(count):
				child = VisualTreeHelper.GetChild(dep_obj, i)
				recurse(child)
		except Exception:
			pass

	recurse(root_element)
	return all_elements
def cs(v):
	if v < 1024:
		return str(v)+" B"
	elif v >= 1024 and v < 1_000_024:
		return str(round(v/1024))+" KB"
	elif v > 1_000_024  < 1_000_000_024:
		return str(round(v/1e+6,2))+" MB"
	elif v >= 1_000_000_024:
		return str(round(v/1e+9,2))+" GB"
from win32more.Windows.UI.Xaml import UIElement
from win32more.Windows.UI.Xaml.Media import VisualTreeHelper
from win32more.Windows.UI.Xaml import DependencyObject

from mods import popbuilder

	
class AppState:
	STARTING = 0x00
	RUNNING = 0x01
	LOGIN = 0x02
class InvalidRequest:
	pass
class ServerLost:
	pass
def calculate_slope(data):
	times = [(t - data[0][0]) / 60 for t, _ in data]
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

vinfo = json.load(open('versioninfo.json'))
if vinfo['release'] in ["stable","beta"]:
	USERKEY = f"com.sedwards.deskscout-{vinfo['release']}"
else:
	USERKEY = f"com.sedwards.deskscout"
__release__ = vinfo['release']
del(vinfo)

class App(XamlApplication):
	
	def OnLaunched(self, args):
		# App Start
		ui.debug("App OnLaunched called")
		self.dispatch = []
		self.page = "home" # Set the page to home
		self.fetchState = 0 # Set the fetcher state to disable
		self.lastFetch = -1 # Set the last successful fetch time to none
		self.lsc = -1 # Set the last synced reading tome to none
		self.raf = RAFManager() # Create an Request Animation Frame manager
		self.state = 0 # Stores the app state
		self.glucose = {} # No glucose data yet
		ui.debug("Loading window.xaml")
		win = XamlReader().Load(open("../assets/ui/window.xaml", "r", encoding='utf-8').read()).as_(Window)
		self.win = win
		ui.debug("Loaded window.xaml")
		win.SystemBackdrop = MicaBackdrop()  # Set the window backdrop (optional)
		ui.debug("Aquiring NavigationView")
		self.NavView = win.Content.as_(FrameworkElement).FindName("NavView").as_(NavigationView)
		ui.debug("Setting up NavigationView")
		self.NavView.SelectedItem = self.NavView.MenuItems[0] # Set the selected item to the first nav item
		self.navert = self.NavView.add_SelectionChanged(self.NavChangeSelect)
		ui.debug("Loading the document")
		self.document = win.Content.as_(FrameworkElement).FindName("ContentFrame").as_(Frame)
		ui.debug("Content loaded")
		ui.info("Main frame loaded")
		self.document.Content = XamlReader().Load(open("../assets/ui/home.xaml", "r", encoding='utf-8').read())

		if 1 != 1: #Dont ask me why I did this
			self.page = 'home'
			
			self.document.Content = XamlReader().Load(open("../assets/ui/home.xaml", "r", encoding='utf-8').read()) # Set page content
			self.state = AppState.RUNNING # Change app state to allow dataFetch to run
			app.info("Starting background thread")
			self.fetchState = 4 # Pauses the data fetch task because we cant connect tot he service
			_thread.start_new_thread(self.dataFetch,()) # Start the data fetch task
		else:
			try:
				serviceworker.info("Checking if service is alive")
				resp = requests.get("http://127.0.0.1:49152/getStatus") # Get the deskscout service status
				serviceworker.info("Service is alive")
				serviceworker.debug(f"Service Respone: {resp.text}")
				serviceworker.info("Checking if service version is compatible")
				resp = requests.get("http://127.0.0.1:49152/about") # Get the deskscout service version
				ver = json.loads(resp.text)
				if not ver['build'] in supported_service:
					serviceworker.warning(f"Service build may be incompatible")

					messagebox.showwarning("Potentially Incompatible Service",f"The version of the client may not be compatible with the version of the service you have installed")
				resp = requests.get("http://127.0.0.1:49152/getStatus")
			except Exception as e:
				# Big OOPS
				messagebox.showwarning("Cant connect to DeskScout service","Please make sure the service is started before running the app")
				serviceworker.info("Could not contact service, stopping here",str(e))
				app.fatal("Startup failed","NO_SERVICE_CONNECTION",exc_info=Exception("NO_SERVICE_CONNECTION"))
			if not self.getSetting("setup"):
				self.launchOOBE() # Launch the oobe
				

			else:
				app.info("Checking login status")
				status = json.loads(resp.text)
				print(resp.text)
				if status['login_state'] == "offline":
					print("OFFLINE")
					self.fetchState = 4
					app.info("Starting background thread")
					self.state = AppState.RUNNING
					_thread.start_new_thread(self.dataFetch,())
					self.fetchState = 4
					
				elif status['login_state'] == "unknown":
					self.showSignIn(self.goHome)
				elif status['login_state'] == False:
					app.info("Authenticating")
					try:
						serviceworker.info("Authenticating user")
						resp = requests.get("http://127.0.0.1:49152/authenticate")

					except Exception as e:
						serviceworker.fatal("Could not connect to service")
						app.fatal("App terminating unable to reach serivce")
						exit(0)
					try:
						data = json.loads(resp.text)
					except:
						serviceworker.fatal("Service worker sent malformed response")
						exit(0)
					print(data)
					if data['status'] == "ok":
						serviceworker.info("Authentication successful")
						print("Login OK")
						self.state = AppState.RUNNING
						_thread.start_new_thread(self.dataFetch,())

						
					else:

						self.showSignIn(self.goHome)
						
						
				elif status['login_state'] == True:
					app.info("Authentication complete")
					self.state = AppState.RUNNING
					app.info("Starting background thread")
					_thread.start_new_thread(self.dataFetch,())
				ui.debug("Activating window")
		win.Activate()

		ui.info("Window is active")
		icon_path = os.path.abspath(os.path.join(os.getcwd(),'../assets/icons/logo/04.ico'))
		# Weird windows thing
		hicon = LoadImageW(
			None,
			icon_path,
			IMAGE_ICON,
			0,
			0,
			LR_LOADFROMFILE
		)
		# Set the window title
		self.win.Title = "DeskScout"
		current_pid = os.getpid()
		hwnd = get_hwnds_by_pid(current_pid)[0]
		self.hwnd = hwnd

		#resp = requests.get("http://127.0.0.1:49152/authenticate")

		from win32more.Windows.Win32.UI.WindowsAndMessaging import SendMessageW, WM_SETICON, ICON_SMALL, ICON_BIG
		# Set the window icon
		SendMessageW(hwnd, WM_SETICON, ICON_SMALL, hicon)
		SendMessageW(hwnd, WM_SETICON, ICON_BIG, hicon)

		#Runs the self.update_Display at an interfval
		self._resize_timer = DispatcherTimer()
		interval = TimeSpan()
		self.pbts = None
		self.ups = False
		interval.Duration = 100000 # 100ms
		self._resize_timer.Interval = interval
		self._resize_timer.Tick += self.update_Display
		self._resize_timer.Start()
		self.lastUpdateCheck = time.time()
		self.popupShown = None
		self.documentProvider = self.document
		if self.fetchState == 4:
			self.popupShown = "ce.serviceOffline"
			ctx = self.showPopup("Connection Error",popbuilder.ok("The DeskScout service could not connect to Dexcom Share"))
			ctx.as_(FrameworkElement).FindName("popup.content.ok").as_(Button).Click += lambda sender,args: self.hidePopup()
		if "updatemanifest.json" in os.listdir():
			manifest = json.load(open("updatemanifest.json"))
			appbuild = json.load(open("versioninfo.json"))['app']
			if manifest['build'] == appbuild:
				self.page = "updatecomplete"
				self.NavView.put_IsPaneVisible(False) # Hides the NavPanel making it impossible to leave the page

				self.document.Content = XamlReader().Load(open("../assets/ui/update_complete.xaml", "r", encoding='utf-8').read()) # Set page content
				
				self.document.Content.as_(FrameworkElement).FindName("uc.title").as_(TextBlock).Text = f"Whats new in {manifest['name']}:"
				self.document.Content.as_(FrameworkElement).FindName("uc.changes").as_(TextBox).Text = manifest['info']
				PlaySoundW(PWSTR(os.path.abspath("../assets/sounds/update_complete.wav")), None, SND_FILENAME | SND_ASYNC)

				def complete(sender,args):
					os.remove(os.path.join(os.getcwd(),"updatemanifest.json"))
					self.goHome()
				self.document.Content.as_(FrameworkElement).FindName("uc.next").as_(Button).Click += complete
		else:
			self.goHome()
		import argparse
		parser = argparse.ArgumentParser()
		parser.add_argument("-intent",required=False,default="")
		print(sys.argv)
		args = parser.parse_args(sys.argv[1:])
		self.runIntent(args.intent)

		

	def runIntent(self,intent):
		if intent == "Home":
			self.NavView.SelectedItem = self.NavView.MenuItems[0]
		elif intent == "History":
			self.transitionElementContent(self.document,XamlReader().Load(open("../assets/ui/loading.xaml", "r", encoding='utf-8').read()),lambda a=self:exec('a.page = ""\na.lsc = -1\na.initHistoryPage()'))			
		elif intent == "Settings":
			self.page = "settings"
			self.transitionElementContent(self.document,XamlReader().Load(open("../assets/ui/settings.xaml", "r", encoding='utf-8').read()),self.initSettingsPage)
		elif intent == "Settings/About":
			self.page = "about"
			self.transitionElementContent(self.document,XamlReader().Load(open("../assets/ui/about.xaml", "r", encoding='utf-8').read()),self.initAboutPage)
		elif intent == "Settings/Sounds":
			self.page = "settings"
			self.transitionElementContent(self.document,XamlReader().Load(open("../assets/ui/settings/sounds.xaml", "r", encoding='utf-8').read()),lambda: self.initAlarmSoundSettings(self.document))
		elif intent == "Settings/Update":
			self.transitionElementContent(self.document,XamlReader().Load(open("../assets/ui/settings/update.xaml", "r", encoding='utf-8').read()),self.initUpdatePage)
		if intent:
			self.bringToFront()
	def NotImplemented(self,*args):
		messagebox.showerror("Work in progress","Feature is not implemented")
	def launchOOBE(self):
		import psutil
		subprocess.Popen("../core/pythonw.exe DeskScoutSetup.py")
		p = psutil.Process(os.getpid())
		p.kill()
	def doRestore(self,path):
		
		from zipfile import ZipFile
		try:
			zip = ZipFile(path)
			for i in zip.filelist:
				if i.filename == ".deskscout":
					break
			else:
				messagebox.showerror("Deskscout","Error restoring settings")
				self.restoreState = -1
			for i in zip.filelist:
				if i.filename.startswith("sounds/"):
					print(i.filename)
					if i.filename == "sounds/":
						continue
					x = zip.open(i.filename)
					y = open(f"../assets/sounds/extern/{os.path.basename(i.filename)}",'wb+')
					y.write(x.read())
					y.close()
			for i in zip.filelist:
				if i.filename == "settings.json":
					x = zip.open("settings.json")
					y = open("../data/settings.json",'wb+')
					y.write(x.read())
					y.close()
			for i in zip.filelist:
				if i.filename == "glucose.gdr":
					self.changeSetting("gdrState",'0')
					x = zip.open("glucose.gdr")
					y = open("../data/glucose.gdr",'wb+')
					y.write(x.read())
					y.close()
					os.system("py gdrmanage.py unpack")
					self.changeSetting("gdrState",'1')
					
			self.restoreState = 1
			


		except Exception as e:
			messagebox.showerror("Deskscout",f"Error restoring settings\n{str(e)}")
			self.restoreState = -1
			return
	
	def afterRestore(self):
		# This code is a bitch, not the slaying kind, unless it slays exiting the program
		if self.restoreState == -1:
			self.launchOOBE()
		elif self.restoreState == 1:
			self.showDisclaimer(lambda: self.setupAuthCheck(self.setupComplete))
			

	def restoreButton(self,sender,args):
		from tkinter import filedialog
		ans = filedialog.askopenfilename(filetypes=[["Zip Files",[".zip"]]])
		if not ans:
			return
		self.restoreState = 0

		self.loadAsync(self.document,lambda:self.doRestore(ans),XamlReader().Load(open("../assets/ui/loading.xaml", "r", encoding='utf-8').read()),self.afterRestore)
		
	def doOOBE(self,page="alarmsetup"):
		def PresetRoot(internal=False):
			if page == "alarmsetup":
				doc = self.document.Content.as_(FrameworkElement).FindName("frame").as_(Frame) # Get document context
				self.initSettingsPage(doc)
				# Hide some unimportant buttons and views
				doc.Content.as_(FrameworkElement).FindName("settings.about").as_(Button).Visibility = 1
				doc.Content.as_(FrameworkElement).FindName("settings.pcloseapp").as_(Button).Visibility = 1
				doc.Content.as_(FrameworkElement).FindName("settings.psignout").as_(Button).Visibility = 1
		if page == "alarmsetup":
			self.NavView.put_IsPaneVisible(False)

			self.document.Content = XamlReader().Load(open("../assets/ui/oobe/page0.xaml", "r", encoding='utf-8').read()) # Load the new page
			self.document.Content.as_(FrameworkElement).FindName("frame").as_(Frame).Content = XamlReader().Load(open("../assets/ui/settings.xaml", "r", encoding='utf-8').read()) #Set the frame content
			self.document.Loaded += lambda sender,args: PresetRoot() # Runs after page load to hide elements
			self.document.Content.as_(FrameworkElement).FindName("oobe.next").as_(Button).add_Click(lambda sender,args: self.setupComplete()) #Bind oobe.next click event to setupComplete	
	def welcome(self):
		self.goHome()
		self.page = "home"
		PlaySoundW(PWSTR(os.path.join(os.getcwd(),'../assets/sounds/open.wav')), None, SND_FILENAME | SND_ASYNC) # Play the open jingle
	def setupComplete(self):
		# Shows the setup complete page
		self.NavView.put_IsPaneVisible(False) # Hide the NavPanel
		if self.fetchState == 0:
			import _thread
			_thread.start_new_thread(self.dataFetch,()) # Start the fetch service
		self.changeSetting("setup",True)
		self.changeSetting("gdrState","1")

		self.document.Content = XamlReader().Load(open("../assets/ui/setup_complete.xaml", "r", encoding='utf-8').read()) # Start the page update
		self.document.Content.as_(FrameworkElement).FindName("oobe.finish").as_(Button).add_Click(lambda sender,args: self.goHome()) # Go home when oobe.finish is clicked
		PlaySoundW(PWSTR(os.path.join(os.getcwd(),'../assets/sounds/setup_done.wav')), None, SND_FILENAME | SND_ASYNC) # Play a whimsical little jingle



	def setupAuthCheck(self,onFinish=None):
		# Runs an authentication check
		try:
			serviceworker.info("Authenticating user")
			resp = requests.get("http://127.0.0.1:49152/authenticate") #Attempts service authentication

		except Exception as e:
			# Dead service moment
			serviceworker.fatal("Could not connect to service")
			app.fatal("App terminating unable to reach serivce")
			exit(0)
		try:
			data = json.loads(resp.text)
		except:
			# Dead service moment
			serviceworker.fatal("Service worker sent malformed response")
			exit(0)

		if data['status'] == "ok":
			# Authentication successful
			serviceworker.info("Authentication successful")
			if onFinish:
				onFinish()
		else:
			# Authentication failed
			self.showSignIn(onFinish)
	def goHome(self):
		# Goes to the home screen
		self.NavView.put_IsPaneVisible(True) # Show the nav pannel
		self.state = AppState.RUNNING #Allow the fetcher to run

		# Check if the fetcher si not running and start the fetcher
		if self.fetchState == 0:
			import _thread
			_thread.start_new_thread(self.dataFetch,()) # Start the fetcher
		self.document.Content = XamlReader().Load(open("../assets/ui/home.xaml", "r", encoding='utf-8').read()) # Load the home screen
		self.page = "home"
		uri = Uri.CreateUri(os.path.abspath(os.path.join(os.getcwd(),"../","assets",'pride_flag.png')))
		img = self.document.Content.as_(FrameworkElement).FindName("Background").as_(Image)
		bitmap = Imaging.BitmapImage()
		bitmap.UriSource = uri
		img.Source = bitmap
	def showSignIn(self,onFinish=None):
		# Starts the sign-in flow
		from win32more.Windows.Win32.UI.WindowsAndMessaging import (
		GetForegroundWindow,
		SetForegroundWindow,
		FindWindowW,
		ShowWindow,
		IsIconic,
		SW_RESTORE,
		SW_HIDE,
		SW_MINIMIZE,
		SW_SHOW
		)
		self.state = AppState.LOGIN #This will stop the fetch stast
		ShowWindow(self.hwnd, SW_HIDE)
		resp = subprocess.run("../core/pythonw.exe DeskScoutSetup.py signin")
		ShowWindow(self.hwnd, SW_SHOW)
		SetForegroundWindow(self.hwnd)
		if onFinish:
			onFinish()


		
	def showDisclaimer(self,onAccept=None):
		# Shows the legal disclaimer for deskscout
		self.NavView.put_IsPaneVisible(False) # Hides the NavPanel making it impossible to leave the page
		self.page = "disclaimer"
		self.document.Content = XamlReader().Load(open("../assets/ui/disclaimer.xaml", "r", encoding='utf-8').read()) #Set the page content
		PlaySoundW(PWSTR(os.path.join(os.getcwd(),'../assets/sounds/disclaimer.wav')), None, SND_FILENAME | SND_ASYNC) # Play disclaimer sound effect
		def finish(sender,args):
			self.NavView.put_IsPaneVisible(True) #Show the NavPanel again
			if onAccept:
				onAccept() # Self explanatory

		self.document.Content.as_(FrameworkElement).FindName("disclaimer.next").as_(Button).add_Click(finish) # Bind button click

	def hourAhead(self):
		from mods import gdr
		import datetime
		rec = gdr.RecordReader(os.path.abspath("../data/glucose.gdr"))
		i = rec.getRecordCount()
		rec1 = []
		for x in range(i):
			rec1.append(rec.getRecordByIndex(x))
		seen = []
		dseen = []
		final = []
		records = []
		date = int(time.time())
		last = 0
		for x in rec1:
			tx = time.localtime(float(x.time / 1000))
			if int(x.time/1000) in range(date-1800,date):

				
				if (tx.tm_year,tx.tm_yday,tx.tm_hour,tx.tm_min) in seen:
					continue
				else:
					seen.append((tx.tm_year,tx.tm_yday,tx.tm_hour,tx.tm_min))
					final.append((int(x.time/1000),x.value))
		records.extend(final)
		records.reverse()
		
		now = datetime.datetime.now()
		today = datetime.datetime(now.year, now.month, now.day, 0, 0).timestamp()
		slope = calculate_slope(records)
		predictions = []
		for i in range(0,65,5):
			predictions.append(int(predict_glucose(records[-1][1],slope,i)))
		print("Prediction",predictions)

	def bringToFront(self):
		from win32more.Windows.Win32.UI.WindowsAndMessaging import (
		GetForegroundWindow,
		SetForegroundWindow,
		FindWindowW,
		ShowWindow,
		IsIconic,
		SW_RESTORE,
		)
		if IsIconic(self.hwnd):
			ShowWindow(self.hwnd, SW_RESTORE)
			# Bring to front
			SetForegroundWindow(self.hwnd)



	def getUpdateStatus(self):
		try:
			resp = requests.get(SERVICE_URL+"/getUpdateStatus")
			return json.loads(resp.text)
		except:
			return False
	def updateButtonHandler(self):
		print("UPS",self.ups)
		if self.ups == 0:
			try:
				requests.get(SERVICE_URL+"/downloadUpdate")
			except:
				pass
		elif self.ups == 1:
			self.win.Close()
			try:
				requests.get(SERVICE_URL+"/shutdown")
			except:
				pass
			import subprocess
			subprocess.Popen("../core/pythonw.exe DeskScout.pyw",start_new_session=True)
			p = psutil.Process(os.getpid())
			p.kill()
	def update_Display(self,sender,args):
		# Updates the main glucose display
		
		import re
		if self.dispatch:
			task = self.dispatch[0]
			self.dispatch.pop(0)
			task()
			return


		#print("FS",self.fetchState,self.state)
		#Check if the user is logged in
		width,height = self.win.Content.as_(FrameworkElement).ActualWidth,self.win.Content.as_(FrameworkElement).ActualHeight
		self.win.Content.as_(FrameworkElement).FindName("popup.container").as_(Grid).Height = height
		if self.page == "update":
			if time.time()-self.lastUpdateCheck >= 0.25:
				
				stat = self.getUpdateStatus()
				if stat == False:
					self.popupShown = "ce.serverLost"
					ctx = self.showPopup("Something went wrong",popbuilder.ok("Try again later"))
					PlaySoundW(PWSTR("../assets/sounds/conflict.wav"), None, SND_FILENAME | SND_ASYNC)
					self.NavView.SelectedItem = self.NavView.MenuItems[0] # Set the selected item to the first nav item
					

					return
				if stat['status'] == "ready":
					if stat['result'] == "ok":
						import platform
						myv = json.load(open('versioninfo.json'))
						if not platform.release() in stat['vinfo']['osSupport'][sys.platform]['official-stable']:
							self.document.Content.as_(FrameworkElement).FindName("update.endoflife").as_(InfoBar).IsOpen = True
						else:
							self.document.Content.as_(FrameworkElement).FindName("update.endoflife").as_(InfoBar).IsOpen = False
						if myv['app'] in stat['vinfo']['deprecated'][sys.platform]['official-stable']:
							self.document.Content.as_(FrameworkElement).FindName("update.deprecated").as_(InfoBar).IsOpen = True
						else:
							self.document.Content.as_(FrameworkElement).FindName("update.deprecated").as_(InfoBar).IsOpen = False


						if not stat['isUpToDate']:
							self.document.Content.as_(FrameworkElement).FindName("update.ok").as_(TextBlock).Visibility = Visibility.Collapsed

							self.document.Content.as_(FrameworkElement).FindName("update.preview.name").as_(TextBlock).Text = stat['manifest']['name']
							self.document.Content.as_(FrameworkElement).FindName("update.preview.build").as_(TextBlock).Text = f"Build {stat['manifest']['build']}"
							self.document.Content.as_(FrameworkElement).FindName("update.preview.info").as_(TextBox).Text = stat['manifest']['info']
							self.document.Content.as_(FrameworkElement).FindName("update.preview.action").as_(Button).Content = "Download Update"
							self.document.Content.as_(FrameworkElement).FindName("update.preview.action").as_(Button).Visibility = Visibility.Visible
							self.ups = 0
								



							self.document.Content.as_(FrameworkElement).FindName("update.preview.size").as_(TextBlock).Text = cs(stat['manifest']['size'])
							self.document.Content.as_(FrameworkElement).FindName("update.preview").as_(StackPanel).Visibility = Visibility.Visible
							
						else:
							self.document.Content.as_(FrameworkElement).FindName("update.ok").as_(TextBlock).Visibility = Visibility.Visible
							self.document.Content.as_(FrameworkElement).FindName("update.preview").as_(StackPanel).Visibility = Visibility.Collapsed
						self.document.Content.as_(FrameworkElement).FindName("update.check").as_(Button).Content = "Check for update"
						self.document.Content.as_(FrameworkElement).FindName("update.check").as_(Button).IsEnabled = True
					elif stat['result'] == "installReady":
						manifest = json.load(open('updatemanifest.json'))
						self.document.Content.as_(FrameworkElement).FindName("update.preview.name").as_(TextBlock).Text = manifest['name']
						self.document.Content.as_(FrameworkElement).FindName("update.preview.build").as_(TextBlock).Text = f"Build {manifest['build']}"
						self.document.Content.as_(FrameworkElement).FindName("update.preview.info").as_(TextBox).Text = manifest['info']


						self.document.Content.as_(FrameworkElement).FindName("update.preview.size").as_(TextBlock).Text = cs(manifest['size'])
						self.document.Content.as_(FrameworkElement).FindName("update.preview").as_(StackPanel).Visibility = Visibility.Visible
						self.document.Content.as_(FrameworkElement).FindName("update.preview.status").as_(TextBlock).Visibility = Visibility.Collapsed
						self.document.Content.as_(FrameworkElement).FindName("update.preview.progress").as_(ProgressRing).Visibility = Visibility.Collapsed


						self.document.Content.as_(FrameworkElement).FindName("update.preview.action").as_(Button).Visibility = Visibility.Visible
						self.document.Content.as_(FrameworkElement).FindName("update.preview.action").as_(Button).Content = "Install Update"
						self.ups = 1

				elif stat['status'] == "cfu":
					self.document.Content.as_(FrameworkElement).FindName("update.check").as_(Button).Content = "Checking for update"
					self.document.Content.as_(FrameworkElement).FindName("update.check").as_(Button).IsEnabled = False
				elif stat['status'] == 'dc':
					self.document.Content.as_(FrameworkElement).FindName("update.check").as_(Button).IsEnabled = False
					self.document.Content.as_(FrameworkElement).FindName("update.preview.action").as_(Button).Visibility = Visibility.Collapsed
					self.document.Content.as_(FrameworkElement).FindName("update.preview.progress").as_(ProgressRing).IsIndeterminate = True
					self.document.Content.as_(FrameworkElement).FindName("update.preview.status").as_(TextBlock).Text = "Ensuring latest version is requested"
					self.document.Content.as_(FrameworkElement).FindName("update.preview.progress").as_(ProgressRing).Visibility = Visibility.Visible
					self.document.Content.as_(FrameworkElement).FindName("update.preview.status").as_(TextBlock).Visibility = Visibility.Visible
				elif stat['status'] == "dr":
					self.document.Content.as_(FrameworkElement).FindName("update.check").as_(Button).IsEnabled = False
					self.document.Content.as_(FrameworkElement).FindName("update.preview.action").as_(Button).Visibility = Visibility.Collapsed
					self.document.Content.as_(FrameworkElement).FindName("update.preview.progress").as_(ProgressRing).IsIndeterminate = True
					self.document.Content.as_(FrameworkElement).FindName("update.preview.status").as_(TextBlock).Text = "Download requested"
					self.document.Content.as_(FrameworkElement).FindName("update.preview.progress").as_(ProgressRing).Visibility = Visibility.Visible
					self.document.Content.as_(FrameworkElement).FindName("update.preview.status").as_(TextBlock).Visibility = Visibility.Visible
				elif stat['status'] == "download":
					manifest = json.load(open('updatemanifest.json'))
					self.document.Content.as_(FrameworkElement).FindName("update.preview.name").as_(TextBlock).Text = manifest['name']
					self.document.Content.as_(FrameworkElement).FindName("update.preview.build").as_(TextBlock).Text = f"Build {manifest['build']}"
					self.document.Content.as_(FrameworkElement).FindName("update.preview.info").as_(TextBox).Text = manifest['info']


					self.document.Content.as_(FrameworkElement).FindName("update.preview.size").as_(TextBlock).Text = cs(manifest['size'])
					self.document.Content.as_(FrameworkElement).FindName("update.check").as_(Button).IsEnabled = False
					self.document.Content.as_(FrameworkElement).FindName("update.preview.action").as_(Button).Visibility = Visibility.Collapsed
					self.document.Content.as_(FrameworkElement).FindName("update.preview.progress").as_(ProgressRing).IsIndeterminate = False
					self.document.Content.as_(FrameworkElement).FindName("update.preview.progress").as_(ProgressRing).Value = stat['progress']

					self.document.Content.as_(FrameworkElement).FindName("update.preview.status").as_(TextBlock).Text = f"Downloading {stat['progress']}% - {cs(os.stat("../data/.update.zip").st_size)}"
					self.document.Content.as_(FrameworkElement).FindName("update.preview.progress").as_(ProgressRing).Visibility = Visibility.Visible
					self.document.Content.as_(FrameworkElement).FindName("update.preview.status").as_(TextBlock).Visibility = Visibility.Visible
				self.lastUpdateCheck = time.time()

		if self.page == "history":
			if self.oldwidth != width:
			
				history = []
				for i in self.records:
					history.append((i.value,int(i.time/1000)))
				
				if self.records:
					makeGraph(int(width)-20,320,int(self.records[0].time),int(self.records[-1].time),self.getSetting("notify/low/level") if self.getSetting("notify/low/enabled") else None ,self.getSetting("notify/high/level") if self.getSetting("notify/high/enabled") else None,history,self.getSetting("useMGDL"))
					img = self.document.Content.as_(FrameworkElement).FindName("Graph").as_(Image)
					bitmap = Imaging.BitmapImage()
					print((os.path.abspath(os.path.join(os.getcwd(),'../data','glucose.png'))))
					bitmap.UriSource = Uri(os.path.abspath(os.path.join(os.getcwd(),'../data','glucose.png')))
					img.Source = bitmap
					self.oldwidth = width


		if (self.fetchState == 1 or self.fetchState == 2) and self.page != "oobe" and self.state == AppState.RUNNING:
			self.fetchState = 0 # Set fetch state to dsibaled
			self.showSignIn(self.goHome) # Go to the sign in page, upon success return tot ht ehome apge
			ctx = self.showPopup("Account Error",popbuilder.ok("Please check your credentials and try again"))
			PlaySoundW(PWSTR("../assets/sounds/conflict.wav"), None, SND_FILENAME | SND_ASYNC)
		elif self.fetchState == 4:
			# The fetcher could not connect to the service
			if self.page == "home":
				if self.popupShown != "ce.serviceOffline":
					self.popupShown = "ce.serviceOffline"
					ctx = self.showPopup("Connection Error",popbuilder.ok("The DeskScout service could not connect to Dexcom Share"))
					PlaySoundW(PWSTR("../assets/sounds/conflict.wav"), None, SND_FILENAME | SND_ASYNC)

					ctx.as_(FrameworkElement).FindName("popup.content.ok").as_(Button).Click += lambda sender,args: self.hidePopup()
					
				glucose = self.document.Content.as_(FrameworkElement).FindName("reading").as_(TextBlock)
				last = self.document.Content.as_(FrameworkElement).FindName("last_update").as_(TextBlock)
				trend = self.document.Content.as_(FrameworkElement).FindName("trendarrow").as_(TextBlock)
				last.Text = "Not Connected"
			return
		elif self.fetchState == 5:
			# No glucose data available
			
			if self.page == "home":
				if self.popupShown != "de.noReadings":
					self.popupShown = "de.noReadings"
					
					ctx = self.showPopup("No Glucose Data Available",popbuilder.ok("Check your Dexcom app"))
					PlaySoundW(PWSTR("../assets/sounds/conflict.wav"), None, SND_FILENAME | SND_ASYNC)
					ctx.as_(FrameworkElement).FindName("popup.content.ok").as_(Button).Click += lambda sender,args: self.hidePopup()
				glucose = self.document.Content.as_(FrameworkElement).FindName("reading").as_(TextBlock)
				last = self.document.Content.as_(FrameworkElement).FindName("last_update").as_(TextBlock)
				trend = self.document.Content.as_(FrameworkElement).FindName("trendarrow").as_(TextBlock)
				last.Text = "No Glucose Data"
				glucose.Text = "-?-"
				trend.Text = ""
				
			return
		if self.popupShown == "ce.serviceOffline":
			self.hidePopup()

		if self.page == "home" and self.state == AppState.RUNNING:
			# Update the home screen
			if self.glucose:
				#print(self.glucose)
				
				glucose = self.document.Content.as_(FrameworkElement).FindName("reading").as_(TextBlock)
				last = self.document.Content.as_(FrameworkElement).FindName("last_update").as_(TextBlock)
				trend = self.document.Content.as_(FrameworkElement).FindName("trendarrow").as_(TextBlock)
				units = self.document.Content.as_(FrameworkElement).FindName("units").as_(TextBlock)


				# Get the actual time from (Value is enclosed in Date() )
				lut = self.glucose["Timestamp"]
				
				if self.lsc != int(lut): # Has the last reading change time changed?
					ui.info("Change detected, updating display")
					self.document.Content.as_(FrameworkElement).FindName("Alert.Low").as_(TextBlock).Visbility = Visibility.Visible
					self.document.Content.as_(FrameworkElement).FindName("Alert.High").as_(TextBlock).Visbility = Visibility.Collapsed
					self.document.Content.as_(FrameworkElement).FindName("Alert.UrgentLow").as_(TextBlock).Visbility = Visibility.Collapsed
					self.document.Content.as_(FrameworkElement).FindName("Alert.UrgentLowSoon").as_(TextBlock).Visbility = Visibility.Collapsed
					self.document.Content.as_(FrameworkElement).FindName("Alert.FallingFast").as_(TextBlock).Visbility = Visibility.Collapsed
					self.document.Content.as_(FrameworkElement).FindName("Alert.RisingFast").as_(TextBlock).Visbility = Visibility.Collapsed

					self.document.Content.as_(FrameworkElement).FindName("reading").as_(TextBlock).Visbility = Visibility.Visible
					self.document.Content.as_(FrameworkElement).FindName("reading").as_(TextBlock).Text = "---"
					self.document.Content.as_(FrameworkElement).FindName("reading.red").as_(TextBlock).Visbility = Visibility.Collapsed
					self.document.Content.as_(FrameworkElement).FindName("reading.yellow").as_(TextBlock).Visbility = Visibility.Collapsed
					self.lsc = int(lut)
					# Update the display according to the users preferences
					if self.getSetting("notify/urgentLow/enabled"):
						if self.glucose['Value'] <= self.getSetting("notify/urgentLow/level"):
							glucose = self.document.Content.as_(FrameworkElement).FindName("reading.red").as_(TextBlock)
							self.document.Content.as_(FrameworkElement).FindName("reading").as_(TextBlock).Visibility = Visibility.Collapsed
					if self.getSetting("notify/low/enabled"):
						print(type(self.getSetting("notify/low/level")))

						if self.glucose['Value'] <= self.getSetting("notify/low/level"):
							print("LOWWW")
							glucose = self.document.Content.as_(FrameworkElement).FindName("reading.red").as_(TextBlock)
							self.document.Content.as_(FrameworkElement).FindName("reading").as_(TextBlock).Visibility = Visibility.Collapsed
					if self.getSetting("notify/high/enabled"):
						if self.glucose['Value'] >= self.getSetting("notify/high/level"):
							glucose = self.document.Content.as_(FrameworkElement).FindName("reading.yellow").as_(TextBlock)
							self.document.Content.as_(FrameworkElement).FindName("reading").as_(TextBlock).Visibility = Visibility.Collapsed
						
					glucose.Visibility = Visibility.Visible
					if self.getSetting("useMGDL"):
						glucose.Text = str(self.glucose['Value'])
						units.Text = "mg/dl"
					else:
						glucose.Text = str(round(self.glucose['Value']/18,1))
						units.Text = "mmol/L"

					last.Text = "Last synced reading: "+time.ctime(lut/1000)
					trends = {
						"None":"",
						"DoubleUp":chr(0xe110)*2,
						"SingleUp":chr(0xe110),
						"FortyFiveUp":chr(0xe143),
						"Flat":chr(0xe0ad),
						"FortyFiveDown":chr(0xe741),
						"SingleDown":chr(0xe1fd),
						"DoubleDown":chr(0xe1fd)*2,
					}
					#trend.FontFamily = FontFamily(os.path.abspath(os.path.join(os.getcwd(),"../assets/icons/SEGMDL2.TTF")))
					trend.Text = trends[self.glucose["Trend"]]




	def dataFetch(self):
		import time
		fetcher.info("Fetch task is online")
		while self.state == AppState.RUNNING:
			if False == True:
				#I dont even know what this was supposed to do.
				pass
			else:
				try:
					# Check the status pf the server
					resp = requests.get("http://127.0.0.1:49152/getIntent",timeout=5)
					status = json.loads(resp.text)
					print(status)
					if status['data'] != None:
						self.dispatch.append(lambda x=status['data']:self.runIntent(x))
						print("Intent added")
				except Exception as e:
					app.error(str(e))
				fetcher.info("Retrieving glucose data")
				try:
					# Check the status pf the server
					resp = requests.get("http://127.0.0.1:49152/getStatus",timeout=15)
					status = json.loads(resp.text) # Parse the server response
					serviceworker.debug(f"Server response {resp.text}")
					if status['login_state'] == "unknown":
						serviceworker.error("User not signed in, please run sign in flow")

						self.fetchState = 1 #Error
					elif status['login_state'] == "offline":
						self.fetchState = 4 #Device offline
					elif status['login_state'] == False:
						serviceworker.info("User not authenticated, authenticating")
						# Authenticate the glucose service
						resp = requests.get("http://127.0.0.1:49152/authenticate",timeout=10)
						data = json.loads(resp.text)
						if data['status'] == "ok":
							serviceworker.info("Authentication Successful")
							if self.fetchState == 4: #If the service was previously offline then:
								self.lsc = 0 #Reset the last sync reading
						else:
							self.fetchState = 2 # Authentication Failed 
							serviceworker.error("Authentication Failed")
						

					elif status['login_state'] == True:
						# Get latest glucose reading
						resp = requests.get("http://127.0.0.1:49152/getLatestReading",timeout=10)
						if resp.text:
							data = json.loads(resp.text)
							if self.fetchState == 4:
								self.lsc = 0 #Reset the last sync time
							if data['status'] == "ok":
								# Store the glucose data
								self.glucose = data['data']
								self.fetchState = 3 # Fetch OK, glucose data found
								self.lastFetch = time.time() # Updated the time of last glucose fetch
						else:
							self.fetchState = 5 #No glucose data
							
						
						
				except Exception as e:
					print("Error",e)
					self.fetchState = 4 #Could not reach service
			time.sleep(1)
		self.fetchState = 0
	def loadAsync(self,root,function,endUI,onFinish=None):
		# Add a loading page intersitital
		def dummy():
			pass
		def startLoad():
			function() #Call function after loading animation complete
			self.transitionElementContent(root,endUI,dummy if not onFinish else onFinish) #Transition to the final UI page
		# Start the loading animation
		self.transitionElementContent(root,XamlReader().Load(open("../assets/ui/loading.xaml", "r", encoding='utf-8').read()),dummy,startLoad)
	def signOut(self):
		import keyring
		#Remove password for keyring
		try:
			keyring.delete_password(USERKEY,self.getSetting("username"))
		except:
			pass
		requests.get(SERVICE_URL+"/reloadExts")
		requests.get(SERVICE_URL+"/authenticate")

		#Blank out username
		self.changeSetting("username",'""')
		#Start sign in flow
		self.showSignIn(self.setupComplete)
	def changeSetting(self,path,value):
		# Changes a setting at path to value
		try:
			#Send a POST request to the settings endpoint
			resp = requests.post("http://127.0.0.1:49152/settings",data={"action":"set","path":path,"value":value})
			data = json.loads(resp.text)
			if data['status'] == "ok":
				return True
			else:
				return False
		except:
			return False
	def getSetting(self,path):
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
	def validateSetting(self,value):
		# Check if setting response contains a value
		if isinstance(value,InvalidRequest) or isinstance(value,ServerLost):
			return False
		return True
	def initManageSoundsPage(self,onSelect=None,root=None):
		# Check if page root has been assigned
		if not root:
			root = self.document #A ssign page root to global
		back = root.Content.as_(FrameworkElement).FindName("settings.back").as_(Button)
		back.add_Click(lambda sender,args: self.transitionElementContent(root,XamlReader().Load(open("../assets/ui/settings/sounds.xaml", "r", encoding='utf-8').read()),lambda: self.initAlarmSoundSettings(root)))
		soundbox = root.Content.as_(FrameworkElement).FindName("settings.manage_sounds.sounds").as_(StackPanel)
		def prepremove(sender,args):
			if root.Content.as_(FrameworkElement).FindName("settings.manage_sounds.remove").as_(Primitives.ToggleButton).IsChecked:
				root.Content.as_(FrameworkElement).FindName("settings.manage_sounds.remove").as_(Primitives.ToggleButton).Content = "Click a sound to remove"
			else:
				root.Content.as_(FrameworkElement).FindName("settings.manage_sounds.remove").as_(Primitives.ToggleButton).Content = "Remove sound"
		def addsound(sender,args):
			# f8hw948qy708ryfuijhraeo8uht4ruipdsfhnuhnj38p94uewjdmiosfjf3rewifpadsjp
			from tkinter import filedialog
			import shutil
			fns = filedialog.askopenfilenames(filetypes=[["Wave Files",[".wav"]]])
			for x in fns:
				shutil.copy(x,os.path.join(os.getcwd(),'../assets/sounds/extern',os.path.basename(x)))
			reloadChoices()
		root.Content.as_(FrameworkElement).FindName("settings.manage_sounds.remove").as_(Primitives.ToggleButton).add_Checked(prepremove)
		root.Content.as_(FrameworkElement).FindName("settings.manage_sounds.remove").as_(Primitives.ToggleButton).add_Unchecked(prepremove)
		root.Content.as_(FrameworkElement).FindName("settings.manage_sounds.add").as_(Button).add_Click(addsound)


		internal_sounds = json.load(open("../data/default_sounds.json"))
		def soundSelected(path,internal=False):
			# No more please
			if root.Content.as_(FrameworkElement).FindName("settings.manage_sounds.remove").as_(Primitives.ToggleButton).IsChecked:
				if not internal:
					root.Content.as_(FrameworkElement).FindName("settings.manage_sounds.remove").as_(Primitives.ToggleButton).IsChecked = False
					os.remove(path)
					reloadChoices()
					return
				else:
					content = XamlReader().Load(
						"""
						<Page
xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
	  xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
	  xmlns:d="http://schemas.microsoft.com/expression/blend/2008"
	  xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006">
	<StackPanel>
		<TextBlock Text="You cannot remove this sound as its part of the app"/>
		<Button Name="popup.content.ok" Content="OK"/>
	</StackPanel>
</Page>"""
						)
				ctx = self.showPopup("Oops!",content)
				ctx.as_(FrameworkElement).FindName("popup.content.ok").as_(Button).Click += lambda sender,args: self.hidePopup()
			print("Sound selected",path)
			if onSelect:
				onSelect(path)
		def previewSelectedSound(path):
			# sound thing
			print("Sound selected to preview",path)
			PlaySoundW(PWSTR(path), None, SND_FILENAME | SND_ASYNC)
		def reloadChoices():
			#OMG I CANT KEEP COPYING AND PASTING THE DOCUMENTATION
			soundbox.Children.Clear()
			for i in internal_sounds:
				container = StackPanel()
				container.Orientation = 1
				selector = HyperlinkButton()

				selector.Content = internal_sounds[i]
				selector.add_Click(lambda sender,args,sx=i:soundSelected(sx,True))
				preview = Button()
				preview.Content = "Preview"
				selector.Tag = "internal"
				preview.add_Click(lambda sender,args,sx=i:previewSelectedSound(sx))
				container.Children.Append(selector)
				container.Children.Append(preview)
				soundbox.Children.Append(container)
			for i in os.listdir("../assets/sounds/extern"):
				i = os.path.join(os.getcwd(),'../assets/sounds/extern',i)
				container = StackPanel()
				container.Orientation = 1
				selector = HyperlinkButton()
				selector.Content = os.path.basename(i) + " (Imported)"
				selector.add_Click(lambda sender,args,sx=i:soundSelected(sx))
				preview = Button()
				preview.Content = "Preview"
				preview.add_Click(lambda sender,args,sx=i:previewSelectedSound(sx))
				container.Children.Append(selector)
				container.Children.Append(preview)
				soundbox.Children.Append(container)
		reloadChoices()

	def alterSound(self,st,path,root=None):
		if not root:
			root = self.document
		print("Alter",st,path)
		translate = {
			"uls":"urgentLowSoon",
			"ul":"urgentLow",
			"low":"low",
			"high":"high",
			"rf":"risingFast",
			"ff":"fallingFast",


		}
		self.changeSetting(f"notify/{translate[st]}/sound",'"'+path.replace('\\','/')+'"')
		self.transitionElementContent(root,XamlReader().Load(open("../assets/ui/settings/sounds.xaml", "r", encoding='utf-8').read()),lambda: self.initAlarmSoundSettings(root))


			 
	def initAlarmSoundSettings(self,root=None):
		# i dont wanna do this anymore
		if not root:
			root = self.document
		def changeSound(sid):
			self.transitionElementContent(root,XamlReader().Load(open("../assets/ui/settings/manage_sounds.xaml", "r", encoding='utf-8').read()),lambda: self.initManageSoundsPage(lambda path:self.alterSound(sid,path,root),root))
		def alertToggle(alt):
			translate = {
			"uls":"urgentLowSoon",
			"ul":"urgentLow",
			"low":"low",
			"high":"high",
			"rf":"risingFast",
			"ff":"fallingFast",


			}
			print(root.Content.as_(FrameworkElement).FindName(f"settings.sounds.alarms.{alt}.enable").as_(CheckBox).get_IsChecked())
			self.changeSetting(f"notify/{translate[alt]}/soundOn",root.Content.as_(FrameworkElement).FindName(f"settings.sounds.alarms.{alt}.enable").as_(CheckBox).IsChecked)
		back = root.Content.as_(FrameworkElement).FindName("settings.back").as_(Button)
		back.add_Click(lambda sender,args: self.transitionElementContent(root,XamlReader().Load(open("../assets/ui/settings.xaml", "r", encoding='utf-8').read()),lambda: self.initSettingsPage(root)))
		ms = root.Content.as_(FrameworkElement).FindName("settings.manage_sounds").as_(Button)
		ms.add_Click(lambda sender,args: self.transitionElementContent(root,XamlReader().Load(open("../assets/ui/settings/manage_sounds.xaml", "r", encoding='utf-8').read()),lambda: self.initManageSoundsPage(root=root)))
		alts = ["uls",'ul','low','high','ff','rf']
		translate = {
			"uls":"urgentLowSoon",
			"ul":"urgentLow",
			"low":"low",
			"high":"high",
			"rf":"risingFast",
			"ff":"fallingFast",


		}
		internal_sounds = json.load(open("../data/default_sounds.json"))

		for i in alts:
			root.Content.as_(FrameworkElement).FindName(f"settings.sounds.alarms.{i}.change").as_(Button).add_Click(lambda sender,args,i=i: changeSound(i))
			x = self.getSetting(f"notify/{translate[i]}/sound")
			
			if x:
				if x in internal_sounds:
					root.Content.as_(FrameworkElement).FindName(f"settings.sounds.alarms.{i}.name").as_(TextBlock).Text = internal_sounds[x]
				else:
					root.Content.as_(FrameworkElement).FindName(f"settings.sounds.alarms.{i}.name").as_(TextBlock).Text = os.path.basename(x)
			else:
				root.Content.as_(FrameworkElement).FindName(f"settings.sounds.alarms.{i}.name").as_(TextBlock).Text = "None"

					

			root.Content.as_(FrameworkElement).FindName(f"settings.sounds.alarms.{i}.enable").as_(CheckBox).IsChecked = self.getSetting(f"notify/{translate[i]}/soundOn")
			root.Content.as_(FrameworkElement).FindName(f"settings.sounds.alarms.{i}.enable").as_(CheckBox).add_Click(lambda sender,args,i=i: alertToggle(i))





			

	def initSettingsPage(self,root=None):
		# make it stop
		if not root:
			root = self.document
		
		class Settings:
			class general:
				autostart = root.Content.as_(FrameworkElement).FindName("settings.autostart").as_(CheckBox)
			class display:
				units = root.Content.as_(FrameworkElement).FindName("settings.display_mmol").as_(CheckBox)
			enable_alarms = root.Content.as_(FrameworkElement).FindName("settings.enable_alarms").as_(CheckBox)
			sounds = root.Content.as_(FrameworkElement).FindName("settings.change_alarm_sounds").as_(Button)

			signout = root.Content.as_(FrameworkElement).FindName("settings.signout").as_(Button)
			class alarms:
				class ul:
					enabled = root.Content.as_(FrameworkElement).FindName("settings.alarms.ul.enable").as_(CheckBox)
					value = root.Content.as_(FrameworkElement).FindName("settings.alarms.ul.value").as_(ComboBox)
					snooze = root.Content.as_(FrameworkElement).FindName("settings.alarms.uls.snooze").as_(NumberBox)
				class uls:
					enabled = root.Content.as_(FrameworkElement).FindName("settings.alarms.uls.enable").as_(CheckBox)
					snooze = root.Content.as_(FrameworkElement).FindName("settings.alarms.uls.snooze").as_(NumberBox)
				class low:
					enabled = root.Content.as_(FrameworkElement).FindName("settings.alarms.low.enable").as_(CheckBox)
					value = root.Content.as_(FrameworkElement).FindName("settings.alarms.low.value").as_(NumberBox)
					delay = root.Content.as_(FrameworkElement).FindName("settings.alarms.low.delay").as_(NumberBox)
					delaymode = root.Content.as_(FrameworkElement).FindName("settings.alarms.low.delaymode").as_(ComboBox)
					snooze = root.Content.as_(FrameworkElement).FindName("settings.alarms.low.snooze").as_(NumberBox)
					snoozemode = root.Content.as_(FrameworkElement).FindName("settings.alarms.low.snoozemode").as_(ComboBox)
				class high:
					enabled = root.Content.as_(FrameworkElement).FindName("settings.alarms.high.enable").as_(CheckBox)
					value = root.Content.as_(FrameworkElement).FindName("settings.alarms.high.value").as_(NumberBox)
					delay = root.Content.as_(FrameworkElement).FindName("settings.alarms.high.delay").as_(NumberBox)
					delaymode = root.Content.as_(FrameworkElement).FindName("settings.alarms.high.delaymode").as_(ComboBox)
					snooze = root.Content.as_(FrameworkElement).FindName("settings.alarms.high.snooze").as_(NumberBox)
					snoozemode = root.Content.as_(FrameworkElement).FindName("settings.alarms.high.snoozemode").as_(ComboBox)
				class ff:
					enabled = root.Content.as_(FrameworkElement).FindName("settings.alarms.ff.enable").as_(CheckBox)
					value = root.Content.as_(FrameworkElement).FindName("settings.alarms.ff.value").as_(NumberBox)
					trend = root.Content.as_(FrameworkElement).FindName("settings.alarms.ff.trend").as_(ComboBox)
					delay = root.Content.as_(FrameworkElement).FindName("settings.alarms.ff.delay").as_(NumberBox)
					delaymode = root.Content.as_(FrameworkElement).FindName("settings.alarms.ff.delaymode").as_(ComboBox)
					snooze = root.Content.as_(FrameworkElement).FindName("settings.alarms.ff.snooze").as_(NumberBox)
					snoozemode = root.Content.as_(FrameworkElement).FindName("settings.alarms.ff.snoozemode").as_(ComboBox)
				class rf:
					enabled = root.Content.as_(FrameworkElement).FindName("settings.alarms.rf.enable").as_(CheckBox)
					value = root.Content.as_(FrameworkElement).FindName("settings.alarms.rf.value").as_(NumberBox)
					trend = root.Content.as_(FrameworkElement).FindName("settings.alarms.rf.trend").as_(ComboBox)
					delay = root.Content.as_(FrameworkElement).FindName("settings.alarms.rf.delay").as_(NumberBox)
					delaymode = root.Content.as_(FrameworkElement).FindName("settings.alarms.rf.delaymode").as_(ComboBox)
					snooze = root.Content.as_(FrameworkElement).FindName("settings.alarms.rf.snooze").as_(NumberBox)
					snoozemode = root.Content.as_(FrameworkElement).FindName("settings.alarms.rf.snoozemode").as_(ComboBox)
			class ns:
				enabled = root.Content.as_(FrameworkElement).FindName("settings.ns.enable").as_(CheckBox)
				url = root.Content.as_(FrameworkElement).FindName("settings.ns.url").as_(TextBox)
				token = root.Content.as_(FrameworkElement).FindName("settings.ns.token").as_(TextBox)
				freq = root.Content.as_(FrameworkElement).FindName("settings.ns.period").as_(ComboBox)
				test = root.Content.as_(FrameworkElement).FindName("settings.ns.test").as_(Button)
				sync = root.Content.as_(FrameworkElement).FindName("settings.ns.sync").as_(Button)
				viewlog = root.Content.as_(FrameworkElement).FindName("settings.ns.viewlog").as_(Button)
			class overlay:
				enabled = root.Content.as_(FrameworkElement).FindName("settings.overlay.enable").as_(CheckBox)
				detect_steam = root.Content.as_(FrameworkElement).FindName("settings.overlay.detect.steam").as_(CheckBox)
				detect_fullscreen = root.Content.as_(FrameworkElement).FindName("settings.overlay.detect.fullscreen").as_(CheckBox)
				detect_process = root.Content.as_(FrameworkElement).FindName("settings.overlay.detect.process").as_(CheckBox)






			save = root.Content.as_(FrameworkElement).FindName("settings.save").as_(Button)
			change_alarm_sounds = root.Content.as_(FrameworkElement).FindName("settings.change_alarm_sounds").as_(Button)
			signout = root.Content.as_(FrameworkElement).FindName("settings.signout").as_(Button)
			closeapp = root.Content.as_(FrameworkElement).FindName("settings.closeapp").as_(Button)
			about = root.Content.as_(FrameworkElement).FindName("settings.about").as_(Button)
			class gdp:
				info = root.Content.as_(FrameworkElement).FindName("settings.gdp.info").as_(Button)
				edit = root.Content.as_(FrameworkElement).FindName("settings.gdp.edit").as_(Button)

				name= root.Content.as_(FrameworkElement).FindName("settings.gdp.name").as_(TextBlock)
			class sharing:
				discord = root.Content.as_(FrameworkElement).FindName("settings.sharing.discord.rp").as_(CheckBox)
				
		
		def saveAll(saver="manual"):
			if saver == "manual":
				ctx = self.showPopup("Saving Settings",popbuilder.progress("Please Wait...",0))

			# General Alarms
			self.lsc = -1
			self.changeSetting("autostart",Settings.general.autostart.IsChecked)
			self.changeSetting("useMGDL",not Settings.display.units.IsChecked)
			self.changeSetting("enableNotify",Settings.enable_alarms.IsChecked)
			# Urgent Low
			self.changeSetting("notify/urgentLow/enabled",Settings.alarms.ul.enabled.IsChecked)
			self.changeSetting("notify/urgentLow/level",int(Settings.alarms.ul.value.Text))
			self.changeSetting("notify/urgentLow/silence",int(Settings.alarms.ul.snooze.get_Value()*60))

			#Urgent Low Soon
			self.changeSetting("notify/urgentLowSoon/enabled",Settings.alarms.uls.enabled.IsChecked)
			self.changeSetting("notify/urgentLowSoon/silence",int(Settings.alarms.uls.snooze.get_Value()*60))

			#Low
			self.changeSetting("notify/low/enabled",Settings.alarms.low.enabled.IsChecked)
			self.changeSetting("notify/low/level",Settings.alarms.low.value.get_Value())
			print(Settings.alarms.low.delaymode.Text)
			if Settings.alarms.low.delaymode.Text == "minutes":
				if Settings.alarms.low.delay.get_Value() > 59:
					final = cap(Settings.alarms.low.delay.get_Value()/60,4)*60
				else:
					final = cap(Settings.alarms.low.delay.get_Value()*60,3600*4)
			else:

				final = cap(Settings.alarms.low.delay.get_Value(),4)*3600
			self.changeSetting('notify/low/delay',final)
			if Settings.alarms.low.snoozemode.Text == "minutes":
				if Settings.alarms.low.snooze.get_Value() > 59:
					final = cap(Settings.alarms.low.snooze.get_Value()/60,4)*60
				else:
					final = cap(Settings.alarms.low.snooze.get_Value()*60,3600*4)
			else:
				final = cap(Settings.alarms.low.snooze.get_Value(),4)*3600
			self.changeSetting('notify/low/silence',final)

			#High
			self.changeSetting("notify/high/enabled",Settings.alarms.high.enabled.IsChecked)
			self.changeSetting("notify/high/level",Settings.alarms.high.value.get_Value())
			if Settings.alarms.high.delaymode.Text == "minutes":
				if Settings.alarms.high.delay.get_Value() > 59:
					final = cap(Settings.alarms.high.delay.get_Value()/60,4)*60
				else:
					final = cap(Settings.alarms.high.delay.get_Value()*60,3600*4)
			else:

				final = cap(Settings.alarms.high.delay.get_Value(),4)*3600
			self.changeSetting('notify/high/delay',final)
			if Settings.alarms.high.snoozemode.Text == "minutes":
				if Settings.alarms.high.snooze.get_Value() > 59:
					final = cap(Settings.alarms.high.snooze.get_Value()/60,4)*60
				else:
					final = cap(Settings.alarms.high.snooze.get_Value()*60,3600*4)
			else:
				final = cap(Settings.alarms.high.snooze.get_Value(),4)*3600
			self.changeSetting('notify/high/silence',final)

			#Rising Fast
			self.changeSetting("notify/risingFast/enabled",Settings.alarms.rf.enabled.IsChecked)
			self.changeSetting("notify/risingFast/level",Settings.alarms.rf.value.get_Value())
			if Settings.alarms.rf.trend.Text == "One Arrow Up":
				self.changeSetting("notify/risingFast/arrow","one")
			elif Settings.alarms.rf.trend.Text == "Two Arrows Up":
				self.changeSetting("notify/risingFast/arrow","two")
			
			if Settings.alarms.rf.delaymode.Text == "minutes":
				if Settings.alarms.rf.delay.get_Value() > 59:
					final = cap(Settings.alarms.rf.delay.get_Value()/60,4)*60
				else:
					final = cap(Settings.alarms.rf.delay.get_Value()*60,3600*4)
			else:

				final = cap(Settings.alarms.rf.delay.get_Value(),4)*3600
			self.changeSetting('notify/risingFast/delay',final)
			if Settings.alarms.rf.snoozemode.Text == "minutes":
				if Settings.alarms.rf.snooze.get_Value() > 59:
					final = cap(Settings.alarms.rf.snooze.get_Value()/60,4)*60
				else:
					final = cap(Settings.alarms.rf.snooze.get_Value()*60,3600*4)
			else:
				final = cap(Settings.alarms.rf.snooze.get_Value(),4)*3600
			self.changeSetting('notify/risingFast/silence',final)

			#Falling Fast
			self.changeSetting("notify/fallingFast/enabled",Settings.alarms.ff.enabled.IsChecked)
			self.changeSetting("notify/fallingFast/level",Settings.alarms.ff.value.get_Value())
			if Settings.alarms.ff.trend.Text == "One Arrow Down":
				self.changeSetting("notify/fallingFast/arrow","one")
			elif Settings.alarms.ff.trend.Text == "Two Arrows Down":
				self.changeSetting("notify/fallingFast/arrow","two")
			
			if Settings.alarms.ff.delaymode.Text == "minutes":
				if Settings.alarms.ff.delay.get_Value() > 59:
					final = cap(Settings.alarms.ff.delay.get_Value()/60,4)*60
				else:
					final = cap(Settings.alarms.ff.delay.get_Value()*60,3600*4)
			else:

				final = cap(Settings.alarms.ff.delay.get_Value(),4)*3600
			self.changeSetting('notify/fallingFast/delay',final)
			if Settings.alarms.ff.snoozemode.Text == "minutes":
				if Settings.alarms.ff.snooze.get_Value() > 59:
					final = cap(Settings.alarms.ff.snooze.get_Value()/60,4)*60
				else:
					final = cap(Settings.alarms.ff.snooze.get_Value()*60,3600*4)
			else:
				final = cap(Settings.alarms.ff.snooze.get_Value(),4)*3600
			
			self.changeSetting('notify/fallingFast/silence',final)
			self.changeSetting("ns/enabled",Settings.ns.enabled.IsChecked)
			self.changeSetting("ns/url",f'"{Settings.ns.url.get_Text()}"')
			self.changeSetting("ns/token",f'"{Settings.ns.token.get_Text()}"')
			ts = {
				"As soon as possible":0,"Automatic":1,"Every 15 minutes":2,"Every hour":3,"Every 3 hours":4
			}
			self.changeSetting("ns/delay",ts[Settings.ns.freq.Text])
			overlaySettings = json.load(open('../data/overlay/setup.json'))
			self.changeSetting("overlay",Settings.overlay.enabled.IsChecked)
			overlaySettings['sources']['steam'] = Settings.overlay.detect_steam.IsChecked
			overlaySettings['sources']['processRecognition'] = Settings.overlay.detect_process.IsChecked
			overlaySettings['sources']['processRecognition'] = Settings.overlay.detect_fullscreen.IsChecked
			json.dump(overlaySettings,open('../data/overlay/setup.json','w+'))
			self.changeSetting("drp",Settings.sharing.discord.IsChecked)
			
			if saver == 'manual':
				ctx = self.showPopup("Settings saved",popbuilder.ok("Your changes have been saved"))
				ctx.as_(FrameworkElement).FindName("popup.content.ok").as_(Button).Click += lambda sender,args: self.hidePopup()
			

		# Initiaize the settings view

		# Check units
		s = self.getSetting("autostart")
		if self.validateSetting(s):
			Settings.general.autostart.IsChecked = s
		s = self.getSetting("useMGDL")
		if self.validateSetting(s):
			Settings.display.units.IsChecked = not s
		Settings.display.units.Click += lambda sender,args:saveAll('auto')
		#Alarms On?
		s = self.getSetting("enableNotify")
		if self.validateSetting(s):
			Settings.enable_alarms.IsChecked = s
		Settings.enable_alarms.Click += lambda sender,args:saveAll('auto')

		# Urgent Low Notifiactions
		s = self.getSetting("notify/urgentLow/enabled")
		if self.validateSetting(s):
			Settings.alarms.ul.enabled.IsChecked = s
		Settings.alarms.ul.enabled.Click += lambda sender,args: saveAll('auto')
		
		s = self.getSetting("notify/urgentLow/level")
		if self.validateSetting(s):
			Settings.alarms.ul.value.Text = str(s)

		
		
		s = self.getSetting("notify/urgentLow/silence")
		if self.validateSetting(s):
			Settings.alarms.ul.snooze.put_Value(s/60)

		#Urgent Low Soon

		s = self.getSetting("notify/urgentLowSoon/enabled")
		if self.validateSetting(s):
			Settings.alarms.uls.enabled.IsChecked = s
		Settings.alarms.uls.enabled.Click += lambda sender,args: saveAll('auto')
		s = self.getSetting("notify/urgentLowSoon/silence")
		if self.validateSetting(s):
			Settings.alarms.uls.snooze.put_Value(s/60)
		
		# Low Glucose
		s = self.getSetting("notify/low/enabled")
		if self.validateSetting(s):
			Settings.alarms.low.enabled.IsChecked = s
		Settings.alarms.low.enabled.Click += lambda sender,args: saveAll('auto')
		s = self.getSetting("notify/low/level")
		if self.validateSetting(s):
			Settings.alarms.low.value.Value = s
		s = self.getSetting("notify/low/delay")
		if self.validateSetting(s):
			if s == 0:
				Settings.alarms.low.delay.put_Value(s)
				Settings.alarms.low.delaymode.Text = "minutes"
			elif s < 3600:
				Settings.alarms.low.delay.put_Value(s/60)
				Settings.alarms.low.delaymode.Text = "minutes"
			else:
				Settings.alarms.low.delay.put_Value(s/3600)
				Settings.alarms.low.delaymode.Text = "hours"
		s = self.getSetting("notify/low/silence")
		if self.validateSetting(s):
			if s == 0:
				Settings.alarms.low.snooze.put_Value(s)
				Settings.alarms.low.snoozemode.Text = "minutes"
			elif s < 3600:
				Settings.alarms.low.snooze.put_Value(s/60)
				Settings.alarms.low.snoozemode.Text = "minutes"
			else:
				Settings.alarms.low.snooze.put_Value(s/3600)
				Settings.alarms.low.snoozemode.Text = "hours"
		
		# High Glucose
		s = self.getSetting("notify/high/enabled")
		if self.validateSetting(s):
			Settings.alarms.high.enabled.IsChecked = s
		Settings.alarms.high.enabled.Click += lambda sender,args: saveAll('auto')
		
		s = self.getSetting("notify/high/level")
		if self.validateSetting(s):
			print()
			Settings.alarms.high.value.put_Value(s)
		s = self.getSetting("notify/high/delay")
		if self.validateSetting(s):
			if s == 0:
				Settings.alarms.high.delay.put_Value(s)
				Settings.alarms.high.delaymode.Text = "minutes"
			elif s < 3600:
				Settings.alarms.high.delay.put_Value(s/60)
				Settings.alarms.high.delaymode.Text = "minutes"
			else:
				Settings.alarms.high.delay.put_Value(s/3600)
				Settings.alarms.high.delaymode.Text = "hours"
		s = self.getSetting("notify/high/silence")
		if self.validateSetting(s):
			if s == 0:
				Settings.alarms.high.snooze.put_Value(s)
				Settings.alarms.high.snoozemode.Text = "minutes"
			elif s < 3600:
				Settings.alarms.high.snooze.put_Value(s/60)
				Settings.alarms.high.snoozemode.Text = "minutes"
			else:
				Settings.alarms.high.snooze.put_Value(s/3600)
				Settings.alarms.high.snoozemode.Text = "hours"
		

		# Rising Fast

		s = self.getSetting("notify/risingFast/enabled")
		if self.validateSetting(s):
			Settings.alarms.rf.enabled.IsChecked = s
		Settings.alarms.rf.enabled.Click += lambda sender,args: saveAll('auto')
		
		s = self.getSetting("notify/risingFast/level")
		if self.validateSetting(s):
			Settings.alarms.rf.value.Text = str(s)
		s = self.getSetting("notify/risingFast/arrow")
		if self.validateSetting(s):
			if s == "one":
				Settings.alarms.rf.trend.Text = "One Arrow Up"
			elif s == "two":
				Settings.alarms.rf.trend.Text = "Two Arrows Up"

		s = self.getSetting("notify/risingFast/delay")
		if self.validateSetting(s):
			if s == 0:
				Settings.alarms.rf.delay.put_Value(s)
				Settings.alarms.rf.delaymode.Text = "minutes"
			elif s < 3600:
				Settings.alarms.rf.delay.put_Value(s/60)
				Settings.alarms.rf.delaymode.Text = "minutes"
			else:
				Settings.alarms.rf.delay.put_Value(s/3600)
				Settings.alarms.rf.delaymode.Text = "hours"
		s = self.getSetting("notify/risingFast/silence")
		if self.validateSetting(s):
			if s == 0:
				Settings.alarms.rf.snooze.put_Value(s)
				Settings.alarms.rf.snoozemode.Text = "minutes"
			elif s < 3600:
				Settings.alarms.rf.snooze.put_Value(s/60)
				Settings.alarms.rf.snoozemode.Text = "minutes"
			else:
				Settings.alarms.rf.snooze.put_Value(s/3600)
				Settings.alarms.rf.snoozemode.Text = "hours"
		

		# Falling Fast
		s = self.getSetting("notify/fallingFast/enabled")
		if self.validateSetting(s):
			Settings.alarms.ff.enabled.IsChecked = s
		Settings.alarms.ff.enabled.Click += lambda sender,args: saveAll('auto')
		
		s = self.getSetting("notify/fallingFast/level")
		if self.validateSetting(s):
			Settings.alarms.ff.value.Text = str(s)
		s = self.getSetting("notify/fallingFast/arrow")
		if self.validateSetting(s):
			if s == "one":
				Settings.alarms.ff.trend.Text = "One Arrow Up"
			elif s == "two":
				Settings.alarms.ff.trend.Text = "Two Arrows Up"

		s = self.getSetting("notify/fallingFast/delay")
		if self.validateSetting(s):
			if s == 0:
				Settings.alarms.ff.delay.put_Value(s)
				Settings.alarms.ff.delaymode.Text = "minutes"
			elif s < 3600:
				Settings.alarms.ff.delay.put_Value(s/60)
				Settings.alarms.ff.delaymode.Text = "minutes"
			else:
				Settings.alarms.ff.delay.put_Value(s/3600)
				Settings.alarms.ff.delaymode.Text = "hours"
		s = self.getSetting("notify/fallingFast/silence")
		if self.validateSetting(s):
			if s == 0:
				Settings.alarms.ff.snooze.put_Value(s)
				Settings.alarms.ff.snoozemode.Text = "minutes"
			elif s < 3600:
				Settings.alarms.ff.snooze.put_Value(s/60)
				Settings.alarms.ff.snoozemode.Text = "minutes"
			else:
				Settings.alarms.ff.snooze.put_Value(s/3600)
				Settings.alarms.ff.snoozemode.Text = "hours"
		s = self.getSetting("notify/risingFast/arrow")
		if self.validateSetting(s):
			if s == "one":
				Settings.alarms.rf.trend.Text = "One Arrow Down"
			elif s == "two":
				Settings.alarms.rf.trend.Text = "Two Arrows Down"
		s = self.getSetting("ns/enabled")
		if self.validateSetting(s):
			Settings.ns.enabled.IsChecked = s
		s = self.getSetting("ns/url")
		if self.validateSetting(s):
			Settings.ns.url.Text = s
		s = self.getSetting("ns/token")
		if self.validateSetting(s):
			Settings.ns.token.Text = s
		s = self.getSetting("ns/delay")
		if self.validateSetting(s):
			vx = ["As soon as possible","Automatic","Every 15 minutes","Every hour","Every 3 hours"]
			Settings.ns.freq.Text = vx[s]
		s = self.getSetting("overlay")
		if self.validateSetting(s):
			Settings.overlay.enabled.IsChecked = s
		s = self.getSetting("drp")
		if self.validateSetting(s):
			Settings.sharing.discord.IsChecked = s
		Settings.overlay.enabled.Click += lambda sender,args: saveAll('auto')
		Settings.sharing.discord.Click += lambda sender,args: saveAll('auto')
		Settings.general.autostart.Click += lambda sender,args: saveAll('auto')


		Settings.overlay.detect_steam.Click += lambda sender,args: saveAll('auto')
		Settings.overlay.detect_process.Click += lambda sender,args: saveAll('auto')
		Settings.overlay.detect_fullscreen.Click += lambda sender,args: saveAll('auto')
		overlaySettings = json.load(open('../data/overlay/setup.json'))
		Settings.overlay.detect_steam.IsChecked = overlaySettings['sources']['steam']
		Settings.overlay.detect_process.IsChecked = overlaySettings['sources']['processRecognition']
		Settings.overlay.detect_fullscreen.IsChecked = overlaySettings['sources']['fullscreen']
		uri = Uri.CreateUri(os.path.abspath(os.path.join(os.getcwd(),"../","assets",'drp_example.png')))
		
		# Create the SvgImageSource

		# Create ImageBrush and set properties
		img = self.document.Content.as_(FrameworkElement).FindName("DRPImage").as_(Image)
		bitmap = Imaging.BitmapImage()
		bitmap.UriSource = uri
		img.Source = bitmap


		try:
			resp = requests.get(SERVICE_URL+"/extInfo")
			gdp = self.getSetting("gdp")
			exts = json.loads(resp.text)['data']
			print(exts)
			for i in exts:
				if i['uuid'] == gdp:
					Settings.gdp.name.Text = i["name"]
					break
			else:
				raise Exception()
		except:
			Settings.gdp.name.Text = "Error"
		def urlFilter(sender,args):
			try:
				from urllib.parse import urlparse, parse_qs,urlunparse
				parsed_url = urlparse(Settings.ns.url.Text)

				# Get query parameters as a dictionary of lists
				params = parse_qs(parsed_url.query)
				if "token" in params:
					print(params)
					Settings.ns.token.Text = params['token'][0]
					Settings.ns.url.Text = urlunparse(parsed_url._replace(query=""))
			except Exception as e:
				print(e)
		def aboutPage(sender,args):
			self.page = "about"
			self.transitionElementContent(root,XamlReader().Load(open("../assets/ui/loading.xaml", "r", encoding='utf-8').read()),lambda: print(),self.initAboutPage)
		def shutdown():
			import psutil
			try:
				requests.get("http://127.0.0.1:49152/shutdown")
			except:
				pass
			self.state = 0
			p = psutil.Process(os.getpid())
			for proc in p.children(recursive=True):
				proc.kill()
			p.kill()
		def soundsPage():
			self.transitionElementContent(root,XamlReader().Load(open("../assets/ui/settings/sounds.xaml", "r", encoding='utf-8').read()),lambda: self.initAlarmSoundSettings(root))
		def extInfoPage():
			self.transitionElementContent(root,XamlReader().Load(open("../assets/ui/loading.xaml", "r", encoding='utf-8').read()),lambda: print(),self.initExtensionInfoPage)
		def editGDP():
			from win32more.Windows.Win32.UI.WindowsAndMessaging import (
			GetForegroundWindow,
			SetForegroundWindow,
			FindWindowW,
			ShowWindow,
			IsIconic,
			SW_RESTORE,
			SW_HIDE,
			SW_MINIMIZE,
			SW_SHOW
			)
			ShowWindow(self.hwnd, SW_HIDE)
			resp = subprocess.run("../core/pythonw.exe DeskScoutSetup.py setGDP")
			ShowWindow(self.hwnd, SW_SHOW)
			SetForegroundWindow(self.hwnd)
			try:
				resp = requests.get(SERVICE_URL+"/extInfo")
				gdp = self.getSetting("gdp")
				exts = json.loads(resp.text)['data']
				print(exts)
				for i in exts:
					if i['uuid'] == gdp:
						Settings.gdp.name.Text = i["name"]
						break
				else:
					raise Exception()
			except:
				Settings.gdp.name.Text = "Error"
		def checkNS(sender,args):
			from mods import nightscout
			ns = nightscout.NightScout(self.getSetting("ns/url"),self.getSetting("ns/token"))
			saveAll('auto')
			try:
				resp = ns.checkToken()
				if resp == 2:
					ctx = self.showPopup("Connection successful",popbuilder.ok("We can connect to your Nightscout instance"))
					ctx.as_(FrameworkElement).FindName("popup.content.ok").as_(Button).Click += lambda sender,args: self.hidePopup()
				elif resp == 1:
					ctx = self.showPopup("Permission error",popbuilder.ok("We can connect to your Nightscout instance, but the token lacks write permissions"))
					ctx.as_(FrameworkElement).FindName("popup.content.ok").as_(Button).Click += lambda sender,args: self.hidePopup()
				elif resp == 0:
					ctx = self.showPopup("Connection unsuccessful",popbuilder.ok("We can't connect to your Nightscout instance"))
					ctx.as_(FrameworkElement).FindName("popup.content.ok").as_(Button).Click += lambda sender,args: self.hidePopup()

			except Exception as e:
				ctx = self.showPopup("Oops! We couldn't reach your Nighscout",popbuilder.ok(f"{str(e)}"))
				ctx.as_(FrameworkElement).FindName("popup.content.ok").as_(Button).Click += lambda sender,args: self.hidePopup()

		Settings.ns.url.Paste += urlFilter
		Settings.ns.url.TextChanged += urlFilter
		root.Content.as_(FrameworkElement).FindName("settings.change_alarm_sounds").as_(Button).add_Click(lambda sender,args:soundsPage())

		root.Content.as_(FrameworkElement).FindName("settings.signout").as_(Button).add_Click(lambda sender,args:self.signOut())
		root.Content.as_(FrameworkElement).FindName("settings.closeapp").as_(Button).add_Click(lambda sender,args:shutdown())
		root.Content.as_(FrameworkElement).FindName("settings.save").as_(Button).add_Click(lambda sender,args:saveAll())
		Settings.gdp.info.add_Click(lambda sender,args:extInfoPage())
		Settings.gdp.edit.add_Click(lambda sender,args:editGDP())



		Settings.ns.test.Click += checkNS
		#Settings.ns.viewlog.Click += self.NotImplemented
		#Settings.ns.sync.Click += self.NotImplemented





		root.Content.as_(FrameworkElement).FindName("settings.about").as_(Button).add_Click(aboutPage)
		return Settings()
	def initExtensionInfoPage(self):
		gdp = self.getSetting("gdp")
		resp = requests.get(SERVICE_URL+"/extInfo")
		if resp.status_code == 200:
			try:
				exts = json.loads(resp.text)['data']
				print(exts)
				for i in exts:
					if i['uuid'] == gdp:
						info = i
						break
				else:
					raise Exception()
			except:
				content = XamlReader().Load(
					"""
					<Page
xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
	xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
	xmlns:d="http://schemas.microsoft.com/expression/blend/2008"
	xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006">
<StackPanel>
	<TextBlock Text="Could not load info"/>
	<Button Name="popup.content.ok" Content="OK"/>
</StackPanel>
</Page>"""
					)
				self.transitionElementContent(self.document,XamlReader().Load(open("../assets/ui/settings.xaml", "r", encoding='utf-8').read()),self.initSettingsPage)
				ctx = self.showPopup("Error",content)
				ctx.as_(FrameworkElement).FindName("popup.content.ok").Click += lambda sender,args: self.hidePopup()
				PlaySoundW(PWSTR("../assets/sounds/conflict.wav"), None, SND_FILENAME | SND_ASYNC)
				
				return
			def showExtInfo():
				back = self.document.Content.as_(FrameworkElement).FindName("settings.back").as_(Button)
				back.add_Click(lambda sender,args: self.transitionElementContent(self.document,XamlReader().Load(open("../assets/ui/settings.xaml", "r", encoding='utf-8').read()),lambda: self.initSettingsPage()))
				
				self.document.Content.as_(FrameworkElement).FindName("extinfo.name").as_(TextBlock).Text = f"Name: {i['name']}"
				self.document.Content.as_(FrameworkElement).FindName("extinfo.version").as_(TextBlock).Text = f"Version: {i['version']}"
				self.document.Content.as_(FrameworkElement).FindName("extinfo.id").as_(TextBlock).Text = f"{i['id']}"
				self.document.Content.as_(FrameworkElement).FindName("extinfo.serviceName").as_(TextBlock).Text = f"Service Name: {i['serviceName']}"

				self.document.Content.as_(FrameworkElement).FindName("extinfo.author").as_(TextBlock).Text = f"Author: {i['author']}"
				self.document.Content.as_(FrameworkElement).FindName("extinfo.desc").as_(TextBlock).Text = f"{i['short']}"

			self.transitionElementContent(self.document,XamlReader().Load(open("../assets/ui/extinfo.xaml", "r", encoding='utf-8').read()),showExtInfo)
			
		
	def doImportData(self):
		pass
	def initDataImportPage(self):
		back = self.document.Content.as_(FrameworkElement).FindName("settings.back").as_(Button)
		
		run = self.document.Content.as_(FrameworkElement).FindName("import.start").as_(Button)
		def backupData():
			subprocess.run("../core/pythonw.exe DeskScoutSetup.py restore")

			self.transitionElementContent(self.document,XamlReader().Load(open("../assets/ui/data_manage.xaml", "r", encoding='utf-8').read()),self.initDataManagement)
		def start(sender,args):
			
			self.loadAsync(self.document,lambda :backupData(),XamlReader().Load(open("../assets/ui/data_manage.xaml", "r", encoding='utf-8').read()),self.initDataManagement)
		run.add_Click(start)
		back.add_Click(lambda sender,args: self.transitionElementContent(self.document,XamlReader().Load(open("../assets/ui/data_manage.xaml", "r", encoding='utf-8').read()),lambda: self.initDataManagement()))
	def initDataBackupPage(self):
		
		back = self.document.Content.as_(FrameworkElement).FindName("settings.back").as_(Button)
		run = self.document.Content.as_(FrameworkElement).FindName("backup.start").as_(Button)
		def backupData(path):
			subprocess.run(f"../core/pythonw.exe dataexport.py \"{path}\"")
			self.transitionElementContent(self.document,XamlReader().Load(open("../assets/ui/data_manage.xaml", "r", encoding='utf-8').read()),self.initDataManagement)
		def start(sender,args):
			from tkinter import filedialog
			ans = filedialog.asksaveasfilename(filetypes=[["Zip Archive",['.zip']]])
			if not ans:
				return
			self.loadAsync(self.document,lambda a=ans:backupData(a),XamlReader().Load(open("../assets/ui/data_manage.xaml", "r", encoding='utf-8').read()),self.initDataManagement)
		run.add_Click(start)
		back.add_Click(lambda sender,args: self.transitionElementContent(self.document,XamlReader().Load(open("../assets/ui/data_manage.xaml", "r", encoding='utf-8').read()),lambda: self.initDataManagement()))
		
	def initDataManagement(self):
		# peeved.
		def cs(v):
			if v < 1024:
				return str(v)+" B"
			elif v >= 1024 and v < 1_000_024:
				return str(round(v/1024))+" KB"
			elif v > 1_000_024  < 1_000_000_024:
				return str(round(v/1e+6,2))+" MB"
			elif v >= 1_000_000_024:
				return str(round(v/1e+9,2))+" GB"
		def loadContent():
			space = 0
			space2 = 0
			space3 = 0
			space += os.stat(os.path.abspath("../data/settings.json")).st_size
			space2 += 0
			space2 += os.stat(os.path.abspath("app_boot.log")).st_size
			for root,dirs,files in os.walk("../data/glucose"):
				print(root,dirs,files)
				for i in files:
					space3 += os.stat(os.path.join(root,i)).st_size
				



			for root,dirs,files in os.walk(os.path.abspath("../assets/sounds")):
				for i in files:
					space += os.stat(os.path.join(root,i)).st_size
			self.document.Content.as_(FrameworkElement).FindName("dm.glucose_usage").as_(TextBlock).Text = f"Usage: {cs(os.stat(os.path.abspath("../data/glucose.gdr")).st_size+space3)}"

			self.document.Content.as_(FrameworkElement).FindName("dm.app_usage").as_(TextBlock).Text = f"Usage: {cs(space)}"
			self.document.Content.as_(FrameworkElement).FindName("dm.log_usage").as_(TextBlock).Text = f"Usage: {cs(space2)}"


			backup = self.document.Content.as_(FrameworkElement).FindName("dm.backup").as_(Button)
			backup.add_Click(lambda sender,args: self.transitionElementContent(self.document,XamlReader().Load(open("../assets/ui/settings/backup.xaml", "r", encoding='utf-8').read()),self.initDataBackupPage))

			dataImport = self.document.Content.as_(FrameworkElement).FindName("dm.import").as_(Button)
			dataImport.add_Click(lambda sender,args: self.transitionElementContent(self.document,XamlReader().Load(open("../assets/ui/settings/import.xaml", "r", encoding='utf-8').read()),self.initDataImportPage))
			
			
			back = self.document.Content.as_(FrameworkElement).FindName("dm.back").as_(Button)
			back.add_Click(lambda sender,args: self.transitionElementContent(self.document,XamlReader().Load(open("../assets/ui/loading.xaml", "r", encoding='utf-8').read()),self.initAboutPage))
		self.transitionElementContent(self.document,XamlReader().Load(open("../assets/ui/data_manage.xaml", "r", encoding='utf-8').read()),loadContent)
	def initNetworkLogPage(self):
		back = self.document.Content.as_(FrameworkElement).FindName("settings.back").as_(Button)
		back.add_Click(lambda sender,args: self.transitionElementContent(self.document,XamlReader().Load(open("../assets/ui/loading.xaml", "r", encoding='utf-8').read()),self.initAboutPage))
		logselect = self.document.Content.as_(FrameworkElement).FindName("logs.logselect").as_(ComboBox)
		logview = self.document.Content.as_(FrameworkElement).FindName("logs.logdata").as_(TextBox)
		def onLogChange(sender,args):
			if sender.as_(ComboBox).SelectedIndex == 0:
				print("Logs change")
		logselect.SelectionChanged += onLogChange
		logview.Text = open('netlogs/service.log').read()
	def initAppLogPage(self):
		back = self.document.Content.as_(FrameworkElement).FindName("settings.back").as_(Button)
		back.add_Click(lambda sender,args: self.transitionElementContent(self.document,XamlReader().Load(open("../assets/ui/loading.xaml", "r", encoding='utf-8').read()),self.initAboutPage))
		logview = self.document.Content.as_(FrameworkElement).FindName("logs.logdata").as_(TextBox)
		logview.Text = open('app_boot.log').read()
	def initOpenSourceLicensePage(self):
		osl = json.load(open("../data/osl.json"))
		box = self.document.Content.as_(FrameworkElement).FindName("osl.main").as_(StackPanel)
		def loadLicense(n,path):
			name = self.document.Content.as_(FrameworkElement).FindName("osl.name").as_(TextBlock)
			lx = self.document.Content.as_(FrameworkElement).FindName("osl.license").as_(TextBox)
			name.Text = n
			lx.Text = open(path,'r').read()
			back = self.document.Content.as_(FrameworkElement).FindName("settings.back").as_(Button)
			back.add_Click(lambda sender,args: self.transitionElementContent(self.document,XamlReader().Load(open("../assets/ui/osl/main.xaml", "r", encoding='utf-8').read()),self.initOpenSourceLicensePage))
		for i in osl:
			button = Button()
			button.Content = i
			button.add_Click(lambda sender,args,n=i,p=osl[i]: self.transitionElementContent(self.document,XamlReader().Load(open("../assets/ui/osl/view.xaml",'r',encoding='utf-8').read()),lambda:loadLicense(n,p)))
			box.Children.Append(button)
		back = self.document.Content.as_(FrameworkElement).FindName("settings.back").as_(Button)
		back.add_Click(lambda sender,args:self.transitionElementContent(self.document,XamlReader().Load(open("../assets/ui/loading.xaml", "r", encoding='utf-8').read()),lambda: print(),self.initAboutPage))
		
	def showPopup(self,title,content):
		popup = self.win.Content.as_(FrameworkElement).FindName('popup').as_(Frame)
		_title = self.win.Content.as_(FrameworkElement).FindName('popup.title').as_(TextBlock)
		_content = self.win.Content.as_(FrameworkElement).FindName('popup.content').as_(Frame)
		_content.Content = content
		
		_title.Text = title
		popup.Visibility = Visibility.Visible
		popup.Opacity = 0
		def opaci(elapsed,data):
			if data['i'] != 100:
				popup = data['s'].win.Content.as_(FrameworkElement).FindName('popup').as_(Frame)
				popup.Opacity = data['i']*0.01
				data['i'] += 10
				return self.raf.Respond(data)
			else:
				popup = data['s'].win.Content.as_(FrameworkElement).FindName('popup').as_(Frame)

				popup.Opacity = 1

				return self.raf.Respond(data,True)
				
		self.raf.request_animation_frame(opaci,{'i':0,"s":self})
		return _content.Content
	def hidePopup(self):
		popup = self.win.Content.as_(FrameworkElement).FindName('popup').as_(Frame)
		def opaci(elapsed,data):
			if data['i'] != 100:
				popup = data['s'].win.Content.as_(FrameworkElement).FindName('popup').as_(Frame)
				popup.Opacity = (100-data['i'])*0.01
				data['i'] += 10
				return self.raf.Respond(data)
			else:
				popup = data['s'].win.Content.as_(FrameworkElement).FindName('popup').as_(Frame)

				popup.Visibility = Visibility.Collapsed

				return self.raf.Respond(data,True)
				
		self.raf.request_animation_frame(opaci,{'i':0,"s":self})
	def initUpdatePage(self):
		try:
			requests.get(SERVICE_URL+"/checkForUpdate")
		except:
			pass
		self.page = "update"
		back = self.document.Content.as_(FrameworkElement).FindName("settings.back").as_(Button)
		def goBack(sender,adrgs):
			self.page = ""
			self.transitionElementContent(self.document,XamlReader().Load(open("../assets/ui/loading.xaml", "r", encoding='utf-8').read()),self.initAboutPage)
		back.add_Click(goBack)
		cfu = self.document.Content.as_(FrameworkElement).FindName("update.check").as_(Button)
		self.document.Content.as_(FrameworkElement).FindName("update.preview.action").as_(Button).Click += lambda sender,args: self.updateButtonHandler()
		def checkForUpdate(sender,args):
			try:
				requests.get(SERVICE_URL+"/checkForUpdate")
			except:
				pass
		cfu.add_Click(checkForUpdate)
		




	def initAboutPage(self):
		# splish splah i was updatin some text
		self.NavView.SelectedItem = None
		serverinfo = {}

		def loadContent():
			self.document.Content.as_(FrameworkElement).FindName("about.appversion").as_(TextBlock).Text = f"App Build: {json.load(open("versioninfo.json"))['app']}"
			self.document.Content.as_(FrameworkElement).FindName("about.version").as_(TextBlock).Text = f"Version: {__version__}"
			self.document.Content.as_(FrameworkElement).FindName("about.build").as_(TextBlock).Text = f"Build: {__build__}"
			self.document.Content.as_(FrameworkElement).FindName("about.release").as_(TextBlock).Text = f"Release: {__release__}"
			
			self.document.Content.as_(FrameworkElement).FindName("about.platform").as_(TextBlock).Text = f"Platform: {sys.platform}"
			self.document.Content.as_(FrameworkElement).FindName("about.reset").as_(Button).add_Click(reset)
			self.document.Content.as_(FrameworkElement).FindName("about.server_version").as_(TextBlock).Text = f"Version: {serverinfo['version']}"
			if serverinfo['build'] in supported_service:
				self.document.Content.as_(FrameworkElement).FindName("about.server_build").as_(TextBlock).Text = f"Build: {serverinfo['build']}"
			else:
				self.document.Content.as_(FrameworkElement).FindName("about.server_build").as_(TextBlock).Text = f"Build: {serverinfo['build']} (Potential compatibility issue)"

			self.document.Content.as_(FrameworkElement).FindName("about.server_release").as_(TextBlock).Text = f"Release: {serverinfo['release']}"
			self.document.Content.as_(FrameworkElement).FindName("about.server_channel").as_(TextBlock).Text = f"Channel: {serverinfo['channel']}"
			# I want to speak to the manager, the data manager
			self.document.Content.as_(FrameworkElement).FindName("about.datamanage").as_(Button).add_Click(lambda sender,args: self.transitionElementContent(self.document,XamlReader().Load(open("../assets/ui/loading.xaml", "r", encoding='utf-8').read()),lambda: print(),self.initDataManagement))
			self.document.Content.as_(FrameworkElement).FindName("about.logs").as_(Button).add_Click(lambda sender,args: self.transitionElementContent(self.document,XamlReader().Load(open("../assets/ui/logs/network.xaml", "r", encoding='utf-8').read()),self.initNetworkLogPage))
			self.document.Content.as_(FrameworkElement).FindName("about.alog").as_(Button).add_Click(lambda sender,args: self.transitionElementContent(self.document,XamlReader().Load(open("../assets/ui/logs/app.xaml", "r", encoding='utf-8').read()),self.initAppLogPage))
			self.document.Content.as_(FrameworkElement).FindName("about.osl").as_(Button).add_Click(lambda sender,args: self.transitionElementContent(self.document,XamlReader().Load(open("../assets/ui/osl/main.xaml", "r", encoding='utf-8').read()),self.initOpenSourceLicensePage))
			self.document.Content.as_(FrameworkElement).FindName("about.update").as_(Button).add_Click(lambda sender,args: self.transitionElementContent(self.document,XamlReader().Load(open("../assets/ui/settings/update.xaml", "r", encoding='utf-8').read()),self.initUpdatePage))


			
			back = self.document.Content.as_(FrameworkElement).FindName("settings.back").as_(Button)
			back.add_Click(lambda sender,args: self.transitionElementContent(self.document,XamlReader().Load(open("../assets/ui/settings.xaml", "r", encoding='utf-8').read()),self.initSettingsPage))
		

		def reset(sender,args):
			# So maybe we could, start all over, start all over again
			import keyring,subprocess
			self.NavView.put_IsPaneVisible(False)
			self.transitionElementContent(self.document,XamlReader().Load(open("../assets/ui/loading.xaml", "r", encoding='utf-8').read()),lambda: subprocess.Popen("../core/pythonw.exe resetApp.py -quiet -autostart",start_new_session=True))
			

			
			
		resp = requests.get("http://127.0.0.1:49152/about")
		serverinfo = json.loads(resp.text)
		self.transitionElementContent(self.document,XamlReader().Load(open("../assets/ui/about.xaml", "r", encoding='utf-8').read()),loadContent)
		
	def initHistoryPage(self):
		from win32more.Microsoft.UI.Xaml.Controls import CalendarDatePicker,DatePicker
		from win32more.Windows.UI.Xaml import RoutedEventHandler
		from win32more.Windows.Foundation import DateTime
		import datetime
		WINRT_EPOCH = datetime.datetime(1601, 1, 1)
		def seconds_to_winrt(seconds: float) -> DateTime:
			unix_epoch = datetime.datetime(1970, 1, 1)
			offset = (unix_epoch - WINRT_EPOCH).total_seconds()  # seconds between 1601 and 1970
			total_seconds = seconds + offset
			ticks = int(total_seconds * 10_000_000)  # 10^7 ticks per second
			dt = DateTime()
			dt.UniversalTime = ticks
			return dt

		# Convert WinRT DateTime back to seconds since Unix epoch
		def winrt_to_seconds(winrt_datetime: DateTime) -> float:
			unix_epoch = datetime.datetime(1970, 1, 1)
			offset = (unix_epoch - WINRT_EPOCH).total_seconds()
			return (winrt_datetime.UniversalTime / 10_000_000) - offset
		dates = []
		def pushData():
			from win32more.Microsoft.UI.Xaml.Controls import TextBlock, ToolTip,ComboBoxItem
			from win32more.Microsoft.UI.Xaml.Controls import ToolTipService
			area = self.document.Content.as_(FrameworkElement).FindName("History").as_(StackPanel)
			avg = 0

			area.Children.Clear()
			TREND_ARROWS: list[str] = ["", "↑↑", "↑", "↗", "→", "↘", "↓", "↓↓", "?", "-"]
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
			
			unit = self.getSetting("useMGDL")
			last = None
			seen = []
			date_picker = self.document.Content.as_(FrameworkElement).FindName("DatePicker").as_(ComboBox)
			i2 = 0
			print(dates,'almanac')
			for i in dates:
				item = ComboBoxItem()
				item.Content = i
				try:
					tx = time.localtime(float(records[0].time/1000))
					
					
					print(i, f"{tx.tm_mon}-{tx.tm_mday if tx.tm_mday > 10 else str(f'0{tx.tm_mday}')}-{tx.tm_year}" )
					if f"{tx.tm_mon if tx.tm_mon > 9 else str(f'0{tx.tm_mon}')}-{tx.tm_mday if tx.tm_mday > 10 else str(f'0{tx.tm_mday}')}-{tx.tm_year}" == i:
						item.IsSelected = True
				except:
					pass
				date_picker.Items.Append(item)
			gap = False
			for x in records:
				tx = time.localtime(float(x.time/1000))
				avg += x.value
				if int(x.time/1000) in seen:
					continue
				else:
					seen.append(int(x.time/1000))


				# Container for the individual record
				entry_container = StackPanel()
				entry_container.Orientation = 1

				# Timestamp
				timestamp = TextBlock()
				timestamp.Text = time.strftime("%I:%M %p", tx)

				# Glucose reading
				glucose = TextBlock()
				glucose.FontSize = 24
				glucose.Text = f"{x.value} mg/dl" if unit else f"{round(x.value / 18, 1)} mmol/L"

				# Trend info
				trend = TextBlock()
				trend.FontSize = 24
				trend.Text = TREND_ARROWS[x.trendArrow]

				tooltip = ToolTip()
				tooltip.Content = TREND_DESCRIPTIONS[x.trendArrow]
				ToolTipService.SetToolTip(trend, tooltip)

				# Add spacing and elements
				for element in (timestamp, glucose, trend):
					spacer = Border()
					spacer.Width = 32
					entry_container.Children.Append(spacer)
					entry_container.Children.Append(element)

				# Append entry to page
				area.Children.Append(entry_container)

				# Spacer between records
				if x != records[-1]:
					spacer = Border()
					spacer.Height = 8
					area.Children.Append(spacer)
				gap = False
				for i in range(0,len(records),2):
					y = records[i:i+2]
					try:
						if -(int(y[1].time)-int(y[0].time)) > 3600:
							gap = True
							break
					except:
						pass
						
			if gap:
				print("GAP")
				self.document.Content.as_(FrameworkElement).FindName("GapDisclaimer").as_(InfoBar).IsOpen = True

			if len(records) < 72 and records:
				self.document.Content.as_(FrameworkElement).FindName("LowDataDisclaimer").as_(InfoBar).IsOpen = True
				self.document.Content.as_(FrameworkElement).FindName("LowDataDisclaimer").as_(InfoBar).Message = f"You only have {int(len(records)/12)} hours of data. Insights, predictions, and averages will not be correct"
			elif not records:
				self.document.Content.as_(FrameworkElement).FindName("LowDataDisclaimer").as_(InfoBar).IsOpen = True
				self.document.Content.as_(FrameworkElement).FindName("LowDataDisclaimer").as_(InfoBar).Message = f"No glucose data was recorded"
			def update(sender,args):
				records.clear()

				date = dates[sender.as_(ComboBox).SelectedIndex].split('-')
				dates.clear()
				today = datetime.datetime(int(date[2]), int(date[0]), int(date[1]), 0, 0).timestamp()
				self.loadAsync(self.document,lambda: loadData(int(today)),XamlReader().Load(open("../assets/ui/history.xaml", "r", encoding='utf-8').read()),pushData)
			davg = self.document.Content.as_(FrameworkElement).FindName("DailyAverage").as_(TextBlock)
			readings = self.document.Content.as_(FrameworkElement).FindName("Readings").as_(TextBlock)
			if records:
				davg.Text = f"Average: {int(avg/len(records)) if unit else round((avg/len(records))/18,1)}{'mg/dl' if unit else 'mmol/L'}"
				readings.Text = f"({len(seen)} readings / {int((len(seen)/288)*100)}%)"
			date_picker.SelectionChanged += update
			history = []
			records.reverse()
			self.records = records
			self.oldwidth = int(self.win.Content.as_(FrameworkElement).ActualWidth)

			for i in records:
				history.append((i.value,int(i.time)))
			
			if records:
				makeGraph(int(self.win.Content.as_(FrameworkElement).ActualWidth)-20,320,int(records[0].time),int(records[-1].time),self.getSetting("notify/low/level") if self.getSetting("notify/low/enabled") else None ,self.getSetting("notify/high/level") if self.getSetting("notify/high/enabled") else None,history,self.getSetting("useMGDL"))
				img = self.document.Content.as_(FrameworkElement).FindName("Graph").as_(Image)
				bitmap = Imaging.BitmapImage()
				bitmap.UriSource = Uri(os.path.join(os.getcwd(),'../data','glucose.png'))
				img.Source = bitmap
			self.page = "history"
		def loadData(date):
			self.page = ""
			dy = time.strftime("%Y-%m-%d",time.localtime(date))
			from mods import gdr
			# Create the drop down
			for dx in os.listdir("../data/glucose/daily"):
				parsed = os.path.splitext(dx)[0].split("-")
				dates.append("-".join([parsed[1],parsed[2],parsed[0]]))
			try:
				rec = gdr.RecordReader(os.path.abspath(f"../data/glucose/daily/{dy}.gdr"))
			except FileNotFoundError:
				self.popupShown = "ae.gdr_FNFE"
				ctx = self.showPopup("Couldn't load data",popbuilder.ok("No data available for the date selected"))
				PlaySoundW(PWSTR("../assets/sounds/conflict.wav"), None, SND_FILENAME | SND_ASYNC)
				ctx.as_(FrameworkElement).FindName("popup.content.ok").as_(Button).Click += lambda sender,args: self.hidePopup()
				return
			i = rec.getRecordCount()
			seen = []
			dseen = []
			for x in range(i):
				y = int(rec.getRecordByIndex(x).time)
				if y in seen:
					continue
				records.append(rec.getRecordByIndex(x))
				seen.append(y)

			
			last = 0
			
			records.reverse()
			dates.reverse()
		records = []
		now = datetime.datetime.now()
		today = datetime.datetime(now.year, now.month, now.day, 0, 0).timestamp()

		self.loadAsync(self.document,lambda: loadData(int(today)),XamlReader().Load(open("../assets/ui/history.xaml", "r", encoding='utf-8').read()),pushData)
		
		
		
	def NavChangeSelect(self,sender,args):
		# My fingies hurt now
		if args.SelectedItem:
			item = args.SelectedItem.as_(NavigationViewItem)
			if item.Tag.as_(str) == "Settings":
				self.page = "settings"
				self.transitionElementContent(self.document,XamlReader().Load(open("../assets/ui/settings.xaml", "r", encoding='utf-8').read()),self.initSettingsPage)
			elif item.Tag.as_(str) == "App.Home":
				self.transitionElementContent(self.document,XamlReader().Load(open("../assets/ui/home.xaml", "r", encoding='utf-8').read()),lambda a=self:exec("""
a.page = "home"
a.lsc = -1
uri = Uri.CreateUri(os.path.abspath(os.path.join(os.getcwd(),"../","assets",'pride_flag.png')))
img = a.document.Content.as_(FrameworkElement).FindName("Background").as_(Image)
bitmap = Imaging.BitmapImage()
bitmap.UriSource = uri
img.Source = bitmap
																																				   
"""))
			elif item.Tag.as_(str) == "App.Historical":
				self.transitionElementContent(self.document,XamlReader().Load(open("../assets/ui/loading.xaml", "r", encoding='utf-8').read()),lambda a=self:exec('a.page = ""\na.lsc = -1\na.initHistoryPage()'))

	def transitionElementContent(self,element,newContent,onChange,onFinish=None,speed=20):
		# transitions content with a fade
		self.raf.request_animation_frame(self._transitionElementContentRunner,{
				'i':0,
				'x':0,
				'element':element,
				"newContent":newContent,
				"speed":speed,
				"onChange":onChange,
				"onFinish":onFinish})

	def _transitionElementContentRunner(self,elapsed,data):
		# it does the actual animaztion
		if data['x'] == 0:
			if data['i'] < 101:
				data['i'] += data['speed']
				data['element'].Opacity = (100-data['i'])*0.01
				data['element'].UpdateLayout()
				
				return self.raf.Respond(data)
			else:
				data['x'] = 1
				data['i'] = 0
				return self.raf.Respond(data)
		elif data['x'] == 1:

			data['element'].Content = data['newContent']
			data['element'].UpdateLayout()

			data['onChange']()
			data['x'] = 2
			return self.raf.Respond(data)
		elif data['x'] == 2:
			if data['i'] < 101:
				data['i'] += data['speed']
				data['element'].Opacity = (data['i'])*0.01
				data['element'].UpdateLayout()
				
				return self.raf.Respond(data)
			else:
				data['element'].Opacity = 1
				data['element'].UpdateLayout()
				if data['onFinish']:
					data['onFinish']()
				return self.raf.Respond(data,True)


boot.info("Starting Application, you wont be hearing from me anymore")
XamlApplication.Start(App)
# I dont like writing comments, i hate doing this, but im doing this for you. 