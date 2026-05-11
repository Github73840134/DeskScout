print("DeskScout-Do not close this window")

import sys,os,subprocess,shlex,zipfile,json
os.chdir(os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(0,os.path.join(os.getcwd(), "libs"))
sys.path.append(os.path.join(os.getcwd(), "mods"))
os.chdir(os.path.dirname(__file__))
import requests
path = sys.argv[1]
def changeSetting(path,value):
		# Changes a setting at path to value
		try:
			#Send a POST request to the settings endpoint
			resp = requests.post("http://127.0.0.1:49152/settings",data={"action":"set","path":path,"value":value})
			data = json.loads(resp.text)
			if data['status'] == "ok":
				return True
			else:
				return False
		except:
			return False
zip = zipfile.ZipFile(path)
for i in zip.filelist:
	if i.filename.startswith("sounds/"):
		if i.filename == "sounds/":
			continue
		x = zip.open(i.filename)
		y = open(f"../assets/sounds/extern/{os.path.basename(i.filename)}",'wb+')
		y.write(x.read())
		y.close()
for i in zip.filelist:
	if i.filename.startswith("extensions/"):
		if i.filename == "extensions/":
			continue
		x = zip.open(i.filename)
		y = open(f"../cache/{os.path.basename(i.filename)}",'wb+')
		y.write(x.read())
		y.close()
		os.system(f"py ExtensionTools/install.py localfs -src ../cache/{os.path.basename(i.filename)} -quiet -silent")
		os.remove(f"../cache/{os.path.basename(i.filename)}")
try:
	resp = requests.get("http://127.0.0.1:49152/reloadExts") #Get Extensions
except:
	pass
for i in zip.filelist:
	if i.filename == "settings.json":
		x = zip.open("settings.json")
		y = open("../data/settings.json",'wb+')
		y.write(x.read())
		y.close()
for i in zip.filelist:
	if i.filename == "glucose.gdr":
		try:
			changeSetting("gdrState",'0')
		except:
			pass
		x = zip.open("glucose.gdr")
		y = open("../data/glucose.gdr",'wb+')
		y.write(x.read())
		y.close()
		os.system("py gdrmanage.py unpack")
		try:
			changeSetting("gdrState",'1')
		except:
			pass
