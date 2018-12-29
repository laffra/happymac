import error
import json
import log
import preferences
import requests
import uuid

def get_license():
    try:
        return preferences.get("license") or download_license()
    except:
        log.log("Cannot find license")

def download_license():
    url = "https://www.happymac.app/_functions/agree/?token=%s" % uuid.get_hardware_uuid()
    log.log("Getting license from: %s" % url)
    license = requests.get(url).content
    key = json.loads(license)["key"]
    log.log("Received license key: %s" % key)
    preferences.set("license", key)