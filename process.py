import utils

import os
import psutil
import time

total_times = {}
cpu_cache = {}

def clear_cache():
  cpu_cache.clear()

def cpu(pid=-1):
  if pid in cpu_cache:
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

def name(pid):
  return psutil.Process(pid).name()

def parent(pid):
  return psutil.Process(pid).ppid()

def nice(pid, value=None):
  return psutil.Process(pid).nice(value)

def cmdline(pid):
  return psutil.Process(pid).cmdline()

def process_time(pid):
  times = psutil.Process(pid).cpu_times() if pid != -1 else psutil.cpu_times()
  return times.user + times.system + getattr(times, "children_user", 0) + getattr(times, "children_system", 0)

def children(pid, includeParent=False):
  children = psutil.Process(pid).children()
  if includeParent:
    children.append(psutil.Process(pid))
  return children

def details(pid):
  process = psutil.Process(pid)
  return "%s - %s - %s\n" % (
    process.cwd(),
    process.connections(),
    process.open_files()
  )

def top(excludeParentPid, count=5):
  my_pid = os.getpid()
  def create_process(pid):
    try:
      process = psutil.Process(pid)
      if excludeParentPid in [pid, process.ppid()] or pid == my_pid:
        return None
      return process
    except psutil.AccessDenied:
      return None

  processes = filter(None, (create_process(pid) for pid in psutil.pids()))
  return sorted(processes, key=lambda p: -cpu(p.pid))[:5]

def terminate(pid):
  try:
    psutil.Process(pid).terminate()
  except Exception as e:
    print "Error in terminate: %s" % e

def suspend(pid):
  try:
    psutil.Process(pid).suspend()
  except Exception as e:
    print "Error in suspend: %s" % e

def resume(pid):
  try:
    psutil.Process(pid).resume()
  except Exception as e:
    print "Error in resume: %s" % e