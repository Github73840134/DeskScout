import sys,os,time
os.chdir(os.path.dirname(__file__))
sys.path.append(os.path.abspath(os.path.join(os.getcwd(),'../','app','libs')))
sys.path.append(os.path.abspath(os.path.join(os.getcwd(),'../','app','mods')))
import PySimpleGUI as sg
import gdr
from tkinter import filedialog,messagebox
class Menus:
	default = [
		["&File",["&Open","&About"]]
	]
	edit = [
		["&File",["&Open","&About"]],
		["&Cleanup",["Remove &Nearby Entries"]]
	]
layout = [
	[sg.Menu(Menus.default,key="menu")],
	[sg.Frame("Original",[
		[sg.Tree(sg.TreeData(),col0_heading="Millis",headings=["Date","Time","Value","Trend"],key="original")]
	]),
	sg.Frame("Modified",[
		[sg.Tree(sg.TreeData(),col0_heading="Millis",headings=["Date","Time","Value","Trend"],key="modified")]
	])],
	[sg.Button("Remove")],
	[sg.ProgressBar(100,size=(10,20),key='prog',visible=False),sg.Text("Ready-No File Open",key='status')]
]
def genStatus():
	recordstate = ""
	savestate = ""
	if isinstance(record,gdr.RecordAccess):
		recordstate = f"({os.path.basename(fn)}) Ready"
		if saved:
			savestate = "Saved"
		else:
			savestate = "Unsaved Changes"
	else:
		recordstate = "Ready"
	return f"{recordstate}-{savestate}"
def setupEditor():
	global record
	trc = record.getRecordCount()
	window['prog'].update(visible=True)
	window['prog'].UpdateBar(0,max=trc)
	original.clear()
	modified.clear()
	for i in range(trc):
		original.append(record.getRecordByIndex(i))
		modified.append(record.getRecordByIndex(i))
		window['prog'].UpdateBar(i+1)
		window.refresh()
	window['prog'].update(visible=False)
	window.refresh()
		

def makeOriginTree():
	tree = sg.TreeData()
	for rec in original:
		millis = int(rec.time/1000)
		date = time.strftime("%m/%d/%Y",time.localtime(millis))
		_time = time.strftime("%H:%M:%S",time.localtime(millis))

		tree.Insert("","record."+str(rec.time/1000),str(rec.time/1000),[date,_time,str(rec.value),str(rec.trendArrow)])
	return tree
def makeModifiedTree():
	tree = sg.TreeData()
	for rec in modified:
		millis = int(rec.time/1000)
		date = time.strftime("%m/%d/%Y",time.localtime(millis))
		_time = time.strftime("%H:%M:%S",time.localtime(millis))

		tree.Insert("","record."+str(rec.time/1000),str(rec.time/1000),[date,_time,str(rec.value),str(rec.trendArrow)])
	return tree
def removeNearbyEntries():
	first = modified.copy()
		
window = sg.Window("GDR View Tool",layout)
original = []
modified = []
record = gdr.RecordAccess
saved = True
fn = None
while True:
	event, values = window.read()
	if event == sg.WIN_CLOSED:
		exit(0)
	if event == "Open":
		fn = filedialog.askopenfilename(filetypes=[["Glucose Data Record",".gdr"]],initialfile=os.path.abspath(os.path.join(os.getcwd(),"../",'data','glucose.gdr')),initialdir=os.path.abspath(os.path.join(os.getcwd(),"../",'data')))
		if not fn:
			continue

		if isinstance(record,gdr.RecordAccess) and not saved:
			ans = messagebox.askyesno("Warning","You have unsaved chnages. Are you",icon="warning")
			if not ans:
				continue
		window['status'].Update("Checking File...")
		window.refresh()
		try:
			record = gdr.RecordAccess(fn)
		except:
			messagebox.showerror("Error","Glucose data record could not be parsed")
			window['status'].Update(genStatus())
			window.refresh()
			continue
		window['status'].Update("Loading Data")
		window.refresh()
		setupEditor()
		window['original'].Update(makeOriginTree())
		window['modified'].Update(makeModifiedTree())
		window['status'].Update(genStatus())