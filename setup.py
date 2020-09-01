from setuptools import setup

APP = ['virtualschoolcontroller.py']
DATA_FILES = ['config.txt']
OPTIONS = {
    'argv_emulation': True,
    'iconfile': 'Calendar.icns',
    'plist': {
        'CFBundleShortVersionString': '0.2.0',
        'LSUIElement': '1'
    },
    'packages': ['rumps'],
}

setup(
    app=APP,
    name='Virtual School Controller',
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'], install_requires=['rumps']
)
