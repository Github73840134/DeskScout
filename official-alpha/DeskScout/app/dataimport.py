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
def merge_dicts(destination, source):
	for key, value in source.items():
		if (
			key in destination
			and isinstance(destination[key], dict)
			and isinstance(value, dict)
		):
			# Recursively merge nested dictionaries
			merge_dicts(destination[key], value)
		else:
			# Only add key if it doesn't already exist
			destination.setdefault(key, value)

	return destination
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
		subprocess.run(f"../core/pythonw.exe ExtensionTools/install.py localfs -src ../cache/{os.path.basename(i.filename)} -quiet -silent")
		os.remove(f"../cache/{os.path.basename(i.filename)}")
try:
	resp = requests.get("http://127.0.0.1:49152/reloadExts") #Get Extensions
except:
	pass
for i in zip.filelist:
	if i.filename == "settings.json":
		x = merge_dicts(json.load(zip.open("settings.json")),json.load(open("../data/settings.json",'r')))
		y = open("../data/settings.json",'wb+')
		y.write(json.dumps(x).encode())
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
		subprocess.run("../core/pythonw.exe gdrmanage.py unpack")
		try:
			changeSetting("gdrState",'1')
		except:
			pass
