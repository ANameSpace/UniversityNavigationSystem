import sys

from PySide6.QtWidgets import QApplication

from ui.UI import UI
from utils.Log import Log

u_name = "Name"
window = None

if __name__ == '__main__':
    Log().send(Log.LogType.INFO, "Launching the program...")
    Log().send(Log.LogType.INFO, "Uploading data...")
    #TODO
    Log().send(Log.LogType.INFO, "Launching the window...")
    app = QApplication(sys.argv)
    window = UI(u_name)
    window.show()
    Log().send(Log.LogType.INFO, "The program was successfully launched!")
    sys.exit(app.exec())
