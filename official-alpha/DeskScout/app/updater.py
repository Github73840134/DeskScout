import zipfile,json
import os
import logging,time
import os, sys
os.chdir(os.path.dirname(__file__))
sys.path.append(os.path.join(os.getcwd(), "libs"))
sys.path.append(os.path.join(os.getcwd(), "mods"))
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
if not "update.zip" in os.listdir("../data"):
	log.error("No Update Available")
	exit(2)
else:
	log.info("Update found")
try:
	zip = zipfile.ZipFile("../data/update.zip")
except Exception as e:
	log.critical(f"Failed to open update {str(e)}")
	exit(3)
dirs = zip.open("dirs.txt").read().decode().split("\n")
files = json.load(zip.open("files.txt"))
os.chdir(os.path.dirname(os.path.dirname(__file__)))
for i in dirs:
	try:
		log.info(f"Making Directory {i}")
		os.mkdir(i)
	except:
		print("Directory already found")
for i in files:
	try:
		log.info(f"Copying file {files[i]}")
		file = zip.open(i,'r')
		out = open(files[i],'wb+')
		out.write(file.read())
	except Exception as e:
		log.critical(f"Error during copy {files[i]} ({i}): {str(e)}")
		exit(3)
log.info("Checking for settings update")
if "newSettings.pref" in os.listdir("data"):
	log.info("Updating settings")
	try:
		
		import prefs
		prefs.reader("data/newSettings.pref","data/")
		os.remove('data/newSettings.pref')
		log.info("Settings updated")
	except Exception as e:
		log.critical(f"Error during settings update: {str(e)}")
		exit(3)
else:
	log.info("No settings needed to be updated")
log.info("Update Complete")