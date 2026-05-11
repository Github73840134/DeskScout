import os, sys
os.chdir(os.path.dirname(__file__))
sys.path.append(os.path.join(os.getcwd(), "libs"))
sys.path.append(os.path.join(os.getcwd(), "mods"))
import prefs
prefs.reader("../data/newSettings.json","../data/")