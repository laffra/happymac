from collections import defaultdict
import process

VERBOSE = False
RESOURCE_HOG_COUNT = 5
BACKGROUND_PROCESS_MAX_CPU = 0.35
busy_count = defaultdict(int)

suspended_tasks = set()
resumed_tasks = set()

def manage(foregroundTasks, backgroundTasks):
    if VERBOSE: print "manage %d %d" % (len(foregroundTasks), len(backgroundTasks))
    for task in foregroundTasks:
        busy_count[task.pid] = 0
        resume(task.pid)

    for task in filter(lambda task: process.cpu(task.pid) > BACKGROUND_PROCESS_MAX_CPU, backgroundTasks):
        busy_count[task.pid] += 1
        max_busy_count = RESOURCE_HOG_COUNT
        if VERBOSE: print "busy %d %d %s" % (busy_count[task.pid], max_busy_count, process.process(task.pid))
        if busy_count[task.pid] > max_busy_count:
            suspend(task.pid)

def suspend(pid):
    if VERBOSE: print "suspend %d:" % pid
    if pid in resumed_tasks:
        resumed_tasks.remove(pid)
        if VERBOSE: print "    remove from resumed tasks %s" % resumed_tasks
    if process.suspend(pid):
        suspended_tasks.add(pid)
        if VERBOSE: print "    add to suspended tasks %s" % suspended_tasks
    process.process(pid).suspended = True

def resume(pid):
    if pid in suspended_tasks:
        suspended_tasks.remove(pid)
    if process.resume(pid):
        resumed_tasks.add(pid)
    process.process(pid).suspended = False

def get_suspended_tasks():
    return [process.process(pid) for pid in suspended_tasks]