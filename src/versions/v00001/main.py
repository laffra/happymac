import error
import functools
import gc
import install
import license
import log
import os
import preferences
import process
import rumps
import suspender
import sys
import time
import utils
import version_manager
import webbrowser

RESOURCE_PATH = getattr(sys, "_MEIPASS", os.path.abspath("."))
ICONS = [
    os.path.join(RESOURCE_PATH, "icons/happy-transparent.png"),
    os.path.join(RESOURCE_PATH, "icons/unhappy-transparent.png"),
    os.path.join(RESOURCE_PATH, "icons/sweating.png"),
    os.path.join(RESOURCE_PATH, "icons/burn.png"),
]
if not os.path.exists(ICONS[0]):
    ICONS[0] = os.path.join(RESOURCE_PATH, "icons/happy.png")
if not os.path.exists(ICONS[1]):
    ICONS[1] = os.path.join(RESOURCE_PATH, "icons/frown.png")
DARK_ICONS = [
    os.path.join(RESOURCE_PATH, "icons/happy-white-transparent.png"),
    os.path.join(RESOURCE_PATH, "icons/unhappy-white-transparent.png"),
    os.path.join(RESOURCE_PATH, "icons/sweating.png"),
    os.path.join(RESOURCE_PATH, "icons/burn.png"),
]
if not os.path.exists(DARK_ICONS[0]):
    print("Missing icon 0")
    DARK_ICONS[0] = os.path.join(RESOURCE_PATH, "icons/happy.png")
if not os.path.exists(DARK_ICONS[0]):
    print("Still missing icon 0")
if not os.path.exists(DARK_ICONS[1]):
    DARK_ICONS[1] = os.path.join(RESOURCE_PATH, "icons/frown.png")

TITLE_QUIT = "Quit HappyMac"
TITLE_LOADING = "HappyMac: Sampling..."
TITLE_ABOUT = "About HappyMac - %s"
TITLE_CURRENT_PROCESSES = "Current App Tasks:"
TITLE_OTHER_PROCESSES = "Background Tasks:"
TITLE_SUSPENDED_PROCESSES = "Suspended Background Tasks:"

TITLE_TERMINATE = "Terminate"
TITLE_RESUME = "Resume"
TITLE_SUSPEND_ALWAYS = "Suspend Always"
TITLE_SUSPEND_ON_BATTERY = "Suspend on Battery"
TITLE_GOOGLE = "Google this..."
TITLE_GOOGLE_SYSTEM = "Google this system process..."

LAUNCHD_PID = 1
IDLE_PROCESS_PERCENT_CPU = 3

running_local = not getattr(sys, "_MEIPASS", False)

