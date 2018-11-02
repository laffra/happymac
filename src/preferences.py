import log
import os
import sys

try:
    import cPickle as pickle
except ImportError:
    import pickle as pickle

def get_preferences_path():
    home_dir = os.path.join(os.path.expanduser("~"), "HappyMacApp")
    if not os.path.exists(home_dir):
        os.makedirs(home_dir)
    return os.path.join(home_dir, "happymac.prefs")

preferences = {}

if os.path.exists(get_preferences_path()):
    with open(get_preferences_path(), "rb") as file:
        preferences = pickle.load(file)

def get(key, default=None):
    return preferences.get(key, default)

def set(key, value):
    preferences[key] = value
    with open(get_preferences_path(), "wb") as file:
         pickle.dump(preferences, file, 2)
    log.log("Set preference %s to %s" % (key, repr(value)))
