import importlib
import json
import os
import sys
os.chdir(os.path.dirname(__file__))
sys.path.insert(0,os.path.join(os.getcwd(),'libs'))
sys.path.append(os.path.join(os.getcwd(),'mods'))
def DeskScoutAPIRequire(sdk_id):
	sdkmanifest = json.load(open("../data/sdk.json"))
	if sdk_id in sdkmanifest:
		if sdkmanifest[sdk_id]['type'] == "api":
			spec = importlib.util.spec_from_file_location("sdk.api.v1", f"{sdkmanifest[sdk_id]['path']}")
			api = importlib.util.module_from_spec(spec)
			# Register the module in sys.modules (optional but good practice)
			# Execute the module code
			spec.loader.exec_module(api)
			api.mods = importlib.import_module("mods",package="mods")
			return api
	else:
		raise Exception("Invalid SDK")



exec(open(sys.argv[1]).read(),{"DeskScoutAPIRequire":DeskScoutAPIRequire})
