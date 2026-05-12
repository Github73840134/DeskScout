print("DeskScout-Do not close this window")
import os, sys,subprocess
builtin_exts = ["gdp_dexshare","gdp_dexshareJP","gdp_dexshareOUS","gdp_librelink"]
os.chdir(os.path.dirname(__file__))
sys.path.append(os.path.join(os.getcwd(), "libs"))
sys.path.append(os.path.join(os.getcwd(), "mods"))
import time
import zipfile
zip = zipfile.ZipFile(sys.argv[1],'w')
zip.open(".deskscout_2026_3_11",'w').close()
file = zip.open('settings.json','w')
file.write(open("../data/settings.json",'rb').read())
file.close()
zip.mkdir('sounds')
zip.mkdir('extensions')

# Copy sounds to backup
for i in os.listdir("../assets/sounds/extern"):
	x = open(f"../assets/sounds/extern/{i}",'rb')
	y = zip.open(f"sounds/{i}",'w')
	y.write(x.read())
	y.close()

# Extensions
for i in os.listdir("../data/extensions"):
	if i in builtin_exts:
		continue
	res = subprocess.run(f"pyw ../tools/deu build \"{os.path.abspath('../data/extensions/'+i)}\" -output \"{os.path.abspath('../cache')}\"")
	if res.returncode == 0:
		pkg = zip.open(f"extensions/{i}.dep",'w')
		file = open(f"../cache/{i}.dep",'rb')
		pkg.write(file.read())
		file.close()
		pkg.close()
		os.remove(f"../cache/{i}.dep")

# Glucose History
file = zip.open('glucose.gdr','w')
file.write(open("../data/glucose.gdr",'rb').read())
file.close()

zip.close()
