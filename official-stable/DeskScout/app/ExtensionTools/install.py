# Installs Extensions
import argparse
import os, sys
os.chdir(os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(0,os.path.join(os.getcwd(), "libs"))
sys.path.append(os.path.join(os.getcwd(), "mods"))
import time
from win32more.Windows.UI.Xaml.Markup import XamlReader
from win32more.Windows.UI.Xaml.Controls import ContentControl
from win32more.Windows.UI.Xaml.Hosting import WindowsXamlManager
from win32more.Windows.UI.Xaml.Interop import TypeName
from win32more.Windows.UI.Xaml import UIElement
from win32more.Windows.Win32.System.Threading import Sleep
from win32more import Windows
from win32more.winui3 import XamlApplication
from win32more.Microsoft.UI.Xaml import Window, FrameworkElement
from win32more.Microsoft.UI.Xaml.Media import MicaBackdrop,Imaging,FontFamily,CompositionTarget,VisualTreeHelper
from win32more.Microsoft.UI.Xaml.Markup import XamlReader
from win32more.Windows.UI.Xaml.Interop import TypeKind
from win32more.Windows.UI.Xaml import GridLength, GridLengthHelper, GridUnitType,DependencyObject,Thickness,Visibility
from win32more.Microsoft.UI.Xaml.Controls import InfoBar,Primitives,ProgressBar,ToggleSplitButton,Border,ToggleSwitch,Page,HyperlinkButton,Button,CheckBox,ComboBox,NumberBox, ProgressRing,Image,PasswordBox,TextBlock,TextBox, Slider, StackPanel, NavigationView, Frame, NavigationViewItem, RowDefinition, Grid, GridView, GroupStyle, Canvas, ToolTip
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
import threading,json,zipfile,requests
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

class InstallUI(XamlApplication):
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

		# Load splash screen XAML
		xaml = open("../assets/ui/exts/install/frame.xaml", encoding="utf-8").read()
		self.splash_window = XamlReader.Load(xaml).as_(Window)
		self.splash_window.SystemBackdrop = MicaBackdrop()
		self.document = self.splash_window.Content.as_(FrameworkElement).FindName("Content").as_(Frame)
		self.document.Content = XamlReader().Load(open("../assets/ui/exts/install/loading.xaml", encoding="utf-8").read())
		
		
		self.splash_window.Title = "DeskScout Extension Installer"
		
		self.splash_window.Activated += self.OnActivated
		self.splash_window.Activate()
		
		
		

		# Start background thread to simulate loading
		
		self.launched = False
		self.loadState = 1
		self.timer = DispatcherTimer()
		self.timer.Interval = TimeSpan(100)  # 100ms
		self.timer.Tick += lambda s, e: self._check_thread(None)
		self.timer.Start()
		self.page = "init"
		
	def OnActivated(self,obj,args):
		pass
	def _check_thread(self, thread):


		if self.launched:
			if self.page == "init":
				self.page = "main"
				self._load_main_app()
			elif self.page == "install":
				if InstallStatus.state == "decompressing":
					self.document.Content.as_(FrameworkElement).FindName("install.status").as_(TextBlock).Text = "Preparing to install"
				elif InstallStatus.state == "dircreate":
					self.document.Content.as_(FrameworkElement).FindName("install.status").as_(TextBlock).Text = "Installing"
					self.document.Content.as_(FrameworkElement).FindName("install.progress").as_(ProgressBar).IsIndeterminate = False
					self.document.Content.as_(FrameworkElement).FindName("install.progress").as_(ProgressBar).Value = InstallStatus.progress
				elif InstallStatus.state == "filecopy":
					self.document.Content.as_(FrameworkElement).FindName("install.status").as_(TextBlock).Text = f"Installing - Copying Files ({int(InstallStatus.progress)}%)"
					self.document.Content.as_(FrameworkElement).FindName("install.progress").as_(ProgressBar).IsIndeterminate = False
					self.document.Content.as_(FrameworkElement).FindName("install.progress").as_(ProgressBar).Value = InstallStatus.progress
				elif InstallStatus.state == "finished":
					self.page = "done"
					self.document.Content = XamlReader().Load(open("../assets/ui/exts/install/success.xaml", encoding="utf-8").read())
					self.document.Content.as_(FrameworkElement).FindName("install.ok").as_(Button).add_Click(self.finish)





					
		else:
			hwnd = self.splash_window.AppWindow.Id.Value
			self._set_window_properties(hwnd)
	def finish(self,b,a):
		self.splash_window.Close()
		exit(0)
	def _set_window_properties(self, hwnd):
		if self.launched:
			return
		# You can use win32 APIs to set size, position, etc.
		from win32more.Windows.Win32.UI.WindowsAndMessaging import (
			GetWindowRect, MoveWindow
		)

		# Example: center on screen
		from win32more.Windows.Win32.UI.WindowsAndMessaging import GetSystemMetrics
		from win32more.Windows.Win32.UI.WindowsAndMessaging import SM_CXSCREEN, SM_CYSCREEN

		screen_w = GetSystemMetrics(SM_CXSCREEN)
		screen_h = GetSystemMetrics(SM_CYSCREEN)
		self.splash_window.Content.as_(FrameworkElement).ActualWidth
		win_w, win_h = int(self.splash_window.Content.as_(FrameworkElement).ActualWidth), int(self.splash_window.Content.as_(FrameworkElement).ActualHeight)
		print(win_w,win_h)
		if not 0 in [win_w,win_h]:
			x = (screen_w - win_w) // 2
			y = (screen_h - win_h) // 2

			MoveWindow(hwnd, x, y, win_w, win_h, True)
			self.launched = True
	def _load_main_app(self):
		# Simulate work
		print("START")
		if args.type == "localfs":
			pkg = zipfile.ZipFile(args.src)
			manifest = json.load(pkg.open("install.json"))
			self.document.Content = XamlReader().Load(open("../assets/ui/exts/install/main.xaml", encoding="utf-8").read())
			self.document.Content.as_(FrameworkElement).FindName("install.name").as_(TextBlock).Text = manifest['manifest']['name']
			#Get expanded type name
			etn = json.load(open("../data/expandedTypes.json"))
			self.document.Content.as_(FrameworkElement).FindName("install.type").as_(TextBlock).Text = f"Type: {etn[manifest['manifest']['type']] if manifest['manifest']['type'] in list(etn) else 'Unknown ('+manifest['manifest']['type']+')'}"
			self.document.Content.as_(FrameworkElement).FindName("install.author").as_(TextBlock).Text = f"Author: {manifest['manifest']['author']}"
			self.document.Content.as_(FrameworkElement).FindName("install.version").as_(TextBlock).Text = f"Version: {manifest['manifest']['version']}"
			self.document.Content.as_(FrameworkElement).FindName("install.description").as_(TextBox).Text = manifest['manifest']['short']
			self.document.Content.as_(FrameworkElement).FindName("install.install").as_(Button).add_Click(self.beginInstall)

	def beginInstall(self,handle,bargs):
		InstallConfig.location = args.type
		InstallConfig.path = args.src
		self.page = "install"
		self.document.Content.as_(FrameworkElement).FindName("install.pbox").as_(StackPanel).Visibility = Visibility.Visible
		self.document.Content.as_(FrameworkElement).FindName("install.install").as_(Button).Visibility = Visibility.Collapsed
		Installer.run()
		
		

	def OnSuspending(self, args):
		print("App suspending...")

	def OnResuming(self, args):
		print("App resuming...")
class InstallConfig:
	location = "" # uri,store,selfhosted,localfs
	path = "" # Location of dep file, or store uuid
	start = False
class InstallStatus:
	progress = 0
	state = "ready"

class Installer:
	def fromLocalFs():
		print("Starting Installer")
		InstallStatus.state = "decompressing"
		pkg = zipfile.ZipFile(InstallConfig.path)
		manifest = json.load(pkg.open("install.json"))

		time.sleep(5)
		InstallStatus.state = "dircreate"
		try:
			os.mkdir('../data/extensions/'+manifest['manifest']['uuid'])
		except FileExistsError:
			pass
		actions = 0
		for i in manifest['dirs']:
			try:
				os.mkdir('../data/extensions/'+manifest['manifest']['uuid']+"/"+i)
			except FileExistsError:
				pass
			actions += 1
			InstallStatus.progress = round((actions/manifest['actions'])*100,1)
		InstallStatus.state = "filecopy"
		
		for i in range(len(manifest['files'])):
			file = open('../data/extensions/'+manifest['manifest']['uuid']+"/"+manifest['files'][i],'wb+')
			actions += 1
			InstallStatus.progress = round((actions/manifest['actions'])*100,1)
			infile = pkg.open("build/"+str(i),'r')
			for x in infile.read():
				file.write(x.to_bytes())
				actions += 1
				InstallStatus.progress = round((actions/manifest['actions'])*100,1)
			file.close()
		InstallStatus.state = "finished"
		try:
			requests.get("http://127.0.0.1:49152/reloadExts",timeout=5)
			print("Refreshing server ok")
		except:
			pass


		
	def run():
		import _thread
		
		if InstallConfig.location == "localfs":
			_thread.start_new_thread(Installer.fromLocalFs,())
			
parser = argparse.ArgumentParser("install")
parser.add_argument("-quiet",action="store_true")
parser.add_argument("-silent",action="store_true",help="use with -silent to truely install silently")

parser.add_argument("type",choices=["uri","store",'selfhosted',"localfs"])
parser.add_argument("-src",default="")
parser.add_argument("-uuid",default="")
args = parser.parse_args()
print(args.quiet)

if args.quiet:
	print("Quiet install detected")
	InstallConfig.location = args.type
	InstallConfig.path = args.src
	Installer.run()
	if not args.silent:
		from windows_toasts import InteractableWindowsToaster, Toast, ToastProgressBar
		toaster = InteractableWindowsToaster('DeskScout')

		newToast = Toast(['Starting.'])
		progressBar = ToastProgressBar('Installing...', progress=0)
		newToast.progress_bar = progressBar
		toaster.show_toast(newToast)
	
		if InstallStatus.state == "decompressing":
			progressBar.status = "Preparing to install..."
		elif InstallStatus.state == "dircreate":
			progressBar.status = "Preparing to install..."
			progressBar.progress = InstallStatus.progress*0.01

		elif InstallStatus.state == "filecopy":
			progressBar.status = "Installing"

			progressBar.progress = InstallStatus.progress*0.01
		
		newToast.text_fields = [f'Installing Extension']
		toaster.update_toast(newToast)
		if InstallStatus.state == "finished":
			toaster.remove_toast(newToast)
			newToast = Toast(['Extension installed'])
			toaster.show_toast(newToast)
	else:
		while InstallStatus.state != "finished":
			pass

		

else:
	XamlApplication.Start(InstallUI)
	print("Started")