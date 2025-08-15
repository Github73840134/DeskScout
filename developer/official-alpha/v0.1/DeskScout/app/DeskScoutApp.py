import os, sys,json,_thread,time,logging
ast = None
os.chdir(os.path.dirname(__file__))
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
					handlers=[handler],
					level=logging.DEBUG)
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
from win32more.Windows.UI.Xaml import GridLength, GridLengthHelper, GridUnitType,DependencyObject
from win32more.Microsoft.UI.Xaml.Controls import Primitives,ToggleSplitButton,ToggleSwitch,Page,HyperlinkButton,Button,CheckBox,ComboBox,NumberBox, ProgressRing,Image,PasswordBox,TextBlock,TextBox, Slider, StackPanel, NavigationView, Frame, NavigationViewItem, RowDefinition, Grid, GridView, GroupStyle, Canvas, ToolTip
from win32more.Windows.Foundation import PropertyValue,IPropertyValue,Uri
from win32more.Windows.Win32.System.WinRT import IInspectable
from win32more.Microsoft.UI.Windowing import AppWindow
from win32more.Microsoft.UI import WindowId
from win32more.Microsoft.UI.Xaml import DispatcherTimer
from win32more.Windows.Foundation import TimeSpan
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

from win32more.Windows.UI.Xaml import UIElement
from win32more.Windows.UI.Xaml.Media import VisualTreeHelper
from win32more.Windows.UI.Xaml import DependencyObject

def find_elements_with_tag(parent, target_tag):
	from win32more.Windows.UI.Xaml.Controls import Panel, Frame, ContentControl, ItemsControl
	matched = []

	def recurse(element):
		print("RECURSE",element,dir(element))
		if element is None:
			return

		# Check Tag
		tag = getattr(element, "Tag", None)
		print("TAGSTATE:",tag)
		if tag == target_tag:
			matched.append(element)

		# Try Panel.Children (StackPanel, Grid, etc.)
		try:
			panel = element.as_(StackPanel)
			for child in panel.Children:
				print("|_",child)
				recurse(child)
			return
		except Exception as e:
			print("ERX",e)

		# Try Frame.Content
		try:
			frame = element.as_(Frame)
			if frame.Content:
				recurse(frame.Content)
			return
		except Exception:
			pass

		# Try ContentControl.Content
		try:
			content_control = element.as_(ContentControl)
			if content_control.Content:
				recurse(content_control.Content)
			return
		except Exception:
			pass

		# Try ItemsControl.Items
		try:
			items_control = element.as_(ItemsControl)
			for item in items_control.Items:
				recurse(item)
			return
		except Exception:
			pass

		# Try VisualTreeHelper fallback
		try:
			dep_obj = element.as_(DependencyObject)
			count = VisualTreeHelper.GetChildrenCount(dep_obj)
			for i in range(count):
				child = VisualTreeHelper.GetChild(dep_obj, i)
				recurse(child)
		except Exception:
			pass

		# Try generic get_Children
		try:
			children = getattr(element, "Children", None)
			if children:
				for child in children:
					recurse(child)
		except Exception:
			pass

	recurse(parent)
	return matched




class AppState:
	STARTING = 0x00
	RUNNING = 0x01
	LOGIN = 0x02
class InvalidRequest:
	pass
class ServerLost:
	pass

