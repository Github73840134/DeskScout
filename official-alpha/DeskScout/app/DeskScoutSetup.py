# DeskScout Setup
# Putting you in glucose
# horrible slogan, it will be changed
# Anyways

from tkinter import messagebox

import os, sys,json,_thread,time,logging

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
handler = logging.StreamHandler(open("setup_boot.log","w+"))

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
sys.path.append(os.path.join(os.getcwd(), "libs"))
sys.path.append(os.path.join(os.getcwd(), "mods"))
boot.info("Starting imports")
import requests
boot.debug("Importing the hellscape that is win32more")
from win32more.xaml import XamlApplication
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
def makeGraph(width,height,mintime,maxtime,low,high,history):

	def _map(x, in_min, in_max, out_min, out_max):
		return int((x-in_min) * (out_max-out_min) / (in_max-in_min) + out_min)
	img = PImage.new("RGB",(width,height))
	draw = ImageDraw.Draw(img)
	draw.rectangle((0,0,width,height),(255,255,255))
	draw.rectangle((int(width*0.08),int(height*0.05),int(width*0.08),int(height*0.95)),(0,0,0))
	draw.rectangle((int(width*0.08),int(height*0.95),int(width),int(height*0.95),),(0,0,0))
	for i in range(40,420,20):
		draw.text((int(width*0.04),_map(i,40,400,int(height*0.94),int(height*0.05))),str(i),(0,0,0))
	
	if low:
		draw.text((int(width*0.01),_map(low,40,400,int(height*0.92),int(height*0.05))),str(low),(255,0,0))
		for i in range(int(width*0.08),int(width),40):
			draw.rectangle((i,_map(low,40,400,int(height*0.94),int(height*0.05)),i+20,_map(low,40,400,int(height*0.94),int(height*0.05))),(255,0,0))
	if high:
		draw.text((int(width*0.01),_map(high,40,400,int(height*0.92),int(height*0.05))),str(high),(255,200,0))

		for i in range(int(width*0.08),int(width),40):
			draw.rectangle((i,_map(high,40,400,int(height*0.94),int(height*0.05)),i+20,_map(high,40,400,int(height*0.94),int(height*0.05))),(255,200,0))
	for i in range(mintime,maxtime,3600):
		
		x = _map(i,mintime,maxtime,int(width*0.08),int(width))

		y = _map(i,int(width*0.08),int(width),mintime,maxtime)
		if x-int(width*0.05) > int(width*0.05):
		
			draw.text((x-int(width*0.05),int(height*0.96)),time.strftime("%I%p", time.localtime(i)),(0,0,0))
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
class App(XamlApplication):
	
	def OnLaunched(self, args):
		# App Start
		ui.debug("App OnLaunched called")

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
		self.NavView.put_IsPaneVisible(False) #Show the NavPanel again

		self.NavView.SelectedItem = self.NavView.MenuItems[0] # Set the selected item to the first nav item
		self.navert = self.NavView.add_SelectionChanged(self.NavChangeSelect)
		ui.debug("Loading the document")
		self.document = win.Content.as_(FrameworkElement).FindName("ContentFrame").as_(Frame)
		ui.debug("Content loaded")
		ui.info("Main frame loaded")
		self.document.Content = XamlReader().Load(open("../assets/ui/oobe.xaml", "r", encoding='utf-8').read())
		self.loadFlags = None
		if len(sys.argv) > 1:
			if sys.argv[1] == "setGDP":
				self.selectCGM()
				self.loadFlags = 1
			if sys.argv[1] == "restore":
				self.loadFlags = 2
				self.restoreButton(None,None)
				
		else:
			self.launchOOBE()
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
		self.win.Title = "DeskScout Setup"
		current_pid = os.getpid()
		hwnd = get_hwnds_by_pid(current_pid)[0]
		self.hwnd = hwnd
		from win32more.Windows.Win32.UI.WindowsAndMessaging import (
		GetForegroundWindow,
		SetForegroundWindow,
		FindWindowW,
		ShowWindow,
		IsIconic,
		SW_RESTORE,
		)
		if IsIconic(hwnd):
			ShowWindow(hwnd, SW_RESTORE)
			# Bring to front
			SetForegroundWindow(hwnd)
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
		#self._resize_timer.Start()
		self.lastUpdateCheck = time.time()
		self.popupShown = None
		self.documentProvider = self.document
				
			

			
	def NotImplemented(self,*args):
		messagebox.showerror("Work in progress","Feature is not implemented")
	def launchOOBE(self):
		def fadeIn(elapsed,data):
			print(elapsed)
			if data['x'] == 0:
				# Now Wait...
				if data['i'] < 501:
					data['i'] += data['speed']
					

					
					return self.raf.Respond(data)
				else:
					data['x'] = 1
					data['i'] = 0
					from mods import gdr
					#gdr.createRecordFile("../data/glucose.gdr")
					

					return self.raf.Respond(data)
			elif data['x'] == 1:
				# And try to find another mistake
				if data['i'] < 101:
					data['i'] += data['speed']
					img = self.document.Content.as_(FrameworkElement).FindName("Background").as_(Image)
					img.Opacity = (data['i'])*0.01
					img.UpdateLayout()
					img = self.document.Content.as_(FrameworkElement).FindName("Loader").as_(StackPanel)
					img.Opacity = (100-data['i'])*0.01
					img.UpdateLayout()
					

					
					return self.raf.Respond(data)
				else:
					data['x'] = 2
					data['i'] = 0
					return self.raf.Respond(data)
			elif data['x'] == 2:
				# If you throw it all away then maybe you can change your mind
				if data['i'] < 101:
					data['i'] += data['speed']
					img = self.document.Content.as_(FrameworkElement).FindName("Title").as_(TextBlock)

					img.Opacity = (data['i'])*0.01
					img.UpdateLayout()
					img.UpdateLayout()

					
					return self.raf.Respond(data)
				else:
					data['x'] = 3
					data['i'] = 0
					return self.raf.Respond(data)
			elif data['x'] == 3:
				# Fade in the description
				if data['i'] < 101:
					data['i'] += data['speed']
					img = self.document.Content.as_(FrameworkElement).FindName("Description").as_(TextBlock)

					img.Opacity = (data['i'])*0.01
					img.UpdateLayout()
					img.UpdateLayout()

					
					return self.raf.Respond(data)
				else:
					data['x'] = 4
					data['i'] = 0
					return self.raf.Respond(data)
			elif data['x'] == 4:
				# Fade in the button
				if data['i'] < 101:
					data['i'] += data['speed']
					nextbutton = self.document.Content.as_(FrameworkElement).FindName("oobe.next").as_(Button)
					restore = self.document.Content.as_(FrameworkElement).FindName("oobe.restore").as_(Button)

					nextbutton.Opacity = (data['i'])*0.01
					restore.Opacity = (data['i'])*0.01

					nextbutton.UpdateLayout() #Update the page layout 
					return self.raf.Respond(data)
				else:
					nextbutton = self.document.Content.as_(FrameworkElement).FindName("oobe.next").as_(Button)
					restore = self.document.Content.as_(FrameworkElement).FindName("oobe.restore").as_(Button)
					restore.add_Click(self.restoreButton) # Show disclaimer on button click
					nextbutton.add_Click(lambda sender,args: self.showDisclaimer(self.selectCGM)) # Show disclaimer on button click
					return self.raf.Respond(data,True) # Stop this function

		self.NavView.put_IsPaneVisible(False) # Hide the lading page

		self.document.Content = XamlReader().Load(open("../assets/ui/oobe.xaml", "r", encoding='utf-8').read())
		self.page = "oobe" #Set the page type
		nextbutton = self.document.Content.as_(FrameworkElement).FindName("oobe.next").as_(Button)
		uri = Uri.CreateUri(os.path.abspath(os.path.join(os.getcwd(),"../","assets",'background.png')))
		
		# Create the SvgImageSource

		# Create ImageBrush and set properties
		img = self.document.Content.as_(FrameworkElement).FindName("Background").as_(Image)
		bitmap = Imaging.BitmapImage()
		bitmap.UriSource = uri
		
		img.Loaded += lambda sender,args: self.raf.request_animation_frame(fadeIn,{"i":0,"x":0,"speed":10})
		img.Source = bitmap
		

		#task = lambda: self.setupAuthCheck(lambda: self.doOOBE("alarmsetup")) # Do an auth check and continue to alarm setup
		task = self.selectCGM

		nextbutton.Opacity = 0
	
	def selectCGM(self):
		gdpExts = []
		def loadCGMSupport():
			resp = requests.get("http://127.0.0.1:49152/extInfo") #Get Extensions
			exts = json.loads(resp.text)['data']
			for i in exts:
				if i['type'] == 'gdp':
					gdpExts.append(i)
		def signINGDP(gdp):
			self.changeSetting("gdp",f'"{gdp}"')
			resp = requests.get("http://127.0.0.1:49152/reloadExts") #Get Extensions

			if self.loadFlags == 1:
				requests.get(SERVICE_URL+"/setupGDP")
				self.showSignIn(self.exitSetup)
			else:
				self.showSignIn(self.setupComplete)
		def displayOptions():
			for i in gdpExts:
				option = Button()
				frame = StackPanel()
				frame.Orientation = 0
				title = TextBlock()
				title.Text = i['name']
				title.FontSize = 18
				us = TextBlock()
				us.Text = f"Utilizes {i['serviceName']}"
				us.FontSize = 12
				desc = TextBlock()
				desc.Text = i['short']
				frame.Children.Append(title)
				frame.Children.Append(us)

				frame.Children.Append(desc)
				option.Content = frame
				border = Border()
				border.Height = 10
				self.document.Content.as_(FrameworkElement).FindName("cgmOptions").as_(StackPanel).Children.Append(option)
				self.document.Content.as_(FrameworkElement).FindName("cgmOptions").as_(StackPanel).Children.Append(border)

				option.Click += lambda sender,args,i=i['uuid']: signINGDP(i)

				

				

			



		self.NavView.put_IsPaneVisible(False)
		self.loadAsync(self.document,loadCGMSupport,XamlReader().Load(open("../assets/ui/oobe/gdpSelect.xaml", "r", encoding='utf-8').read()),displayOptions)
	def preSetupUpdateCheck(self):
		def checkForUpdates():
			resp = requests.get("http://127.0.0.1:49152/checkForUpdate") # Attempt ot authenticate

		self.transitionElementContent(self.document,lambda:pass,XamlReader().Load(open("../assets/ui/oobe/gdpSelect.xaml", "r", encoding='utf-8').read()),) #Transition to the final UI page

	def doRestore(self,path):
		from win32more.Windows.Win32.UI.WindowsAndMessaging import (
		GetForegroundWindow,
		SetForegroundWindow,
		FindWindowW,
		ShowWindow,
		IsIconic,
		SW_RESTORE,
		)
		ShowWindow(self.hwnd, SW_RESTORE)
		# Bring to front
		SetForegroundWindow(self.hwnd)
		from zipfile import ZipFile
		from tkinter import messagebox
		restoreType = "old"
		try:
			zip = ZipFile(path)
			for i in zip.filelist:
				if i.filename == ".deskscout":
					restoreType = "old"
					messagebox.showwarning("DeskScout-Restore Incompatibility","You are attempting to restore from an older DeskScout build, your settings will not transfer over, but the rest of your data will")
					break
				if i.filename == ".deskscout_2026_3_11":
					restoreType = "gen1"
					break
			else:
				messagebox.showerror("Deskscout","Error restoring settings")
				self.restoreState = -1
			if restoreType == "old":
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
					if i.filename == "glucose.gdr":
						self.changeSetting("gdrState",'0')
						x = zip.open("glucose.gdr")
						y = open("../data/glucose.gdr",'wb+')
						y.write(x.read())
						y.close()
						os.system("py gdrmanage.py unpack")
						self.changeSetting("gdrState",'1')
						
				self.restoreState = 1
			elif restoreType == "gen1":
				zip.close()
				import subprocess
				subprocess.run(f'pyw dataimport.py "{path}"',shell=True,start_new_session=True)
				resp = requests.get("http://127.0.0.1:49152/reloadExts") #Get Extensions
				resp = requests.get("http://127.0.0.1:49152/reloadExts") #Get Extensions


				self.restoreState = 1
				self.afterRestore()

				


		except Exception as e:
			messagebox.showerror("Deskscout",f"Error restoring settings\n{str(e)}")
			self.restoreState = -1
			return
	
	def afterRestore(self):
		# This code is a bitch, not the slaying kind, unless it slays exiting the program
		if self.restoreState == -1:
			self.launchOOBE()
		elif self.restoreState == 1:
			self.showDisclaimer(lambda: self.showSignIn(self.setupComplete))
		
			

	def restoreButton(self,sender,args):
		from tkinter import filedialog
		ans = filedialog.askopenfilename(filetypes=[["Zip Files",[".zip"]]])
		if not ans:
			if self.loadFlags == 2:
				print("EXIT")
				self.win.Close()
				exit()
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
	def exitSetup(self):
		import subprocess
		if not self.loadFlags:
			subprocess.Popen("pyw DeskScoutApp.py -intent Settings",start_new_session=True)
		self.win.Close()
	def setupComplete(self):
		# Shows the setup complete page
		self.NavView.put_IsPaneVisible(False) # Hide the NavPanel
		self.changeSetting("setup",True)
		self.changeSetting("gdrState","1")
		requests.get(SERVICE_URL+"/initializeGDR")

		self.document.Content = XamlReader().Load(open("../assets/ui/setup_complete.xaml", "r", encoding='utf-8').read()) # Start the page update
		self.document.Content.as_(FrameworkElement).FindName("oobe.finish").as_(Button).add_Click(lambda sender,args: self.exitSetup()) # Go home when oobe.finish is clicked
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
	def showSignIn(self,onFinish=None):
		# Starts the sign-in flow
		self.state = AppState.LOGIN #This will stop the fetch stast
		app.debug(f"App State={self.state}")
		ui.debug(f"Hiding nav panel")
		self.NavView.put_IsPaneVisible(False) # navigation flow
		ui.debug("Loading sign in page")
		# Page Loading
		self.document.Content = XamlReader().Load(open("../assets/ui/signin.xaml", "r", encoding='utf-8').read()) #Set the content
		ui.debug("Sign in page loaded")
		loginbutton = self.document.Content.as_(FrameworkElement).FindName("Complete").as_(Button)
		changegdp = self.document.Content.as_(FrameworkElement).FindName("ChangeGDP").as_(Button)
		changegdp.add_Click(lambda s,e: self.selectCGM())
		def LoginButtonSelected(sender,args):
			#Sign in task
			import keyring
			
			loginbutton = self.document.Content.as_(FrameworkElement).FindName("Complete").as_(Button)
			
			uname = self.document.Content.as_(FrameworkElement).FindName("Username").as_(TextBox)
			password = self.document.Content.as_(FrameworkElement).FindName("Password").as_(PasswordBox)
			status = self.document.Content.as_(FrameworkElement).FindName("Status").as_(TextBlock)

			try:
				# The actual sign-in bits
				# Send a post request to the settings endpoint to set the username
				keyring.set_password("com.sedwards.deskscout",uname.get_Text(),password.get_Password()) # Set the password for this user in the keyring
				resp = requests.post("http://127.0.0.1:49152/settings",data={"action":"set","path":"username","value":'"'+uname.get_Text()+'"'})
				resp = requests.get("http://127.0.0.1:49152/authenticate") # Attempt ot authenticate
				print('login',resp.text)
				res = json.loads(resp.text)
				if res['status'] == "ok":
					# Authentication Successful
					if onFinish:
						onFinish()
				else:
					# Authentication Failed
					status.Visibility = 0
					status.Text = "Authentication Failed"
			except Exception as e:
				# Unexpected error
				status.Visibility = 0 # Make the status visible
				status.Text = "Authentication Failed"
		loginbutton.add_Click(LoginButtonSelected)
		ui.debug("UI setup complete")
		uname = self.document.Content.as_(FrameworkElement).FindName("Username").as_(TextBox)
		
		try:
			serviceworker.info("Connecting to service")
			resp = requests.post("http://127.0.0.1:49152/settings",data={"action":"get","path":"username"})
		except:
			serviceworker.fatal("Couldn't connect to service")
			app.fatal("App Terminated")
			exit(0)

		username = json.loads(resp.text)['data']
		uname.Text = username
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
			subprocess.Popen("pyw DeskScout.pyw",start_new_session=True)
			p = psutil.Process(os.getpid())
			p.kill()
	def update_Display(self,sender,args):
		# Updates the main glucose display
		
		import re
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
						if not stat['isUpToDate']:
							self.document.Content.as_(FrameworkElement).FindName("update.preview.name").as_(TextBlock).Text = stat['manifest']['name']
							self.document.Content.as_(FrameworkElement).FindName("update.preview.build").as_(TextBlock).Text = f"Build {stat['manifest']['build']}"
							self.document.Content.as_(FrameworkElement).FindName("update.preview.info").as_(TextBox).Text = stat['manifest']['info']
							self.document.Content.as_(FrameworkElement).FindName("update.preview.action").as_(Button).Content = "Download Update"
							self.document.Content.as_(FrameworkElement).FindName("update.preview.action").as_(Button).Visibility = Visibility.Visible
							self.ups = 0
								



							self.document.Content.as_(FrameworkElement).FindName("update.preview.size").as_(TextBlock).Text = cs(stat['manifest']['size'])
							self.document.Content.as_(FrameworkElement).FindName("update.preview").as_(StackPanel).Visibility = Visibility.Visible
							
						else:
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
					makeGraph(int(width)-20,320,int(self.records[0].time/1000),int(self.records[-1].time/1000),self.getSetting("notify/low/level") if self.getSetting("notify/low/enabled") else None ,self.getSetting("notify/high/level") if self.getSetting("notify/high/enabled") else None,history)
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
				print(self.glucose)
				
				glucose = self.document.Content.as_(FrameworkElement).FindName("reading").as_(TextBlock)
				last = self.document.Content.as_(FrameworkElement).FindName("last_update").as_(TextBlock)
				trend = self.document.Content.as_(FrameworkElement).FindName("trendarrow").as_(TextBlock)
				units = self.document.Content.as_(FrameworkElement).FindName("units").as_(TextBlock)


				# Get the actual time from (Value is enclosed in Date() )
				lut = re.findall("\\((.*?)\\)",self.glucose['ST'])[0]
				
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

					last.Text = "Last synced reading: "+time.ctime(int(lut)/1000)
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
							self.fetchState = 5
							
						
						
				except Exception as e:
					print("Error",e)
					self.fetchState = 4
			time.sleep(5)
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
		keyring.delete_password("com.sedwards.deskscout",self.getSetting("username"))
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
		self.changeSetting(f"notify/{translate[st]}/sound",'"'+path+'"')
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



			save = root.Content.as_(FrameworkElement).FindName("settings.save").as_(Button)
			change_alarm_sounds = root.Content.as_(FrameworkElement).FindName("settings.change_alarm_sounds").as_(Button)
			signout = root.Content.as_(FrameworkElement).FindName("settings.signout").as_(Button)
			closeapp = root.Content.as_(FrameworkElement).FindName("settings.closeapp").as_(Button)
			about = root.Content.as_(FrameworkElement).FindName("settings.about").as_(Button)
		
		def saveAll(saver="manual"):
			if saver == "manual":
				ctx = self.showPopup("Saving Settings",popbuilder.progress("Please Wait...",0))

			# General Alarms
			self.lsc = -1
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
			if saver == 'manual':
				ctx = self.showPopup("Settings saved",popbuilder.ok("Your changes have been saved"))
				ctx.as_(FrameworkElement).FindName("popup.content.ok").as_(Button).Click += lambda sender,args: self.hidePopup()
			

		# Initiaize the settings view

		# Check units
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
		s = self.getSetting("ns/enable")
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
		Settings.ns.url.Paste += urlFilter
		Settings.ns.url.TextChanged += urlFilter
		root.Content.as_(FrameworkElement).FindName("settings.change_alarm_sounds").as_(Button).add_Click(lambda sender,args:soundsPage())

		root.Content.as_(FrameworkElement).FindName("settings.signout").as_(Button).add_Click(lambda sender,args:self.signOut())
		root.Content.as_(FrameworkElement).FindName("settings.closeapp").as_(Button).add_Click(lambda sender,args:shutdown())
		root.Content.as_(FrameworkElement).FindName("settings.save").as_(Button).add_Click(lambda sender,args:saveAll())
		Settings.ns.test.Click += self.NotImplemented
		Settings.ns.viewlog.Click += self.NotImplemented
		Settings.ns.sync.Click += self.NotImplemented





		root.Content.as_(FrameworkElement).FindName("settings.about").as_(Button).add_Click(aboutPage)
		return Settings()

		
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

		
	def NavChangeSelect(self,sender,args):
		# My fingies hurt now
		if args.SelectedItem:
			item = args.SelectedItem.as_(NavigationViewItem)
			if item.Tag.as_(str) == "Settings":
				self.page = "settings"
				self.transitionElementContent(self.document,XamlReader().Load(open("../assets/ui/settings.xaml", "r", encoding='utf-8').read()),self.initSettingsPage)
			elif item.Tag.as_(str) == "App.Home":
				self.transitionElementContent(self.document,XamlReader().Load(open("../assets/ui/home.xaml", "r", encoding='utf-8').read()),lambda a=self:exec('a.page = "home"\na.lsc = -1'))
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
print("DeskScout-Do not close this window")
XamlApplication.Start(App)
# I dont like writing comments, i hate doing this, but im doing this for you. 