#pylint: disable=E1101
#pylint: disable=E0611

import AppKit
import collections
import log
import os
import process
import psutil
import Quartz
from Quartz import CG, CoreGraphics
import struct
import time
import threading
import traceback

all_windows = None

def get_current_app():
    return AppKit.NSWorkspace.sharedWorkspace().activeApplication()

def get_current_app_name():
    return get_current_app()["NSApplicationName"]

def get_current_app_short_name():
    name = get_current_app().get("NSApplicationBundleIdentifier", "???.%s" % get_current_app_name()).split(".")[-1]
    return name[0].capitalize() + name[1:]

def get_current_app_pid():
    return get_current_app()["NSApplicationProcessIdentifier"]

def get_active_chrome_tabs():
    return [window for window in get_all_windows() if is_chrome_window(window)]

def get_active_window_name():
    return get_window_name(get_current_app_pid())

def get_active_window_dimensions():
    return get_window_dimensions(get_current_app_pid())

def get_screen_pixel(x, y):
    image = CG.CGWindowListCreateImage(
        CoreGraphics.CGRectMake(x, y, 2, 2),
        CG.kCGWindowListOptionOnScreenOnly,
        CG.kCGNullWindowID,
        CG.kCGWindowImageDefault)
    bytes = CG.CGDataProviderCopyData(CG.CGImageGetDataProvider(image))
    b, g, r, a = struct.unpack_from("BBBB", bytes, offset=0)
    return (r, g, b, a)

def is_chrome_window(window):
    return is_active_window(window) and window.valueForKey_('kCGWindowOwnerName') == "Google Chrome"

def is_active_window(window, pid=None):
    if pid and window.valueForKey_('kCGWindowOwnerPID') != pid:
        return False
    return window.valueForKey_('kCGWindowIsOnscreen') and window.valueForKey_('kCGWindowName')

def get_window_name(pid):
    windows = [window for window in get_all_windows() if is_active_window(window, pid)]
    return windows and windows[0].get('kCGWindowName', '') or ''

def get_window_dimensions(pid):
    windows = [window for window in get_all_windows() if is_active_window(window, pid)]
    if windows:
        bounds = windows[0].get('kCGWindowBounds')
        return (bounds['X'], bounds['Y'], bounds['Width'], bounds['Height'])
    return (0,0,0,0)

def clear_windows_cache():
    global all_windows
    all_windows = None

def get_all_windows():
    global all_windows
    if not all_windows:
        all_windows = Quartz.CGWindowListCopyWindowInfo(Quartz.kCGWindowListExcludeDesktopElements, Quartz.kCGNullWindowID)
    for window in all_windows:
        if False and window.valueForKey_('kCGWindowIsOnscreen') :
            print window
    return all_windows

def run_osa_script(script):
    os.system("osascript -e '%s' &" % script)

def get_auto_release_pool():
    return Quartz.NSAutoreleasePool.alloc().init()

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
            except psutil.NoSuchProcess:
                pass # this is normal
            except Exception as e:
                log.log("Error in Timer callback '%s': %s" % (self.callback.im_func.__name__, e))
