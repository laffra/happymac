import os
import shelve
import sys

try:
  shelf = shelve.open(os.path.join(os.path.expanduser("~"), ".happymac"))
except:
  print("Happymac is already running.")
  sys.exit(1)

def get(key, default=None):
    return shelf.get(key, default)

def set(key, value):
    shelf[key] = value

def set_preference(key, value):
    shelf[key] = value
    shelf.sync()
