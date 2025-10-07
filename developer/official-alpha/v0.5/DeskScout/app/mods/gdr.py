# Glucose Data Records (GDR)
import os
import io
class GDRVersionIncompatible(Exception):
	pass
def createRecordFile(path):
	file = open(path,'wb+')
	file.write(b"gdr_v1.0\n")
gdr_versions = [b'gdr_v1.0']
class Record:
	time = None
	value = None
	trendArrow = None
class RecordAccess:
	def __init__(self,path):
		self.file = open(path,'rb+')
		version = b""
		while True:
			x = self.file.read(1)
			if x != b"\n":
				version += x
			else:
				break
		self.recordEntrypoint = self.file.tell()
		if (version in gdr_versions) == False:
			print(version,gdr_versions,(version in gdr_versions))
			raise GDRVersionIncompatible(str(version))
		self.version = version
		self.cache = {}
	def writeRecord(self,entryTime,value,trendArrow):
		self.file.read()
		entry = b""
		entry += int.to_bytes(int(entryTime),8)
		entry += int.to_bytes(value,2)
		entry += int.to_bytes(trendArrow)
		self.file.write(entry)
		self.file.flush()
	def getRecords(self,startTime,endTime):
		results = []
		self.file.seek(self.recordEntrypoint)
		while True:
			x = self.file.read(11)
			if len(x) < 11:
				return results
			x = io.BytesIO(x)
			time = int.from_bytes(x.read(8))
			value = int.from_bytes(x.read(2))
			trend = int.from_bytes(x.read(1))
			if time in range(startTime,endTime+1):
				rec = Record()
				rec.time = time
				rec.value = value
				rec.trendArrow = trend
				results.append(rec)
	def getRecord(self,time):
		self.file.seek(self.recordEntrypoint)
		while True:
			x = self.file.read(11)
			if len(x) < 11:
				return None
			x = io.BytesIO(x)
			_time = int.from_bytes(x.read(8))
			value = int.from_bytes(x.read(2))
			trend = int.from_bytes(x.read(1))
			if _time == time:
				rec = Record()
				rec.time = _time
				rec.value = value
				rec.trendArrow = trend
				return rec
	def getRecordByIndex(self,index):
		self.file.seek(self.recordEntrypoint)
		i = 0
		while True:
			x = self.file.read(11)
			if len(x) < 11:
				return None
			if i == index:
				x = io.BytesIO(x)
				time = int.from_bytes(x.read(8))
				value = int.from_bytes(x.read(2))
				trend = int.from_bytes(x.read(1))
				rec = Record()
				rec.time = time
				rec.value = value
				rec.trendArrow = trend
				return rec
			else:
				i += 1
	def getRecordsByIndex(self,startIndex,endIndex):
		results = []
		i = 0
		self.file.seek(self.recordEntrypoint)
		while True:
			x = self.file.read(11)
			if len(x) < 11:
				return results
			x = io.BytesIO(x)
			time = int.from_bytes(x.read(8))
			value = int.from_bytes(x.read(2))
			trend = int.from_bytes(x.read(1))
			if i in range(startIndex,endIndex):
				rec = Record()
				rec.time = time
				rec.value = value
				rec.trendArrow = trend
				results.append(rec)
			elif i > endIndex:
				return results
			else:
				i += 1
	def deleteRecordByTime(self,time):
		self.file.seek(self.recordEntrypoint)
		while True:
			x = self.file.read(11)
			if len(x) < 11:
				return False
			x = io.BytesIO(x)
			_time = int.from_bytes(x.read(8))
			value = int.from_bytes(x.read(2))
			trend = int.from_bytes(x.read(1))
			if _time == time:
				rp = self.file.tell()-11
				self.file.seek(rp)
				self.file.write(b'\x00'*11)
				
				recs = self.file.read()
				self.file.seek(0)
				prev = self.file.read(rp)
				self.file.truncate(0)
				self.file.write(prev+recs)
				self.file.flush()
				return True
	def getLastRecord(self):
		self.file.seek(self.recordEntrypoint)

		i = 0
		while True:
			x = self.file.read(11)
			if len(x) < 11:
				return None
			x = io.BytesIO(x)
			time = int.from_bytes(x.read(8))
			value = int.from_bytes(x.read(2))
			trend = int.from_bytes(x.read(1))
			if time > i:
				i = time
			else:
				rec = Record()
				rec.time = time
				rec.value = value
				rec.trendArrow = trend
				return rec
	def getLastRecordTime(self):
		self.file.seek(self.recordEntrypoint)
		i = 0
		while True:
			x = self.file.read(11)
			if len(x) < 11:
				return i
			x = io.BytesIO(x)
			time = int.from_bytes(x.read(8))
			value = int.from_bytes(x.read(2))
			trend = int.from_bytes(x.read(1))
			if time > i:
				i = time
			else:
				return time
	def getRecordCount(self):
		self.file.seek(self.recordEntrypoint)
		i = 0
		while True:
			x = self.file.read(11)
			if len(x) < 11:
				return i
			else:
				i += 1
