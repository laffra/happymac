#pylint: disable=E1101
#pylint: disable=E0611

import AppKit
import error
import Foundation
import log
import os
import psutil
import re
import rumps
import time
import utils

total_times = {}
cpu_cache = {}
processes = {}
password = ""
root_allowed = True
dialog_open = False

def on_battery():
    return not psutil.sensors_battery().power_plugged

def battery_percentage():
    return psutil.sensors_battery().percent

def clear_process_cache():
    cpu_cache.clear()
    processes.clear()

def get_cpu_percent():
    if -1 in cpu_cache:
        return cpu_cache[-1]
    cpu_cache[-1] = percent = psutil.cpu_percent()
    return percent

def cpu(pid=-1):
    if pid == 0:
        return 0
    if pid in cpu_cache:
        return cpu_cache[pid]
    try:
        total_time = get_total_time(pid)
        now = time.time()
        if not pid in total_times:
            total_times[pid] = (now, total_time)
        last_when, last_time = total_times[pid]
        result = (total_time - last_time) / (now - last_when + 0.00001)
        total_times[pid] = (now, total_time)
        cpu_cache[pid] = result
        return result
    except psutil.AccessDenied as e:
        cmd = ps_output = "???"
        try:
            cmd = "ps -p %s -o %%cpu | grep -v CPU" % pid
            ps_output = os.popen(cmd).read() or "0"
            return float(ps_output) / 100
        except:
            error.error("Cannot parse '%s' => '%s' into a float in process.cpu" % (cmd, ps_output))
        return 0
    except (psutil.NoSuchProcess, psutil.ZombieProcess) as e:
        return 0
    except Exception as e:
        log.log("Unhandled Error in process.cpu", e)
        return 0

def get_process(pid):
    if not pid in processes:
        try:
            processes[pid] = psutil.Process(pid)
        except (psutil.NoSuchProcess, psutil.ZombieProcess):
            return None
    return processes[pid]

system_locations = [
    "/usr/libexec/",
    "/usr/sbin/",
    "/sbin/",
    "/System/Library/",
]

def is_system_process(pid):
    if pid < 2:
        return True
    name = location(pid)
    for path in system_locations:
        if name.startswith(path):
                return True
    return False

def get_name(pid):
    try:
        name = get_process(pid).name()
        if len(name) == 16:
            # psutil truncates names to 16 characters
            name = location(pid).split("/")[-1]
        return name
    except:
        return ""

def parent_pid(pid):
    return get_process(pid).ppid()

def get_total_time(pid):
    proc = get_process(pid)
    if not proc:
        return 0
    times = proc.cpu_times() if pid != -1 else psutil.cpu_times()
    return times.user + times.system + getattr(times, "children_user", 0) + getattr(times, "children_system", 0)

def child_processes(pid, includeSelf=True):
    p = get_process(pid)
    if not p: return []
    kids = p.children()
    for grandkid in kids:
        kids.extend(child_processes(grandkid.pid, False))
    if includeSelf:
        kids.append(get_process(pid))
    return sorted(set(kids), key=lambda p: cpu(p.pid))

def parents(pid, includeSelf=True):
    processes = []
    p = get_process(pid if includeSelf else parent_pid(pid))
    while p.pid:
        processes.append(p)
        p = get_process(parent_pid(p.pid))
    return sorted(set(processes), key=lambda p: cpu(p.pid))

def family(pid):
    return sorted(set(child_processes(pid) + parents(pid)), key=lambda p: cpu(p.pid))

def family_cpu_usage(pid):
    return sum(map(cpu, [p.pid for p in family(pid)]))

def getMyPid():
    return os.getpid(

def details(pid):
    p = get_process(pid)
    return "%s - %s - %s\n" % (
        p.cwd(),
        p.connections(),
        p.open_files()
    )

def top(exclude, count=5):
    my_pid = os.getpid()
    exclude_pids = set(p.pid for p in exclude)
    def create_process(pid):
        try:
            name = get_name(pid)
            if pid in exclude_pids or pid == my_pid or name == "last":
                return None
            return get_process(pid)
        except:
            return None

    processes = filter(None, (create_process(pid) for pid in psutil.pids()))
    return list(reversed(sorted(processes, key=lambda p: -cpu(p.pid))[:count]))

def location(pid):
    p = get_process(pid)
    if hasattr(p, "location"):
        return p.location
    try:
        path = p.cmdline()[0]
    except psutil.AccessDenied:
        path = os.popen("ps %d" % pid).read()
    except (AttributeError, IndexError, psutil.NoSuchProcess, psutil.ZombieProcess):
        return ""
    try:
        path = re.sub(r".*[0-9] (/[^-]*)-*.*", r"\1", path.split('\n')[-2]).strip()
    except:
        pass
    p.location = path
    return path

def terminate_pid(pid):
    if is_system_process(pid):
        rumps.alert(
            "HappyMac: Terminate Canceled",
            "Process %s (%s) is a critical process that should not be terminated." % (pid, get_name(pid))
        )
        return False
    title = "Are you sure you want to terminate process %s (%s)?" % (pid, get_name(pid))
    message = ("Terminating this process could lead to data loss.\n\n" +
            "We suggest you suspend the process, not terminate it.")
    if rumps.alert(title, message, ok="Terminate, I know what I am doing", cancel="Cancel"):
        return execute_shell_command("terminate", pid, "kill -9 %s" % pid)
    else:
        log.log("User skipped termination of process %d (%s)" % (pid, get_name(pid)))

def suspend_pid(pid):
    if is_system_process(pid):
        rumps.alert(
            "HappyMac: Suspend Canceled",
            "Process %s (%s) is a critical process that should not be suspended." % (pid, get_name(pid))
        )
        return False
    return execute_shell_command("suspend", pid, "kill -STOP %s" % pid)

def resume_pid(pid):
    if is_system_process(pid):
        return False
    return execute_shell_command("resume", pid, "kill -CONT %s" % pid)

def execute_shell_command(operation, pid, command):
    output = os.popen("%s 2>&1" % command).read()
    if "Operation not permitted" in output:
        description = "%s process %d (%s)" % (operation, pid, get_name(pid))
        return execute_as_root(description, command)
    else:
        return True

def set_allow_root(allow_root):
    global root_allowed
    root_allowed = allow_root

def execute_as_root(description, command):
    if not root_allowed:
        return False
    global password, dialog_open
    if dialog_open:
        return
    if not password:
        if not AppKit.NSThread.isMainThread():
            # Cannot show a dialogue on a background thread
            return
        window = rumps.Window(
            "Please enter your admin or root password:",
            "HappyMac: To %s, an admin or root password is needed." % description,
            cancel = "Cancel"
        )
        window._textfield = AppKit.NSSecureTextField.alloc().initWithFrame_(Foundation.NSMakeRect(0, 0, 200, 25))
        window._alert.setAccessoryView_(window._textfield)
        window._alert.window().setInitialFirstResponder_(window._textfield)
        try:
            dialog_open = True
            response = window.run()
        finally:
            dialog_open = False
        if response.clicked:
            password = response.text
    if password:
        os.popen('echo "%s" | sudo -S %s' % (password, command)).read()
        return True
    return False

def resume_all():
    for pid in processes.keys():
        if not resume_pid(pid):
            set_allow_root(False)
