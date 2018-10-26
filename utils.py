import AppKit
import Quartz
import process

def currentApp():
  return AppKit.NSWorkspace.sharedWorkspace().activeApplication()

def currentAppName():
  return currentApp()["NSApplicationName"]

def currentAppShortName():
  name = currentApp()["NSApplicationBundleIdentifier"].split(".")[-1]
  return name[0].capitalize() + name[1:]

def currentAppPid():
  return currentApp()["NSApplicationProcessIdentifier"]

def window_name(pid):
  for window in Quartz.CGWindowListCopyWindowInfo(Quartz.kCGWindowListOptionAll, Quartz.kCGNullWindowID):
    if window.get('kCGWindowOwnerPID') == pid and window.get('kCGWindowName'):
      return window.get('kCGWindowName')
  return process.name(pid)
