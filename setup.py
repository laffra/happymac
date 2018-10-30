from setuptools import setup

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
    },
    'packages': ['rumps', 'Quartz', 'AppKit'],
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': PY2APP_OPTIONS},
    setup_requires=['py2app'],
)