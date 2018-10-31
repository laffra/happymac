import os
import sys
try:
    import cPickle as pickle
except ImportError:
    import pickle as pickle

home_dir = os.path.join(os.path.expanduser("~"), "HappyMacApp")
preferences_path = os.path.join(home_dir, "preferences")
preferences = {}

if not os.path.exists(home_dir):
    os.makedirs(home_dir)
if os.path.exists(preferences_path):
    with open(preferences_path, "rb") as file:
        preferences = pickle.load(file)

def get(key, default=None):
    return preferences.get(key, default)

def set(key, value):
    preferences[key] = value
    with open(preferences_path, "wb") as file:
         pickle.dump(preferences, file, 2)
