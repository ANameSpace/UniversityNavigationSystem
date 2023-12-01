import datetime
import os


class Style:
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
            self.logs_directory = os.path.join(self.current_directory, "logs")
            if not os.path.exists(self.logs_directory):
                os.makedirs(self.logs_directory)
            self.log_file = os.path.join(self.logs_directory, self.generate_file_name())
            Log._init_already = True

    def generate_file_name(self):
        today = datetime.date.today()
        count = 1
        file_name = f"{today}_{count}.txt"

        while os.path.exists(os.path.join(self.logs_directory, file_name)):
            count += 1
            file_name = f"{today}_{count}.txt"

        return file_name

    def sendInfo(self, s):
        print(Style.TEXT_GREY + "[" + Style.TEXT_BLUE + "INFO" + Style.TEXT_GREY + "]" + Style.TEXT_WHITE + " " + str(s) + Style.FORMAT_RESET)
        self.write_to_file("[INFO] " + s)

    def sendWarning(self, s):
        print(Style.TEXT_GREY + "[" + Style.TEXT_YELLOW + "WARNING" + Style.TEXT_GREY + "]" + Style.TEXT_WHITE + " " + str(s) + Style.FORMAT_RESET)
        self.write_to_file("[WARNING] " + s)

    def sendError(self, s):
        print(Style.TEXT_GREY + "[" + Style.TEXT_RED + "ERROR" + Style.TEXT_GREY + "]" + Style.TEXT_WHITE + " " + str(s) + Style.FORMAT_RESET)
        self.write_to_file("[ERROR] " + s)

    def write_to_file(self, message):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        with open(self.log_file, "a") as file:
            file.write(log_entry)
