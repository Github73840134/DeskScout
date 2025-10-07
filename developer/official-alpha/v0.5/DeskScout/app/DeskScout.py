import os, sys
os.chdir(os.path.dirname(__file__))
sys.path.append(os.path.join(os.getcwd(), "libs"))
sys.path.append(os.path.join(os.getcwd(), "mods"))
import subprocess
import requests
import psutil,time
time.sleep(10)

try:
	resp = requests.get("http://127.0.0.1:49152/",timeout=3)
except:
	subprocess.Popen("pyw DeskScoutService.py")
time.sleep(10)
os.system("py DeskScoutApp.py")