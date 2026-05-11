# Un-Installs extensions
import os
import argparse
import zipfile
import sys
import shutil
os.chdir(os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(0,os.path.join(os.getcwd(), "libs"))
sys.path.append(os.path.join(os.getcwd(), "mods"))
parser = argparse.ArgumentParser("uninstall")
parser.add_argument("uuid")

args = parser.parse_args(sys.argv[1:])

import time,json
from windows_toasts import InteractableWindowsToaster, Toast, ToastProgressBar

toaster = InteractableWindowsToaster('DeskScout')


if args.uuid in os.listdir("../data/extensions"):
	manifest = json.load(open(f"../data/extensions/{args.uuid}/manifest.json"))
	newToast = Toast([f"Uninstalling {manifest['name']}"])
	toaster.show_toast(newToast)
	shutil.rmtree(f"../data/extensions/{args.uuid}")
	newToast = Toast([f"Uninstalled {manifest['name']}"])
	toaster.show_toast(newToast)