class App(XamlApplication):
	
	def OnLaunched(self, args):
		ui.debug("App OnLaunched called")

		self.page = "home"
		self.fetchState = 0
		self.lastFetch = -1
		self.lsc = -1
		self.raf = RAFManager()
		self.state = 0
		self.glucose = {}
		ui.debug("Loading window.xaml")
		win = XamlReader().Load(open("../assets/ui/window.xaml", "r", encoding='utf-8').read()).as_(Window)
		self.win = win
		ui.debug("Loaded window.xaml")
		win.SystemBackdrop = MicaBackdrop()  # Set the window backdrop (optional)
		ui.debug("Aquiring NavigationView")
		self.NavView = win.Content.as_(FrameworkElement).FindName("NavView").as_(NavigationView)
		ui.debug("Setting up NavigationView")
		self.NavView.SelectedItem = self.NavView.MenuItems[0]
		self.navert = self.NavView.add_SelectionChanged(self.NavChangeSelect)
		ui.debug("Loading the document")
		self.document = win.Content.as_(FrameworkElement).FindName("ContentFrame").as_(Frame)
		ui.debug("Content loaded")
		ui.info("Main frame loaded")
		self.document.Content = XamlReader().Load(open("../assets/ui/home.xaml", "r", encoding='utf-8').read())

		if 1 != 1:
			self.page = 'home'
			print("BITCH")
			self.document.Content = XamlReader().Load(open("../assets/ui/home.xaml", "r", encoding='utf-8').read())
			self.state = AppState.RUNNING
			app.info("Starting background thread")
			self.fetchState = 4
			_thread.start_new_thread(self.dataFetch,())
		else:
			try:
				serviceworker.info("Checking if service is alive")
				resp = requests.get("http://127.0.0.1:49152/getStatus")
				serviceworker.info("Service is alive")
				serviceworker.debug(f"Service Respone: {resp.text}")

			except Exception as e:
				serviceworker.info("Could not contact service, stopping here",str(e))
				app.fatal("Startup failed","NO_SERVICE_CONNECTION")
				exit(0)
			if not self.getSetting("setup"):
				self.launchOOBE()
				

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
		hicon = LoadImageW(
			None,
			icon_path,
			IMAGE_ICON,
			0,
			0,
			LR_LOADFROMFILE
		)
		
		self.win.Title = "DeskScout"
		current_pid = os.getpid()
		hwnd = get_hwnds_by_pid(current_pid)[0]
		from win32more.Windows.Win32.UI.WindowsAndMessaging import SendMessageW, WM_SETICON, ICON_SMALL, ICON_BIG
		SendMessageW(hwnd, WM_SETICON, ICON_SMALL, hicon)
		SendMessageW(hwnd, WM_SETICON, ICON_BIG, hicon)
		self._resize_timer = DispatcherTimer()
		interval = TimeSpan()
		self.pbts = None
		interval.Duration = 10000000 # 100ms
		self._resize_timer.Interval = interval
		self._resize_timer.Tick += self.update_Display
		self._resize_timer.Start()
		print(is_dark_mode_enabled())
		
		self.documentProvider = self.document
	def launchOOBE(self):
		self.NavView.put_IsPaneVisible(False)

		self.document.Content = XamlReader().Load(open("../assets/ui/oobe.xaml", "r", encoding='utf-8').read())
		self.page = "oobe"
		nextbutton = self.document.Content.as_(FrameworkElement).FindName("oobe.next").as_(Button)
		uri = Uri.CreateUri(os.path.abspath(os.path.join(os.getcwd(),"../","assets",'background.png')))
		print(os.path.abspath(os.path.join(os.getcwd(),"../","assets",'background.png')))
		
		# Create the SvgImageSource

		# Create ImageBrush and set properties
		img = self.document.Content.as_(FrameworkElement).FindName("Background").as_(Image)
		bitmap = Imaging.BitmapImage()
		bitmap.UriSource = uri
		img.Source = bitmap


		task = lambda: self.setupAuthCheck(lambda: self.doOOBE("alarmsetup"))
		nextbutton.add_Click(lambda sender,args: self.showDisclaimer(task))

	def doOOBE(self,page="alarmsetup"):
		def PresetRoot():
			if page == "alarmsetup":
				doc = self.document.Content.as_(FrameworkElement).FindName("frame").as_(Frame)
				self.initSettingsPage(doc)
				
				doc.Content.as_(FrameworkElement).FindName("settings.about").as_(Button).Visibility = 1
				doc.Content.as_(FrameworkElement).FindName("settings.pcloseapp").as_(Button).Visibility = 1
				doc.Content.as_(FrameworkElement).FindName("settings.psignout").as_(Button).Visibility = 1


				print(doc.Content.as_(FrameworkElement).FindName("settings.about").as_(Button).Content)
				print("CALLED")
		if page == "alarmsetup":
			self.NavView.put_IsPaneVisible(False)

			self.document.Content = XamlReader().Load(open("../assets/ui/oobe/page0.xaml", "r", encoding='utf-8').read())
			self.document.Content.as_(FrameworkElement).FindName("frame").as_(Frame).Content = XamlReader().Load(open("../assets/ui/settings.xaml", "r", encoding='utf-8').read())
			self.document.Loaded += lambda sender,args: PresetRoot()
			self.document.Content.as_(FrameworkElement).FindName("oobe.next").as_(Button).add_Click(lambda sender,args: self.setupComplete())



			


			
	def welcome(self):
		self.goHome()
		self.page = "home"
		PlaySoundW(PWSTR(os.path.join(os.getcwd(),'../assets/sounds/open.wav')), None, SND_FILENAME | SND_ASYNC)

	def setupComplete(self):
		self.NavView.put_IsPaneVisible(False)
		if self.fetchState == 0:
			import _thread
			_thread.start_new_thread(self.dataFetch,())
		self.changeSetting("setup",True)
		self.document.Content = XamlReader().Load(open("../assets/ui/setup_complete.xaml", "r", encoding='utf-8').read())
		self.document.Content.as_(FrameworkElement).FindName("oobe.finish").as_(Button).add_Click(lambda sender,args: self.goHome())
		PlaySoundW(PWSTR(os.path.join(os.getcwd(),'../assets/sounds/setup_done.wav')), None, SND_FILENAME | SND_ASYNC)



	def setupAuthCheck(self,onFinish=None):
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
			if onFinish:
				onFinish()
		else:

			self.showSignIn(onFinish)
	def goHome(self):
		self.NavView.put_IsPaneVisible(True)
		self.state = AppState.RUNNING
		if self.fetchState == 0:
			import _thread
			_thread.start_new_thread(self.dataFetch,())
		self.document.Content = XamlReader().Load(open("../assets/ui/home.xaml", "r", encoding='utf-8').read())
	def showSignIn(self,onFinish=None):
		self.state = AppState.LOGIN
		app.debug(f"App State={self.state}")
		ui.debug(f"Hiding nav panel")
		self.NavView.put_IsPaneVisible(False)
		ui.debug("Loading sign in page")
		self.document.Content = XamlReader().Load(open("../assets/ui/signin.xaml", "r", encoding='utf-8').read())
		ui.debug("Sign in page loaded")
		loginbutton = self.document.Content.as_(FrameworkElement).FindName("Complete").as_(Button)
		def LoginButtonSelected(sender,args):
			from pydexcom import Dexcom,errors
			import keyring
			
			loginbutton = self.document.Content.as_(FrameworkElement).FindName("Complete").as_(Button)
			
			uname = self.document.Content.as_(FrameworkElement).FindName("Username").as_(TextBox)
			password = self.document.Content.as_(FrameworkElement).FindName("Password").as_(PasswordBox)
			status = self.document.Content.as_(FrameworkElement).FindName("Status").as_(TextBlock)

			try:
				resp = requests.post("http://127.0.0.1:49152/settings",data={"action":"set","path":"username","value":'"'+uname.get_Text()+'"'})
				keyring.set_password("com.sedwards.deskscout",uname.get_Text(),password.get_Password())
				resp = requests.get("http://127.0.0.1:49152/authenticate")
				print('login',resp.text)
				res = json.loads(resp.text)
				if res['status'] == "ok":
					if onFinish:
						onFinish()
				else:
					status.Visibility = 0
					status.Text = "Authentication Failed"
			except errors.AccountError:
				status.Visibility = 0

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
		self.NavView.put_IsPaneVisible(False)
		self.page = "disclaimer"
		self.document.Content = XamlReader().Load(open("../assets/ui/disclaimer.xaml", "r", encoding='utf-8').read())
		def finish(sender,args):
			self.NavView.put_IsPaneVisible(True)
			if onAccept:
				onAccept()

		self.document.Content.as_(FrameworkElement).FindName("disclaimer.next").as_(Button).add_Click(finish)

		PlaySoundW(PWSTR(os.path.join(os.getcwd(),'../assets/sounds/disclaimer.wav')), None, SND_FILENAME | SND_ASYNC)
		
		
	def update_Display(self,sender,args):
		import re
		#print("FS",self.fetchState,self.state)
		if (self.fetchState == 1 or self.fetchState == 2) and self.page != "oobe" and self.state == AppState.RUNNING:
			print("CATASTROPHIC")
			self.fetchState = 0
			self.showSignIn(self.goHome)
		elif self.fetchState == 4:
			print("NO INTERNT")
			glucose = self.document.Content.as_(FrameworkElement).FindName("reading").as_(TextBlock)
			last = self.document.Content.as_(FrameworkElement).FindName("last_update").as_(TextBlock)
			trend = self.document.Content.as_(FrameworkElement).FindName("trendarrow").as_(TextBlock)
			last.Text = "Not Connected"
			return

		if self.page == "home" and self.state == AppState.RUNNING:
			if self.glucose:
				
				glucose = self.document.Content.as_(FrameworkElement).FindName("reading").as_(TextBlock)
				last = self.document.Content.as_(FrameworkElement).FindName("last_update").as_(TextBlock)
				trend = self.document.Content.as_(FrameworkElement).FindName("trendarrow").as_(TextBlock)

				
				lut = re.findall("\\((.*?)\\)",self.glucose['ST'])[0]
				if self.lsc != int(lut):
					ui.info("Change detected, updating display")
					self.lsc = int(lut)
					glucose.Text = str(self.glucose['Value'])
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
				pass
			else:
				fetcher.info("Retrieving glucose data")
				try:
					resp = requests.get("http://127.0.0.1:49152/getStatus",timeout=15)
					status = json.loads(resp.text)
					print("DF",status)
					if status['login_state'] == "unknown":
						serviceworker.error("User not signed in, please run sign in flow")

						self.fetchState = 1
					elif status['login_state'] == "offline":
						self.fetchState = 4
					elif status['login_state'] == False:
						serviceworker.info("User not authenticated, authenticating")

						resp = requests.get("http://127.0.0.1:49152/authenticate",timeout=10)
						data = json.loads(resp.text)
						if data['status'] == "ok":
							serviceworker.info("Authentication Successful")
							if self.fetchState == 4:
								self.lsc = 0
						
						else:
							self.fetchState = 2
							serviceworker.error("Authentication Failed")
						

					elif status['login_state'] == True:
						resp = requests.get("http://127.0.0.1:49152/getLatestReading",timeout=10)
						data = json.loads(resp.text)
						if self.fetchState == 4:
							self.lsc = 0
						if data['status'] == "ok":
							self.glucose = data['data']
							self.fetchState = 3
							self.lastFetch = time.time()
				except Exception as e:
					print("Error",e)
					self.fetchState = 4
			time.sleep(5)
		self.fetchState = 0
	def loadAsync(self,root,function,endUI):
		def dummy():
			pass
		def startLoad():
			function()
			self.transitionElementContent(root,endUI,dummy)

		self.transitionElementContent(root,XamlReader().Load(open("../assets/ui/loading.xaml", "r", encoding='utf-8').read()),dummy,startLoad)
	def signOut(self):
		import keyring
		keyring.delete_password("com.sedwards.deskscout",self.getSetting("username"))
		self.changeSetting("username",'""')
		self.showSignIn(self.setupComplete)
	def changeSetting(self,path,value):
		try:
			resp = requests.post("http://127.0.0.1:49152/settings",data={"action":"set","path":path,"value":value})
			data = json.loads(resp.text)
			if data['status'] == "ok":
				return True
			else:
				return False
		except:
			return False
	def getSetting(self,path):
		try:
			resp = requests.post("http://127.0.0.1:49152/settings",data={"action":"get","path":path},timeout=10)
			data = json.loads(resp.text)
			if data['status'] == "OK":
				return data['data']
			else:
				return InvalidRequest()
		except:
			return ServerLost()
	def validateSetting(self,value):
		if isinstance(value,InvalidRequest) or isinstance(value,ServerLost):
			return False
		return True
	def initManageSoundsPage(self,onSelect=None,root=None):
		if not root:
			root = self.document
		back = root.Content.as_(FrameworkElement).FindName("settings.back").as_(Button)
		back.add_Click(lambda sender,args: self.transitionElementContent(root,XamlReader().Load(open("../assets/ui/settings/sounds.xaml", "r", encoding='utf-8').read()),lambda: self.initAlarmSoundSettings(root)))
		soundbox = root.Content.as_(FrameworkElement).FindName("settings.manage_sounds.sounds").as_(StackPanel)
		def prepremove(sender,args):
			if root.Content.as_(FrameworkElement).FindName("settings.manage_sounds.remove").as_(Primitives.ToggleButton).IsChecked:
				root.Content.as_(FrameworkElement).FindName("settings.manage_sounds.remove").as_(Primitives.ToggleButton).Content = "Click a sound to remove"
			else:
				root.Content.as_(FrameworkElement).FindName("settings.manage_sounds.remove").as_(Primitives.ToggleButton).Content = "Remove sound"
		def addsound(sender,args):
			from tkinter import filedialog
			import shutil
			fns = filedialog.askopenfilenames(filetypes=[["Wave Files",[".wav"]],["MPEG-3 Audio",[".mp3"]]])
			for x in fns:
				shutil.copy(x,os.path.join(os.getcwd(),'../assets/sounds/extern',os.path.basename(x)))
			reloadChoices()
		root.Content.as_(FrameworkElement).FindName("settings.manage_sounds.remove").as_(Primitives.ToggleButton).add_Checked(prepremove)
		root.Content.as_(FrameworkElement).FindName("settings.manage_sounds.remove").as_(Primitives.ToggleButton).add_Unchecked(prepremove)
		root.Content.as_(FrameworkElement).FindName("settings.manage_sounds.add").as_(Button).add_Click(addsound)


		internal_sounds = json.load(open("../data/default_sounds.json"))
		def soundSelected(path,internal=False):
			if root.Content.as_(FrameworkElement).FindName("settings.manage_sounds.remove").as_(Primitives.ToggleButton).IsChecked:
				if not internal:
					root.Content.as_(FrameworkElement).FindName("settings.manage_sounds.remove").as_(Primitives.ToggleButton).IsChecked = False
					os.remove(path)
					reloadChoices()
					return
			print("Sound selected",path)
			if onSelect:
				onSelect(path)
		def previewSelectedSound(path):
			print("Sound selected to preview",path)
			PlaySoundW(PWSTR(path), None, SND_FILENAME | SND_ASYNC)
		def reloadChoices():
			soundbox.Children.Clear()
			for i in internal_sounds:
				print(i)
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
		if not root:
			root = self.document
		
		class Settings:
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
			save = root.Content.as_(FrameworkElement).FindName("settings.save").as_(Button)
			change_alarm_sounds = root.Content.as_(FrameworkElement).FindName("settings.change_alarm_sounds").as_(Button)
			signout = root.Content.as_(FrameworkElement).FindName("settings.signout").as_(Button)
			closeapp = root.Content.as_(FrameworkElement).FindName("settings.closeapp").as_(Button)
			about = root.Content.as_(FrameworkElement).FindName("settings.about").as_(Button)


		# Initiaize the settings view

		#Alarms On?
		s = self.getSetting("enableNotify")
		if self.validateSetting(s):
			Settings.enable_alarms.IsChecked = s

		# Urgent Low Notifiactions
		s = self.getSetting("notify/urgentLow/enabled")
		if self.validateSetting(s):
			Settings.alarms.ul.enabled.IsChecked = s
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
		s = self.getSetting("notify/urgentLowSoon/silence")
		if self.validateSetting(s):
			Settings.alarms.uls.snooze.put_Value(s/60)
		
		# Low Glucose
		s = self.getSetting("notify/low/enabled")
		if self.validateSetting(s):
			Settings.alarms.low.enabled.IsChecked = s
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
		def saveAll(sender,args):
			# General Alarms
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
			from windows_toasts import InteractableWindowsToaster, Toast, ToastActivatedEventArgs, ToastButton
			interactableToaster = InteractableWindowsToaster('')
			newToast = Toast(['DeskScout',"Noitce",f"Your settings have been saved"])
			interactableToaster.show_toast(newToast)
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

		root.Content.as_(FrameworkElement).FindName("settings.save").as_(Button).add_Click(saveAll)
		root.Content.as_(FrameworkElement).FindName("settings.change_alarm_sounds").as_(Button).add_Click(lambda sender,args:soundsPage())

		root.Content.as_(FrameworkElement).FindName("settings.signout").as_(Button).add_Click(lambda sender,args:self.signOut())
		root.Content.as_(FrameworkElement).FindName("settings.closeapp").as_(Button).add_Click(lambda sender,args:shutdown())


		root.Content.as_(FrameworkElement).FindName("settings.about").as_(Button).add_Click(aboutPage)
		return Settings()
	def initDataManagement(self):
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
			space += os.stat(os.path.abspath("../data/settings.json")).st_size

			for root,dirs,files in os.walk(os.path.abspath("../assets/sounds")):
				for i in files:
					space += os.stat(os.path.join(root,i)).st_size
			self.document.Content.as_(FrameworkElement).FindName("dm.app_usage").as_(TextBlock).Text = f"Usage: {cs(space)}"
			
			back = self.document.Content.as_(FrameworkElement).FindName("dm.back").as_(Button)
			back.add_Click(lambda sender,args: self.transitionElementContent(self.document,XamlReader().Load(open("../assets/ui/loading.xaml", "r", encoding='utf-8').read()),self.initAboutPage))
		self.transitionElementContent(self.document,XamlReader().Load(open("../assets/ui/data_manage.xaml", "r", encoding='utf-8').read()),loadContent)


	def initAboutPage(self):
		self.NavView.SelectedItem = None
		serverinfo = {}

		def loadContent():
			self.document.Content.as_(FrameworkElement).FindName("about.version").as_(TextBlock).Text = "Version: 0.1.0"
			self.document.Content.as_(FrameworkElement).FindName("about.platform").as_(TextBlock).Text = f"Platform: {sys.platform}"
			self.document.Content.as_(FrameworkElement).FindName("about.reset").as_(Button).add_Click(reset)
			self.document.Content.as_(FrameworkElement).FindName("about.server_version").as_(TextBlock).Text = f"Version: {serverinfo['version']}"
			self.document.Content.as_(FrameworkElement).FindName("about.server_build").as_(TextBlock).Text = f"Build: {serverinfo['build']}"
			self.document.Content.as_(FrameworkElement).FindName("about.server_release").as_(TextBlock).Text = f"Release: {serverinfo['release']}"
			self.document.Content.as_(FrameworkElement).FindName("about.server_channel").as_(TextBlock).Text = f"Channel: {serverinfo['channel']}"
			self.document.Content.as_(FrameworkElement).FindName("about.datamanage").as_(Button).add_Click(lambda sender,args: self.transitionElementContent(self.document,XamlReader().Load(open("../assets/ui/loading.xaml", "r", encoding='utf-8').read()),lambda: print(),self.initDataManagement))
			back = self.document.Content.as_(FrameworkElement).FindName("settings.back").as_(Button)
			back.add_Click(lambda sender,args: self.transitionElementContent(self.document,XamlReader().Load(open("../assets/ui/settings.xaml", "r", encoding='utf-8').read()),self.initSettingsPage))
		

		def reset(sender,args):
			import keyring,subprocess
			keyring.delete_password("com.sedwards.deskscout",self.getSetting("username"))
			self.changeSetting("username",'""')
			self.changeSetting("setup",False)
			resp = requests.get("http://127.0.0.1:49152/authenticate")

			self.NavView.put_IsPaneVisible(False)
			self.document.Content = XamlReader().Load(open("../assets/ui/oobe.xaml", "r", encoding='utf-8').read())
			self.page = "oobe"
			nextbutton = self.document.Content.as_(FrameworkElement).FindName("oobe.next").as_(Button)
			task = lambda: self.setupAuthCheck(lambda: self.doOOBE("alarmsetup"))
			nextbutton.add_Click(lambda sender,args: self.showDisclaimer(task))
		resp = requests.get("http://127.0.0.1:49152/about")
		serverinfo = json.loads(resp.text)
		self.transitionElementContent(self.document,XamlReader().Load(open("../assets/ui/about.xaml", "r", encoding='utf-8').read()),loadContent)
		

			
		
		
	def NavChangeSelect(self,sender,args):
		if args.SelectedItem:
			item = args.SelectedItem.as_(NavigationViewItem)
			if item.Tag.as_(str) == "Settings":
				self.page = "settings"
				self.transitionElementContent(self.document,XamlReader().Load(open("../assets/ui/settings.xaml", "r", encoding='utf-8').read()),self.initSettingsPage)
			elif item.Tag.as_(str) == "App.Home":
				self.transitionElementContent(self.document,XamlReader().Load(open("../assets/ui/home.xaml", "r", encoding='utf-8').read()),lambda a=self:exec('a.page = "home"\na.lsc = -1'))
			elif item.Tag.as_(str) == "App.Historical":
				self.transitionElementContent(self.document,XamlReader().Load(open("../assets/ui/history.xaml", "r", encoding='utf-8').read()),lambda a=self:exec('a.page = "history"\na.lsc = -1'))

	def transitionElementContent(self,element,newContent,onChange,onFinish=None,speed=20):
		self.raf.request_animation_frame(self._transitionElementContentRunner,{
				'i':0,
				'x':0,
				'element':element,
				"newContent":newContent,
				"speed":speed,
				"onChange":onChange,
				"onFinish":onFinish})

	def _transitionElementContentRunner(self,elapsed,data):
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