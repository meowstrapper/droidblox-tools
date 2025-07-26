from kivy.logger import Logger
from kivy.utils import platform

import json
import os

TAG = "DBSettings" + ": "

settingsTemplate = {"token": None}

if platform == "android":
    from android.storage import app_storage_path # type: ignore
    dbPath = app_storage_path()
else:
    dbPath = os.path.expanduser("~/.dbtools")
    os.makedirs(dbPath, exist_ok = True)

Logger.info(TAG + f"Running on {platform}, setting path to {dbPath}")

dbSettings = os.path.join(dbPath, "settings.json")

def getSetting(setting = None, all = False):
    with open(dbSettings, "r") as readSettings:
        settingsJson = json.load(readSettings)
        if all: return settingsJson
        else: return settingsJson.get(setting)

def setSetting(setting = None, newValue = None, create = False):
    if create: settingsJson = settingsTemplate
    else:
        settingsJson = getSetting(all = True)
        settingsJson[setting] = newValue

    with open(dbSettings, "w") as writeSettings:
        json.dump(settingsJson, writeSettings)

try:
    getSetting(all = True)
except:
    Logger.info(TAG + "Creating settings.json file")
    setSetting(create = True)