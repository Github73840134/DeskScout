# Glucose Data Provider SDK
# SDK Version: 1
# Author: Seth Edwards
#
__version__ = 1
class GlucoseReading:
	timestamp = None
	value = None
	trend = None
	trend_description = None
	json = None
class AuthenticationState:
	UNAUTHED = 0x00
	INVALID_CREDENTIALS = 0x01
	INVALID_TOKEN = 0x02
	AUTHED = 0x03
class State:
	SERVICE_UNREACHABLE = 0x00
	SERVICE_ONLINE = 0x01
	SERVICE_ISSUE = 0x02


class Error:
	class AuthenticationError(Exception):
		"""Invalid authentication """
		pass
	class ServiceOffline(Exception):
		"""Service is unreachable"""
		pass