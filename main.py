import sys

from PySide6.QtWidgets import QApplication
import os

from ui.UI import UI
from utils.tools.Log import Log

u_name = "Name"
window = None

if __name__ == '__main__':
    Log().send(Log.LogType.INFO, "Launching the program...")
    Log().send(Log.LogType.INFO, "Uploading data...")
    # Create data folder
    app_directory = os.path.join(os.getcwd(), "data")
    if not os.path.exists(app_directory):
        os.makedirs(app_directory)
    #self.log_file = os.path.join(self.logs_directory, self._generate_file_name())
    #TODO
    Log().send(Log.LogType.INFO, "Launching the window...")
    app = QApplication(sys.argv)
    window = UI(u_name)
    window.show()
    Log().send(Log.LogType.INFO, "The program was successfully launched!")
    sys.exit(app.exec())
