from collections import defaultdict
import log
import os
import process
import preferences
import utils

suspended_tasks = set()

ACTIVATE_CURRENT_APP = """
    set currentApp to path to frontmost application
    delay 2
    activate currentApp
"""

last_activated_pid = 0

def manage(foregroundTasks, backgroundTasks):
    for task in foregroundTasks:
        if not process.is_system_process(task.pid):
            resume_process(task.pid)
    for task in filter(lambda task: get_suspend_preference(task.pid), backgroundTasks):
        if not process.is_system_process(task.pid):
            suspend_process(task.pid)

def activate_current_app():
    global last_activated_pid
    pid = utils.get_current_app_pid()
    if pid != last_activated_pid:
        os.system("osascript -e \"%s\" &" % ACTIVATE_CURRENT_APP)
        last_activated_pid = pid

def suspend_process(pid, manual=False):
    name = process.get_name(pid)
    if process.suspend_pid(pid):
        suspended_tasks.add((pid, name))
        if manual:
            set_suspend_preference(name, True)
    else:
        set_suspend_preference(name, False)

def resume_process(pid, manual=False):
    name = process.get_name(pid)
    if manual or (pid,name) in suspended_tasks:
        if process.resume_pid(pid):
            for pid, suspended_name in list(suspended_tasks):
                if name == suspended_name:
                    suspended_tasks.remove((pid, name))
            if manual:
                set_suspend_preference(name, False)

def set_suspend_preference(name, value):
    preferences.set("suspend - %s" % name, value)

def get_suspend_preference(pid):
    return preferences.get("suspend - %s" % process.get_name(pid))

def get_suspended_tasks():
    return [process.get_process(pid) for pid,_ in suspended_tasks]

def exit():
    for pid,_ in suspended_tasks:
        process.resume_pid(pid)