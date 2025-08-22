import sys
import os
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
	for i in range(rlen):
		recs.append(records.getRecordByIndex(i))
	recs = remove_duplicates(recs)
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
	for i in range(rlen):
		recs.append(records.getRecordByIndex(i).time)
	for i in recs:
		print(i)
		dups += recs.count(i)-1
	print("Duplicates found:",dups)


	