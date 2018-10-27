import functools
import os
import preferences
import process
import rumps
import time
import utils
import webbrowser

ICONS = [ "icons/happy.png", "icons/frown.png", "icons/sweating.png", "icons/burn.png" ]

TITLE_QUIT = "Quit HappyMac"
TITLE_ACTIVITY_MONITOR = "Open Activity Monitor"
TITLE_ABOUT = "About HappyMac"
TITLE_CURRENT_PROCESSES = "Current App \"%s\""
TITLE_OTHER_PROCESSES = "Other Apps and Tasks:"

TITLE_TERMINATE = "Terminate"
TITLE_SUSPEND = "Suspend When In Background"
TITLE_GOOGLE = "Google this..."

TITLE_PREFERENCES = "Preferences"
TITLE_STATUS_BAR = "Status Bar"
TITLE_JUST_EMOJI = "Show just an emoji"
TITLE_EMOJI_AND_NAME = "Show emoji and name"

KEY_ICON_DETAILS = 'icon_details'
KEY_PROCESS_POLICY = 'process_prolicy'

POLICY_SUSPEND = 'suspend'
POLICY_RESUME = 'resume'

class HappyMacStatusBarApp(rumps.App):
    def __init__(self):
        super(HappyMacStatusBarApp, self).__init__("")
        self.quit_button = TITLE_QUIT
        self.last_title = ""
        self.menu = []
        self.update(None)

    def show_emoji(self, menuItem):
        preferences.set(KEY_ICON_DETAILS, TITLE_JUST_EMOJI)

    def show_emoji_and_name(self, menuItem):
        preferences.set(KEY_ICON_DETAILS, TITLE_EMOJI_AND_NAME)

    def addTasks(self):
        menu_items = filter(None, map(
            self.task_item,
            process.children(utils.currentAppPid(), includeParent=True)
        ))
        return sorted(menu_items, key=lambda p: -process.cpu(p.pid))

    def terminate(self, menuItem, pid):
        process.terminate(pid)

    def suspend(self, menuItem, pid):
        try:
            preferences.set(process.name(pid), POLICY_SUSPEND)
            process.suspend(pid)
        except Exception as e:
            print e

    def resume(self, menuItem, pid):
        preferences.set(process.name(pid), POLICY_RESUME)
        process.resume(pid)

    def google(self, menuItem, pid):
        webbrowser.open("https://google.com/?q=Mac process '%s'" % process.name(pid))

    def activity_monitor(self, menuItem):
        self.apple_script('''tell application "Activity Monitor" to activate''')

    def apple_script(self, script):
        os.system("osascript -e '%s'" % script)

    def task_item(self, p):
        name = p.name()
        cpu = process.cpu(p.pid)
        percent = int(100 * cpu)
        if percent == 0:
            return None
        item = rumps.MenuItem("%s - %d%%" % (name, percent))
        item.icon = self.getIcon(percent)
        item.percent = percent
        item.pid = p.pid
        item.add(rumps.MenuItem(TITLE_GOOGLE, callback=functools.partial(self.google, pid=p.pid)))
        # item.add(rumps.MenuItem(TITLE_SUSPEND, callback=functools.partial(self.suspend, pid=p.pid)))
        item.add(rumps.MenuItem(TITLE_TERMINATE, callback=functools.partial(self.terminate, pid=p.pid)))
        return item

    @rumps.timer(1)
    def update(self, _):
        try:
            process.clear_cache()
            title = utils.currentAppShortName()
            tasks = self.addTasks()
            top = filter(None, map(self.task_item, process.top(excludeParentPid=utils.currentAppPid())))
            percent = sum(task.percent for task in tasks) + int(process.cpu(-1) * 25)
            self.icon = self.getIcon(percent) if title == self.last_title else ICONS[0]
            self.title = title if preferences.get('icon_details') == TITLE_EMOJI_AND_NAME else ""
            self.menu.clear()
            taskHeader = [
                rumps.MenuItem(TITLE_ABOUT, callback=self.about),
                None,
                TITLE_CURRENT_PROCESSES % utils.currentAppName(),
            ]
            topHeader = [
                None,
                TITLE_OTHER_PROCESSES,
            ]
            footer = [
                None,
                rumps.MenuItem(TITLE_ACTIVITY_MONITOR, callback=self.activity_monitor),
                {TITLE_PREFERENCES:
                    {TITLE_STATUS_BAR: [
                        rumps.MenuItem(TITLE_JUST_EMOJI, callback=self.show_emoji),
                        rumps.MenuItem(TITLE_EMOJI_AND_NAME, callback=self.show_emoji_and_name),
                    ]},
                },
                None,
                rumps.MenuItem(TITLE_QUIT, callback=self.quit),
            ]
            self.menu = taskHeader + tasks + topHeader + top + footer
            self.last_title = title
        except Exception as e:
            print e

    def quit(self, menuItem):
        rumps.quit_application()

    def getIcon(self, percent):
        iconIndex = 0 if not percent else max(0, min(len(ICONS) - 1, int(percent * len(ICONS) / 100.0)))
        return ICONS[iconIndex]

    def about(self, menuItem):
        webbrowser.open("http://chrislaffra.com/happymac")


def main():
    HappyMacStatusBarApp().run()