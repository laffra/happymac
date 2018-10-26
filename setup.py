from setuptools import setup

APP = ['happymac.py']
DATA_FILES = [
    'burn.png', 'frown.png', 'happy.png', 'nauseated.png', 'ok.png', 'sweating.png', 'unhappy.png'
]
PY2APP_OPTIONS = {
    'argv_emulation': True,
    'plist': {
        'LSUIElement': True,
    },
    'packages': ['rumps', 'Quartz', 'AppKit'],
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': PY2APP_OPTIONS},
    setup_requires=['py2app'],
)