class RecordReader:
	def __init__(self,path):
		self.file = open(path,'rb')
		version = b""
		while True:
			x = self.file.read(1)
			if x != b"\n":
				version += x
			else:
				break
		self.recordEntrypoint = self.file.tell()
		if (version in gdr_versions) == False:
			print(version,gdr_versions,(version in gdr_versions))
			raise GDRVersionIncompatible(str(version))
		self.version = version
	def getRecords(self,startTime,endTime):
		results = []
		self.file.seek(self.recordEntrypoint)
		while True:
			x = self.file.read(11)
			if len(x) < 11:
				return results
			x = io.BytesIO(x)
			time = int.from_bytes(x.read(8))
			value = int.from_bytes(x.read(2))
			trend = int.from_bytes(x.read(1))
			if time in range(startTime,endTime+1):
				rec = Record()
				rec.time = time
				rec.value = value
				rec.trendArrow = trend
				results.append(rec)
	def getRecord(self,time):
		self.file.seek(self.recordEntrypoint)
		while True:
			x = self.file.read(11)
			if len(x) < 11:
				return None
			x = io.BytesIO(x)
			_time = int.from_bytes(x.read(8))
			value = int.from_bytes(x.read(2))
			trend = int.from_bytes(x.read(1))
			if _time == time:
				rec = Record()
				rec.time = _time
				rec.value = value
				rec.trendArrow = trend
				return rec
	def getRecordByIndex(self,index):
		self.file.seek(self.recordEntrypoint)
		i = 0
		while True:
			x = self.file.read(11)
			if len(x) < 11:
				return None

			if i == index:

				x = io.BytesIO(x)
				time = int.from_bytes(x.read(8))
				value = int.from_bytes(x.read(2))
				trend = int.from_bytes(x.read(1))
				rec = Record()
				rec.time = time
				rec.value = value
				rec.trendArrow = trend
				return rec
			else:
				i += 1
	def getRecordsByIndex(self,startIndex,endIndex):
		results = []
		i = 0
		self.file.seek(self.recordEntrypoint)
		while True:
			x = self.file.read(11)
			if len(x) < 11:
				return results
			x = io.BytesIO(x)
			time = int.from_bytes(x.read(8))
			value = int.from_bytes(x.read(2))
			trend = int.from_bytes(x.read(1))
			if i in range(startIndex,endIndex):
				rec = Record()
				rec.time = time
				rec.value = value
				rec.trendArrow = trend
				results.append(rec)
			elif i > endIndex:
				return results
			else:
				i += 1
	def getLastRecord(self):
		self.file.seek(self.recordEntrypoint)

		i = 0
		while True:
			x = self.file.read(11)
			if len(x) < 11:
				return None
			x = io.BytesIO(x)
			time = int.from_bytes(x.read(8))
			value = int.from_bytes(x.read(2))
			trend = int.from_bytes(x.read(1))
			if time > i:
				i = time
			else:
				rec = Record()
				rec.time = time
				rec.value = value
				rec.trendArrow = trend
				return rec
	def getLastRecordTime(self):
		self.file.seek(self.recordEntrypoint)
		i = 0
		while True:
			x = self.file.read(11)
			if len(x) < 11:
				return None
			x = io.BytesIO(x)
			time = int.from_bytes(x.read(8))
			value = int.from_bytes(x.read(2))
			trend = int.from_bytes(x.read(1))
			if time > i:
				i = time
			else:
				return i
	def getRecordCount(self):
		self.file.seek(self.recordEntrypoint)
		i = 0
		while True:
			x = self.file.read(11)
			if len(x) < 11:
				return i
			else:
				i += 1
	def getRawDataUnderHeader(self):
		self.file.seek(self.recordEntrypoint)
		return self.file.read()