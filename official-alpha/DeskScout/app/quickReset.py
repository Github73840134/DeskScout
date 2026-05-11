import os
os.chdir(os.path.dirname(__file__))
import json
import shutil
ans = input("Do a quick reset? type y")
if ans == "y":
	shutil.rmtree("../data/glucose/daily")
	os.mkdir("../data/glucose/daily")
	try:
		os.remove("../data/glucose.gdr")
	except:
		pass
	import requests
	requests.get("http://127.0.0.1:49152/initializeGDR")