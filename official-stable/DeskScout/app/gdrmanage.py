import sys
import os,time
os.chdir(os.path.dirname(__file__))
from mods import gdr
def remove_duplicates(items):
	seen = set()
	unique = []
	for item in items:
		if item not in seen:
			seen.add(item)
			unique.append(item)
	return unique
if sys.argv[1] == 'create':
	gdr.createRecordFile(os.path.abspath("../data/glucose.gdr"))
elif sys.argv[1] == "removeDuplicates":
	print("removing dupes")
	records = gdr.RecordAccess(os.path.abspath("../data/glucose.gdr"))

	rlen = records.getRecordCount()
	recs = []
	recs = []
	times = []
	dups = 0
	for i in range(records.getRecordCount()):
		if records.getRecordByIndex(i).time in times:
			print("Duplicate entry with id",i,dups)
			dups += 1
		else:
			times.append(records.getRecordByIndex(i).time)
			recs.append(records.getRecordByIndex(i))
	gdr.createRecordFile(os.path.abspath("../data/glucose.gdr"))
	records = gdr.RecordAccess(os.path.abspath("../data/glucose.gdr"))
	for i in recs:
		print(i.time)
		records.writeRecord(i.time,i.value,i.trendArrow)
elif sys.argv[1] == "checkForDuplicates":
	dups = 0
	records = gdr.RecordAccess(os.path.abspath("../data/glucose.gdr"))

	rlen = records.getRecordCount()
	recs = []
	times = []
	for i in range(records.getRecordCount()):
		if not records.getRecordByIndex(i).time in times:
			dups += 1
		else:
			times.append(records.getRecordByIndex(i).time)
			recs.append(records.getRecordByIndex(i))
	print("Duplicates found:",dups)
elif sys.argv[1] == "backup":
	import shutil
	print("Backing up glucose records")
	shutil.copy("../data/glucose.gdr",sys.argv[2])
elif sys.argv[1] == "restore":
	import shutil
	print("Importing glucose records")
	shutil.copy(sys.argv[2],"../data/glucose.gdr")
elif sys.argv[1] == "summarize":
	print("Combining glucose data")
	gdr.createRecordFile("../data/glucose/summary.gdr")
	out = gdr.RecordAccess("../data/glucose/summary.gdr")
	out.file.seek(out.recordEntrypoint)	
	for i in os.listdir("../data/glucose/daily"):
		_in = gdr.RecordReader(os.path.abspath(f"../data/glucose/daily/{i}"))
		out.file.write(_in.getRawDataUnderHeader())
elif sys.argv[1] == "unpack":
	_in = gdr.RecordReader("../data/glucose.gdr")
	last = ""
	rec = None
	for i in range(_in.getRecordCount()):
		x = _in.getRecordByIndex(i)
		if time.strftime("%Y-%m-%d",time.localtime(x.time/1000)) != last:
			last = time.strftime("%Y-%m-%d",time.localtime(x.time/1000))
			print("NEW DAY",last)
			gdr.createRecordFile(f"../data/glucose/daily/{last}.gdr")
			rec = gdr.RecordAccess(f"../data/glucose/daily/{last}.gdr")
		else:
			rec.writeRecord(_in.getRecordByIndex(i).time,_in.getRecordByIndex(i).value,_in.getRecordByIndex(i).trendArrow)
elif sys.argv[1] == "list":
	rec = gdr.RecordReader(sys.argv[2])
	for i in range(rec.getRecordCount()):
		print(time.strftime("%m/%d/%Y-%H:%M:%S",time.localtime(rec.getRecordByIndex(i).time/1000)),rec.getRecordByIndex(i).value)
elif sys.argv[1] == "rebuild":
	print("Combining glucose data")
	gdr.createRecordFile("../data/glucose.gdr")
	out = gdr.RecordAccess("../data/glucose.gdr")
	out.file.seek(out.recordEntrypoint)	
	for i in os.listdir("../data/glucose/daily"):
		_in = gdr.RecordReader(os.path.abspath(f"../data/glucose/daily/{i}"))
		out.file.write(_in.getRawDataUnderHeader())