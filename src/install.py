import utils
import os
import preferences

APP_LOCATION = "/Applications/happymac.app"
SETUP_SCRIPT = 'tell application "System Events" to make login item at end with properties {path:"%s", hidden:false}' % APP_LOCATION
LAUNCH_AT_LOGIN_KEY = "ENABLE_LAUNCH_AT_LOGIN"

if os.path.exists(APP_LOCATION):
    if preferences.get(LAUNCH_AT_LOGIN_KEY):
        preferences.set(LAUNCH_AT_LOGIN_KEY, "true")
        utils.run_osa_script(SETUP_SCRIPT)
        print "Enable launch at login"
    else:
        print "Launch at login already enabled"

