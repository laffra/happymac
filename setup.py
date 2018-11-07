from setuptools import setup

APP_NAME = "HappyMac"
APP = ['src/happymac.py']
DATA_FILES = [
    'icons',
    'icons/burn.png', 'icons/frown.png', 'icons/happy.png', 'icons/nauseated.png', 'icons/ok.png', 'icons/sweating.png', 'icons/unhappy.png'
]
PY2APP_OPTIONS = {
    'argv_emulation': True,
    'iconfile': 'icons/app.icns',
    'plist': {
        'LSUIElement': True,
        'CFBundleName': APP_NAME,
        'CFBundleDisplayName': APP_NAME,
        'CFBundleGetInfoString': "HappyMac App",
        'CFBundleIdentifier': "com.chrislaffra.osx.happymac",
        'CFBundleVersion': "0.1.0",
        'CFBundleShortVersionString': "0.1.0",
        'NSHumanReadableCopyright': "Copyright 2018, Chris Laffra, All Rights Reserved"
    },
    'packages': ['rumps', 'Quartz', 'AppKit'],
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': PY2APP_OPTIONS},
    setup_requires=['py2app'],
)