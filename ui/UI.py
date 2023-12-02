from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtGui import QPainter, QBrush, QFont, QColor, QPen
from PySide6.QtWidgets import QMainWindow, QPushButton, QLineEdit, QLabel, QFrame, QScrollArea, QVBoxLayout, QWidget, QGridLayout
from PySide6.QtCore import Qt, QTime, QSize, QTimer

from ui import AFK
from utils import Data
from utils.tools.Log import Log


class UI(QMainWindow):
    def __init__(self, str_name="None"):
        super().__init__()
        # temp
        self.origin = None
        self.task_num = 0
        self.str_name_len = 15 * len(str(str_name)) + 8
        self.floor_btns = []

        # zoom
        self.zoom_factor = 10.0
        self.offset = QtCore.QPoint(60, 60)

        # navigation
        self.current_floor = Data.get_default_floor()
        self.has_result = False
        self.route_ladders = []
        self.route_segments = []

        # window
        self.setWindowTitle(str_name)
        self.setStyleSheet("background-color: rgb(240, 240, 240);")
        self.setGeometry(100, 100, 300, 500)
        self.setMinimumSize(800, 370 + Data.get_floors_num() * 50)
        self.img = QtGui.QPixmap("./resources/icons/icon.png")
        if self.img.isNull():
            Log().send(Log.LogType.ERROR, "Failed to load ./resources/icons/icon.png")
        self.setWindowIcon(self.img)
        self.setIconSize(QSize(100, 100))

        # timer
        self.time_timer = QTimer(self)
        self.time_timer.timeout.connect(self.task_executor)
        self.time_timer.start(1000)

        # input
        self.input_field = QLineEdit(self)
        self.input_field.setGeometry(60, 7, self.width() - 60 * 2, 50)
        self.input_field.setFont(QFont("Arial", 16, weight=QFont.Bold))
        self.input_field.setStyleSheet("background-color: white; border-radius: 10px; border: 2px solid black;")
        self.completer = QtWidgets.QCompleter(Data.get_names_list())
        self.completer.popup().setStyleSheet("font-size: 16px;")
        self.input_field.setCompleter(self.completer)

        # clear button
        self.clear_btn = QPushButton(self)
        self.clear_btn.setEnabled(False)
        self.clear_btn.setGeometry(7, 7, 50, 50)
        self.clear_btn.setStyleSheet("background-color: rgb(235, 35, 48); border-radius: 10px;")
        self.img = QtGui.QPixmap("./resources/icons/close.png")
        if self.img.isNull():
            Log().send(Log.LogType.ERROR, "Failed to load ./resources/icons/close.png")
        self.clear_btn.setIcon(self.img)
        self.clear_btn.setIconSize(QSize(50, 50))
        self.clear_btn.clicked.connect(lambda: self.input_field.clear())
        self.clear_btn.clicked.connect(lambda: self.use(True))
        self.clear_btn.clicked.connect(lambda: Log().send(Log.LogType.INFO, "Button CLEAR_BTN was pressed"))

        # find button
        self.find_btn = QPushButton(self)
        self.find_btn.setGeometry(self.width() - 57, 7, 50, 50)
        self.find_btn.setStyleSheet("background-color: rgb(35, 92, 235); border-radius: 10px;")
        self.img = QtGui.QPixmap("./resources/icons/find.png")
        if self.img.isNull():
            Log().send(Log.LogType.ERROR, "Failed to load ./resources/icons/find.png")
        self.find_btn.setIcon(self.img)
        self.find_btn.setIconSize(QSize(36, 36))
        self.find_btn.clicked.connect(lambda: self.use(False))
        self.find_btn.clicked.connect(lambda: Log().send(Log.LogType.INFO, "Button FIND_BTN was pressed"))

        # floors frame
        self.floors_frame = QFrame(self)
        self.floors_frame.setStyleSheet("background-color: white; border-radius: 10px; border: 2px solid black;")
        self.floors_frame.setGeometry(7, self.height() - 30 - 50 * Data.get_floors_num(), 50, 50 * Data.get_floors_num())
        self.floors_layout = QGridLayout(self.floors_frame)
        row = 0
        for name in Data.get_floors():
            self.button = QLabel(str(name))
            self.button.setFixedSize(30, 30)
            self.button.setFont(QFont("Arial", 16, weight=QFont.Bold))
            if name == self.current_floor:
                self.button.setStyleSheet("background-color: rgb(39, 219, 57);")
            else:
                self.button.setStyleSheet("background-color: white;")
            self.floor_btns.append(self.button)
            self.floors_layout.addWidget(self.floor_btns[row], row, 0)
            row += 1

        # time
        self.time_label = QLabel("00:00", self)
        self.time_label.setFont(QFont("Arial", 16, weight=QFont.Bold))
        self.time_label.setStyleSheet("color: white; border-radius: 10px; background-color: rgb(49, 51, 56);")
        self.time_label.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.time_label.setGeometry(7, self.height() - 27, 65, 25)

        # name
        self.name_label = QLabel(str(str_name + " "), self)
        self.name_label.setFont(QFont("Arial", 16, weight=QFont.Bold))
        self.name_label.setStyleSheet("color: white; border-radius: 10px; background-color: rgb(49, 51, 56);")
        self.name_label.setAlignment(Qt.AlignTop | Qt.AlignRight)
        self.name_label.setGeometry(self.width() - (self.str_name_len + 7), 7, self.str_name_len, 25)

        # info frame
        self.info_frame = QFrame(self)
        self.info_frame.setVisible(False)
        self.info_frame.setStyleSheet("background-color: white; border-radius: 0px; border: 2px solid black;")
        if self.height() < self.width() and self.width() / 3 > self.height() / 2:
            self.info_frame.setGeometry(self.width() - self.width() // 2, 60, self.width() // 2, self.height() - 60)
        else:
            self.info_frame.setGeometry(10, self.height() // 2, self.width() - 20, self.height() // 2)

        # frame text
        self.frame_error_label = QLabel("НИЧЕГО НЕ НАЙДЕНО :/", self.info_frame)
        self.frame_error_label.setFont(QFont("Arial", 16, weight=QFont.Bold))
        self.frame_error_label.setStyleSheet("color: red; border: 0px; border-radius: 0px;")
        self.frame_error_label.setGeometry(self.info_frame.width() // 2 - 140, self.info_frame.height() // 2 - 15, 280, 25)

        # frame scroll
        self.frame_scroll_area = QScrollArea(self.info_frame)
        self.frame_scroll_area.setGeometry(0, 0, self.info_frame.width(), self.info_frame.height())
        self.frame_scroll_area.setFont(QFont("Arial", 16))
        self.frame_scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.frame_scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scrollbar_style = """
            QScrollBar:vertical {
                background: #f1f1f1;
                width: 10px;
                margin: 0px;
            }

            QScrollBar::handle:vertical {
                background: #888888;
                min-height: 20px;
            }

            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                background: none;
            }
        """
        self.frame_scroll_area.setStyleSheet(scrollbar_style)
        # frame scroll_layout
        self.frame_scroll_widget = QWidget()
        self.vbox = QVBoxLayout()
        for i in range(1, 100):
            # TODO text
            object = QLabel("тут будет текст")
            self.vbox.addWidget(object)
        self.frame_scroll_widget.setStyleSheet("border: 0px; border-radius: 0px;")
        self.frame_scroll_widget.setLayout(self.vbox)
        self.frame_scroll_area.setWidget(self.frame_scroll_widget)

    # Tasks
    def task_executor(self):
        # update time
        self.time_label.setText(QTime.currentTime().toString(" hh:mm"))
        if self.task_num == 0:
            if AFK.check_time():
                self.afk_close()
        self.task_num += 1
        if self.task_num > 60:
            self.task_num = 0

    # Ui actions
    def set_floor(self, floor):
        self.current_floor = floor
        for b in self.floor_btns:
            if str(b.text()) == str(floor):
                b.setStyleSheet("background-color: rgb(39, 219, 57);")
            else:
                b.setStyleSheet("background-color: white;")
        self.update()

    def use(self, close):
        AFK.action()
        if close:
            self.time_label.setVisible(True)
            self.name_label.setVisible(True)
            self.input_field.setEnabled(True)
            self.clear_btn.setEnabled(False)
            self.find_btn.setEnabled(True)
            self.info_frame.setVisible(False)
            self.has_result = False
            self.route_ladders = []
            self.route_segments = []
        else:
            self.name_label.setVisible(False)
            self.input_field.setEnabled(False)
            self.has_result = Data.is_valid_name(self.input_field.text())
            self.find_btn.setEnabled(False)
            self.clear_btn.setEnabled(True)
            self.info_frame.setVisible(True)
            self.resize_frame()
            if self.has_result:
                self.frame_error_label.setVisible(False)
                self.frame_scroll_area.setVisible(True)
            else:
                self.frame_error_label.setVisible(True)
                self.frame_scroll_area.setVisible(False)
                # TODO result add
        self.resize_frame()
        self.update()

    def afk_close(self):
        self.input_field.clear()
        self.set_floor(Data.get_default_floor())
        self.offset = QtCore.QPoint(60, 60)
        self.zoom_factor = 10.0
        self.use(True)

    def resize_frame(self):
        # frames
        if self.height() < self.width() and self.width() / 3 > self.height() / 2:
            # info
            self.info_frame.setGeometry(self.width() - self.width() // 2, 60, self.width() // 2, self.height() - 60)
            self.time_label.setVisible(True)
            # floors
            self.floors_frame.setGeometry(7, self.height() - 30 - 50 * Data.get_floors_num(), 50,
                                          50 * Data.get_floors_num())
        else:
            # info
            self.info_frame.setGeometry(10, self.height() // 2, self.width() - 20, self.height() // 2)
            self.time_label.setVisible(False)
            # floors
            self.floors_frame.setGeometry(7, self.height() - self.height() // 2 - 50 * Data.get_floors_num(), 50,
                                          50 * Data.get_floors_num())
        # content
        if self.has_result:
            self.frame_scroll_area.setGeometry(0, 0, self.info_frame.width(), self.info_frame.height())
        else:
            self.frame_error_label.setGeometry(self.info_frame.width() // 2 - 140, self.info_frame.height() // 2 - 15,
                                               280, 25)

    # Events (0.0.1-FINAL)
    def paintEvent(self, event):
        # draw map
        painter = QPainter(self)
        painter.setPen(QPen(QColor(0, 0, 0), 2))

        for wall in Data.get_walls(self.current_floor):
            x1, y1, x2, y2 = wall
            scaled_x1 = x1 * self.zoom_factor + self.offset.x()
            scaled_y1 = y1 * self.zoom_factor + self.offset.y()
            scaled_x2 = x2 * self.zoom_factor + self.offset.x()
            scaled_y2 = y2 * self.zoom_factor + self.offset.y()
            painter.drawLine(scaled_x1, scaled_y1, scaled_x2, scaled_y2)
        painter.setPen(QPen(QColor(0, 0, 0), 1))

        for empty_rooms in Data.get_empty_rooms(self.current_floor):
            x, y, width, height = empty_rooms
            scaled_x = x * self.zoom_factor + self.offset.x()
            scaled_y = y * self.zoom_factor + self.offset.y()
            scaled_width = width * self.zoom_factor
            scaled_height = height * self.zoom_factor
            painter.setBrush(QBrush(QColor(41, 41, 41)))
            painter.drawRect(scaled_x, scaled_y, scaled_width, scaled_height)

        for ladder in Data.get_ladders(self.current_floor):
            ladder_id, x, y, width, height = ladder
            scaled_x = x * self.zoom_factor + self.offset.x()
            scaled_y = y * self.zoom_factor + self.offset.y()
            scaled_width = width * self.zoom_factor
            scaled_height = height * self.zoom_factor
            if self.has_result:
                if self.route_ladders.count(str(ladder_id)) == 1:
                    painter.setBrush(QBrush(QColor(238, 255, 46)))
                else:
                    painter.setBrush(QBrush(QColor(183, 194, 64)))
            else:
                painter.setBrush(QBrush(QColor(194, 207, 58)))
            painter.drawRect(scaled_x, scaled_y, scaled_width, scaled_height)

        for room in Data.get_rooms_list(self.current_floor):
            name, x, y, width, height, x222 = room
            scaled_x = x * self.zoom_factor + self.offset.x()
            scaled_y = y * self.zoom_factor + self.offset.y()
            scaled_width = width * self.zoom_factor
            scaled_height = height * self.zoom_factor
            if self.has_result:
                if self.input_field.text() == name:
                    painter.setBrush(QBrush(QColor(59, 196, 57)))
                else:
                    painter.setBrush(QBrush(QColor(37, 73, 115)))
            else:
                painter.setBrush(QBrush(QColor(62, 127, 201)))
            painter.drawRect(scaled_x, scaled_y, scaled_width, scaled_height)

        if str(self.current_floor) == str(Data.get_default_floor()):
            point_id, x, y, r = Data.get_you_pos()
            scaled_x = x * self.zoom_factor + self.offset.x()
            scaled_y = y * self.zoom_factor + self.offset.y()
            scaled_r = r * self.zoom_factor
            painter.setBrush(QBrush(QColor(242, 137, 39)))
            painter.drawEllipse(scaled_x, scaled_y, scaled_r, scaled_r)

        painter.setPen(QPen(QColor(242, 39, 63), 3))
        for line in self.route_segments:
            x1, y1, x2, y2 = line
            scaled_x1 = x1 * self.zoom_factor + self.offset.x()
            scaled_y1 = y1 * self.zoom_factor + self.offset.y()
            scaled_x2 = x2 * self.zoom_factor + self.offset.x()
            scaled_y2 = y2 * self.zoom_factor + self.offset.y()
            painter.drawLine(scaled_x1, scaled_y1, scaled_x2, scaled_y2)

        painter.end()

    def resizeEvent(self, event):
        AFK.action()
        # input
        self.input_field.setGeometry(60, 7, self.width() - 60 * 2, 50)
        # find
        self.find_btn.setGeometry(self.width() - 57, 7, 50, 50)
        # time
        self.time_label.setGeometry(7, self.height() - 27, 65, 25)
        # name
        self.name_label.setGeometry(self.width() - (self.str_name_len + 7), self.height() - 27, self.str_name_len, 25)
        # frame
        if self.info_frame.isVisible():
            self.resize_frame()
        else:
            self.floors_frame.setGeometry(7, self.height() - 30 - 50 * Data.get_floors_num(), 50,
                                          50 * Data.get_floors_num())

    def wheelEvent(self, event):
        AFK.action()
        # frame
        if self.floors_frame.underMouse():
            return
        if self.info_frame.underMouse():
            return
        # map
        delta = event.angleDelta().y() / 120
        zoom_step = 0.9

        if delta > 0:
            self.zoom_factor += zoom_step
        else:
            self.zoom_factor -= zoom_step
        if self.zoom_factor < zoom_step:
            self.zoom_factor = zoom_step

        self.update()

    def mousePressEvent(self, event):
        AFK.action()
        if event.button() == Qt.LeftButton:
            # floor buttons action
            if self.floors_frame.underMouse():
                for b in self.floor_btns:
                    if b.underMouse():
                        Log().send(Log.LogType.INFO, "Button FLOOR_" + b.text() + "_BTN was pressed")
                        self.set_floor(b.text())
                        continue
            # set origin point
            self.origin = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        AFK.action()
        if event.buttons() & Qt.LeftButton:
            delta = event.globalPosition().toPoint() - self.origin
            # frame
            if self.floors_frame.underMouse():
                return
            if self.info_frame.underMouse():
                self.frame_scroll_area.verticalScrollBar().setValue(
                    self.frame_scroll_area.verticalScrollBar().value() - delta.y() // 10)
                return
            # map
            self.offset += delta
            self.origin = event.globalPosition().toPoint()
            # update
            self.update()
