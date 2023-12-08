import sys

from PySide6.QtWidgets import QApplication
import os

from ui.UI import UI
from utils.Data import Data
from utils.tools import UpdateChecker
from utils.tools.Log import Log

APP_VERSION = "0.0.4"


# BUILD
# pip3 freeze > requirements.txt
# nuitka --onefile --plugin-enable=pyside6 --include-data-dir=./resources=resources --remove-output --disable-console --output-dir=out --output-filename=UniversityNavigationSystem --no-pyi-file --jobs=4 main.py
if __name__ == '__main__':
    # Create data folder
    app_directory = os.path.join(os.getcwd(), "UniversityNavigationSystem")
    if not os.path.exists(app_directory):
        os.makedirs(app_directory)

    # Init logs system
    log = Log()
    log.send(Log.LogType.INFO, "Launching the program...")

    # Checking for updates
    log.send(Log.LogType.INFO, "Checking for updates...")
    UpdateChecker.check(APP_VERSION)

    # Init data system
    log.send(Log.LogType.INFO, "Uploading data...")
    data = Data()
    #TODO

    # Loading the window
    Log().send(Log.LogType.INFO, "Loading the window...")
    app = None
    u_name = "Name"
    try:
        app = QApplication(sys.argv)
        window = UI(Data().get_name())
        window.show()
    except:
        Log().send(Log.LogType.ERROR, "The window could not be created!")
    else:
        Log().send(Log.LogType.INFO, "The program was successfully launched!")
    finally:
        sys.exit(app.exec())
