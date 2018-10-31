import os
import sys
try:
    import cPickle as pickle
except ImportError:
    import pickle as pickle

path = os.path.join(os.path.expanduser("~"), "happymac.preferences")
prefs = {}

try:
    if os.path.exists(path):
        with open(path, "rb") as file:
            prefs = pickle.load(file)
except Exception as e:
    print "Cannot load preferences. Is Happymac is already running? %s" % e
    sys.exit(1)

def get(key, default=None):
    return prefs.get(key, default)

def set(key, value):
    prefs[key] = value
    with open(path, "wb") as file:
         pickle.dump(prefs, file, 2)
