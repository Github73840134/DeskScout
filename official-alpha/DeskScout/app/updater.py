import zipfile,json
import os
import logging,time
import os, sys,shutil
import argparse
import sys
import time
mods = [m for m in sys.modules if "charset" in m.lower()]
print(mods)
os.chdir(os.path.dirname(__file__))
sys.path.append(os.path.join(os.getcwd(), "libs"))
sys.path.append(os.path.join(os.getcwd(), "mods"))
from mods import PySimpleGUI as sg
sg.theme('SystemDefault')
def wait_until_unlocked(path, timeout=30, interval=0.5):
	start = time.time()

	while True:
		try:
			# rename test (very reliable on Windows)
			temp = path + ".locktest"

			os.rename(path, temp)
			os.rename(temp, path)

			return True

		except PermissionError:
			if time.time() - start > timeout:
				return False

			time.sleep(interval)

		except FileNotFoundError:
			# file vanished
			return False
parser = argparse.ArgumentParser("update")
parser.add_argument("-file",default="../data/update.zip",required=False)
args = parser.parse_args(sys.argv[1:])
class DeltaTimeFormatter(logging.Formatter):
	def format(self, record):
		record.delta = time.time()-ast
		return super().format(record)
handler = logging.StreamHandler(open("updater.log","w"))
LOGFORMAT = '+%(asctime)s [%(delta)s] %(name)s %(levelname)s: %(message)s'
fmt = DeltaTimeFormatter(LOGFORMAT)
handler.setFormatter(fmt)
logging.basicConfig(
					format='%(asctime)s [%(delta)s] %(levelname)-9s: %(message)s',
					datefmt='%Y-%m-%d %H:%M:%S',
					handlers=[handler],
					level=logging.DEBUG)
log = logging.getLogger("update")
ast = time.time()
log.info("Checking for update")
if not os.path.exists(args.file):
	log.error("No Update Available")
	exit(2)
else:
	log.info("Update found")
	layout = [
	[sg.Text("Please wait",key="status")],
	[sg.ProgressBar(0,size=(20,10),key='prog')]
	]
	window = sg.Window("DeskScout Installer",layout,finalize=True,disable_close=True)
	window.refresh()
	for i in range(0,10):
		time.sleep(1)
		window.refresh()
	window['status'].update("Installing updates")
	window.refresh()



try:
	zip = zipfile.ZipFile(args.file)
except Exception as e:
	log.critical(f"Failed to open update {str(e)}")
	exit(3)
dirs = zip.open("dirs.txt").read().decode().split("\n")
dtd = zip.open("dtd.txt").read().decode().split("\n")
ftd = zip.open("ftd.txt").read().decode().split("\n")

files = json.load(zip.open("files.txt"))
ta = int(zip.open("ta").read().decode())
actions = 0
window['prog'].UpdateBar(0,max=ta)
os.chdir(os.path.dirname(os.path.dirname(__file__)))
for i in ftd:
	try:
		log.info(f"Deleting file {i}")
		os.remove(i)
		actions += 1
		window['prog'].UpdateBar(actions)
	except:
		#print("Directory already found")
		pass
for i in dtd:
	try:
		log.info(f"Deleting Directory {i}")
		shutil.rmtree(i)
		actions += 1
		window['prog'].UpdateBar(actions)
	except:
		#print("Directory already found")
		pass
for i in dirs:
	try:
		log.info(f"Making Directory {i}")
		os.mkdir(i)
		actions += 1
		window['prog'].UpdateBar(actions)
	except:
		#print("Directory already found")
		pass
for i in files:
	try:
		#log.info(f"Waiting for file unlock {files[i]}")
			
		log.info(f"Copying file {files[i]}")
		
		file = zip.open(i,'r')
		
		out = open(files[i],'wb+')
		actions += 1
		window['prog'].UpdateBar(actions)

		out.write(file.read())
		actions += file.tell()
		window['prog'].UpdateBar(actions)
			
	except Exception as e:
		log.critical(f"Error during copy {files[i]} ({i}): {str(e)}")
		exit(3)
os.chdir(os.path.dirname(__file__))
log.info("Checking for settings updates")
if os.listdir("../data/upgradeSettings") != []:
	window['status'].update("Finishing up...")
	window['prog'].UpdateBar(0,max=len(os.listdir("../data/upgradeSettings")))
	x = 0
	for i in os.listdir("../data/upgradeSettings"):
		log.info(f"Updating {i}")
		try:
			
			from mods import prefs
			prefs.reader(f"../data/upgradeSettings/{i}","../data/")
			os.remove(f"../data/upgradeSettings/{i}")
			log.info(f"Settings {i} updated")
			window['prog'].UpdateBar(x+1)
			x += 1
		
		except Exception as e:
			log.critical(f"Error during settings update: {str(e)}")
			exit(3)
else:
	log.info("No settings needed to be updated")
log.info("Update Complete")