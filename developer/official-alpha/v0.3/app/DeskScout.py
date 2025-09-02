import os, sys
os.chdir(os.path.dirname(__file__))
sys.path.append(os.path.join(os.getcwd(), "libs"))
sys.path.append(os.path.join(os.getcwd(), "mods"))
import subprocess
import requests
import psutil

try:
	resp = requests.get("http://127.0.0.1:49152/",timeout=3)
except:
	subprocess.Popen("pyw DeskScoutService.py")
os.system("pyw DeskScoutApp.py")