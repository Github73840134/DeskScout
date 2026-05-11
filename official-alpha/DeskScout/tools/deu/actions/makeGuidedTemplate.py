import os,argparse,json,time

__args__ = None
parser = argparse.ArgumentParser("makeTemplate","makeTemplate [path]","Makes an extension template")
parser.add_argument("path")

__manifest__ = {
	"name":"Test Extension",
	"type":"",
	"sdk":"",
	"serviceName":"",
	"author":"",
	"url":"",
	"update":"",
	"version":time.strftime("%Y.%m.%d-%H%M",time.localtime()),
	"logo":None,
	"id":"",
	"uuid":"test_",
	"short":""
}
__sdks__ = ['sdk.gdp.v1']
__exttypes__ = ['gdp']

print(__manifest__)
def run():
	args = parser.parse_args(__args__)
	# Get info about
	import tgui
	screen = tgui.Screen()
	screen.open()
	screen.clear()
	if not os.path.exists(os.path.dirname(args.path)):
		tgui.Popup.message("Error","The path specified does not exist")
		print("\u001b[0m")
		screen.clear()
		screen.close()
		return
	run = True
	oans = 0
	while run:
		ans = tgui.menu("Create a DeskScout Extension",
			[f"Name: {__manifest__['name']}",f"SDK Version: {__manifest__['sdk']}",f"Type: {__manifest__['type']}",f"Author: {__manifest__['author']}",f"URL: {__manifest__['url']}",f"Update URL: {__manifest__['update']}",f"Version: {__manifest__['version']}",f"Logo path: {__manifest__['logo']}",f"ID: {__manifest__['id']}",f"UUID: {__manifest__['uuid']}","Description:","[Make]"],
			hint="Select Make to create your template, press ESC to exit.")
		if ans != None:
			oans = ans
		if ans == 0:
			screen.clear()
			name = tgui.Popup.input_popup("Enter the name for your project",__manifest__['name'])
			if name != None:
				__manifest__['name'] = name
		if ans == 1:
			screen.clear()
			name = tgui.menu("Select the SDK Version",__sdks__)
			if name != None:
				__manifest__['sdk'] = __sdks__[name]
		if ans == 2:
			screen.clear()
			name = tgui.menu("Select the Extension Type",__exttypes__)
			if name != None:
				__manifest__['type'] = __exttypes__[name]
		if ans == 3:
			screen.clear()
			name = tgui.Popup.input_popup("Enter your name",__manifest__['author'])
			if name != None:
				__manifest__['author'] = name
		if ans == 4:
			screen.clear()
			name = tgui.Popup.input_popup("Enter the project homepage url if applicable",__manifest__['url'])
			if name != None:
				__manifest__['url'] = name
		if ans == 5:
			screen.clear()
			name = tgui.Popup.input_popup("Enter the update server url",__manifest__['update'])
			if name != None:
				__manifest__['update'] = name
		if ans == 6:
			screen.clear()
			name = tgui.Popup.input_popup("Enter the version of your project",__manifest__['version'])
			if name != None:
				__manifest__['version'] = name
		if ans == 7:
			screen.clear()
			name = tgui.Popup.input_popup("Enter the logo of your project",__manifest__['logo'])
			if name != None:
				__manifest__['logo'] = name
		if ans == 8:
			screen.clear()
			name = tgui.Popup.input_popup("Enter the ID of your project",__manifest__['id'])
			if name != None:
				__manifest__['id'] = name
		if ans == 9:
			screen.clear()
			name = tgui.Popup.input_popup("Enter the UUID of your project (SEE DOCUMENTATION FOR DETAILS)",__manifest__['uuid'])
			if name != None:
				__manifest__['uuid'] = name
		if ans == 10:
			screen.clear()
			name = tgui.Popup.input_popup("Enter the description of your project",__manifest__['short'])
			if name != None:
				__manifest__['short'] = name
		if ans == 11:
			run = False
			build = True
		if ans == None:
			build = False
			break
	
	print("\u001b[0m")
	screen.clear()
	screen.close()
	if build:
		print("Creating build folder")
		os.mkdir(args.path)
		print("Creating manifest")
		file = open(os.path.join(args.path,'manifest.json'),'w+')
		file.write(json.dumps(__manifest__))
		file.close()
		file = open(os.path.join(args.path,'__init__.py'),"w+")
	
		file.close()

	
	