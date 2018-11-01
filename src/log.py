import datetime
import os

home_dir = os.path.join(os.path.expanduser("~"), "HappyMacApp")
log_path = os.path.join(os.path.expanduser("~"), "happymac.log")

if not os.path.exists(log_path):
    with open(log_path, "w") as output:
        output.write("HappyMac Activity Log:\n")

def log(message, error=None):
    line = "%s: %s %s" % (datetime.datetime.utcnow(), message, error or "")
    with open(log_path, "a") as output:
        output.write("    %s" % line)
        output.write("\n")
    print line

def get_log():
    with open(log_path) as input:
        return input.read()