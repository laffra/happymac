import error
import json
import log
import os
import preferences
import requests

def get_license():
    try:
        return preferences.get("license") or download_license()
    except:
        error.error("Cannot find license")

def download_license():
    url = "https://www.happymac.app/_functions/agree/?token=%s" % get_hardware_uuid()
    log.log("Getting license from: %s" % url)
    license = requests.get(url).content
    key = json.loads(license)["key"]
    log.log("Received license key: %s" % key)
    preferences.set("license", key)
    return key

def get_hardware_uuid():
    return os.popen("system_profiler SPHardwareDataType | grep UUID | sed 's/.* //' ").read()
