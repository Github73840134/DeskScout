# Constants

SERVICE_URL = "http://127.0.0.1:49152"
class Service:
	class Url:
		settingsEndpoint = SERVICE_URL+"/settings"
		appIntent = SERVICE_URL+"/putIntent"
	class NotAvailable(Exception):
		pass
	class InvalidRequest(Exception):
		pass
	class Status:
		Success = 0
		InvalidCommand = 1
		InvalidParameter = 2
		InvalidType = 3
		InvalidValue = 4
		CommandFailed = 5
	class Settings:
		enableNotifications = "enableNotify"
		gdp = "gdp"
		gdrState = "gdrState"
		overlay = "overlay"
		useMGDL = "useMGDL"
		class Notifications:
			class UrgentLow:
				enabled = "notify/urgentLow/enabled"
				level = "notify/urgentLow/level"
				delay = "notify/urgentLow/delay"
				sound = "notify/urgentLow/sound"
				silence = "notify/urgentLow/silence"
			class UrgentLowSoon:
				enabled = "notify/urgentLowSoon/enabled"
				level = "notify/urgentLowSoon/level"
				delay = "notify/urgentLowSoon/delay"
				sound = "notify/urgentLowSoon/sound"
				silence = "notify/urgentLowSoon/silence"
			class Low:
				enabled = "notify/low/enabled"
				level = "notify/low/level"
				delay = "notify/low/delay"
				sound = "notify/low/sound"
				silence = "notify/low/silence"
			class High:
				enabled = "notify/high/enabled"
				level = "notify/high/level"
				delay = "notify/high/delay"
				sound = "notify/high/sound"
				silence = "notify/high/silence"
			class RisingFast:
				enabled = "notify/risingFast/enabled"
				level = "notify/risingFast/level"
				delay = "notify/risingFast/delay"
				sound = "notify/risingFast/sound"
				silence = "notify/risingFast/silence"
				arrow = "notify/risingFast/arrow"
			class FallingFast:
				enabled = "notify/fallingFast/enabled"
				level = "notify/fallingFast/level"
				delay = "notify/fallingFast/delay"
				sound = "notify/fallingFast/sound"
				silence = "notify/fallingFast/silence"
				arrow = "notify/fallingFast/arrow"


