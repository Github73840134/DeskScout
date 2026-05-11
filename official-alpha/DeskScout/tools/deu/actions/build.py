import zipfile
import json
import os
import argparse

__args__ = None
parser = argparse.ArgumentParser("build","build [path] [output]","Makes an extension installable")
parser.add_argument("path")
parser.add_argument("-output",default=os.getcwd(),required=False)
def run():
	
	args = parser.parse_args(__args__)
	cdir = os.getcwd()
	os.chdir(args.path)
	manifest = json.load(open("manifest.json"))
	os.chdir(cdir)
	pkg = zipfile.ZipFile(os.path.join(args.output,manifest['uuid']+".dep"),'w')
	os.chdir(args.path)
	pkg.mkdir("build")
	
	dtc = []
	ftc = []
	actionId = 0
	print(f"Building {manifest['name']}")
	
	for root,dirs,files in os.walk("."):
		for i in dirs:
			print("Adding Directory",os.path.normpath(os.path.join(root,i)))
			dtc.append(os.path.normpath(os.path.join(root,i)))
			actionId += 1
		for i in files:
			print("Adding File",os.path.normpath(os.path.join(root,i)))

			outfile = pkg.open(os.path.join("build",str(len(ftc))),'w')
			ftc.append(os.path.normpath(os.path.join(root,i)))
			file = open(os.path.join(root,i),"rb")
			data = file.read()
			actionId += len(data)
			outfile.write(data)
			outfile.close()
	mfst = pkg.open("install.json","w")
	mfst.write(json.dumps({
		"platform":"win32",
		"actions":actionId,
		"dirs":dtc,
		"files":ftc,
		"manifest":manifest
	}).encode())
	mfst.close()
	pkg.close()