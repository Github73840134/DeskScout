import os,json,subprocess,requests
os.chdir(os.path.dirname(__file__))
settings = json.load(open("../data/settings.json"))
if settings['autostart']:
	subprocess.Popen("py DeskScoutService.py -fromDeskScoutPy",shell=True,start_new_session=True)