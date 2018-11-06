import error
import json
import log
import os
import preferences
import requests
import rumps
import webbrowser

def get_license(callback):
    global license_callback
    license_callback = callback
    license = preferences.get("license")
    if license:
        callback(license)
        return

    log.log("No local license key found; Show I Agree dialog now.")
    rumps.notification("HappyMac", "Welcome to HappyMac", "Please accept the agreement in the HappyMac dialog.")
    dialog = rumps.Window(
        "Welcome to HappyMac",
        "HappyMac",
        "Please agree to the terms and conditions for HappyMac provided at\n\nhttps://happymac.app/eula",
        ok="I Agree",
        cancel="I do not Agree"
    )
    result = dialog.run()
    log.log("I Agree dialog result: %s" % result.clicked)
    if result.clicked == 1:
        callback(download_license())

def download_license():
    try:
        url = "https://www.happymac.app/_functions/agree/?token=%s" % get_hardware_uuid()
        log.log("Getting license from: %s" % url)
        license = requests.get(url).content
        key = json.loads(license)["key"]
        log.log("Received license key: %s" % key)
        preferences.set("license", key)
        return key
    except Exception as e:
        error.error("Cannot download license")

def get_hardware_uuid():
    return os.popen("system_profiler SPHardwareDataType | grep UUID | sed 's/.* //' ").read()

if __name__ == "__main__":

    preferences.set("license", None)
    def agree(key):
        print "Got a license:", key
    get_license(agree)
