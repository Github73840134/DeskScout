class Settings:
	class Int:
		"""Settings Integer"""
		def __init__(self,value):
			self.value = value
		def __str__(self):
			return str(self.value)
	class String:
		def __init__(self,value):
			self.value = value
		def __str__(self):
			return f"'{self.value}'"
	class Bool:
		def __init__(self,value):
			self.value = value
		def __str__(self):
			return f"{'True' if self.value else 'False'}"