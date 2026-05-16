import os, sys
os.chdir(os.path.dirname(__file__))
sys.path.append(os.path.join(os.getcwd(), "libs"))
sys.path.append(os.path.join(os.getcwd(), "mods"))
os.chdir(os.path.dirname(__file__))
print("Checking for settings updates")
if os.listdir("../data/upgradeSettings") != []:
	for i in os.listdir("../data/upgradeSettings"):
		print(f"Updating {i}")
		try:
			
			from mods import prefs
			prefs.reader(f"../data/upgradeSettings/{i}","../data/")
			os.remove(f"../data/upgradeSettings/{i}")
			print(f"Settings {i} updated")
		
		except Exception as e:
			print(f"Error during settings update: {str(e)}")
			exit(3)
else:
	print("No settings needed to be updated")
print("Update Complete")