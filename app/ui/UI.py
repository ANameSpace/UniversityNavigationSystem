import os.path

from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtGui import QPainter, QBrush, QFont, QColor, QPen
from PySide6.QtWidgets import QMainWindow, QPushButton, QLineEdit, QLabel, QFrame, QScrollArea, QVBoxLayout, QWidget, QGridLayout
from PySide6.QtCore import Qt, QTime, QSize, QTimer, QPoint

from app.utils.Navigation import Navigation
from app.utils.tools.Log import Log
from app.utils.Data import Data

from app.ui.utils.AfkUtil import AfkUtil


class UI(QMainWindow):
    def __init__(self, str_name="None"):
        super().__init__()

        self.afk_util = AfkUtil()
        self.data = Data()
        self.navigator = Navigation()

        # temp
        self.origin = None
        self.task_num = 0
        self.floor_btns = []

        # zoom
        self.zoom_factor = 10.0
        self.offset = QtCore.QPoint(60, 60)

        # navigation
        self.current_floor = self.data.get_default_floor()
        self.has_result = False
        self.route_ladders = []
        self.route_segments = []

        # window
        self.setWindowTitle(str_name)
        self.setStyleSheet("background-color: rgb(240, 240, 240);")
        self.setGeometry(100, 100, 300, 500)
        self.setMinimumSize(800, 370 + self.data.get_floors_count() * 50)
        self.img = QtGui.QPixmap("./resources/icons/icon.png")
        if self.img.isNull():
            Log().send(Log.LogType.ERROR, "Failed to load ./resources/icons/icon.png")
            self.img = QtGui.QPixmap(os.path.join(os.getcwd(), "UniversityNavigationSystem","resources","icons","icon.png"))
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
        self.completer = QtWidgets.QCompleter(self.data.get_rooms_names())
        self.completer.popup().setStyleSheet("font-size: 16px;")
        self.input_field.setCompleter(self.completer)

        # clear button
        self.clear_btn = QPushButton(self)
        self.clear_btn.setEnabled(False)
        self.clear_btn.setGeometry(7, 7, 50, 50)
        self.clear_btn.setStyleSheet("background-color: rgb(235, 35, 48); border-radius: 10px;")
        self.img = QtGui.QPixmap("resources\icons\close.png")
        # print(os.path.join(os.getcwd(), "resources", "icons", "close.png"))
        if self.img.isNull():
            Log().send(Log.LogType.ERROR, "Failed to load ./resources/icons/close.png")
            self.img = QtGui.QPixmap(os.path.join(os.getcwd(), "UniversityNavigationSystem","resources","icons","close.png"))
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
            self.img = QtGui.QPixmap(os.path.join(os.getcwd(), "UniversityNavigationSystem","resources","icons","find.png"))
        self.find_btn.setIcon(self.img)
        self.find_btn.setIconSize(QSize(36, 36))
        self.find_btn.clicked.connect(lambda: self.use(False))
        self.find_btn.clicked.connect(lambda: Log().send(Log.LogType.INFO, "Button FIND_BTN was pressed"))

        # floors frame
        self.floors_frame = QFrame(self)
        self.floors_frame.setStyleSheet("background-color: white; border-radius: 10px; border: 2px solid black;")
        self.floors_frame.setGeometry(7, self.height() - 30 - 50 * self.data.get_floors_count(), 50, 50 * self.data.get_floors_count())
        self.floors_layout = QGridLayout(self.floors_frame)
        row = 0
        for name in self.data.get_floors():
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
        self.str_name_len = self.name_label.fontMetrics().boundingRect(self.name_label.text()).width() + 15
        self.name_label.setGeometry(self.width() - self.str_name_len, 7, self.str_name_len, 25)

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
        self.frame_scroll_area.setFont(QFont("Arial", 32))
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
        self.frame_scroll_widget.setStyleSheet("border: 0px; border-radius: 0px;")

    # Tasks
    def task_executor(self):
        # update time
        self.time_label.setText(QTime.currentTime().toString(" hh:mm"))
        if self.task_num == 0:
            if self.afk_util.check_new_changes():
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
            self.afk_util.action()
            self.name_label.setVisible(False)
            self.input_field.setEnabled(False)

            dl = self.frame_scroll_widget.layout()
            #self.clearLayout(dl)

            self.has_result = self.data.is_valid_name(self.input_field.text())
            self.find_btn.setEnabled(False)
            self.clear_btn.setEnabled(True)
            self.info_frame.setVisible(True)
            self.resize_frame()
            if self.has_result:
                # TODO

                trobject = self.data.get_rooms_by_name(self.input_field.text())

                tm = list(self.navigator.run(self.input_field.text(), trobject.getflor()))
                Log().send(Log.LogType.INFO, "Routed segments " + str(tm))
                self.route_ladders = []
                self.route_segments = []
                for zi in tm:
                    if zi == "f1" or zi == "f2":
                        continue
                    try:
                        lol = int(zi)
                    except:
                        self.route_segments.append(self.data.get_lines_by_name(zi))
                Log().send(Log.LogType.INFO, "Routed segments2 " + str(self.route_segments))

                if trobject.getflor() == "2":
                    self.route_ladders.append("1")

                vbox = QVBoxLayout()
                self.frame_error_label.setVisible(False)
                self.frame_scroll_area.setVisible(True)

                object = QLabel("МАРШРУТ (Терминал -> " + self.input_field.text() + ")")
                object.setFont(QFont("Arial", 16, weight=QFont.Bold))
                vbox.addWidget(object)
                object = QLabel("Длительность " + str(1 + int(((len(tm) - 2))/ 2)) + " мин.")
                object.setFont(QFont("Arial", 15))
                vbox.addWidget(object)
                vbox.addWidget(QLabel(" "))

                if len(self.route_ladders) == 1:
                    object = QLabel("- Пройдите влево и начните подниматься по лестнице")
                    object.setFont(QFont("Arial", 16))
                    vbox.addWidget(object)

                    self.img = QtGui.QPixmap(self.data.get_patch_to_image("ladder1.png"))
                    if self.img.isNull():
                        Log().send(Log.LogType.ERROR, "Failed to load navigation image!")
                    else:
                        object = QLabel()
                        object.setPixmap(self.img)
                        vbox.addWidget(object)
                    vbox.addWidget(QLabel(" "))

                    object = QLabel("- Поднимиться по лестнице на второй этаж")
                    object.setFont(QFont("Arial", 16))
                    vbox.addWidget(object)

                    self.img = QtGui.QPixmap(self.data.get_patch_to_image("ladder2.png"))
                    if self.img.isNull():
                        Log().send(Log.LogType.ERROR, "Failed to load navigation image!")
                    else:
                        object = QLabel()
                        object.setPixmap(self.img)
                        vbox.addWidget(object)
                    vbox.addWidget(QLabel(" "))

                for ri in self.route_segments:
                    object = QLabel("- " + ri.getText())
                    object.setFont(QFont("Arial", 16))
                    vbox.addWidget(object)

                    self.img = QtGui.QPixmap(ri.getImg())
                    if self.img.isNull():
                        Log().send(Log.LogType.ERROR, "Failed to load navigation image!")
                    else:
                        object = QLabel()
                        object.setPixmap(self.img)
                        vbox.addWidget(object)
                    vbox.addWidget(QLabel(" "))

                object = QLabel("- " + trobject.getText())
                object.setFont(QFont("Arial", 16))
                vbox.addWidget(object)

                vbox.addWidget(trobject.getImgL())
                vbox.addWidget(QLabel(" "))

                object = QLabel("ВЫ ПРИБЫЛИ В ПУНКТ НАЗНАЧЕНИЯ")
                object.setFont(QFont("Arial", 16, weight=QFont.Bold))
                vbox.addWidget(object)

                self.frame_scroll_widget.setLayout(vbox)
                self.frame_scroll_area.setWidget(self.frame_scroll_widget)
                del vbox
            else:
                self.frame_error_label.setVisible(True)
                self.frame_scroll_area.setVisible(False)
        self.resize_frame()
        self.update()

    def afk_close(self):
        self.input_field.clear()
        self.set_floor(Data().get_default_floor())
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
            self.floors_frame.setGeometry(7, self.height() - 30 - 50 * Data().get_floors_count(), 50,
                                          50 * Data().get_floors_count())
        else:
            # info
            self.info_frame.setGeometry(10, self.height() // 2, self.width() - 20, self.height() // 2)
            self.time_label.setVisible(False)
            # floors
            self.floors_frame.setGeometry(7, self.height() - self.height() // 2 - 50 * Data().get_floors_count(), 50,
                                          50 * Data().get_floors_count())
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
        painter.setFont(QFont("Arial", int(1 * self.zoom_factor)))

        for wall in self.data.get_walls(self.current_floor):
            x1, y1, x2, y2 = wall.getLocation()
            scaled_x1 = x1 * self.zoom_factor + self.offset.x()
            scaled_y1 = y1 * self.zoom_factor + self.offset.y()
            scaled_x2 = x2 * self.zoom_factor + self.offset.x()
            scaled_y2 = y2 * self.zoom_factor + self.offset.y()
            painter.drawLine(scaled_x1, scaled_y1, scaled_x2, scaled_y2)
        painter.setPen(QPen(QColor(0, 0, 0), 1))

        for empty_rooms in self.data.get_empty_rooms(self.current_floor):
            x, y, width, height = empty_rooms.getLocation()
            scaled_x = x * self.zoom_factor + self.offset.x()
            scaled_y = y * self.zoom_factor + self.offset.y()
            scaled_width = width * self.zoom_factor
            scaled_height = height * self.zoom_factor
            painter.setBrush(QBrush(QColor(41, 41, 41)))
            painter.drawRect(scaled_x, scaled_y, scaled_width, scaled_height)

        for ladder in self.data.get_ladders(self.current_floor):
            x, y, width, height = ladder.getLocation()
            scaled_x = x * self.zoom_factor + self.offset.x()
            scaled_y = y * self.zoom_factor + self.offset.y()
            scaled_width = width * self.zoom_factor
            scaled_height = height * self.zoom_factor
            if self.has_result:
                if str(ladder.getName()) == "1" and len(self.route_ladders) == 1:
                    painter.setBrush(QBrush(QColor(238, 255, 46)))
                else:
                    painter.setBrush(QBrush(QColor(183, 194, 64)))
            else:
                painter.setBrush(QBrush(QColor(194, 207, 58)))
            painter.drawRect(scaled_x, scaled_y, scaled_width, scaled_height)

        for room in self.data.get_rooms(self.current_floor):
            x, y, width, height = room.getLocation()
            scaled_x = x * self.zoom_factor + self.offset.x()
            scaled_y = y * self.zoom_factor + self.offset.y()
            scaled_width = width * self.zoom_factor
            scaled_height = height * self.zoom_factor
            if self.has_result:
                if self.input_field.text() == room.getName():
                    painter.setBrush(QBrush(QColor(59, 196, 57)))
                else:
                    painter.setBrush(QBrush(QColor(0, 127, 70)))
            else:
                painter.setBrush(QBrush(QColor(62, 127, 201)))
            painter.drawRect(scaled_x, scaled_y, scaled_width, scaled_height)

            painter.setPen(QPen(QColor(255, 255, 255), 3))
            rn = room.getName()
            painter.drawText(QPoint(scaled_x + (scaled_width / 2) - 10, scaled_y + (scaled_height / 2) + 10), rn)
            painter.setPen(QPen(QColor(0, 0, 0), 2))


        if str(self.current_floor) == str(self.data.get_default_floor()):
            point_id, r, x, y = self.data.get_you_pos()
            scaled_x = x * self.zoom_factor + self.offset.x()
            scaled_y = y * self.zoom_factor + self.offset.y()
            scaled_r = r * self.zoom_factor
            painter.setBrush(QBrush(QColor(242, 137, 39)))
            painter.drawEllipse(scaled_x, scaled_y, scaled_r, scaled_r)
            painter.setPen(QPen(QColor(0, 0, 0), 2))

        if self.has_result:
            painter.setPen(QPen(QColor(0, 148, 255), 5))

            if len(self.route_ladders) == 1 and self.current_floor == "1":
                x1, y1, x2, y2 = 22, 40, 19, 38
                scaled_x1 = x1 * self.zoom_factor + self.offset.x()
                scaled_y1 = y1 * self.zoom_factor + self.offset.y()
                scaled_x2 = x2 * self.zoom_factor + self.offset.x()
                scaled_y2 = y2 * self.zoom_factor + self.offset.y()
                painter.drawLine(scaled_x1, scaled_y1, scaled_x2, scaled_y2)

            for line in self.route_segments:
                if self.current_floor == self.data.get_rooms_by_name(self.input_field.text()).getflor():
                    x1, y1, x2, y2 = line.getLocation()
                    scaled_x1 = x1 * self.zoom_factor + self.offset.x()
                    scaled_y1 = y1 * self.zoom_factor + self.offset.y()
                    scaled_x2 = x2 * self.zoom_factor + self.offset.x()
                    scaled_y2 = y2 * self.zoom_factor + self.offset.y()
                    painter.drawLine(scaled_x1, scaled_y1, scaled_x2, scaled_y2)

        painter.end()

    def resizeEvent(self, event):
        self.afk_util.action()
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
            self.floors_frame.setGeometry(7, self.height() - 30 - 50 * self.data.get_floors_count(), 50,
                                          50 * self.data.get_floors_count())

    def wheelEvent(self, event):
        self.afk_util.action()
        # frame
        if self.floors_frame.underMouse():
            return
        if self.info_frame.underMouse():
            return
        # map
        delta = event.angleDelta().y() / 120
        zoom_step = 0.9

        if self.zoom_factor < 5.0:
            if delta == -1.0:
                return
        if self.zoom_factor > 50.0:
            if delta == 1.0:
                return

        if delta > 0:
            self.zoom_factor += zoom_step
        else:
            self.zoom_factor -= zoom_step

        if self.zoom_factor < zoom_step:
            self.zoom_factor = zoom_step

        self.update()

    def mousePressEvent(self, event):
        self.afk_util.action()
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
        self.afk_util.action()
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

    def clearLayout(self, qqq):
        if qqq is not None:
            while qqq.count():
                item = qqq.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clearLayout(item.layout())