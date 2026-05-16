import os,sys,json
os.chdir(os.path.dirname(__file__))
sys.path.insert(0,os.path.join(os.getcwd(),'libs'))
sys.path.append(os.path.join(os.getcwd(),'mods'))
from win32more.Windows.UI.Xaml.Markup import XamlReader
from win32more.Windows.UI.Xaml.Controls import ContentControl
from win32more.Windows.UI.Xaml.Hosting import WindowsXamlManager
from win32more.Windows.UI.Xaml.Interop import TypeName
from win32more.Windows.UI.Xaml import UIElement
from win32more.Windows.Win32.System.Threading import Sleep
from win32more import Windows
from win32more.xaml import XamlApplication
from win32more.Microsoft.UI.Xaml import Window, FrameworkElement
from win32more.Microsoft.UI.Xaml.Media import MicaBackdrop,Imaging,FontFamily,CompositionTarget,VisualTreeHelper
from win32more.Microsoft.UI.Xaml.Markup import XamlReader
from win32more.Windows.UI.Xaml.Interop import TypeKind
from win32more.Windows.UI.Xaml import GridLength, GridLengthHelper, GridUnitType,DependencyObject,Thickness,Visibility
from win32more.Microsoft.UI.Xaml.Controls import InfoBar,Primitives,ToggleSplitButton,Border,ToggleSwitch,Page,HyperlinkButton,Button,CheckBox,ComboBox,NumberBox, ProgressRing,Image,PasswordBox,TextBlock,TextBlock, Slider, StackPanel, NavigationView, Frame, NavigationViewItem, RowDefinition, Grid, GridView, GroupStyle, Canvas, ToolTip
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
import threading,json,requests
from time import sleep
from win32more.Windows.Win32.UI.WindowsAndMessaging import (
	GetWindowLongW, SetWindowLongW,
	GetWindowLongPtrW, SetWindowLongPtrW,
	GWL_STYLE,
	WS_OVERLAPPEDWINDOW, WS_CAPTION, WS_THICKFRAME, WS_SYSMENU, WS_MINIMIZEBOX, WS_MAXIMIZEBOX
)
from win32more.Windows.Win32.Foundation import HWND
SERVICE_URL = "http://127.0.0.1:49152"
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
    "rising fast",
    "rising fast",
    "rising slightly",
    "steady",
    "falling slightly",
    "falling fast",
    "falling fast",
    "unknown",
    "unknown",
]
def remove_titlebar(hwnd: HWND):
	"""Removes title bar and window borders using Win32 style flags."""
	style = GetWindowLongW(hwnd, GWL_STYLE)
	# Remove caption, thickframe, minimize/maximize boxes, and system menu
	style &= ~(WS_CAPTION | WS_THICKFRAME | WS_MINIMIZEBOX | WS_MAXIMIZEBOX | WS_SYSMENU)
	SetWindowLongW(hwnd, GWL_STYLE, style)
