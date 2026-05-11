api = DeskScoutAPIRequire("sdk.api.v1")
print(api.Service.changeSetting(api.const.Service.Settings.enableNotifications,api.types.Settings.Bool(False)))
api.App.putIntent("Settings")
import time
time.sleep(5)
print(api.Service.changeSetting(api.const.Service.Settings.enableNotifications,api.types.Settings.Bool(True)))
api.App.putIntent("Settings")