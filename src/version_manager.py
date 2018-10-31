import os
import glob
import inspect
import preferences
import versions

def main():
    switch_version(preferences.get("version", last_version()))

def switch_version(version):
    set_version(version)
    mod = getattr(versions, version)
    main = getattr(mod, "main")
    main.main()

def set_version(version):
    print "Version Manager: set version %s" % version
    preferences.set("version", None if version == last_version else version)

def last_version():
    return sorted(get_versions())[-1]

def get_versions():
    available_versions = filter(inspect.ismodule, [ getattr(versions, name) for name in dir(versions) ])
    print "versions", [version.__name__ for version in available_versions]
    return [version.__name__.split(".")[-1] for version in available_versions]
