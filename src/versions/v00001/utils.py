#pylint: disable=E1101
#pylint: disable=E0611

import AppKit
import collections
import error
import Foundation
import log
import os
import sys
import objc
import process
import psutil
import Quartz
from Quartz import CG
from Quartz import CoreGraphics
import rumps
import struct
import time
import subprocess
import threading
import traceback

all_windows = None
menu_is_open = False

NO_APP = {
   "NSApplicationName": "",
   "NSApplicationBundleIdentifier": "",
   "NSApplicationProcessIdentifier": -1,
}

def set_menu_open(value):
    global menu_is_open
    menu_is_open = value

def is_menu_open():
    return menu_is_open

def get_current_app():
    return AppKit.NSWorkspace.sharedWorkspace().activeApplication() or NO_APP

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

def dark_mode():
    return os.popen("defaults read -g AppleInterfaceStyle 2>/dev/null").read()

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

def on_ethernet():
    try:
        interface = get_line(['route', '-n', 'get', 'default'], ["interface"]).split(' ')[-1]
        device = get_line(
            ['networksetup', 'listnetworkserviceorder'], ['ethernet(,|\s\d+,)','lan(,|\s\d+,)','ethernet adapter(,|\s\d+,)','ethernet slot\s\d+,'] # MacOS likes to enumerate adapters if it has seen the same model before e.g., `Ethernet` the first time `Ethernet 1` afterwards
        ).split(' ')[-1] 
        return interface in device
    except Exception as e:
        return False

def get_line(command, regexes):
    output = subprocess.check_output(command)
    lines = output.split('\n')
    return filter(lambda line: any(re.search(regex, line) for regex in regexes), lines)[0]

class OnMainThread():
    def initWithCallback_(self, callback):
        self.callback = callback
        return self

    @objc.namedselector("run_:")
    def run_(self, args=None):
        self.callback()

    def run(self):
        try:
            self.pyobjc_performSelectorOnMainThread_withObject_("run_:", None)
        except Exception as e:
            print(e)
            rumps.quit_application()


class Timer(threading.Thread):
    def __init__(self, interval, callback):
        global OnMainThread
        super(Timer, self).__init__(name="Timer for %ds for %s" % (interval, callback))
        OnMainThread = type('OnMainThread', (Foundation.NSObject,), dict(OnMainThread.__dict__))
        self.callback = OnMainThread.alloc().initWithCallback_(callback)
        self.interval = interval

    def run(self):
        while True:
            time.sleep(self.interval)
            try:
                self.callback.run()
            except psutil.NoSuchProcess:
                pass # this is normal
            except Exception as e:
                error.error("Error in Timer callback '%s': %s" % (self.callback.callback.im_func.__name__, e))

image_cache = {}
rumps_nsimage_from_file = rumps.rumps._nsimage_from_file

def _nsimage_from_file(path, dimensions=None, template=None):
    if path in image_cache:
        return image_cache[path]
    else:
        image = rumps_nsimage_from_file(path, None, None)
        image_cache[path] = image
        return image

rumps.rumps._nsimage_from_file = _nsimage_from_file