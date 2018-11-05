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
        "Please agree to the terms and conditions for HappyMac provided at\n\nhttps://happymac.app/eula\n\n%s" % LICENSE,
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

LICENSE = """
=== Welcome to HappyMac

These terms and conditions outline the rules and regulations for the use of the HappyMac app for MacOS and the corresponding website at happymac.app, hereafter collectively referred to as "HappyMac".

By using HappyMac we assume you accept these terms and conditions in full. Stop using HappyMac if you do not accept all of the terms and conditions stated on this page. The following terminology applies: "You" refers to the person using HappyMac. "We" refers to HappyMac.

=== Loss of application data

HappyMac makes it easy to suspend and/or terminate processes running on your laptop or desktop. The same capabilities are already offered by the MacOS built-in "Activity Monitor" application or the Option, Command, and Esc (Escape) dialog. See https://support.apple.com/en-us/HT201276 for more details.

You understand and agree that by terminating or suspending a process running on your device using the HappyMac app, you do so at your own risk, and you are solely responsible for any harm or damage that you suffer as a result, including but not limited to any loss of application data or operating system corruption.

=== Website Cookies

We employ the use of cookies on the HappyMac website. By visiting the site you consent to the use of cookies in accordance with HappyMac's privacy policy.

Most of the modern day interactive web sites use cookies to enable us to retrieve user details for each visit. Cookies are used in some areas of our site to enable the functionality of this area and ease of use for those people visiting. Some of our affiliate / advertising partners may also use cookies.

=== License

Unless otherwise stated, HappyMac and/or it's licensors own the intellectual property rights for all material on HappyMac. All intellectual property rights are reserved. You may view and/or print pages from https://happymac.app for your own personal use subject to restrictions set in these terms and conditions.

You must not:

- Republish material from https://happymac.app
- Sell, rent or sub-license material from https://happymac.app
- Reproduce, duplicate or copy material from https://happymac.app
- Reeingineer the internal workings of the HappyMac app
- Copy and redistribute the HappyMac app in any form or shapee it
- Redistribute content from HappyMac (unless content is specifically made for redistribution).

=== Hyperlinking to our Content

Any organization may link to our website without prior written approval.

Disclaimer

=== To the maximum extent permitted by applicable law, we exclude all representations, warranties and conditions relating to the use of HappyMac, both the app and the website (including, without limitation, any warranties implied by law in respect of satisfactory quality, fitness for purpose and/or the use of reasonable care and skill). Nothing in this disclaimer will:

- limit or exclude our or your liability for death or personal injury resulting from negligence;
- limit or exclude our or your liability for fraud or fraudulent misrepresentation;
- limit any of our or your liabilities in any way that is not permitted under applicable law; or
- exclude any of our or your liabilities that may not be excluded under applicable law.

The limitations and exclusions of liability set out in this Section and elsewhere in this disclaimer: (a) are subject to the preceding paragraph; and (b) govern all liabilities arising under the disclaimer or in relation to the subject matter of this disclaimer, including liabilities arising in contract, in tort (including negligence) and for breach of statutory duty.

To the extent that the website and the information and services on the website are provided free of charge, we will not be liable for any loss or damage of any nature.
"""

if __name__ == "__main__":
    preferences.set("license", None)
    def agree(key):
        print "Got a license:", key
    get_license(agree)
