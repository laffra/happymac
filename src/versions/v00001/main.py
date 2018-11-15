import activity
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
import server
import suspender
import sys
import time
import utils
import version_manager
import webbrowser

RESOURCE_PATH = getattr(sys, "_MEIPASS", os.path.abspath("."))
ICONS = [
    os.path.join(RESOURCE_PATH, "icons/happy.png"),
    os.path.join(RESOURCE_PATH, "icons/frown.png"),
    os.path.join(RESOURCE_PATH, "icons/sweating.png"),
    os.path.join(RESOURCE_PATH, "icons/burn.png"),
]

TITLE_QUIT = "Quit HappyMac"
TITLE_REPORT = "Show Activity Report..."
TITLE_ABOUT = "About HappyMac - %s"
TITLE_CURRENT_PROCESSES = "Current App Tasks"
TITLE_OTHER_PROCESSES = "Background Tasks:"
TITLE_SUSPENDED_PROCESSES = "Suspended Background Tasks:"

TITLE_TERMINATE = "Terminate"
TITLE_RESUME = "Resume"
TITLE_SUSPEND = "Suspend"
TITLE_GOOGLE = "Google this..."
TITLE_GOOGLE_SYSTEM = "Google this system process..."

TITLE_SHOW_NAME_IN_STATUSBAR = "Show name in Statusbar"
KEY_SHOW_NAME_IN_STATUSBAR = 'show_name_in_statusbar'

LAUNCHD_PID = 1
IDLE_PROCESS_PERCENT_CPU = 3

running_local = not getattr(sys, "_MEIPASS", False)

class HappyMacStatusBarApp(rumps.App):
    def __init__(self, quit_callback=None):
        super(HappyMacStatusBarApp, self).__init__("", quit_button=None)
        self.quit_button = None
        self.last_title = ""
        self.quit_callback = quit_callback
        self.menu = []
        self.create_menu()
        self.start = time.time()
        self.menu_is_open = False
        server.start_server()
        utils.Timer(0.25, self.update).start()
        self.update_skip_counter = 8
        log.log("Started HappyMac %s" % version_manager.last_version())

    def toggle_name_in_statusbar(self, menuItem=None):
        try:
            value = preferences.get(KEY_SHOW_NAME_IN_STATUSBAR, False)
            preferences.set(KEY_SHOW_NAME_IN_STATUSBAR, not value)
            self.name_in_statusbar.state = not value
            self.create_menu()
        except:
            error.error("Error in menu callback")
        finally:
            self.handle_action()

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

    def suspend(self, menuItem, pid):
        try:
            suspender.suspend_process(pid, manual=True)
        except:
            error.error("Error in menu callback")
        finally:
            self.handle_action()

    def google(self, menuItem, pid):
        try:
            webbrowser.open("https://google.com/search?q=Mac process '%s'" % process.get_name(pid))
            log.log("Google process %d (%s)" % (pid, process.get_name(pid)))
        except:
            error.error("Error in menu callback")
        finally:
            self.handle_action()

    def report(self, menuItem=None):
        try:
            activity.generate_report()
        except:
            error.error("Error in menu callback")
        finally:
            self.handle_action()

    def version(self):
        return version_manager.last_version()

    def menu_item_for_process(self, p, resumable=False, suspendable=False):
        name = process.get_name(p.pid)
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
        else:
            item.add(rumps.MenuItem(TITLE_SUSPEND, callback=functools.partial(self.suspend, pid=p.pid)))
        item.add(rumps.MenuItem(TITLE_TERMINATE, callback=functools.partial(self.terminate, pid=p.pid)))
        return item

    def create_menu(self):
        title = utils.get_current_app_short_name()
        self.icon = ICONS[0]
        show_name = preferences.get(KEY_SHOW_NAME_IN_STATUSBAR, False)
        self.title = title if show_name else ""
        self.last_title = title
        self.menu.clear()
        self.name_in_statusbar = rumps.MenuItem(TITLE_SHOW_NAME_IN_STATUSBAR, callback=self.toggle_name_in_statusbar)
        self.name_in_statusbar.state = show_name
        report = [rumps.MenuItem(TITLE_REPORT, callback=self.report), None] if running_local else []
        self.menu = [
            rumps.MenuItem(TITLE_ABOUT % self.version(), callback=self.about),
            None,
            self.name_in_statusbar,
            None,
            rumps.MenuItem(TITLE_CURRENT_PROCESSES),
            None,
            rumps.MenuItem(TITLE_OTHER_PROCESSES),
            None,
            rumps.MenuItem(TITLE_SUSPENDED_PROCESSES),
            None,
        ] + report + [
            rumps.MenuItem(TITLE_QUIT, callback=self.quit),
        ]
        self.menu._menu.setDelegate_(self)

    def menuWillOpen_(self, menu):
        self.menu_is_open = True
        self.update_skip_counter = 0

    def menuDidClose_(self, menu):
        self.menu_is_open = False

    def update_statusbar(self):
        title = utils.get_current_app_short_name()
        percent = process.get_cpu_percent()
        self.icon = self.get_icon(percent) if title == self.last_title else ICONS[0]
        self.title = title if preferences.get(KEY_SHOW_NAME_IN_STATUSBAR, False) else ""
        self.last_title = title

    def update_menu(self, foreground_tasks, background_tasks, suspended_tasks, force_update=False):
        foreground_menu_items = filter(None, map(self.menu_item_for_process, foreground_tasks))
        background_menu_items = filter(None, map(functools.partial(self.menu_item_for_process, suspendable=True), background_tasks))
        suspended_menu_items = filter(None, map(functools.partial(self.menu_item_for_process, resumable=True), suspended_tasks))
        for key, menu_item in self.menu.items():
            if hasattr(menu_item, "pid"):
                del self.menu[key]
        for item in foreground_menu_items:
            self.menu.insert_after(TITLE_CURRENT_PROCESSES, item)
        for item in background_menu_items:
            self.menu.insert_after(TITLE_OTHER_PROCESSES, item)
        for item in suspended_menu_items:
            self.menu.insert_after(TITLE_SUSPENDED_PROCESSES, item)

    def update(self, force_update=False):
        if not force_update and self.update_skip_counter > 0:
            self.update_skip_counter -= 1
            return
        self.update_skip_counter = 8
        process.clear_process_cache()
        utils.clear_windows_cache()
        activity.update_activities()
        self.update_statusbar()
        percent = process.get_cpu_percent()
        if force_update or percent > 25 or self.menu_is_open:
            foreground_tasks = process.family(utils.get_current_app_pid())
            background_tasks = process.top(exclude=foreground_tasks)
            suspender.manage(foreground_tasks, background_tasks)
            suspended_tasks = suspender.get_suspended_tasks()
            if force_update or not self.menu_is_highlighted():
                self.update_menu(foreground_tasks, background_tasks, suspended_tasks, force_update)

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
        iconIndex = 0 if not percent else max(0, min(len(ICONS) - 1, int(percent * len(ICONS) / 70.0)))
        return ICONS[iconIndex]

    def about(self, menuItem=None):
        webbrowser.open("http://happymac.app")

    def handle_action(self, menuItem=None):
        if menuItem:
            log.log("Handled menu item %s" % menuItem)
        self.update(force_update=True)


def run(quit_callback=None):
    if license.get_license():
        rumps.notification("HappyMac", "HappyMac is now running", "See the emoji icon in the status bar", sound=False)
        HappyMacStatusBarApp(quit_callback).run()
