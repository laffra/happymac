#pylint: disable=E0401

import error
import imp
import log
import os
import glob
import inspect
import json
import preferences
import requests
import rumps
import sys
import tempfile
import traceback
import uuid
import versions

try:
    import cPickle as pickle
except ImportError:
    import pickle as pickle

home_dir = os.path.join(os.path.expanduser("~"), "HappyMacApp")
downloads_dir = os.path.join(home_dir, "downloads")
if not os.path.exists(downloads_dir):
    os.makedirs(downloads_dir)

sys.path.append(home_dir)
running_local = not getattr(sys, "_MEIPASS", False)
testing = False


def main(quit_callback=None):
    if testing or not running_local:
        download_latest()
    try:
        load_version(last_version(), quit_callback)
    except Exception as e:
        log.log("ERROR: Could not load version due to %s. Loading built-in v00001" % e)
        log.log(traceback.format_exc())
        load_version("v00001", quit_callback)

def load_version(version, quit_callback=None):
    log.log("Load version %s" % version)
    try:
        mod = find_version(version)
    except Exception as e:
        log.log("Could not find version %s due to %s" % (version, e))
        mod = find_version(last_version())
    if mod:
        main_mod = getattr(mod, "main")
        log.log("Calling run on %s" % main_mod)
        main_mod.run(quit_callback)
    else:
        log.log("Cannot load version %s" % version)

def find_version(version):
    log.log("Find version %s" % version)
    return getattr(versions, version, find_downloaded_version(version))

def find_downloaded_version(version):
    version_path = os.path.join(downloads_dir, '%s' % version)
    if not os.path.exists(version_path):
        log.log("Downloads: Could not find version %s in %s" % (version, version_path))
        return None
    try:
        with open(version_path, "rb") as file:
            package = pickle.load(file)
        mod = load_module_from_source(version, package["contents"])
        mod.main = mod
        return mod
    except Exception as e:
        error.error("Download: Problem with version %s: %s" % (version, e))

def load_module_from_source(module_name, source):
    temporary_path = tempfile.mkstemp(".py")[1]
    with open(temporary_path, "w") as fout:
        fout.write(source)
    mod =  imp.load_source(module_name, temporary_path)
    if not testing:
        os.remove(temporary_path)
    return mod

def download_latest():
    try:
        hardware_uuid = uuid.get_hardware_uuid()
        latest_url = 'https://happymac.app/_functions/latest?version=%s&uuid=%s' % (last_version(), hardware_uuid)
        log.log("Download: getting the latest version at %s" % latest_url)
        latest = json.loads(requests.get(latest_url).content)
        latest['contents'] = latest['contents'].replace("@@@", "\n")
        save_contents(latest)
    except:
        error.error("Download: cannot get latest version")

def save_contents(latest):
    version = latest["version"]
    path = os.path.join(downloads_dir, '%s' % version)
    if os.path.exists(path):
        log.log("Download: version %s already installed" % version)
    else:
        with open(path, "wb") as file:
            pickle.dump(latest, file, 2)
        log.log("Download: extracted version %s to %s" % (version, path))
        rumps.notification("HappyMac Update", "A new version was downloaded", "Running %s" % version, sound=False)
    log.log("Download: available versions: %s" % get_versions())

def last_version():
    if not testing and running_local:
        return "v00001"
    return sorted(get_versions())[-1]

def get_versions():
    available_builtin_versions = filter(inspect.ismodule, [ getattr(versions, name) for name in dir(versions) ])
    builtin_versions = [version.__name__.split(".")[-1] for version in available_builtin_versions]
    available_downloaded_versions = glob.glob(os.path.join(downloads_dir, "v[0-9]*"))
    downloaded_versions = [version.split(os.path.sep)[-1] for version in available_downloaded_versions]
    return sorted(builtin_versions + downloaded_versions)

if __name__ == "__main__":
    testing = True
    main()