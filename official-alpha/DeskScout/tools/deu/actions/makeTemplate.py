import os,argparse

__args__ = None
parser = argparse.ArgumentParser("makeTemplate","makeTemplate [path]","Makes an extension template")
parser.add_argument("path")

__manifest__ = f"""{{
	"name":"Test Extension",
	"type":"",
	"sdk":"",
	"serviceName":""
	"author":"",
	"url":"",
	"update":"",
	"version":"",
	"logo":null,
	"id":"",
	"uuid":"",
	"short":""
}}"""
print(__manifest__)
def run():
	args = parser.parse_args(__args__)
	os.mkdir(args.path)
	file = open(os.path.join(args.path,'manifest.json'),'w+')
	file.write(__manifest__)
	file.close()
	open(os.path.join(args.path,'__init__.py'),"w+").close()
