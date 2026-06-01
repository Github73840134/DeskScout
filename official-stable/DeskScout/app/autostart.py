import os,json,subprocess,requests
os.chdir(os.path.dirname(__file__))
settings = json.load(open("../data/settings.json"))
if settings['autostart']:
	subprocess.Popen("../core/pythonw.exe DeskScoutService.py -fromDeskScoutPy",start_new_session=True)