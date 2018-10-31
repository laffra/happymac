import os
import glob
import inspect
import preferences
import sys
import versions

home_dir = os.path.join(os.path.expanduser("~"), "HappyMacApp")
downloads_dir = os.path.join(home_dir, "downloads")
if not os.path.exists(downloads_dir):
    os.makedirs(downloads_dir)

sys.path.append(home_dir)

import downloads

def main():
    switch_version(preferences.get("version", last_version()))

def switch_version(version):
    set_version(version)
    mod = find_version(version)
    main = getattr(mod, "main")
    main.main()

def find_version(version):
    try:
        return getattr(versions, version)
    except:
        return getattr(downloads, version)


def set_version(version):
    print "Version Manager: set version %s" % version
    preferences.set("version", None if version == last_version else version)

def last_version():
    return sorted(get_versions())[-1]

def get_versions():
    available_builtin_versions = filter(inspect.ismodule, [ getattr(versions, name) for name in dir(versions) ])
    builtin_versions = [version.__name__.split(".")[-1] for version in available_builtin_versions]
    available_downloaded_versions = glob.glob(os.path.join(downloads_dir, "v[0-9]*"))
    downloaded_versions = [version.split(os.path.sep)[-1] for version in available_downloaded_versions]
    print "builtin_versions", builtin_versions
    print "downloaded_versions", downloaded_versions
    return builtin_versions + downloaded_versions
