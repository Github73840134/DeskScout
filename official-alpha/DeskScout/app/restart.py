import sys,os,subprocess
os.chdir(os.path.dirname(__file__))
sys.path.insert(0,os.path.join(os.getcwd(), "libs"))
sys.path.append(os.path.join(os.getcwd(), "mods"))
import requests
try:
	requests.get("http://127.0.0.1:49152/shutdown")
except:
	pass
subprocess.Popen("pyw DeskScoutService.py",shell=True,start_new_session=True)