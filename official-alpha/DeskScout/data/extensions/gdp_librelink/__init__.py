from mods.sdk.gdp import v1 as sdk
class GlucoseDataProvider():
	def __init__(self):
		import tkinter.messagebox
		tkinter.messagebox.showinfo("LibreLink Extension","The extension does not work yet")
	
	def setup(self):
		import tkinter.messagebox
		tkinter.messagebox.showinfo("LibreLink Extension","The extension does not work yet")
	def login(self,username,password):
		# Username and password both need to be a string
		pass
	def getAuthStatus(self):
		# Must return one of the states described in the AuthenticationState Class
		return sdk.AuthenticationState.UNAUTHED
	def getLatestGlucoseReading(self):
		# Return a GlucoseReading object
		return GlucoseReading()
	def getState(self):
		pass
	def getAllReadings(self):
		# Return multiple GlucoseReading objects
		return [GlucoseReading(),GlucoseReading(),GlucoseReading()]
__gdp__ = GlucoseDataProvider