print("Tray Service Is Starting")
import os,sys
from PIL import Image,ImageDraw,ImageFont
import _thread

os.chdir(os.path.dirname(__file__))
sys.path.append(os.path.join(os.getcwd(), "libs"))
sys.path.append(os.path.join(os.getcwd(), "mods"))
import pystray
import requests,psutil,time
from pystray import Icon as icon, Menu as menu, MenuItem as item
state = False

def shutdown(icon, item):
	requests.get("http://localhost:60/shutdown")
def backup(icon,item):
	pass
def viewstatus(icon,item):
	pass
def openbackup(icon,item):
	requests.post("http://localhost:60/api",{"cmd":'open_ui',"data":""})
backupstatus = item("Backup Not Run",viewstatus)
backupbutton = item('Start backup now',backup)
icon = pystray.Icon(
	'DeskScout',
	icon=Image.open("../assets/icons/sync_working.png"),
	menu=menu(
		item("DeskScout",default=True,action=openbackup),
		backupstatus,
		backupbutton,
		item(
		'Shutdown Deskscout',
		shutdown)
	),

	)

def manager(x):
	x.visible = True
	while True:
		#s = requests.get("http://localhost:49152/getLatestReading")
	#	if s.status_code == 200:
		space = Image.new("RGBA",(50,50))
		x = ImageDraw.Draw(space,"RGBA")
		font = ImageFont.truetype("arial.ttf",50)
		x.text((0,10), "→", fill=(255,255,255), font=font)
		font = ImageFont.truetype("arial.ttf",30)
		x.text((0,0), "100", fill=(255,255,255), font=font)
		icon.icon = space
		time.sleep(5)


# To finally show you icon, call run
icon.run(manager)
