import sys

from PySide6.QtWidgets import QApplication

from ui.UI import UI
from utils.Log import Log

u_name = "Name"
window = None

if __name__ == '__main__':
    Log().sendInfo("Launching the program...")
    Log().sendInfo("Uploading data...")
    #TODO
    Log().sendInfo("Launching the window...")
    app = QApplication(sys.argv)
    window = UI(u_name)
    window.show()
    Log().sendInfo("The program was successfully launched!")
    sys.exit(app.exec())