class HappyMacStatusBarApp(rumps.App):
    def __init__(self, quit_callback=None):
        super(HappyMacStatusBarApp, self).__init__("", quit_button=None)
        self.quit_button = None
        self.quit_callback = quit_callback
        self.menu = [ ]
        self.loading()
        self.menu._menu.setDelegate_(self)
        self.start = time.time()
        self.need_menu = False
        utils.set_menu_open(False)
        utils.Timer(1.0, self.update).start()
        log.log("Started HappyMac %s" % version_manager.last_version())

    def terminate(self, menuItem, pid):
        try:
            process.terminate_pid(pid)
        except:
            error.error("Error in menu callback")
        finally:
            self.handle_action()

    def resume(self, menuItem, pid):
        try:
            suspender.resume_process(pid, manual=True)
        except:
            error.error("Error in menu callback")
        finally:
            self.handle_action()

    def suspend(self, menuItem, pid, battery=False):
        try:
            suspender.suspend_process(pid, manual=True, battery=battery)
        except:
            error.error("Error in menu callback")
        finally:
            self.handle_action()

    def google(self, menuItem, pid):
        try:
            webbrowser.open("https://google.com/search?q=Mac process '%s'" % process.get_name(pid))
        except:
            error.error("Error in menu callback")
        finally:
            self.handle_action()

    def version(self):
        return version_manager.last_version()

    def menu_item_for_process(self, p, resumable=False, suspendable=False):
        if not p:
            return None
        name = process.get_name(p.pid)
        if not name:
            return None
        cpu = process.cpu(p.pid)
        percent = max(0 if resumable else 1, int(100 * cpu))
        if p.pid != utils.get_current_app_pid() and not resumable and percent < IDLE_PROCESS_PERCENT_CPU:
            return None
        item = rumps.MenuItem("%s - %d%%" % (name, percent))
        item.icon = self.get_icon(percent)
        item.percent = percent
        item.pid = p.pid
        item.add(rumps.MenuItem(TITLE_GOOGLE, callback=functools.partial(self.google, pid=p.pid)))
        if resumable:
            item.add(rumps.MenuItem(TITLE_RESUME, callback=functools.partial(self.resume, pid=p.pid)))
        elif suspendable:
            item.add(rumps.MenuItem(TITLE_SUSPEND_ALWAYS, callback=functools.partial(self.suspend, pid=p.pid)))
            item.add(rumps.MenuItem(TITLE_SUSPEND_ON_BATTERY, callback=functools.partial(self.suspend, pid=p.pid, battery=True)))
        item.add(rumps.MenuItem(TITLE_TERMINATE, callback=functools.partial(self.terminate, pid=p.pid)))
        return item

    def create_menu(self):
        self.icon = DARK_ICONS[0] if utils.dark_mode() else ICONS[0]
        foreground_tasks = process.family(utils.get_current_app_pid())
        background_tasks = process.top(exclude=foreground_tasks)
        suspender.manage(foreground_tasks, background_tasks)
        suspended_tasks = suspender.get_suspended_tasks()
        foreground_menu_items = filter(None, map(self.menu_item_for_process, foreground_tasks))
        background_menu_items = filter(None, map(functools.partial(self.menu_item_for_process, suspendable=True), background_tasks))
        suspended_menu_items = filter(None, map(functools.partial(self.menu_item_for_process, resumable=True), suspended_tasks))
        self.clean_menu()
        self.menu = (
            [
                rumps.MenuItem(TITLE_ABOUT % self.version(), callback=self.about),
                None,
                rumps.MenuItem(TITLE_CURRENT_PROCESSES),
            ] + foreground_menu_items + [
                None,
                rumps.MenuItem(TITLE_OTHER_PROCESSES),
            ] + background_menu_items + [
                None,
                rumps.MenuItem(TITLE_SUSPENDED_PROCESSES),
            ] + suspended_menu_items + [
                None,
                rumps.MenuItem(TITLE_QUIT, callback=self.quit),
        ])
        self.need_menu = False

    def menuWillOpen_(self, menu):
        utils.set_menu_open(True)
        self.need_menu = True

    def clean_menu(self):
        for key, menu_item in self.menu.items():
            if hasattr(menu_item, "pid"):
                menu_item.clear()
        self.menu.clear()

    def loading(self):
        self.clean_menu()
        item = rumps.MenuItem(TITLE_LOADING)
        item.icon = os.path.join(RESOURCE_PATH, "icons/happymac.png")
        self.menu = [ item ]

    def menuDidClose_(self, menu):
        utils.set_menu_open(False)
        self.loading()

    def update_statusbar(self):
        self.icon = self.get_icon(process.get_cpu_percent())

    def update(self, force_update=False):
        process.clear_process_cache()
        self.update_statusbar()
        if not force_update:
            myCPU = process.cpu(process.getMyPid())
            if myCPU > 0.25:
                return
        utils.clear_windows_cache()
        if self.need_menu:
            self.create_menu()

    def menu_is_highlighted(self):
        return self.menu._menu.highlightedItem()

    def quit(self, menuItem=None):
        try:
            log.log("Quit - Ran for %d seconds" % int(time.time() - self.start))
            suspender.exit()
            if self.quit_callback:
                self.quit_callback()
        except:
            error.error("Could not quit")
        finally:
            rumps.quit_application()

    def get_icon(self, percent):
        icons = DARK_ICONS if utils.dark_mode() else ICONS
        iconIndex = 0 if not percent else max(0, min(len(icons) - 1, int(percent * len(icons) / 70.0)))
        return icons[iconIndex]

    def about(self, menuItem=None):
        webbrowser.open("http://happymac.app")

    def handle_action(self, menuItem=None):
        return
        if menuItem:
            log.log("Handled menu item %s" % menuItem)
        self.update(force_update=True)


def run(quit_callback=None):
    if license.get_license():
        rumps.notification("HappyMac", "HappyMac is now running", "See the emoji icon in the status bar", sound=False)
        HappyMacStatusBarApp(quit_callback).run()
