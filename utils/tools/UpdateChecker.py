import requests

from utils.tools.Log import Log


def check(ver: str):
    """
        Checking for updates
        :param str ver: Current version
    """
    try:
        response = requests.get("https://api.github.com/repos/ANameSpace/UniversityNavigationSystem/releases/latest", timeout=5)
        latest_ver = response.json()["name"]
        if ver == latest_ver:
            Log().send(Log.LogType.INFO, "You are using the latest version of the program.")
        else:
            Log().send(Log.LogType.WARNING, "A new version has been found!")
            Log().send(Log.LogType.WARNING, "You are using version " + ver + " | The latest version is " + latest_ver)
            Log().send(Log.LogType.WARNING, "Download - https://github.com/ANameSpace/UniversityNavigationSystem/releases/latest")
    except requests.exceptions.Timeout:
        Log().send(Log.LogType.ERROR, "The server is not responding. Failed to check for updates!")
    except KeyError:
        Log().send(Log.LogType.ERROR, "Couldn't find the latest version!")
    except:
        Log().send(Log.LogType.ERROR, "Couldn't check for updates!")
