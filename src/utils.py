import AppKit
import Quartz
from functools import wraps
import process
import time
import threading

def currentApp():
    return AppKit.NSWorkspace.sharedWorkspace().activeApplication()

def currentAppName():
    return currentApp()["NSApplicationName"]

def currentAppShortName():
    name = currentApp().get("NSApplicationBundleIdentifier", "???.%s" % currentAppName()).split(".")[-1]
    return name[0].capitalize() + name[1:]

def currentAppPid():
    return currentApp()["NSApplicationProcessIdentifier"]

def window_name(pid):
    for window in Quartz.CGWindowListCopyWindowInfo(Quartz.kCGWindowListOptionAll, Quartz.kCGNullWindowID):
        if window.get('kCGWindowOwnerPID') == pid and window.get('kCGWindowName'):
            return window.get('kCGWindowName')
    return process.name(pid)

class Timer(threading.Thread):
    def __init__(self, interval, callback):
        super(Timer, self).__init__(name="Timer for %ds for %s" % (interval, callback))
        self.callback = callback
        self.interval = interval

    def run(self):
        while True:
            time.sleep(self.interval)
            self.callback()