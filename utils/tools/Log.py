import datetime
import os
import zipfile
from enum import Enum


class Style:
    """
        Text styles for the console
    """
    FORMAT_RESET = '\33[0m'
    FORMAT_BOLD = '\33[1m'
    FORMAT_ITALIC = '\33[3m'
    FORMAT_URL = '\33[4m'
    FORMAT_BLINK = '\33[5m'
    FORMAT_BLINK2 = '\33[6m'
    FORMAT_SELECTED = '\33[7m'

    TEXT_BLACK = '\33[30m'
    TEXT_RED = '\33[31m'
    TEXT_GREEN = '\33[32m'
    TEXT_YELLOW = '\33[33m'
    TEXT_BLUE = '\33[34m'
    TEXT_VIOLET = '\33[35m'
    TEXT_BEIGE = '\33[36m'
    TEXT_WHITE = '\33[37m'

    BG_BLACK = '\33[40m'
    BG_RED = '\33[41m'
    BG_GREEN = '\33[42m'
    BG_YELLOW = '\33[43m'
    BG_BLUE = '\33[44m'
    BG_VIOLET = '\33[45m'
    BG_BEIGE = '\33[46m'
    BG_WHITE = '\33[47m'

    TEXT_GREY = '\33[90m'
    TEXT_RED2 = '\33[91m'
    TEXT_GREEN2 = '\33[92m'
    TEXT_YELLOW2 = '\33[93m'
    TEXT_BLUE2 = '\33[94m'
    TEXT_VIOLET2 = '\33[95m'
    TEXT_BEIGE2 = '\33[96m'
    TEXT_WHITE2 = '\33[97m'

    BG_GREY = '\33[100m'
    BG_RED2 = '\33[101m'
    BG_GREEN2 = '\33[102m'
    BG_YELLOW2 = '\33[103m'
    BG_BLUE2 = '\33[104m'
    BG_VIOLET2 = '\33[105m'
    BG_BEIGE2 = '\33[106m'
    BG_WHITE2 = '\33[107m'


class Log:
    _instance = None
    _init_already = False

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if not Log._init_already:
            self.current_directory = os.getcwd()
            self.logs_directory = os.path.join(self.current_directory, "data", "logs")
            if not os.path.exists(self.logs_directory):
                os.makedirs(self.logs_directory)
            self.log_file = os.path.join(self.logs_directory, self._generate_file_name())
            Log._init_already = True

    def _generate_file_name(self):
        """
           Generate log file name (PROTECTED)
           :return: File name
           :rtype: str
        """
        today = datetime.date.today()
        count = 1
        file_name = f"{today}_{count}.txt"

        # Archiving of old log files
        old_files = [f for f in os.listdir(self.logs_directory) if f.endswith('.txt')]
        for old_file in old_files:
            txt_filename = os.path.join(self.logs_directory, old_file)
            zip_filename = os.path.join(self.logs_directory, f'{os.path.splitext(old_file)[0]}.zip')
            # create zip
            with zipfile.ZipFile(zip_filename, 'w') as zipf:
                zipf.write(txt_filename, os.path.basename(txt_filename))
                try:
                    os.remove(os.path.join(self.logs_directory, txt_filename))
                except OSError as e:
                    print("Error: %s - %s." % (e.filename, e.strerror))

        # Searching for today's latest log file
        while os.path.exists(os.path.join(self.logs_directory, f"{today}_{count}.zip")):
            count += 1
            file_name = f"{today}_{count}.txt"
        # Return
        return file_name

    class LogType(Enum):
        """
            Types of log messages
        """
        INFO = str(Style.TEXT_BLUE + "INFO")
        WARNING = str(Style.TEXT_YELLOW + "WARNING")
        ERROR = str(Style.TEXT_RED + "ERROR")

    def send(self, log_type: LogType, msg: str):
        """
           Send a message to the log
           :param LogType log_type: Message type
           :param str msg: Message text
        """
        print(Style.TEXT_GREY + "[" + log_type.value + Style.TEXT_GREY + "]" + Style.TEXT_WHITE + " " + str(msg) + Style.FORMAT_RESET)
        self.write_to_file("[" + log_type.name + "] " + msg)

    def write_to_file(self, msg: str):
        """
            Save the message in a file
            :param str msg: Message text
        """
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {msg}\n"
        with open(self.log_file, "a") as file:
            file.write(log_entry)
