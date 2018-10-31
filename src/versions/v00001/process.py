import utils

import os
import psutil
import time

VERBOSE = False
total_times = {}
cpu_cache = {}
processes = {}

def clear_cpu_cache():
    cpu_cache.clear()
    processes.clear()

def cpu(pid=-1):
    if pid != -1 and pid in cpu_cache:
        return cpu_cache[pid]
    try:
        total_time = process_time(pid)
        now = time.time()
        if not pid in total_times:
            total_times[pid] = (now - 0.01, total_time)
        last_when, last_time = total_times[pid]
        result = (total_time - last_time) / (now - last_when)
        total_times[pid] = (now, total_time)
        cpu_cache[pid] = result
        return result
    except (psutil.AccessDenied, psutil.NoSuchProcess, psutil.ZombieProcess):
        return 0
    except Exception as e:
        print "Error in cpu: %s" % e
        return 0

def process(pid):
    if not pid in processes:
        processes[pid] = psutil.Process(pid)
        if VERBOSE: print("add process %d %s" % (pid, processes[pid]))
    return processes[pid]

def name(pid):
    return process(pid).name()

def parent(pid):
    return process(pid).ppid()

def nice(pid, value=None):
    return process(pid).nice(value)

def cmdline(pid):
    return process(pid).cmdline()

def location(pid):
    return process(pid).cmdline()[0]

def process_time(pid):
    times = process(pid).cpu_times() if pid != -1 else psutil.cpu_times()
    return times.user + times.system + getattr(times, "children_user", 0) + getattr(times, "children_system", 0)

def children(pid, includeSelf=True):
    kids = process(pid).children()
    for grandkid in kids:
        kids.extend(children(grandkid.pid, False))
    if includeSelf:
        kids.append(process(pid))
    return sorted(set(kids), key=lambda p: cpu(p.pid))

def parents(pid, includeSelf=True):
    processes = []
    p = process(pid if includeSelf else parent(pid))
    while p.pid:
        processes.append(p)
        p = process(parent(p.pid))
    return sorted(set(processes), key=lambda p: cpu(p.pid))

def family(pid):
    return sorted(set(children(pid) + parents(pid)), key=lambda p: cpu(p.pid))

def details(pid):
    p = process(pid)
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
            p = process(pid)
            if pid in exclude_pids or pid == my_pid:
                return None
            return p
        except:
            return None

    processes = filter(None, (create_process(pid) for pid in psutil.pids()))
    return list(reversed(sorted(processes, key=lambda p: -cpu(p.pid))[:5]))

def terminate(pid):
    try:
        process(pid).terminate()
    except Exception as e:
        print "Error in terminate: %s" % e

def suspend(pid):
    try:
        process(pid).suspend()
        return True
    except psutil.AccessDenied:
        pass
    except Exception as e:
        print "Error in suspend: %s" % e

def resume(pid):
    try:
        process(pid).resume()
        return True
    except psutil.AccessDenied:
        pass
    except Exception as e:
        print "Error in resume: %s" % e