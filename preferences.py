import os
import shelve

shelf = shelve.open(os.path.join(os.path.expanduser("~"), ".happymac"))

def get(key, default=None):
    return shelf.get(key, default)

def set(key, value):
    shelf[key] = value

def set_preference(key, value):
    shelf[key] = value
    shelf.sync()
