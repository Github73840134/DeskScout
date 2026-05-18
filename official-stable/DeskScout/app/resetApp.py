# Resets settings, and removes glucose data, and extensions that did come with the application
import os,subprocess
import argparse
import shutil
import sys,json
from tkinter import messagebox
os.chdir(os.path.dirname(__file__))
try:
	os.mkdir("../cache")
except:
	pass
vinfo = json.load(open('versioninfo.json'))
if vinfo['release'] in ["stable","beta"]:
	USERKEY = f"com.sedwards.deskscout-{vinfo['release']}"
else:
	USERKEY = f"com.sedwards.deskscout"
__release__ = vinfo['release']
del(vinfo)
sys.path.insert(0,os.path.join(os.getcwd(), "libs"))
sys.path.append(os.path.join(os.getcwd(), "mods"))
import PySimpleGUI as sg
import requests
import psutil
parser = argparse.ArgumentParser("resetApp.py")
parser.add_argument("-retainGlucoseHistory",action="store_true",required=False)
parser.add_argument("-retainExtensions",action="store_true",required=False)
parser.add_argument("-retainSounds",action="store_true",required=False)
parser.add_argument("-retainSettings",action="store_true",required=False)
parser.add_argument("-quiet",action="store_true",required=False)
parser.add_argument("-autostart",action="store_true",required=False)


args = parser.parse_args(sys.argv[1:])
print(args)
msg = [
	"Whats going to be cleared",
	f"Settings: {'Yes' if not args.retainSettings else 'No'}",
	f"User added Sounds: {'Yes' if not args.retainSounds else 'No'}",
	f"Glucose History: {'Yes' if not args.retainGlucoseHistory else 'No'}",
	f"Extensions: {'Yes' if not args.retainExtensions else 'No'}",

]
if not args.quiet:
	messagebox.showinfo("DeskScout","\n".join(msg))
	ans = messagebox.askyesno("Reset DeskScout", "Are you sure you want to clear these settings")
	if ans == False:
		exit()
	layout = [
	[sg.Text("Resetting App")],
	[sg.Text("Please wait... This may take several minutes",key="status")]
	]
	window = sg.Window("DeskScout",layout,finalize=True,disable_close=True)
	window.read(timeout=0)
print("Shutting down service")
rebootService = False
try:
	resp = requests.get("http://127.0.0.1:49152/shutdown",timeout=5)
	rebootService = True
except:
	pass
for proc in psutil.process_iter(['pid', 'name','cmdline','exe']):
	if proc.info['name'] in ["pythonw.exe","python.exe","py","pyw"]:
		for i in ["DeskScout.pyw","DeskScoutApp.py","DeskScoutOverlay.py","DeskScoutSetup.py","DeskScoutAlertOverlay.py","DeskScoutDiscordRichPresence.py"]:
			if i in proc.info['cmdline'][1]:
				print("Found",i,proc.info)
				proc.kill()
if not args.retainSettings:
	import json,keyring
	settings = json.load(open('../data/settings.json'))
	try:
		keyring.delete_password(USERKEY,settings['username'])
	except:
		pass
	file = open("../data/settings.json","wb+")
	file.write(open("../data/default_settings.json",'rb').read())
	file.close()
if not args.retainGlucoseHistory:

	shutil.rmtree("../data/glucose/daily")
	os.mkdir("../data/glucose/daily")
	try:
		os.remove("../data/glucose.gdr")
	except:
		pass
if not args.retainExtensions:

	shutil.rmtree("../data/extensions")
	os.mkdir("../data/extensions")
	import subprocess
	ring = []
	for i in os.listdir("../data/basepkgs"):
		ring.append(subprocess.Popen(f"../core/pythonw.exe ExtensionTools/install.py localfs -src ../data/basepkgs/{i} -quiet -silent",shell=True))
	while ring:
		xring = ring
		y = 0
		for i in xring:
			if i.poll() == None:
				pass
			else:
				ring.remove(i)
			y += 1
	print("Complete")
			
if not args.retainSounds:
	shutil.rmtree("../assets/sounds/extern")
	os.mkdir("../assets/sounds/extern")

if args.autostart:
	import subprocess
	subprocess.Popen("../core/pythonw.exe DeskScout.pyw",shell=True,start_new_session=True)
exit(0)