from mods.sdk.gdp import v1 as sdk
from . import PySimpleGUI as sg
class GlucoseDataProvider():
	def __init__(self):
		pass
	def setup(self):
		sg.Popup("B","C")
	def login(self,username,password):
		# Username and password both need to be a string
		pass
	def getAuthStatus(self):
		# Must return one of the states described in the AuthenticationState Class
		return sdk.AuthenticationState.UNAUTHED
	def getLatestGlucoseReading(self):
		# Return a GlucoseReading object
		return sdk.GlucoseReading()
	def getState(self):
		pass
	def getAllReadings(self):
		# Return multiple GlucoseReading objects
		return [sdk.GlucoseReading(),sdk.GlucoseReading(),sdk.GlucoseReading()]
__gdp__ = GlucoseDataProvider