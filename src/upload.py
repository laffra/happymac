import glob
import re
import os

NO_OBFUSCATION = True

output_path = "/tmp/last.py"
files = [
    "src/versions/v00001/activity.py",
    "src/versions/v00001/install.py",
    "src/versions/v00001/main.py",
    "src/versions/v00001/process.py",
    "src/versions/v00001/server.py",
    "src/versions/v00001/suspender.py",
    "src/versions/v00001/utils.py",
]
names = {}

def short_name(name):
    if NO_OBFUSCATION:
        return "_%s_" % name
    if name in names:
        return names[name]
    names[name] = '_%s' % len(names)
    return names[name]

currentid = 0

def nextid(name):
    if NO_OBFUSCATION:
        return name
    global currentid
    currentid += 1
    return '_t%d_' % currentid

contents = ("\n".join([open(file).read() for file in files])
    .replace("import activity", "")
    .replace("import process", "")
    .replace("import suspender", "")
    .replace("import utils", "")
    .replace("import server", "")
    .replace("import install", "")
    .replace("#pylint: disable=E1101", "")

    # main definitions
    .replace('    def show_emoji_and_name(', '    def %s(' % short_name('show_emoji_and_name'))
    .replace('    def show_emoji(', '    def %s(' % short_name('show_emoji'))
    .replace('    def terminate(', '    def %s(' % short_name('terminate'))
    .replace('    def resume(', '    def %s(' % short_name('resume'))
    .replace('    def suspend(', '    def %s(' % short_name('suspend'))
    .replace('    def google(', '    def %s(' % short_name('goold'))
    .replace('    def report(', '    def %s(' % short_name('report'))
    .replace('    def activity_monitor(', '    def %s(' % short_name('activity_monitor'))
    .replace('    def version(', '    def %s(' % short_name('version'))
    .replace('    def menu_item_for_process(', '    def %s(' % short_name('menu_item_for_process'))
    .replace('    def create_menu(', '    def %s(' % short_name('create_menu'))
    .replace('    def update_menu(', '    def %s(' % short_name('update_menu'))
    .replace('    def update(', '    def %s(' % short_name('update'))
    .replace('    def menu_is_highlighted(', '    def %s(' % short_name('menu_is_highlighted'))
    .replace('    def quit(', '    def %s(' % short_name('quit'))
    .replace('    def versions(', '    def %s(' % short_name('versions'))
    .replace('    def load_version(', '    def %s(' % short_name('load_version'))
    .replace('    def restart(', '    def %s(' % short_name('restarts'))
    .replace('    def getIcon(', '    def %s(' % short_name('get_icon'))
    .replace('    def about(', '    def %s(' % short_name('about'))
    .replace('    def handle_action(', '    def %s(' % short_name('hand_action'))

    # main calls
    .replace('self.menu_item_for_process(', 'self.%s(' % short_name('menu_item_for_process'))
    .replace('self.create_menu(', 'self.%s(' % short_name('create_menu'))
    .replace('self.update_menu(', 'self.%s(' % short_name('update_menu'))
    .replace('self.update', 'self.%s' % short_name('update'))
    .replace('self.menu_is_highlighted(', 'self.%s(' % short_name('menu_is_highlighted'))
    .replace('self.versions(', 'self.%s(' % short_name('versions'))
    .replace('self.getIcon(', 'self.%s(' % short_name('get_icon'))
    .replace('self.handle_action(', 'self.%s(' % short_name('hand_action'))
    .replace('HappyMacStatusBarApp', 'c_1')
    .replace('quit_button', nextid("quit_button"))
    .replace('last_title', nextid("last_title"))
    .replace('quit_callback', nextid("quit_callback"))
    .replace('self.menu', 'self.%s' % nextid("menu"))
    .replace('self.start', 'self.%s' % nextid("start"))

    # main callbacks
    .replace('self.about', 'self.%s' % short_name('about'))
    .replace('self.show_emoji_and_name', 'self.%s' % short_name('show_emoji_and_name'))
    .replace('self.show_emoji', 'self.%s' % short_name('show_emoji'))
    .replace('self.terminate', 'self.%s' % short_name('terminate'))
    .replace('self.resume', 'self.%s' % short_name('resume'))
    .replace('self.suspend', 'self.%s' % short_name('suspend'))
    .replace('self.google', 'self.%s' % short_name('goold'))
    .replace('self.report', 'self.%s' % short_name('report'))
    .replace('self.activity_monitor', 'self.%s' % short_name('activity_monitor'))
    .replace('self.version', 'self.%s' % short_name('version'))
    .replace('self.load_version', 'self.%s' % short_name('load_version'))
    .replace('self.restart', 'self.%s' % short_name('restarts'))
    .replace('self.quit', 'self.%s' % short_name('quit'))
    .replace('self.menu_item_for_process', 'self.%s' % short_name('menu_item_for_process'))

    # activity definitions
    .replace('def get_activity_path(', 'def a__%s(' % short_name('get_activity_path'))
    .replace('def get_report_path(', 'def a__%s(' % short_name('get_report_path'))
    .replace('def update(', 'def a__%s(' % short_name('update'))
    .replace('def get_activities(', 'def a__%s(' % short_name('get_activities'))
    .replace('def generate_report(', 'def a__%s(' % short_name('generate_report'))

    # process definitions
    .replace('def clear_process_cache(', 'def p__%s(' % short_name('clear_process_cache'))
    .replace('def cpu(', 'def p__%s(' % short_name('cpu'))
    .replace('def terminate_process(', 'def p__%s(' % short_name('terminate_p'))
    .replace('def process(', 'def p__%s(' % short_name('process'))
    .replace('def parent(', 'def p__%s(' % short_name('parent'))
    .replace('def nice(', 'def p__%s(' % short_name('nice'))
    .replace('def location(', 'def p__%s(' % short_name('location'))
    .replace('def process_time(', 'def p__%s(' % short_name('process_time'))
    .replace('def child_processes(', 'def p__%s(' % short_name('child_processes'))
    .replace('def parents(', 'def p__%s(' % short_name('parents'))
    .replace('def family(', 'def p__%s(' % short_name('family'))
    .replace('def family_cpu_usage(', 'def p__%s(' % short_name('family_cpu_usage'))
    .replace('def details(', 'def p__%s(' % short_name('details'))
    .replace('def top(', 'def p__%s(' % short_name('top'))
    .replace('def suspend_pid(', 'def p__%s(' % short_name('suspend_pid'))
    .replace('def resume_pid(', 'def p__%s(' % short_name('resume_pid'))

    # suspender definitions
    .replace('def busy_count(', 'def s__%s(' % short_name('busy_count'))
    .replace('def manage(', 'def s__%s(' % short_name('manage'))
    .replace('def suspend_process(', 'def s__%s(' % short_name('suspend_process'))
    .replace('def resume_process(', 'def s__%s(' % short_name('resume_process'))
    .replace('def set_auto_preference(', 'def s__%s(' % short_name('set_auto_preference'))
    .replace('def get_auto_preference(', 'def s__%s(' % short_name('get_auto_preference'))
    .replace('def get_resource_hog_count(', 'def s__%s(' % short_name('get_resource_hog_count'))
    .replace('def reset_resource_hog_count(', 'def s__%s(' % short_name('reset_resource_hog_count'))
    .replace('def increase_resource_hog_count(', 'def s__%s(' % short_name('increase_resource_hog_count'))
    .replace('def get_suspended_tasks(', 'def s__%s(' % short_name('get_suspended_tasks'))
    .replace('def exit(', 'def s__%s(' % short_name('exit'))

    # utils definitions
    .replace('def get_current_app(', 'def u__%s(' % short_name('get_current_app'))
    .replace('def get_current_app_name(', 'def u__%s(' % short_name('get_current_app_name'))
    .replace('def get_current_app_short_name(', 'def u__%s(' % short_name('get_current_app_short_name'))
    .replace('def get_current_app_pid(', 'def u__%s(' % short_name('get_current_app_pid'))
    .replace('def get_active_chrome_tabs(', 'def u__%s(' % short_name('get_active_chrome_tabs'))
    .replace('def get_active_window_name(', 'def u__%s(' % short_name('get_active_window_name'))
    .replace('def is_chrome_window(', 'def u__%s(' % short_name('is_chrome_window'))
    .replace('def is_active_window(', 'def u__%s(' % short_name('is_active_window'))
    .replace('def get_window_name(', 'def u__%s(' % short_name('get_window_name'))
    .replace('def clear_windows_cache(', 'def u__%s(' % short_name('clear_windows_cache'))
    .replace('def get_all_windows(', 'def u__%s(' % short_name('get_all_windows'))
    .replace('def run_osa_script((', 'def u__%s(' % short_name('run_osa_script'))

    # activity calls definitions
    .replace('get_activity_path(', 'a__%s(' % short_name('get_activity_path'))
    .replace('get_report_path(', 'a__%s(' % short_name('get_report_path'))
    .replace('update(', 'a__%s(' % short_name('update'))
    .replace('get_activities(', 'a__%s(' % short_name('get_activities'))
    .replace('generate_report(', 'a__%s(' % short_name('generate_report'))

    # suspender calls
    .replace('busy_count(', 's__%s(' % short_name('busy_count'))
    .replace('manage(', 's__%s(' % short_name('manage'))
    .replace('suspend_process(', 's__%s(' % short_name('suspend_process'))
    .replace('resume_process(', 's__%s(' % short_name('resume_process'))
    .replace('set_auto_preference(', 's__%s(' % short_name('set_auto_preference'))
    .replace('get_auto_preference(', 's__%s(' % short_name('get_auto_preference'))
    .replace('get_resource_hog_count(', 's__%s(' % short_name('get_resource_hog_count'))
    .replace('reset_resource_hog_count(', 's__%s(' % short_name('reset_resource_hog_count'))
    .replace('increase_resource_hog_count(', 's__%s(' % short_name('increase_resource_hog_count'))
    .replace('get_suspended_tasks(', 's__%s(' % short_name('get_suspended_tasks'))
    .replace('exit(', 's__%s(' % short_name('exit'))

    # utils calls
    .replace('get_current_app(', 'u__%s(' % short_name('get_current_app'))
    .replace('get_current_app_name(', 'u__%s(' % short_name('get_current_app_name'))
    .replace('get_current_app_short_name(', 'u__%s(' % short_name('get_current_app_short_name'))
    .replace('get_current_app_pid(', 'u__%s(' % short_name('get_current_app_pid'))
    .replace('get_active_chrome_tabs(', 'u__%s(' % short_name('get_active_chrome_tabs'))
    .replace('get_active_window_name(', 'u__%s(' % short_name('get_active_window_name'))
    .replace('is_chrome_window(', 'u__%s(' % short_name('is_chrome_window'))
    .replace('is_active_window(', 'u__%s(' % short_name('is_active_window'))
    .replace('get_window_name(', 'u__%s(' % short_name('get_window_name'))
    .replace('clear_windows_cache(', 'u__%s(' % short_name('clear_windows_cache'))
    .replace('get_all_windows(', 'u__%s(' % short_name('get_all_windows'))
    .replace('run_osa_script(', 'u__%s(' % short_name('run_osa_script'))

    # process calls
    .replace('clear_process_cache(', 'p__%s(' % short_name('clear_process_cache'))
    .replace('cpu(', 'p__%s(' % short_name('cpu'))
    .replace('terminate_process(', 'p__%s(' % short_name('terminate_p'))
    .replace('process(', 'p__%s(' % short_name('process'))
    .replace('parent(', 'p__%s(' % short_name('parent'))
    .replace('nice(', 'p__%s(' % short_name('nice'))
    .replace('location(', 'p__%s(' % short_name('location'))
    .replace('process_time(', 'p__%s(' % short_name('process_time'))
    .replace('child_processes(', 'p__%s(' % short_name('child_processes'))
    .replace('parents(', 'p__%s(' % short_name('parents'))
    .replace('family(', 'p__%s(' % short_name('family'))
    .replace('family_cpu_usage(', 'p__%s(' % short_name('family_cpu_usage'))
    .replace('details(', 'p__%s(' % short_name('details'))
    .replace('top(', 'p__%s(' % short_name('top'))
    .replace('suspend_pid(', 'p__%s(' % short_name('suspend_pid'))
    .replace('resume_pid(', 'p__%s(' % short_name('resume_pid'))

    # special cases
    .replace('map(cpu,', 'map(p__%s,' % short_name('cpu'))
)
contents = re.sub(r"([^a-z_/])process\.", r"\1", contents)
contents = re.sub(r"([^a-z_/])suspender\.", r"\1", contents)
contents = re.sub(r"([^a-z_/])activity\.", r"\1", contents)
contents = re.sub(r"([^a-z_/])server\.", r"\1", contents)
contents = re.sub(r"([^a-z_/])utils\.", r"\1", contents)

with open(output_path, "w") as fout:
    contents = contents.replace('\n', '@@@')
    fout.write(contents)
    fout.write("""if __name__ == "__main__":@@@    run()@@@""")


os.system(r"/Applications/Visual\ Studio\ Code.app/Contents/Resources/app/bin/code %s" % output_path)
