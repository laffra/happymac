import os
import glob
import inspect
import json
import preferences
import sys
import urllib2
import versions

home_dir = os.path.join(os.path.expanduser("~"), "HappyMacApp")
downloads_dir = os.path.join(home_dir, "downloads")
if not os.path.exists(downloads_dir):
    os.makedirs(downloads_dir)

sys.path.append(home_dir)

#pylint: disable=E0401
import downloads

def main():
    download_latest()
    switch_version(preferences.get("version", last_version()))

def switch_version(version):
    set_version(version)
    try:
        mod = find_version(version)
    except:
        mod = find_version(last_version())
    main = getattr(mod, "main")
    main.main()

def find_version(version):
    try:
        return getattr(versions, version)
    except:
        return getattr(downloads, version)

def download_latest():
    try:
        latest = json.loads(urllib2.urlopen('https://happymac.app/_functions/latest').read())
        file_separator = "#@#@#@#@#"
        line_separator = "@@@"
        new_dir = os.path.join(downloads_dir, latest["version"])
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
            fout.write("import %s\n\n" % latest["version"])
        reload(downloads)
    except Exception as e:
        print "Cannot download latest: %s" % e

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