class SplashApp(XamlApplication):
	def __init__(self):
		super().__init__()
		self.xaml_manager = None
		self.splash_window = None
		self.main_window = None
	def getSetting(self,path):
		#Gets setting from path
		import requests
		try:
			#Send a POST request to the settings endpoint
			resp = requests.post("http://127.0.0.1:49152/settings",data={"action":"get","path":path},timeout=10)
			data = json.loads(resp.text)
			if data['status'] == "OK":
				return data['data']
			
		except:
			return 
	def OnLaunched(self, args):
		# Initialize XAML runtime
		import time
		# Load splash screen XAML
		xaml = open("../assets/ui/alertoverlay.xaml", encoding="utf-8").read()
		self.splash_window = XamlReader.Load(xaml).as_(Window)
		loadcheck = self.splash_window.Content.as_(FrameworkElement).FindName("page").as_(Frame)
		resp = requests.get(SERVICE_URL+"/getAlarmStatus")
		data = json.loads(resp.text)
		dk = {
			"None":"",
			"urgentLow":"Urgent Low: ",
			"low":"Low Glucose: ",
			"high":"High Glucose: ",
			"risingFast":"",
			"fallingFast":"",
		}
		if data['data'] != None:
			cas = data["data"]
			resp = requests.get(SERVICE_URL+"/getLatestReading")
			data = json.loads(resp.text)
			if data['status'] == "ok":
				self.splash_window.Content.as_(FrameworkElement).FindName("TrendName").as_(TextBlock).Text = dk[cas]+TREND_DESCRIPTIONS[DEXCOM_TREND_DIRECTIONS[data['data']['Trend']]].upper()
				if self.getSetting("useMGDL"):
					self.splash_window.Content.as_(FrameworkElement).FindName("Value").as_(TextBlock).Text = f"{data['data']['Value']} mg/dl"
				else:
					self.splash_window.Content.as_(FrameworkElement).FindName("Value").as_(TextBlock).Text = f"{data['data']['Value']} mmol/L"
				self.splash_window.Content.as_(FrameworkElement).FindName("Time").as_(TextBlock).Text = time.strftime("%I:%M%p")
				

		self.splash_window.SystemBackdrop = MicaBackdrop()
		loadcheck.add_Loaded(self._load_main_app)
		hwnd = self.splash_window.AppWindow.Id.Value
		self.hwnd = hwnd
		remove_titlebar(hwnd)
		self._set_window_properties(hwnd)
		self.splash_window.Title = "OverlayWindow"
		self.splash_window.Activate()
		

		# Start background thread to simulate loading
		self.launched = False
		self.loadState = 1
		
	def OnLoaded(self,args):
		print("Activated")
	def _check_thread(self, thread):
		pass
	def _set_window_properties(self, hwnd):
		# You can use win32 APIs to set size, position, etc.
		from win32more.Windows.Win32.UI.WindowsAndMessaging import (
			GetWindowRect, MoveWindow,SetWindowPos
		)

		# Example: center on screen
		from win32more.Windows.Win32.UI.WindowsAndMessaging import GetSystemMetrics
		from win32more.Windows.Win32.UI.WindowsAndMessaging import SM_CXSCREEN, SM_CYSCREEN
		from win32more.Windows.Win32.UI.WindowsAndMessaging import HWND_TOPMOST,SWP_NOMOVE,SWP_NOSIZE,SWP_SHOWWINDOW

		screen_w = GetSystemMetrics(SM_CXSCREEN)
		screen_h = GetSystemMetrics(SM_CYSCREEN)
		win_w, win_h = 256,int(screen_h*0.08)
		x = screen_w-win_w
		y = 0
		MoveWindow(hwnd, x, 0, win_w, win_h, True)
		SetWindowPos(
			hwnd,
			HWND_TOPMOST,
			0,
			0,
			0,
			0,
			SWP_NOMOVE | SWP_NOSIZE |SWP_SHOWWINDOW)
		

		# 255 = opaque

		
	def make_topmost(self):
		from win32more.Windows.Win32.Foundation import HWND
		from win32more.Windows.Win32.System.WinRT import IInspectable
		from win32more.Windows.Win32.UI.WindowsAndMessaging import HWND_TOPMOST,SWP_NOMOVE,SWP_NOSIZE,SWP_SHOWWINDOW,FindWindowW,ShowWindow,SetForegroundWindow,BringWindowToTop,SW_SHOW,SetWindowPos
		from win32more.Microsoft.UI.Windowing import OverlappedPresenter
		presenter = OverlappedPresenter.Create()
		presenter = self.splash_window.AppWindow.Presenter
		presenter.IsAlwaysOnTop = True
		presenter.IsResizable = False
		presenter.IsMinimizable = False
		presenter.IsMaximizable = False
		hwnd = FindWindowW(None, "OverlayWindow")
		self.hwnd = hwnd


		SetWindowPos(
			hwnd,
			HWND_TOPMOST,
			0, 0, 0, 0,
			SWP_NOMOVE | SWP_NOSIZE | SWP_SHOWWINDOW
		)
		
	def _load_main_app(self,sender,args):
		
		self.timer = DispatcherTimer()
		self.timer.Interval = TimeSpan(100000000)  # 100ms
		self.timer.Tick += lambda s, e: self.closetime()
		self.timer.Start()
		self.make_topmost()

	def closetime(self):
		print("Closed")
		from win32more.Windows.Win32.UI.WindowsAndMessaging import (
			GetWindowRect, MoveWindow
		)
		from win32more.Windows.Win32.UI.WindowsAndMessaging import GetSystemMetrics
		from win32more.Windows.Win32.UI.WindowsAndMessaging import SM_CXSCREEN, SM_CYSCREEN

		screen_w = GetSystemMetrics(SM_CXSCREEN)
		screen_h = GetSystemMetrics(SM_CYSCREEN)
		win_w, win_h = 256,int(screen_h*0.08)
		x = screen_w-win_w
		y = 0

		import time
		for i in range(0,-win_h,-10):
			MoveWindow(self.hwnd, x, i, win_w, win_h, True)
			time.sleep(0.01)
		self.splash_window.Close()

		exit(0)
		

	def OnSuspending(self, args):
		print("App suspending...")

	def OnResuming(self, args):
		print("App resuming...")


if __name__ == "__main__":
	XamlApplication.Start(SplashApp)
