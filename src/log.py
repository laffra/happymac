from __future__ import print_function
import datetime
import os

home_dir = os.path.join(os.path.expanduser("~"), "HappyMacApp")

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

def log(message, error=None):
    line = "%s: %s %s" % (datetime.datetime.utcnow(), message, error or "")
    with open(get_log_path(), "a") as output:
        output.write("    %s" % line)
        output.write("\n")
    print(line)

def get_log():
    with open(get_log_path()) as input:
        return input.read()