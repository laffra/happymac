#pylint: disable=E0401

import error
import log
import os
import glob
import inspect
import json
import preferences
import rumps
import sys
import urllib2
import versions

home_dir = os.path.join(os.path.expanduser("~"), "HappyMacApp")
downloads_dir = os.path.join(home_dir, "downloads")
if not os.path.exists(downloads_dir):
    os.makedirs(downloads_dir)

sys.path.append(home_dir)

downloads = None
try:
    import downloads
except:
    pass

def main():
    download_latest()
    switch_version(preferences.get("version", last_version()))

def switch_version(version):
    set_version(version)
    try:
        mod = find_version(version)
    except:
        mod = find_version(last_version())
    if mod:
        main = getattr(mod, "main")
        rumps.notification("HappyMac", "HappyMac %s is now running" % version, "See the emoji icon in the status bar")
        main.main()
    else:
        error.error("Cannot switch to version %s" % version)


def find_version(version):
    try:
        return getattr(versions, version)
    except:
        if downloads:
            return getattr(downloads, version)

def download_latest():
    try:
        latest = json.loads(urllib2.urlopen('https://happymac.app/_functions/latest').read())
        file_separator = "#@#@#@#@#"
        line_separator = "@@@"
        version = latest["version"]
        new_dir = os.path.join(downloads_dir, version)
        if os.path.exists(new_dir):
            # this version was already downloaded
            return
        if not os.path.exists(new_dir):
            os.makedirs(new_dir)
        fout = None
        for line in latest["contents"].split(line_separator):
            if line.startswith(file_separator):
                filename = line.split()[-1]
                if fout: fout.close()
                fout = open(os.path.join(new_dir, filename), "w")
            else:
                if fout: fout.write("%s\n" % line)
        if fout: fout.close()
        init_path = os.path.join(downloads_dir, "__init__.py")
        with open(init_path, "a") as fout:
            fout.write("import %s\n\n" % version)
        global downloads
        import downloads
        reload(downloads)
        rumps.notification("HappyMac Update", "A new version was downloaded", "See: Preferences > Versions", sound=True)
    except Exception as e:
        log.log("Cannot download latest: %s" % e)

def set_version(version):
    preferences.set("version", None if version == last_version else version)

def last_version():
    return sorted(get_versions())[-1]

def get_versions():
    available_builtin_versions = filter(inspect.ismodule, [ getattr(versions, name) for name in dir(versions) ])
    builtin_versions = [version.__name__.split(".")[-1] for version in available_builtin_versions]
    available_downloaded_versions = glob.glob(os.path.join(downloads_dir, "v[0-9]*"))
    downloaded_versions = [version.split(os.path.sep)[-1] for version in available_downloaded_versions]
    return builtin_versions + downloaded_versions