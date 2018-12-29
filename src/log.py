import datetime
import os

home_dir = os.path.join(os.path.expanduser("~"), "HappyMacApp")
ONE_KB = 1024
ONE_MB = ONE_KB * ONE_KB

def get_log_path():
    try:
        if not os.path.exists(home_dir):
            os.makedirs(home_dir)
        path = os.path.join(home_dir, "happymac_log.txt")
    except:
        path = os.path.join(os.path.expanduser("~"), "happymac_log.txt")
    if not os.path.exists(path):
        with open(path, "w") as output:
            output.write("HappyMac Activity Log:\n")
    return path

def log(message, error=None, truncate=True):
    line = "%s: %s %s" % (datetime.datetime.utcnow(), message, error or "")
    with open(get_log_path(), "a") as output:
        output.write("    %s" % line)
        output.write("\n")
    print line
    if truncate:
        truncate_log()

def truncate_log():
    size = os.stat(get_log_path()).st_size
    if size > ONE_MB:
        lines = open(get_log_path()).read().split("\n")
        with open(get_log_path(), "w") as output:
            output.write("\n".join(lines[-100:]))
        log("Truncated output to 100 lines", truncate=False)


def get_log():
    with open(get_log_path()) as input:
        return input.read()