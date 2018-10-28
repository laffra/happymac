import functools
import os
import preferences
import process
import rumps
import suspender
import time
import utils
import webbrowser

ICONS = [ "icons/happy.png", "icons/frown.png", "icons/sweating.png", "icons/burn.png" ]

TITLE_QUIT = "Quit HappyMac"
TITLE_ACTIVITY_MONITOR = "Open Activity Monitor"
TITLE_ABOUT = "About HappyMac"
TITLE_CURRENT_PROCESSES = "Current App Tasks"
TITLE_OTHER_PROCESSES = "Other Apps and Tasks:"
TITLE_SUSPENDED_PROCESSES = "Suspended Resource Hogs:"

TITLE_TERMINATE = "Terminate"
TITLE_RESUME = "Resume"
TITLE_SUSPEND = "Suspend"
TITLE_GOOGLE = "Google this..."

TITLE_PREFERENCES = "Preferences"
TITLE_STATUS_BAR = "Status Bar"
TITLE_JUST_EMOJI = "Show just an emoji"
TITLE_EMOJI_AND_NAME = "Show emoji and name"

KEY_ICON_DETAILS = 'icon_details'

LAUNCHD_PID = 1
IDLE_PROCESS_PERCENT_CPU = 3

class HappyMacStatusBarApp(rumps.App):
    def __init__(self):
        super(HappyMacStatusBarApp, self).__init__("")
        self.quit_button = None
        self.last_title = ""
        self.menu = []
        self.create_menu()
        utils.Timer(2, self.update).start()

    def show_emoji(self, menuItem):
        preferences.set(KEY_ICON_DETAILS, TITLE_JUST_EMOJI)

    def show_emoji_and_name(self, menuItem):
        preferences.set(KEY_ICON_DETAILS, TITLE_EMOJI_AND_NAME)

    def terminate(self, menuItem, pid):
        process.terminate(pid)

    def resume(self, menuItem, pid):
        suspender.resume(pid)

    def suspend(self, menuItem, pid):
        suspender.suspend(pid)

    def google(self, menuItem, pid):
        webbrowser.open("https://google.com/?q=Mac process '%s'" % process.name(pid))

    def activity_monitor(self, menuItem):
        self.apple_script('''tell application "Activity Monitor" to activate''')

    def apple_script(self, script):
        os.system("osascript -e '%s'" % script)

    def menu_item_for_process(self, p, resumable=False, suspendable=False):
        name = p.name()
        cpu = process.cpu(p.pid)
        percent = max(1, int(100 * cpu))
        if p.pid != utils.currentAppPid() and not resumable and percent < IDLE_PROCESS_PERCENT_CPU:
            return None
        item = rumps.MenuItem("%s - %d%%" % (name, percent))
        item.icon = self.getIcon(percent)
        item.percent = percent
        item.pid = p.pid
        item.add(rumps.MenuItem(TITLE_GOOGLE, callback=functools.partial(self.google, pid=p.pid)))
        if suspendable:
            item.add(rumps.MenuItem(TITLE_SUSPEND, callback=functools.partial(self.suspend, pid=p.pid)))
        if resumable:
            item.add(rumps.MenuItem(TITLE_RESUME, callback=functools.partial(self.resume, pid=p.pid)))
        item.add(rumps.MenuItem(TITLE_TERMINATE, callback=functools.partial(self.terminate, pid=p.pid)))
        return item

    def create_menu(self):
        title = utils.currentAppShortName()
        self.icon = ICONS[0]
        self.title = title if preferences.get('icon_details') == TITLE_EMOJI_AND_NAME else ""
        self.last_title = title
        self.menu = [
            rumps.MenuItem(TITLE_ABOUT, callback=self.about),
            None,
            {TITLE_PREFERENCES:
                {TITLE_STATUS_BAR: [
                    rumps.MenuItem(TITLE_JUST_EMOJI, callback=self.show_emoji),
                    rumps.MenuItem(TITLE_EMOJI_AND_NAME, callback=self.show_emoji_and_name),
                ]},
            },
            None,
            rumps.MenuItem(TITLE_CURRENT_PROCESSES),
            None,
            rumps.MenuItem(TITLE_OTHER_PROCESSES),
            None,
            rumps.MenuItem(TITLE_SUSPENDED_PROCESSES),
            None,
            rumps.MenuItem(TITLE_ACTIVITY_MONITOR, callback=self.activity_monitor),
            None,
            rumps.MenuItem(TITLE_QUIT, callback=self.quit),
        ]

    def update_menu(self, foreground_tasks, background_tasks, suspended_tasks):
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

    def update(self):
        try:
            process.clear_cpu_cache()
            foreground_tasks = process.family(utils.currentAppPid())
            background_tasks = process.top(exclude=foreground_tasks)
            self.update_menu(foreground_tasks, background_tasks, suspender.get_suspended_tasks())
            suspender.manage(foreground_tasks, background_tasks)
        except Exception as e:
            print "update: %s" % e

    def quit(self, menuItem):
        rumps.quit_application()

    def getIcon(self, percent):
        iconIndex = 0 if not percent else max(0, min(len(ICONS) - 1, int(percent * len(ICONS) / 100.0)))
        return ICONS[iconIndex]

    def about(self, menuItem):
        webbrowser.open("http://chrislaffra.com/happymac")


def main():
    HappyMacStatusBarApp().run()