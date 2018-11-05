import functools
import install
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

ICONS = [ "icons/happy.png", "icons/frown.png", "icons/sweating.png", "icons/burn.png" ]

TITLE_QUIT = "Quit HappyMac"
TITLE_ACTIVITY_MONITOR = "Open Activity Monitor"
TITLE_ABOUT = "About HappyMac - %s"
TITLE_CURRENT_PROCESSES = "Current App Tasks"
TITLE_OTHER_PROCESSES = "Background Tasks:"
TITLE_SUSPENDED_PROCESSES = "Suspended Background Tasks:"

TITLE_TERMINATE = "Terminate"
TITLE_RESUME = "Resume Now"
TITLE_RESUME_AND_NEVER_SUSPEND = "Never Suspend"
TITLE_SUSPEND = "Suspend Now"
TITLE_AUTO_SUSPEND = "Auto Suspend"
TITLE_GOOGLE = "Google this..."
TITLE_RESTART = "Restart"
TITLE_VERSIONS = "Versions"

TITLE_PREFERENCES = "Preferences"
TITLE_STATUS_BAR = "Status Bar"
TITLE_JUST_EMOJI = "Show just an emoji"
TITLE_EMOJI_AND_NAME = "Show emoji and name"

KEY_ICON_DETAILS = 'icon_details'

LAUNCHD_PID = 1
IDLE_PROCESS_PERCENT_CPU = 3

