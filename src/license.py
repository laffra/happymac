import error
import json
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

    rumps.notification("HappyMac", "Welcome to HappyMac", "Please accept the agreement in the next dialogue.")
    dialog = rumps.Window(
        "Welcome to HappyMac",
        "HappyMac",
        "Please agree to the terms and conditions for HappyMac provided at\n\nhttps://happymac.app/eula",
        ok="I agree",
        cancel="I do not agree"
    )
    if dialog.run().clicked == 1:
        callback(download_license())

def download_license():
    try:
        url = "https://www.happymac.app/_functions/agree/?token=%s" % get_hardware_uuid()
        license = requests.get(url).content
        key = json.loads(license)["key"]
        preferences.set("license", key)
        return key
    except Exception as e:
        print "error", e, "Cannot download license"

def get_hardware_uuid():
    return os.popen("system_profiler SPHardwareDataType | grep UUID | sed 's/.* //' ").read()


if __name__ == "__main__":
    preferences.set("license", None)
    def agree(key):
        print "Got a license:", key
    get_license(agree)
