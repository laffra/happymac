from collections import defaultdict
import log
import process
import preferences

suspended_tasks = set()

def manage(foregroundTasks, backgroundTasks):
    for task in foregroundTasks:
        resume_process(task.pid)
    for task in filter(lambda task: get_suspend_preference(task.pid), backgroundTasks):
        suspend_process(task.pid)

def suspend_process(pid, manual=False):
    name = process.get_name(pid)
    if process.suspend_pid(pid):
        suspended_tasks.add((pid, name))
        if manual:
            log.log("Suspender: suspend %d %s - %s" % (pid, name, suspended_tasks))
            set_suspend_preference(pid, True)

def resume_process(pid, manual=False):
    name = process.get_name(pid)
    if process.resume_pid(pid):
        for pid, suspended_name in list(suspended_tasks):
            if name == suspended_name:
                suspended_tasks.remove((pid, name))
        if manual:
            log.log("Resume: resume %d %s - %s" % (pid, process.get_name(pid), suspended_tasks))
            set_suspend_preference(pid, False)

def set_suspend_preference(pid, value):
    preferences.set("suspend - %s" % process.get_name(pid), value)

def get_suspend_preference(pid):
    return preferences.get("suspend - %s" % process.get_name(pid))

def get_suspended_tasks():
    return [process.get_process(pid) for pid,_ in suspended_tasks]

def exit():
    for pid,_ in suspended_tasks:
        process.resume_pid(pid)