class HappyMacStatusBarApp(rumps.App):
    def __init__(self, quit_callback=None):
        super(HappyMacStatusBarApp, self).__init__("")
        self.quit_button = None
        self.last_title = ""
        self.quit_callback = quit_callback
        self.menu = []
        self.create_menu()
        self.start = time.time()
        utils.Timer(2, self.update).start()
        log.log("Started HappyMac")

    def show_emoji(self, menuItem=None):
        preferences.set(KEY_ICON_DETAILS, TITLE_JUST_EMOJI)
        self.handle_action()

    def show_emoji_and_name(self, menuItem=None):
        preferences.set(KEY_ICON_DETAILS, TITLE_EMOJI_AND_NAME)
        self.handle_action()

    def terminate(self, menuItem, pid):
        process.terminate(pid)
        self.handle_action()

    def resume(self, menuItem, pid, auto=False):
        suspender.resume(pid, manual=True, auto=auto)
        self.handle_action()

    def suspend(self, menuItem, pid, auto=False):
        suspender.suspend(pid, manual=True, auto=auto)
        self.handle_action()

    def google(self, menuItem, pid):
        webbrowser.open("https://google.com/search?q=Mac process '%s'" % process.name(pid))
        log.log("Google %s" % process.name(pid))
        self.handle_action()

    def activity_monitor(self, menuItem=None):
        utils.run_osa_script('tell application "Activity Monitor" to activate')
        log.log("Launch Activity Monitor")
        self.handle_action()

    def version(self):
        return os.path.basename(os.path.dirname(__file__))

    def menu_item_for_process(self, p, resumable=False, suspendable=False):
        name = p.name()
        cpu = process.cpu(p.pid)
        percent = max(0 if resumable else 1, int(100 * cpu))
        if p.pid != utils.currentAppPid() and not resumable and percent < IDLE_PROCESS_PERCENT_CPU:
            return None
        item = rumps.MenuItem("%s - %d%%" % (name, percent))
        item.icon = self.getIcon(percent)
        item.percent = percent
        item.pid = p.pid
        item.add(rumps.MenuItem(TITLE_GOOGLE, callback=functools.partial(self.google, pid=p.pid)))
        if suspendable:
            item.add(rumps.MenuItem(TITLE_AUTO_SUSPEND, callback=functools.partial(self.suspend, auto=True, pid=p.pid)))
        if resumable:
            item.add(rumps.MenuItem(TITLE_RESUME, callback=functools.partial(self.resume, pid=p.pid)))
            item.add(rumps.MenuItem(TITLE_RESUME_AND_NEVER_SUSPEND, callback=functools.partial(self.resume, auto=True, pid=p.pid)))
        else:
            item.add(rumps.MenuItem(TITLE_SUSPEND, callback=functools.partial(self.suspend, pid=p.pid)))
        item.add(rumps.MenuItem(TITLE_TERMINATE, callback=functools.partial(self.terminate, pid=p.pid)))
        return item

    def create_menu(self):
        title = utils.currentAppShortName()
        self.icon = ICONS[0]
        self.title = title if preferences.get('icon_details') == TITLE_EMOJI_AND_NAME else ""
        self.last_title = title
        self.menu = [
            rumps.MenuItem(TITLE_ABOUT % self.version(), callback=self.about),
            None,
            {TITLE_PREFERENCES:
                {
                    TITLE_STATUS_BAR: [
                        rumps.MenuItem(TITLE_JUST_EMOJI, callback=self.show_emoji),
                        rumps.MenuItem(TITLE_EMOJI_AND_NAME, callback=self.show_emoji_and_name),
                    ],
                    TITLE_VERSIONS: self.versions()
                }
            },
            None,
            rumps.MenuItem(TITLE_CURRENT_PROCESSES),
            None,
            rumps.MenuItem(TITLE_OTHER_PROCESSES),
            None,
            rumps.MenuItem(TITLE_SUSPENDED_PROCESSES),
            None,
            rumps.MenuItem(TITLE_ACTIVITY_MONITOR, callback=self.activity_monitor),
            rumps.MenuItem(TITLE_RESTART, callback=self.restart),
            None,
            rumps.MenuItem(TITLE_QUIT, callback=self.quit),
        ]

    def update_menu(self, foreground_tasks, background_tasks, suspended_tasks, force_update=False):
        if self.menu_is_highlighted() and not force_update:
            return
        title = utils.currentAppShortName()
        foreground_menu_items = filter(None, map(self.menu_item_for_process, foreground_tasks))
        background_menu_items = filter(None, map(functools.partial(self.menu_item_for_process, suspendable=True), background_tasks))
        suspended_menu_items = filter(None, map(functools.partial(self.menu_item_for_process, resumable=True), suspended_tasks))
        percent = sum(task.percent for task in foreground_menu_items) + int(process.cpu(-1) * 25)
        self.icon = self.getIcon(percent) if title == self.last_title else ICONS[0]
        self.title = title if preferences.get('icon_details') == TITLE_EMOJI_AND_NAME else ""
        self.last_title = title
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
        process.clear_cpu_cache()
        foreground_tasks = process.family(utils.currentAppPid())
        background_tasks = process.top(exclude=foreground_tasks)
        self.update_menu(foreground_tasks, background_tasks, suspender.get_suspended_tasks(), force_update)
        suspender.manage(foreground_tasks, background_tasks)

    def menu_is_highlighted(self):
        return self.menu._menu.highlightedItem() != None

    def quit(self, menuItem=None):
        try:
            log.log("Quit - Ran for %d seconds" % int(time.time() - self.start))
            suspender.exit()
            self.quit_callback()
        finally:
            rumps.quit_application()

    def versions(self):
        return [
            rumps.MenuItem(version, callback=functools.partial(self.switch_version, version=version))
            for version in version_manager.get_versions()
        ]

    def switch_version(self, menuItem, version):
        try:
            log.log("Switch to version %s" % version)
            version_manager.set_version(version)
            self.restart()
        except Exception as e:
            log.log("Cannot switch to version %s" % version, e)

    def restart(self, menuItem=None):
        log.log("Restart");
        utils.run_osa_script("""
            delay 5
            tell application "happymac" to activate
        """)
        self.quit()

    def getIcon(self, percent):
        iconIndex = 0 if not percent else max(0, min(len(ICONS) - 1, int(percent * len(ICONS) / 100.0)))
        return ICONS[iconIndex]

    def about(self, menuItem=None):
        webbrowser.open("http://happymac.app")

    def handle_action(self, menuItem=None):
        if menuItem:
            log.log("Handled menu item %s" % menuItem)
        self.update(True)


def main(quit_callback=None):
    HappyMacStatusBarApp(quit_callback).run()