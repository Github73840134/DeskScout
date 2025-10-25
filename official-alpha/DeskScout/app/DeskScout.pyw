import os, sys
os.chdir(os.path.dirname(__file__))
sys.path.append(os.path.join(os.getcwd(), "libs"))
sys.path.append(os.path.join(os.getcwd(), "mods"))
import time
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
import threading
from time import sleep

from win32more.Windows.Win32.UI.WindowsAndMessaging import (
	GetWindowLongW, SetWindowLongW,
	GetWindowLongPtrW, SetWindowLongPtrW,
	GWL_STYLE,
	WS_OVERLAPPEDWINDOW, WS_CAPTION, WS_THICKFRAME, WS_SYSMENU, WS_MINIMIZEBOX, WS_MAXIMIZEBOX
)
from win32more.Windows.Win32.Foundation import HWND

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

	def OnLaunched(self, args):
		# Initialize XAML runtime

		# Load splash screen XAML
		xaml = open("../assets/ui/splash.xaml", encoding="utf-8").read()
		self.splash_window = XamlReader.Load(xaml).as_(Window)
		self.splash_window.SystemBackdrop = MicaBackdrop()
		
		hwnd = self.splash_window.AppWindow.Id.Value
		remove_titlebar(hwnd)
		self._set_window_properties(hwnd)
		
		self.splash_window.Activate()
		

		# Start background thread to simulate loading
		x = threading.Thread(target=self._load_main_app, daemon=True)
		x.start()
		self.launched = False
		self.loadState = 1
		self.timer = DispatcherTimer()
		self.timer.Interval = TimeSpan(100)  # 100ms
		self.timer.Tick += lambda s, e: self._check_thread(x)
		self.timer.Start()

	def _check_thread(self, thread):
		

		if not thread.is_alive() and not self.launched:
			self.splash_window.Close()
			self.launched = True
		else:
			if self.loadState == 0:
				self.splash_window.Content.as_(FrameworkElement).FindName("Status").as_(TextBlock).Text = "Starting service"
			elif self.loadState == 1:
				self.splash_window.Content.as_(FrameworkElement).FindName("Status").as_(TextBlock).Text = "Starting app"
			elif self.loadState == 2:
				self.splash_window.Content.as_(FrameworkElement).FindName("Status").as_(TextBlock).Text = "Preparing updates"
			elif self.loadState == 3:
				self.splash_window.Content.as_(FrameworkElement).FindName("Status").as_(TextBlock).Text = "Installing updates"
			elif self.loadState == 4:
				self.splash_window.Content.as_(FrameworkElement).FindName("Status").as_(TextBlock).Text = "One Moment"
	def _set_window_properties(self, hwnd):
		# You can use win32 APIs to set size, position, etc.
		from win32more.Windows.Win32.UI.WindowsAndMessaging import (
			GetWindowRect, MoveWindow
		)

		# Example: center on screen
		from win32more.Windows.Win32.UI.WindowsAndMessaging import GetSystemMetrics
		from win32more.Windows.Win32.UI.WindowsAndMessaging import SM_CXSCREEN, SM_CYSCREEN

		screen_w = GetSystemMetrics(SM_CXSCREEN)
		screen_h = GetSystemMetrics(SM_CYSCREEN)
		win_w, win_h = 400, 250
		x = (screen_w - win_w) // 2
		y = (screen_h - win_h) // 2

		MoveWindow(hwnd, x, y, win_w, win_h, True)
	def _load_main_app(self):
		# Simulate work
		import subprocess
		import requests
		import psutil,time
		if "update.zip" in os.listdir("../data"):
			self.loadState = 2

			try:
				resp = requests.get("http://127.0.0.1:49152/shutdown",timeout=3)
			except:
				pass
			self.loadState = 3
			resp = os.system("pyw updater.py")
			if resp == 0:

				self.loadState = 4
				time.sleep(5)
				os.remove("../data/update.zip")
				subprocess.Popen("pyw DeskScout.pyw",start_new_session=True)
				return
			else:
				from tkinter import messagebox
				messagebox.showerror("DeskScout","Failed to install update, your install may be corrupted")
				return


		try:
			resp = requests.get("http://127.0.0.1:49152/",timeout=3)
			subprocess.Popen("pyw DeskScoutApp.py",start_new_session=True)
			return
		except:
			subprocess.Popen("pyw DeskScoutService.py fromDeskscoutPy",start_new_session=True)
		i = 0
		while i != 20:
			try:
				self.loadState = 0
				resp = requests.get("http://127.0.0.1:49152/",timeout=3)
				self.loadState = 1
				time.sleep(1)
				subprocess.Popen("pyw DeskScoutApp.py",start_new_session=True)
				i = 20
			except:
				i += 1

		print("Main app is now active!")
		

	def OnSuspending(self, args):
		print("App suspending...")

	def OnResuming(self, args):
		print("App resuming...")


if __name__ == "__main__":
	XamlApplication.Start(SplashApp)

