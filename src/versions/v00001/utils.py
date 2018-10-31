import AppKit
import Quartz
from functools import wraps
import os
import process
import time
import threading

def currentApp():
    #pylint: disable=E1101
    return AppKit.NSWorkspace.sharedWorkspace().activeApplication()

def currentAppName():
    return currentApp()["NSApplicationName"]

def currentAppShortName():
    name = currentApp().get("NSApplicationBundleIdentifier", "???.%s" % currentAppName()).split(".")[-1]
    return name[0].capitalize() + name[1:]

def currentAppPid():
    return currentApp()["NSApplicationProcessIdentifier"]

def window_name(pid):
    #pylint: disable=E1101
    for window in Quartz.CGWindowListCopyWindowInfo(Quartz.kCGWindowListOptionAll, Quartz.kCGNullWindowID):
        if window.get('kCGWindowOwnerPID') == pid and window.get('kCGWindowName'):
            return window.get('kCGWindowName')
    return process.name(pid)

def run_osa_script(script):
    os.system("osascript -e '%s' &" % script)

class Timer(threading.Thread):
    def __init__(self, interval, callback):
        super(Timer, self).__init__(name="Timer for %ds for %s" % (interval, callback))
        self.callback = callback
        self.interval = interval

    def run(self):
        while True:
            time.sleep(self.interval)
            try:
                self.callback()
            except Exception as e:
                print "Error in %s: %s" % (self, e)
