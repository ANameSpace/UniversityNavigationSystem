import datetime
import os
import zipfile
from enum import Enum
from colorama import Fore


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
            self.logs_directory = os.path.join(self.current_directory, "UniversityNavigationSystem", "logs")
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
                    os.remove(txt_filename)
                except OSError as e:
                    print("Error: %s - %s." % (e.filename, e.strerror))

        # Clear old logs files
        old_files = sorted([os.path.join(self.logs_directory, f) for f in os.listdir(self.logs_directory) if f.endswith('.zip')], key=os.path.getctime)
        if len(old_files) > 5:
            deleted = 0
            for deleted_file in old_files:
                if deleted_file.find(str(today)) != -1:
                    continue
                if len(old_files) - deleted <= 5:
                    continue
                try:
                    os.remove(deleted_file)
                except OSError as e:
                    print("Error: %s - %s." % (e.filename, e.strerror))
                deleted += 1

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
        INFO = str(Fore.BLUE + "INFO")
        WARNING = str(Fore.YELLOW + "WARNING")
        ERROR = str(Fore.RED + "ERROR")

    def send(self, log_type: LogType, msg: str):
        """
           Send a message to the log
           :param LogType log_type: Message type
           :param str msg: Message text
        """
        print(Fore.LIGHTWHITE_EX + "[" + log_type.value + Fore.LIGHTWHITE_EX + "]" + Fore.WHITE + " " + str(msg) + Fore.RESET)
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
