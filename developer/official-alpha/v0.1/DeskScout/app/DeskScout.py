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
	subprocess.Popen(os.path.join(os.getcwd(),"../","python-3.12.2.amd64","pythonw.exe")+" DeskScoutService.py")
	resp = requests.get("http://127.0.0.1:49152/")
	print(resp.status_code)
	print("STARTED")
	subprocess.Popen(os.path.join(os.getcwd(),"../","python-3.12.2.amd64","pythonw.exe")+" TrayButton.py")

os.system(os.path.join(os.getcwd(),"../","python-3.12.2.amd64","pythonw.exe")+" DeskScoutApp.py")