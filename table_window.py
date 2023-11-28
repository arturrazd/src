import json
import os
import time
import locale
from datetime import datetime
from PyQt5 import QtWidgets, QtCore, QtGui, QtPrintSupport
from PyQt5.QtCore import Qt, QSize, pyqtSignal
from PyQt5.QtGui import QFont, QColor, QKeySequence, QPixmap
from PyQt5.QtWidgets import *
from psycopg2 import connect

from data_base import DataBase
from styles import AlignDelegate, Styles

locale.setlocale(category=locale.LC_ALL, locale="Russian")


class TableWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.list_role = list()
        self.list_guild = list()
        self.dict_guilds = dict()
        self.list_teams = list()

        self.dict_month = self.get_list_dates()

        #   Читаем из БД настройки отображения панели для сменных работников с и без наряда.
        try:
            with connect(**DataBase.config(DataBase.login, DataBase.password)) as conn:
                with conn.cursor() as cursor:
                    #   Читаем из БД настройки отображения панели для сменных работников без наряда.
                    cursor.execute(DataBase.sql_read_settings(), ('panel_view_1',))
                    text_panel_view_1 = cursor.fetchall()
                    self.panel_view_1 = list(text_panel_view_1[0][0].replace(",", ""))  # Без наряда.
                    self.panel_view_1 = [int(x) for x in self.panel_view_1]  # Преобразуем в список из чисел.
                    cursor.execute(DataBase.sql_read_settings(), ('panel_view_2',))
                    text_panel_view_2 = cursor.fetchall()
                    self.panel_view_2 = list(text_panel_view_2[0][0].replace(",", ""))  # С нарядом.
                    self.panel_view_2 = [int(x) for x in self.panel_view_2]  # Преобразуем в список из чисел.
        except:
            pass

        self.main_btn_size = QSize(35, 35)
        self.input_btn_size = QSize(200, 30)
        self.middle_btn_size = QSize(95, 30)
        self.little_btn_size = QSize(45, 30)
        self.icon_size = QSize(15, 15)

        self.table_report = TableReport(self)
        self.table_report.setCursor(Qt.PointingHandCursor)

        self.shortcut = QShortcut(QKeySequence("Ctrl+C"), self)
        self.shortcut.activated.connect(self.table_report.copy_report)
        self.shortcut = QShortcut(QKeySequence("Ctrl+V"), self)
        self.shortcut.activated.connect(self.table_report.paste_report)
        self.shortcut = QShortcut(QKeySequence("Del"), self)
        self.shortcut.activated.connect(self.table_report.clear_report)

        self.create_btn_main()
        self.create_filter()

        self.page_layout = QHBoxLayout()
        self.page_layout.setContentsMargins(0, 0, 0, 0)

        self.panel_layout = QVBoxLayout()
        self.panel_layout.setContentsMargins(0, 0, 10, 0)

        self.edit_layout = QVBoxLayout()
        self.edit_layout.setContentsMargins(20, 10, 10, 0)

        self.panel_layout.addLayout(self.button_layout)
        self.panel_layout.addLayout(self.edit_layout)
        self.panel_layout.addStretch(0)
        self.panel_layout.addLayout(self.filter_layout)

        self.page_layout.addWidget(self.table_report)
        self.page_layout.addLayout(self.panel_layout)
        self.setLayout(self.page_layout)

        self.init_panel_types()

        self.table_report.cellClicked.connect(self.show_element_panel)
        self.table_report.cellClicked.connect(self.table_report.fill_panel)

        self.get_list_teams()

    def init_panel_types(self):
        #   Отработанные часы, статус дня.
        self.show_type_1 = [self.create_btn_edit_hours,
                            self.create_btn_input_hours_day,
                            self.create_btn_input_status
                            ]
        #   Отработанные часы, статус дня, тип сменны, площадка, оценка, комментарий, наряд, панель расписания.
        self.show_type_2 = [self.create_btn_edit_hours,
                            self.create_btn_input_hours_day_night,
                            self.create_btn_input_status,
                            self.create_btn_input_rating,
                            self.create_btn_open_description,
                            self.create_btn_generation_permit,
                            self.create_scheduler,
                            ]
        self.show_type_3 = [self.create_btn_edit_hours,
                            self.create_btn_input_hours_day_night,
                            self.create_btn_input_status,
                            self.create_btn_input_rating,
                            self.create_combo_teams,
                            self.create_btn_open_description,
                            self.create_btn_generation_permit,
                            self.create_scheduler,
                            ]

    def show_element_panel(self):
        if self.table_report.col > 2:
            self.clear_panel()
            elements_types = {
                #
                '1': self.show_type_1,
                '2': self.show_type_2,
                '3': self.show_type_3
            }
            element = self.table_report.reports_dict[self.table_report.id_worker][self.table_report.id_date][
                'props_type']

            [f() for f in elements_types[element]]

    def create_btn_main(self):
        # кнопка "обновить"
        self.btn_refresh = QPushButton('', self)
        self.btn_refresh.setIcon(QtGui.QIcon('refresh.png'))
        self.btn_refresh.setIconSize(self.icon_size)
        self.btn_refresh.setFixedSize(self.main_btn_size)
        self.btn_refresh.setStyleSheet(Styles.workers_btn())
        self.btn_refresh.clicked.connect(self.table_report.bild_table)
        self.btn_refresh.setCursor(Qt.PointingHandCursor)

        # кнопка "копировать"
        self.btn_copy = QPushButton('', self)
        self.btn_copy.setIcon(QtGui.QIcon('copy_report.png'))
        self.btn_copy.setIconSize(self.icon_size)
        self.btn_copy.setFixedSize(self.main_btn_size)
        self.btn_copy.setStyleSheet(Styles.workers_btn())
        self.btn_copy.clicked.connect(self.table_report.copy_report)
        self.btn_copy.setCursor(Qt.PointingHandCursor)

        # кнопка "вставить"
        self.btn_paste = QPushButton('', self)
        self.btn_paste.setIcon(QtGui.QIcon('paste_report.png'))
        self.btn_paste.setIconSize(self.icon_size)
        self.btn_paste.setFixedSize(self.main_btn_size)
        self.btn_paste.setStyleSheet(Styles.workers_btn())
        self.btn_paste.clicked.connect(self.table_report.paste_report)
        self.btn_paste.setCursor(Qt.PointingHandCursor)

        # кнопка "очистить"
        self.btn_clear = QPushButton('', self)
        self.btn_clear.setIcon(QtGui.QIcon('delete_report.png'))
        self.btn_clear.setIconSize(self.icon_size)
        self.btn_clear.setFixedSize(self.main_btn_size)
        self.btn_clear.setStyleSheet(Styles.workers_btn())
        self.btn_clear.clicked.connect(self.table_report.clear_report)
        self.btn_clear.setCursor(Qt.PointingHandCursor)

        self.button_layout = QHBoxLayout()
        self.button_layout.setContentsMargins(20, 0, 10, 0)
        self.button_layout.addWidget(self.btn_refresh)
        self.button_layout.addWidget(self.btn_copy)
        self.button_layout.addWidget(self.btn_paste)
        self.button_layout.addWidget(self.btn_clear)
        self.button_layout.setSpacing(20)

    def create_filter(self):

        # надпись "фильтр табеля"
        lbl_filter = QLabel('фильтр')
        lbl_filter.setFont(QFont("CalibriLight", 10, QtGui.QFont.Normal))
        lbl_filter.setStyleSheet('color: rgb(220, 220, 220);')
        lbl_filter.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # кнопка "очистить фильтр"
        btn_clear_filter = QPushButton('очистить', self)
        btn_clear_filter.setIconSize(self.icon_size)
        btn_clear_filter.setFixedSize(self.input_btn_size)
        btn_clear_filter.setStyleSheet(Styles.workers_btn())
        btn_clear_filter.clicked.connect(self.clear_filter)
        btn_clear_filter.setCursor(Qt.PointingHandCursor)

        # фильтр по должности
        self.combo_role = QComboBox(self, objectName='combo_role')
        self.combo_role.addItems(['должность'] + self.get_list_role())
        self.combo_role.setCurrentText(self.table_report.filter_role[1:-1])
        self.combo_role.setFixedSize(self.input_btn_size)
        self.combo_role.setStyleSheet(Styles.workers_combo())
        self.combo_role.activated.connect(self.table_report.get_change_list_guild)
        self.combo_role.activated.connect(self.table_report.set_filter_table)
        self.combo_role.activated.connect(self.table_report.check_table)
        self.combo_role.setCursor(Qt.PointingHandCursor)

        # фильтр по отделу/цеху
        self.combo_guild = QComboBox(self, objectName='combo_guild')
        self.get_list_guild()
        self.table_report.get_change_list_guild()
        self.combo_guild.setCurrentText(self.table_report.filter_guild[1:-1])
        self.combo_guild.setFixedSize(self.input_btn_size)
        self.combo_guild.setStyleSheet(Styles.workers_combo())
        self.combo_guild.activated.connect(self.table_report.set_filter_table)
        self.combo_guild.activated.connect(self.table_report.check_table)
        self.combo_guild.setCursor(Qt.PointingHandCursor)

        # фильтр по году
        self.combo_years = QComboBox(self, objectName='combo_years')
        self.list_years = list(self.get_list_dates().keys())
        self.combo_years.addItems(self.list_years)
        self.combo_years.setCurrentText(str(datetime.now().date().year))
        self.combo_years.setFixedSize(self.input_btn_size)
        self.combo_years.setStyleSheet(Styles.workers_combo())
        self.combo_years.activated.connect(self.change_list_month)
        self.combo_years.activated.connect(self.table_report.set_filter_table)
        self.combo_years.activated.connect(self.table_report.bild_table)
        self.combo_years.setCursor(Qt.PointingHandCursor)

        # фильтр по месяцу
        self.combo_month = QComboBox(self, objectName='combo_month')
        self.list_month = list(self.dict_month[self.combo_years.currentText()].values())
        self.combo_month.addItems(self.list_month)
        current_month = datetime.strptime(str(datetime.now().date()), "%Y-%m-%d").strftime("%B")
        self.combo_month.setCurrentText(current_month)
        self.combo_month.setFixedSize(self.input_btn_size)
        self.combo_month.setStyleSheet(Styles.workers_combo())
        self.combo_month.activated.connect(self.table_report.set_filter_table)
        self.combo_month.activated.connect(self.table_report.bild_table)
        self.combo_month.setCursor(Qt.PointingHandCursor)

        self.filter_layout = QGridLayout()
        self.filter_layout.setContentsMargins(20, 0, 10, 20)
        self.filter_layout.addWidget(lbl_filter, 1, Qt.AlignCenter)
        self.filter_layout.addWidget(self.combo_years, 2, Qt.AlignCenter)
        self.filter_layout.addWidget(self.combo_month, 3, Qt.AlignCenter)
        self.filter_layout.addWidget(self.combo_role, 4, Qt.AlignCenter)
        self.filter_layout.addWidget(self.combo_guild, 5, Qt.AlignCenter)
        self.filter_layout.addWidget(btn_clear_filter, 6, Qt.AlignCenter)

    def create_btn_edit_hours(self):
        # отработанные часы
        self.edit_layout_btn_edit_hours = QGridLayout()
        self.edit_layout_btn_edit_hours.setObjectName('edit_layout_btn_edit_hours')
        self.edit_layout_btn_edit_hours.setContentsMargins(0, 0, 0, 0)

        lbl_work_day = QLabel('настройки дня')
        lbl_work_day.setFont(QFont("CalibriLight", 10, QtGui.QFont.Normal))
        lbl_work_day.setStyleSheet('color: rgb(220, 220, 220);')
        lbl_work_day.setAlignment(Qt.AlignmentFlag.AlignCenter)

        btn_hour_plus = QPushButton('+', self, objectName='btn_hour_plus')
        btn_hour_plus.setFixedSize(self.little_btn_size)
        btn_hour_plus.setStyleSheet(Styles.workers_btn())
        btn_hour_plus.clicked.connect(lambda: self.change_worker_hours((
            (self.table_report.reports_dict[self.table_report.id_worker][self.table_report.id_date]['hour'] + 1),
            self.table_report.reports_dict[self.table_report.id_worker][self.table_report.id_date]['hour'])
            [self.table_report.reports_dict[self.table_report.id_worker][self.table_report.id_date]['hour'] > 23],
            self.table_report.reports_dict[self.table_report.id_worker][self.table_report.id_date]['place'],
            self.table_report.reports_dict[self.table_report.id_worker][self.table_report.id_date]['time_of_day']))
        btn_hour_plus.setCursor(Qt.PointingHandCursor)
        btn_hour_plus.setContentsMargins(0, 0, 0, 0)

        self.lbl_hour = QLabel(str(self.table_report.reports_dict[self.table_report.id_worker][self.table_report.id_date]['hour']))
        self.lbl_hour.objectName = 'lbl_hour'
        self.lbl_hour.setFixedSize(self.little_btn_size)
        self.lbl_hour.setFont(QFont("CalibriLight", 10, QtGui.QFont.Bold))
        self.lbl_hour.setStyleSheet('color: rgb(255, 255, 100);')
        self.lbl_hour.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.lbl_hour.setContentsMargins(0, 0, 0, 0)

        btn_hour_minus = QPushButton('-', self, objectName='btn_hour_minus')
        btn_hour_minus.setFixedSize(self.little_btn_size)
        btn_hour_minus.setStyleSheet(Styles.workers_btn())
        btn_hour_minus.clicked.connect(lambda: self.change_worker_hours((
            (self.table_report.reports_dict[self.table_report.id_worker][self.table_report.id_date]['hour'] - 1),
            self.table_report.reports_dict[self.table_report.id_worker][self.table_report.id_date]['hour'])
            [self.table_report.reports_dict[self.table_report.id_worker][self.table_report.id_date]['hour'] < 1],
            self.table_report.reports_dict[self.table_report.id_worker][self.table_report.id_date]['place'],
            self.table_report.reports_dict[self.table_report.id_worker][self.table_report.id_date]['time_of_day']))
        btn_hour_minus.setCursor(Qt.PointingHandCursor)
        btn_hour_minus.setContentsMargins(0, 0, 0, 0)

        self.edit_layout_btn_edit_hours.addWidget(lbl_work_day, 1, 1, 1, 3, Qt.AlignCenter)
        self.edit_layout_btn_edit_hours.addWidget(btn_hour_minus, 2, 1, Qt.AlignLeft)
        self.edit_layout_btn_edit_hours.addWidget(self.lbl_hour, 2, 2, Qt.AlignCenter)
        self.edit_layout_btn_edit_hours.addWidget(btn_hour_plus, 2, 3, Qt.AlignRight)

        self.edit_layout.addLayout(self.edit_layout_btn_edit_hours)

    def create_btn_input_hours_day_night(self):
        self.edit_layout_btn_hours = QGridLayout()
        self.edit_layout_btn_hours.setObjectName('edit_layout_btn_hours')
        self.edit_layout_btn_hours.setContentsMargins(0, 0, 0, 0)

        btn_day_nuf = QPushButton('НУФ(Д)', self, objectName='btn_day_nuf')
        btn_day_nuf.setFixedSize(self.little_btn_size)
        btn_day_nuf.setStyleSheet(Styles.workers_btn())
        btn_day_nuf.clicked.connect(lambda: self.change_worker_hours(11, 0, 1))
        btn_day_nuf.setToolTip('НУФ - день')
        btn_day_nuf.setCursor(Qt.PointingHandCursor)

        btn_night_nuf = QPushButton('НУФ(Н)', self, objectName='btn_night_nuf')
        btn_night_nuf.setFixedSize(self.little_btn_size)
        btn_night_nuf.setStyleSheet(Styles.workers_btn())
        btn_night_nuf.clicked.connect(lambda: self.change_worker_hours(13, 0, 2))
        btn_night_nuf.setToolTip('НУФ - ночь')
        btn_night_nuf.setCursor(Qt.PointingHandCursor)

        btn_day_chap = QPushButton('ЧАП(Д)', self, objectName='btn_day_chap')
        btn_day_chap.setFixedSize(self.little_btn_size)
        btn_day_chap.setStyleSheet(Styles.workers_btn())
        btn_day_chap.clicked.connect(lambda: self.change_worker_hours(11, 1, 1))
        btn_day_chap.setToolTip('ЧАП - день')
        btn_day_chap.setCursor(Qt.PointingHandCursor)

        btn_night_chap = QPushButton('ЧАП(Н)', self, objectName='btn_night_chap')
        btn_night_chap.setFixedSize(self.little_btn_size)
        btn_night_chap.setStyleSheet(Styles.workers_btn())
        btn_night_chap.clicked.connect(lambda: self.change_worker_hours(13, 1, 2))
        btn_night_chap.setToolTip('ЧАП - ночь')
        btn_night_chap.setCursor(Qt.PointingHandCursor)

        self.edit_layout_btn_hours.addWidget(btn_day_nuf, 1, 1, Qt.AlignCenter)
        self.edit_layout_btn_hours.addWidget(btn_night_nuf, 1, 2, Qt.AlignCenter)
        self.edit_layout_btn_hours.addWidget(btn_day_chap, 1, 3, Qt.AlignCenter)
        self.edit_layout_btn_hours.addWidget(btn_night_chap, 1, 4, Qt.AlignCenter)

        self.edit_layout.addLayout(self.edit_layout_btn_hours)

    def create_btn_input_hours_day(self):
        self.edit_layout_btn_hours = QGridLayout()
        self.edit_layout_btn_hours.setObjectName('edit_layout_btn_hours')
        self.edit_layout_btn_hours.setContentsMargins(0, 0, 0, 0)

        btn_day = QPushButton('8 ч.', self, objectName='btn_day')
        btn_day.setFixedSize(self.input_btn_size)
        btn_day.setStyleSheet(Styles.workers_btn())
        btn_day.clicked.connect(lambda: self.change_worker_hours(8, 0, 0))
        btn_day.setCursor(Qt.PointingHandCursor)

        self.edit_layout_btn_hours.addWidget(btn_day, 1, 1, Qt.AlignCenter)

        self.edit_layout.addLayout(self.edit_layout_btn_hours)

    def create_btn_input_status(self):
        self.edit_layout_btn_status = QGridLayout()
        self.edit_layout_btn_status.setObjectName('edit_layout_btn_status')
        self.edit_layout_btn_status.setContentsMargins(0, 0, 0, 0)

        btn_time_off = QPushButton('б/с', self, objectName='btn_time_off')
        btn_time_off.setFixedSize(self.little_btn_size)
        btn_time_off.setStyleSheet(Styles.workers_btn())
        btn_time_off.clicked.connect(lambda: self.change_worker_status(1))
        btn_time_off.setToolTip('б/с')
        btn_time_off.setCursor(Qt.PointingHandCursor)

        btn_vacation = QPushButton('отпуск', self, objectName='btn_vacation')
        btn_vacation.setFixedSize(self.little_btn_size)
        btn_vacation.setStyleSheet(Styles.workers_btn())
        btn_vacation.clicked.connect(lambda: self.change_worker_status(2))
        btn_vacation.setToolTip('отпуск')
        btn_vacation.setCursor(Qt.PointingHandCursor)

        btn_sick = QPushButton('бол.', self, objectName='btn_sick')
        btn_sick.setFixedSize(self.little_btn_size)
        btn_sick.setStyleSheet(Styles.workers_btn())
        btn_sick.clicked.connect(lambda: self.change_worker_status(3))
        btn_sick.setToolTip('больничный')
        btn_sick.setCursor(Qt.PointingHandCursor)

        btn_hooky = QPushButton('прогул', self, objectName='btn_hooky')
        btn_hooky.setFixedSize(self.little_btn_size)
        btn_hooky.setStyleSheet(Styles.workers_btn())
        btn_hooky.clicked.connect(lambda: self.change_worker_status(4))
        btn_hooky.setToolTip('прогул')
        btn_hooky.setCursor(Qt.PointingHandCursor)

        self.edit_layout_btn_status.addWidget(btn_time_off, 1, 1, Qt.AlignCenter)
        self.edit_layout_btn_status.addWidget(btn_vacation, 1, 2, Qt.AlignCenter)
        self.edit_layout_btn_status.addWidget(btn_sick, 1, 3, Qt.AlignCenter)
        self.edit_layout_btn_status.addWidget(btn_hooky, 1, 4, Qt.AlignCenter)

        self.edit_layout.addLayout(self.edit_layout_btn_status)

    def create_btn_input_rating(self):
        # оценка
        self.edit_layout_btn_rating = QGridLayout()
        self.edit_layout_btn_rating.setObjectName('edit_layout_btn_rating')
        self.edit_layout_btn_rating.setContentsMargins(0, 0, 0, 0)

        btn_one_point = QPushButton('1', self, objectName='btn_one_point')
        btn_one_point.setFixedSize(self.little_btn_size)
        btn_one_point.setStyleSheet(Styles.workers_btn())
        btn_one_point.clicked.connect(lambda: self.change_worker_rating(1))
        btn_one_point.setToolTip('1 балл')
        btn_one_point.setCursor(Qt.PointingHandCursor)

        btn_two_points = QPushButton('2', self, objectName='btn_two_points')
        btn_two_points.setFixedSize(self.little_btn_size)
        btn_two_points.setStyleSheet(Styles.workers_btn())
        btn_two_points.clicked.connect(lambda: self.change_worker_rating(2))
        btn_two_points.setToolTip('2 балла')
        btn_two_points.setCursor(Qt.PointingHandCursor)

        btn_three_points = QPushButton('3', self, objectName='btn_three_points')
        btn_three_points.setFixedSize(self.little_btn_size)
        btn_three_points.setStyleSheet(Styles.workers_btn())
        btn_three_points.clicked.connect(lambda: self.change_worker_rating(3))
        btn_three_points.setToolTip('3 балла')
        btn_three_points.setCursor(Qt.PointingHandCursor)

        self.edit_layout_btn_rating.addWidget(btn_one_point, 1, 1, Qt.AlignLeft)
        self.edit_layout_btn_rating.addWidget(btn_two_points, 1, 2, Qt.AlignCenter)
        self.edit_layout_btn_rating.addWidget(btn_three_points, 1, 3, Qt.AlignRight)

        self.edit_layout.addLayout(self.edit_layout_btn_rating)

    def create_combo_teams(self):
        # бригада
        self.combo_teams = QComboBox(self, objectName='combo_teams')
        self.combo_teams.setFixedSize(self.input_btn_size)
        self.combo_teams.addItems(self.list_teams)
        self.combo_teams.setStyleSheet(Styles.workers_combo())
        self.combo_teams.activated.connect(lambda: self.change_team(self.combo_teams.currentText()))
        self.combo_teams.setToolTip('бригада')
        self.combo_teams.setCursor(Qt.PointingHandCursor)

        self.edit_layout.addWidget(self.combo_teams)

    def create_btn_generation_permit(self):
        # кнопка "сгенерировать наряд"
        self.btn_generation_permit = QPushButton('наряд', self, objectName='btn_generation_permit')
        self.btn_generation_permit.setFixedSize(self.input_btn_size)
        self.btn_generation_permit.setStyleSheet(Styles.workers_btn())
        self.btn_generation_permit.clicked.connect(self.show_permit)
        self.edit_layout.addWidget(self.btn_generation_permit)
        self.btn_generation_permit.setToolTip('сгенерировать наряд')
        self.btn_generation_permit.setCursor(Qt.PointingHandCursor)

    def create_btn_open_description(self):
        # кнопка "записать примечание"
        self.btn_insert_description = QPushButton('примечание', self, objectName='btn_insert_description')
        self.btn_insert_description.setFixedSize(self.input_btn_size)
        self.btn_insert_description.setStyleSheet(Styles.workers_btn())
        self.btn_insert_description.clicked.connect(self.show_input_description)
        self.edit_layout.addWidget(self.btn_insert_description)
        self.btn_insert_description.setCursor(Qt.PointingHandCursor)

    def create_scheduler(self):

        self.edit_layout_scheduler = QGridLayout()
        self.edit_layout_scheduler.setObjectName('edit_layout_scheduler')
        self.edit_layout_scheduler.setContentsMargins(0, 10, 0, 0)

        lbl_scheduler = QLabel('расписание')
        lbl_scheduler.setFont(QFont("CalibriLight", 10, QtGui.QFont.Normal))
        lbl_scheduler.setStyleSheet('color: rgb(220, 220, 220);')
        lbl_scheduler.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.btn_scheduler_type1 = QPushButton('ДД-НН-ОВ', self, objectName='btn_scheduler_type1')
        self.btn_scheduler_type1.setFixedSize(self.middle_btn_size)
        self.btn_scheduler_type1.setStyleSheet(Styles.workers_btn())
        self.btn_scheduler_type1.clicked.connect(self.init_scheduler_type1)
        self.btn_scheduler_type1.setCursor(Qt.PointingHandCursor)
        self.btn_scheduler_type1.setContentsMargins(0, 0, 0, 0)

        self.btn_scheduler_type2 = QPushButton('ДН-ОВ', self, objectName='btn_scheduler_type1')
        self.btn_scheduler_type2.setFixedSize(self.middle_btn_size)
        self.btn_scheduler_type2.setStyleSheet(Styles.workers_btn())
        self.btn_scheduler_type2.clicked.connect(self.init_scheduler_type2)
        self.btn_scheduler_type2.setCursor(Qt.PointingHandCursor)
        self.btn_scheduler_type2.setContentsMargins(0, 0, 0, 0)

        btn_generate_scheduler = QPushButton('заполнить', self, objectName='btn_generate_scheduler')
        btn_generate_scheduler.setIconSize(self.icon_size)
        btn_generate_scheduler.setFixedSize(self.input_btn_size)
        btn_generate_scheduler.setStyleSheet(Styles.workers_btn())
        btn_generate_scheduler.clicked.connect(self.table_report.generate_schedules)
        btn_generate_scheduler.setToolTip('заполнить')
        btn_generate_scheduler.setCursor(Qt.PointingHandCursor)

        btn_clear_scheduler = QPushButton('очистить', self, objectName='btn_clear_scheduler')
        btn_clear_scheduler.setFixedSize(self.input_btn_size)
        btn_clear_scheduler.setStyleSheet(Styles.workers_btn())
        btn_clear_scheduler.setCursor(Qt.PointingHandCursor)
        btn_clear_scheduler.clicked.connect(self.table_report.clear_schedules)
        btn_clear_scheduler.setToolTip('очистить')
        btn_clear_scheduler.setCursor(Qt.PointingHandCursor)

        self.edit_layout_scheduler.addWidget(lbl_scheduler, 1, 1, 1, 2, Qt.AlignCenter)
        self.edit_layout_scheduler.addWidget(self.btn_scheduler_type1, 2, 1, Qt.AlignCenter)
        self.edit_layout_scheduler.addWidget(self.btn_scheduler_type2, 2, 2, Qt.AlignCenter)
        self.edit_layout_scheduler.addWidget(btn_generate_scheduler, 3, 1, 1, 2, Qt.AlignCenter)
        self.edit_layout_scheduler.addWidget(btn_clear_scheduler, 4, 1, 1, 2, Qt.AlignCenter)

        self.edit_layout.addLayout(self.edit_layout_scheduler)

        self.init_scheduler_type1()

    def change_worker_hours(self, h, p, tod):
        self.table_report.copy_report()
        rat = self.table_report.buff_copy_rating
        stat = self.table_report.buff_copy_status
        des = self.table_report.buff_copy_description
        team = self.table_report.buff_copy_team
        self.table_report.write_report(h, rat, stat, p, tod, des, self.table_report.id_worker, self.table_report.id_date, team)
        self.table_report.check_table()
        self.table_report.fill_panel()

    def change_worker_status(self, stat):
        self.table_report.copy_report()
        h = self.table_report.buff_copy_hours
        rat = self.table_report.buff_copy_rating
        p = self.table_report.buff_copy_place
        tod = self.table_report.buff_copy_time_of_day
        des = self.table_report.buff_copy_description
        team = self.table_report.buff_copy_team
        self.table_report.write_report(h, rat, stat, p, tod, des, self.table_report.id_worker, self.table_report.id_date, team)
        self.table_report.check_table()
        self.table_report.fill_panel()

    def change_worker_rating(self, rat):
        self.table_report.copy_report()
        h = self.table_report.buff_copy_hours
        stat = self.table_report.buff_copy_status
        p = self.table_report.buff_copy_place
        tod = self.table_report.buff_copy_time_of_day
        des = self.table_report.buff_copy_description
        team = self.table_report.buff_copy_team
        self.table_report.write_report(h, rat, stat, p, tod, des, self.table_report.id_worker, self.table_report.id_date, team)
        self.table_report.check_table()
        self.table_report.fill_panel()

    def change_worker_description(self, des):
        self.table_report.copy_report()
        h = self.table_report.buff_copy_hours
        rat = self.table_report.buff_copy_rating
        stat = self.table_report.buff_copy_status
        p = self.table_report.buff_copy_place
        tod = self.table_report.buff_copy_time_of_day
        team = self.table_report.buff_copy_team
        self.table_report.write_report(h, rat, stat, p, tod, des, self.table_report.id_worker, self.table_report.id_date, team)
        self.table_report.check_table()
        self.table_report.fill_panel()

    def change_team(self, team):
        self.table_report.copy_report()
        h = self.table_report.buff_copy_hours
        rat = self.table_report.buff_copy_rating
        stat = self.table_report.buff_copy_status
        p = self.table_report.buff_copy_place
        tod = self.table_report.buff_copy_time_of_day
        des = self.table_report.buff_copy_description
        team = (team.split(":")[0], 0)[self.combo_teams.currentIndex() == 0]
        self.table_report.write_report(h, rat, stat, p, tod, des, self.table_report.id_worker, self.table_report.id_date, team)
        self.table_report.check_table()
        self.table_report.fill_panel()

    def init_scheduler_type1(self):
        self.table_report.type_scheduler = 0
        self.btn_scheduler_type1.setDown(True)
        self.btn_scheduler_type2.setDown(False)

    def init_scheduler_type2(self):
        self.table_report.type_scheduler = 1
        self.btn_scheduler_type1.setDown(False)
        self.btn_scheduler_type2.setDown(True)

    def clear_panel(self):

        if self.findChild(QGridLayout, name='edit_layout_btn_edit_hours') is not None:
            for i in reversed(range(self.edit_layout_btn_edit_hours.count())):
                self.edit_layout_btn_edit_hours.itemAt(i).widget().setParent(None)
            self.edit_layout_btn_edit_hours.setParent(None)

        if self.findChild(QGridLayout, name='edit_layout_btn_hours') is not None:
            for i in reversed(range(self.edit_layout_btn_hours.count())):
                self.edit_layout_btn_hours.itemAt(i).widget().setParent(None)
            self.edit_layout_btn_hours.setParent(None)

        if self.findChild(QGridLayout, name='edit_layout_btn_status') is not None:
            for i in reversed(range(self.edit_layout_btn_status.count())):
                self.edit_layout_btn_status.itemAt(i).widget().setParent(None)
            self.edit_layout_btn_status.setParent(None)

        if self.findChild(QGridLayout, name='edit_layout_btn_rating') is not None:
            for i in reversed(range(self.edit_layout_btn_rating.count())):
                self.edit_layout_btn_rating.itemAt(i).widget().setParent(None)
            self.edit_layout_btn_rating.setParent(None)

        if self.findChild(QGridLayout, name='edit_layout_scheduler') is not None:
            for i in reversed(range(self.edit_layout_scheduler.count())):
                self.edit_layout_scheduler.itemAt(i).widget().setParent(None)
            self.edit_layout_scheduler.setParent(None)

        for i in range(self.edit_layout.layout().count()):
            widget = self.edit_layout.layout().itemAt(i).widget()
            widget.deleteLater()

    def get_list_role(self):
        try:
            with connect(**DataBase.config(DataBase.login, DataBase.password)) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(DataBase.sql_list_role())
                    self.list_role = cursor.fetchall()
                    combo_list_role = [role[1] for role in self.list_role]
                    return combo_list_role
        except:
            pass

    def get_list_guild(self):
        try:
            with connect(**DataBase.config(DataBase.login, DataBase.password)) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(DataBase.sql_list_guild())
                    self.list_guild = cursor.fetchall()
                    for role in self.list_role:
                        self.dict_guilds[role[1]] = []
                        for guild in self.list_guild:
                            if role[0] == guild[2]:
                                self.dict_guilds[role[1]].append(guild[1])
        except:
            pass

    def get_list_dates(self):
        try:
            with connect(**DataBase.config(DataBase.login, DataBase.password)) as conn:
                with conn.cursor() as cursor:
                    all_date_dict = dict()
                    cursor.execute(DataBase.sql_list_all_date())
                    date_list = cursor.fetchall()
                    year = 0
                    for date in date_list:
                        if year != date[0]:
                            all_date_dict[str(date[0])] = dict()
                            year = date[0]
                        all_date_dict[str(date[0])][str(date[1])] = str(date[2]).lower()
                    return all_date_dict
        except:
            pass

    def get_list_teams(self):
        try:
            with connect(**DataBase.config(DataBase.login, DataBase.password)) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(DataBase.sql_list_teams())
                    list_teams_tmp = cursor.fetchall()
                    self.list_teams = [str(team[1]) + ': ' + team[2] for team in list_teams_tmp]
                    self.list_teams[0] = 'бригада'
        except:
            pass

    def change_list_month(self):
        self.combo_month.clear()
        self.list_month = list(self.get_list_dates()[self.combo_years.currentText()].values())
        self.combo_month.addItems(self.list_month)

    def clear_filter(self):
        self.combo_years.setCurrentText(str(datetime.now().date().year))
        self.combo_month.setCurrentText(str(datetime.now().date().month))
        self.combo_role.setCurrentText('должность')
        self.combo_guild.setCurrentText('специальность')
        self.table_report.set_filter_table()
        self.table_report.check_table()

    def show_permit(self, role):

        p_manager = ' ' + self.get_settings('permit_manager_electric')[0][0]
        p_producer = ' ' + self.get_settings('permit_producer_electric')[0][0]

        #   Определяем дату в наряде в соответствии с выделенной ячейкой.
        #   "Id_date" текущей ячейки обновляется каждый раз по клику мыши в click_table.
        for date in self.table_report.dates:  # Перебираем строки дат в текущем месяце.
            if self.table_report.id_date in date:  # Ищем id_date в dates.
                p_date = ' ' + date[1].strftime('%d.%m.%Y')

        #   Определяем исполнителя работ. Берем значение ячейки второго столбца текущей строки.
        p_worker = ' ' + self.table_report.item(self.table_report.row, 1).text()

        #   Определяем смену работ
        time_of_day_dict = {0: '', 1: ' дневная', 2: ' ночная'}
        p_time_of_day = time_of_day_dict[self.combo_time_of_day.currentIndex()]  # Читаем из combo-box текущее значение.

        #   Определяем текст дополнительных работ из примечания к рабочему дню (input_decription).
        p_description = self.input_decription.toPlainText().strip('--').split(sep='--')

        #   Определяем специальность работника.
        p_guild = self.table_report.reports_dict[self.table_report.id_worker][self.table_report.id_date]['guild']

        printer = QtPrintSupport.QPrinter(QtPrintSupport.QPrinter.PrinterResolution)
        printer.setOutputFormat(QtPrintSupport.QPrinter.PdfFormat)
        printer.setPaperSize(QtPrintSupport.QPrinter.A4)
        printer.setOrientation(QtPrintSupport.QPrinter.Portrait)
        printer.setOutputFileName('filename.pdf')

        doc = QtGui.QTextDocument()

        #   Создаем объект наряда.
        self.permit = PermitHtml(p_date, p_manager, p_producer, p_worker, p_time_of_day, p_description, p_guild)

        doc.setHtml(self.permit.html_content)
        doc.setPageSize(QtCore.QSizeF(printer.pageRect().size()))
        doc.print_(printer)

    def get_settings(self, setting):
        try:
            with connect(**DataBase.config(DataBase.login, DataBase.password)) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(DataBase.sql_read_settings(), (setting,))
                    return cursor.fetchall()
        except:
            pass

    def show_input_description(self):
        worker = self.table_report.id_worker
        date = self.table_report.id_date
        cur_text = self.table_report.reports_dict[worker][date]['description']
        self.window_description = InputDescription(cur_text)
        self.window_description.btn_apply.clicked.connect(lambda x: self.change_worker_description(self.window_description.input_decription.toPlainText()))
        self.window_description.show()


# класс - таблица
class TableReport(QTableWidget):
    def __init__(self, wg):
        super().__init__(wg)

        self.change_panel = False

        self.path_to_file = os.path.join("C:\\Users", os.environ["username"], "filter.json")

        self.init_item_table()

        if os.path.isfile(self.path_to_file):
            with open(self.path_to_file, 'r', encoding='utf-8') as f:
                self.filter_text = json.load(f)
        else:
            data = {"filterRole": "rs.role", "filterGuild": "gd.guild"}
            with open(self.path_to_file, 'w', encoding='utf-8') as f:
                json.dump(data, f)
                self.filter_text = {"filterRole": "rs.role", "filterGuild": "gd.guild"}

        self.show_panel_mode = 0
        self.type_scheduler = 0
        self.wg = wg
        self.verticalHeader().hide()
        self.horizontalHeader().setSectionsClickable(False)
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setStyleSheet(Styles.table_table())
        self.horizontalScrollBar().setStyleSheet(Styles.hor_scrollbar())
        self.verticalScrollBar().setStyleSheet(Styles.ver_scrollbar())
        self.horizontalHeader().setStyleSheet(Styles.table_header())
        self.setEditTriggers(QTableWidget.NoEditTriggers)  # запретить изменять поля
        self.cellClicked.connect(self.click_table)  # установить обработчик щелча мыши в таблице
        self.setMinimumSize(500, 500)
        self.setSelectionBehavior(QAbstractItemView.SelectItems)
        pix_size = QtCore.QSize(10, 10)
        self.pix_descript = QPixmap('descript.png')
        self.pix_descript = self.pix_descript.scaled(pix_size)
        self.set_filter_table()
        self.bild_table()

    def set_filter_table(self):
        if self.wg.findChild(QComboBox, name='combo_role') is None:
            self.filter_role = self.filter_text.get('filterRole')
            self.filter_guild = self.filter_text.get('filterGuild')
            self.filter_year = str(datetime.now().date().year)
            self.filter_month = str(datetime.now().date().month)
        else:
            months = {'январь': '1', 'февраль': '2', 'март': '3', 'апрель': '4', 'май': '5', 'июнь': '6',
                      'июль': '7', 'август': '8', 'сентябрь': '9', 'октябрь': '10', 'ноябрь': '11', 'декабрь': '12'}
            combo_role_text = self.wg.combo_role.currentText()
            self.filter_role = ("'" + combo_role_text + "'", 'rs.role')[combo_role_text == 'должность']
            combo_guild_text = self.wg.combo_guild.currentText()
            self.filter_guild = ("'" + combo_guild_text + "'", 'gd.guild')[combo_guild_text == 'специальность']
            self.filter_year = self.wg.combo_years.currentText()
            self.filter_month = months[self.wg.combo_month.currentText()]

            filter_write = {'filterRole': self.filter_role,
                            'filterGuild': self.filter_guild}

            with open(self.path_to_file, 'w', encoding="utf-8") as outfile:
                json.dump(filter_write, outfile, ensure_ascii=False)

    def get_reports(self):
        with connect(**DataBase.config(DataBase.login, DataBase.password)) as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    DataBase.sql_read_workers_report(self.filter_role, self.filter_year, self.filter_month,
                                                     self.filter_guild))
                self.reports = cursor.fetchall()
                id_report = 0
                new_reports_dict = dict()
                for report in self.reports:
                    if id_report != report[7]:
                        new_reports_dict[report[7]] = dict()
                        id_report = report[7]
                    new_reports_dict[report[7]][report[8]] = {'role': report[13], 'hour': report[4],
                                                              'rating': report[5], 'status': report[6],
                                                              'place': report[10], 'time_of_day': report[11],
                                                              'description': report[12], 'team': report[14],
                                                              'brigadier': report[15], 'guild': report[9],
                                                              'props_type': report[16]}
                return new_reports_dict

    def get_dates(self, year, month):
        try:
            with connect(**DataBase.config(DataBase.login, DataBase.password)) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(DataBase.sql_read_date_report(), (year, month,))
                    return tuple(cursor.fetchall())
        except:
            pass

    def click_table(self, row, col):  # row - номер строки, col - номер столбца
        if col > 2:
            self.row = row
            self.col = col
            [self.item(i, 1).setForeground(QColor(200, 200, 200, 255)) for i in range(1, self.rowCount())]
            self.item(row, 1).setForeground(QColor(255, 255, 255, 255))
            self.check_table()
            self.id_worker = int(self.item(row, 2).text())
            self.id_date = int(self.item(0, col).text())

    def fill_panel(self):
        if self.col > 2:
            self.wg.lbl_hour.setText(str(self.reports_dict[self.id_worker][self.id_date]['hour']))
            if self.wg.findChild(QComboBox, name='combo_teams') is not None:
                self.wg.combo_teams.setCurrentText(str(self.reports_dict[self.id_worker][self.id_date]['team']) + ': ' +
                                                   self.reports_dict[self.id_worker][self.id_date]['brigadier'])

    def copy_report(self):
        if self.col > 2 and self.row > 0:
            self.buff_copy_hours = self.reports_dict[self.id_worker][self.id_date]['hour']
            self.buff_copy_rating = self.reports_dict[self.id_worker][self.id_date]['rating']
            self.buff_copy_status = self.reports_dict[self.id_worker][self.id_date]['status']
            self.buff_copy_place = self.reports_dict[self.id_worker][self.id_date]['place']
            self.buff_copy_time_of_day = self.reports_dict[self.id_worker][self.id_date]['time_of_day']
            self.buff_copy_description = self.reports_dict[self.id_worker][self.id_date]['description']
            self.buff_copy_team = self.reports_dict[self.id_worker][self.id_date]['team']

    def paste_report(self):
        if self.col > 2 and self.row > 0:
            match self.reports_dict[self.id_worker][self.id_date]['props_type']:
                case '1':
                    hour = self.buff_copy_hours
                    status = self.buff_copy_status
                    team = 0
                    time_of_day = 0
                    place = 0
                    rating = 0
                    description = ''
                    self.write_report(hour, rating, status, place, time_of_day, description, self.id_worker,
                                      self.id_date, team)
                case '2':
                    hour = self.buff_copy_hours
                    status = self.buff_copy_status
                    team = 0
                    time_of_day = self.buff_copy_time_of_day
                    place = self.buff_copy_place
                    rating = self.buff_copy_rating
                    description = self.buff_copy_description
                    self.write_report(hour, rating, status, place, time_of_day, description, self.id_worker,
                                      self.id_date, team)
                case '3':
                    hour = self.buff_copy_hours
                    status = self.buff_copy_status
                    team = self.buff_copy_team
                    time_of_day = self.buff_copy_time_of_day
                    place = self.buff_copy_place
                    rating = self.buff_copy_rating
                    description = self.buff_copy_description
                    self.write_report(hour, rating, status, place, time_of_day, description, self.id_worker,
                                      self.id_date, team)

            self.click_cell()

    def clear_report(self):
        self.init_item_table()
        if self.col > 2 and self.row > 0:
            hour = 0
            rating = 0
            status = 0
            place = 0
            time_of_day = 0
            description = ''
            team = 0
            self.write_report(hour, rating, status, place, time_of_day, description, self.id_worker, self.id_date, team)
            self.click_cell()

    def write_report(self, hour, rating, status, place, time_of_day, description, id_worker, id_date, team):
        try:
            with connect(**DataBase.config(DataBase.login, DataBase.password)) as conn:
                conn.autocommit = True
                with conn.cursor() as cursor:
                    cursor.execute(DataBase.sql_edit_table(),
                                   (hour, rating, status, place, time_of_day, description, team, id_worker, id_date))
            self.check_table()
        except:
            pass

    def check_table(self):
        new_reports_dict = self.get_reports()
        keys_equal = True
        if len(new_reports_dict) == len(self.reports_dict):
            for key in new_reports_dict:
                if key not in self.reports_dict:
                    keys_equal = False
                    break
        else:
            keys_equal = False
        if keys_equal:
            if new_reports_dict != self.reports_dict:
                self.updt_cell(new_reports_dict)
                self.reports_dict = new_reports_dict
        else:
            self.bild_table()

    def updt_cell(self, new_reports_dict):
        start_time = time.time()
        i = 1
        for id_worker, data_worker in new_reports_dict.items():
            if id_worker in self.reports_dict:
                if data_worker != self.reports_dict[id_worker]:
                    j = 0
                    for id_day, data in data_worker.items():
                        if data != self.reports_dict[id_worker][id_day]:
                            self.fill_table(data, i, j)
                        j += 1

            else:
                self.bild_table()
                break
            i += 1

        print(str(datetime.now())[:19], "updt_table %s seconds ---" % str(time.time() - start_time)[:5])

    # обновление таблицы
    def bild_table(self):
        start_time = time.time()
        scroll = self.verticalScrollBar()
        old_position_scroll = scroll.value() / (scroll.maximum() or 1)
        self.setColumnCount(0)
        self.setRowCount(0)
        self.dates = self.get_dates(self.filter_year, self.filter_month)
        self.reports_dict = self.get_reports()

        fio_dict = {report[7]: report[0] + ' ' + report[1][:1] + '. ' + report[2][:1] + '.' for report in
                    self.reports}

        dates_dict = {1: 'пн', 2: 'вт', 3: 'ср', 4: 'чт', 5: 'пт', 6: 'сб', 7: 'вс'}
        i = 0
        for i in range(len(self.dates) + 3):
            self.setColumnCount(self.columnCount() + 1)
            self.horizontalHeader().setSectionResizeMode(i, QHeaderView.Stretch)
            self.setHorizontalHeaderItem(i, QTableWidgetItem(str(i - 2) + '\n' + dates_dict[self.dates[i - 3][2]]))
        self.setRowCount(self.rowCount() + 1)

        i = 3
        for date in self.dates:
            self.setItem(0, i, QTableWidgetItem(str(date[0])))
            i += 1

        self.setRowHidden(0, True)  # скрываем нулевую строку с идентификаторами дней
        self.setColumnHidden(2, True)  # скрываем 3 столбец с идентификатором работника
        self.setHorizontalHeaderItem(0, QTableWidgetItem("№"))
        self.setHorizontalHeaderItem(1, QTableWidgetItem("ФИО"))
        self.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        delegate = AlignDelegate(self)
        self.setItemDelegateForColumn(0, delegate)

        i = 1
        for worker_dict in self.reports_dict:
            self.setRowCount(self.rowCount() + 1)

            j, k = 0, 3
            for data in self.reports_dict[worker_dict].values():
                self.setItem(i, k, QTableWidgetItem())
                header_text = self.horizontalHeaderItem(k).text()
                if 'сб' in header_text or 'вс' in header_text:
                    self.item(i, k).setBackground(QColor(50, 50, 50, 255))
                self.fill_table(data, i, j)
                k += 1
                j += 1

            self.setRowHeight(i, 40)
            self.setItem(i, 0, QTableWidgetItem(str(i)))
            self.setItem(i, 1, QTableWidgetItem(fio_dict[worker_dict]))
            self.setItem(i, 2, QTableWidgetItem(str(worker_dict)))

            flags = self.item(i, 1).flags()
            flags &= ~QtCore.Qt.ItemIsEnabled
            self.item(i, 0).setFlags(flags)
            self.item(i, 1).setFlags(flags)
            i += 1

        self.setCurrentCell(self.row, self.col)
        scroll.setValue(round(old_position_scroll * scroll.maximum()))
        print(str(datetime.now())[:19], "bild_table %s seconds ---" % str(time.time() - start_time)[:5])

    def fill_table(self, data, i, j):
        data_hour = data['hour']
        data_status = data['status']
        data_rating = data['rating']
        data_place = data['place']
        data_time_of_day = data['time_of_day']
        data_description = data['description']
        data_team = data['team']

        # верх - лево
        time_of_day = QtWidgets.QLabel(('', ('д', 'н')[data_time_of_day != 1])[data_time_of_day != 0])
        time_of_day.setFont(QFont("CalibriLight", 8, QtGui.QFont.Normal))
        time_of_day.setStyleSheet('color: rgb(150, 150, 150);')

        # верх - центр
        if data_description is not None and data_description != '':
            lbl_descript = QLabel()
            lbl_descript.setPixmap(self.pix_descript)
        else:
            lbl_descript = QtWidgets.QLabel('')

        # верх - право
        rating = QtWidgets.QLabel(('', str(data_rating))[data_rating != 0])
        rating.setFont(QFont("CalibriLight", 8, QtGui.QFont.Normal))
        dict_color_rating = {0: '',
                             1: 'color: rgb(200, 0, 0);',
                             2: 'color: rgb(150, 150, 0);',
                             3: 'color: rgb(0, 150, 0);'}
        rating.setStyleSheet(dict_color_rating.get(data_rating))

        # центр - лево, низ - центр (пустышка)
        lbl_empty = QtWidgets.QLabel('')

        # центр
        hours = QtWidgets.QLabel(('', str(data_hour))[data_hour != 0])
        hours.setFont(QFont("CalibriLight", 10, QtGui.QFont.Bold))
        hours.setStyleSheet('color: rgb(255, 255, 100);')

        # центр - право
        team = QtWidgets.QLabel(('', str(data_team))[data_team != 0])
        team.setFont(QFont("CalibriLight", 6, QtGui.QFont.Normal))
        team.setStyleSheet('color: rgb(150, 150, 150);')

        # низ - лево
        dict_data_status = {0: '', 1: 'бс', 2: 'от', 3: 'бл', 4: 'пр'}
        dict_color_status = {0: '',
                             1: 'color: rgb(255, 255, 100);',
                             2: 'color: rgb(0, 255, 0);',
                             3: 'color: rgb(255, 0, 0);',
                             4: 'color: rgb(255, 0, 0);'}
        status = QtWidgets.QLabel(dict_data_status.get(data_status))
        status.setFont(QFont("CalibriLight", 8, QtGui.QFont.Normal))
        status.setStyleSheet(dict_color_status.get(data_status))

        # низ - право
        place = QtWidgets.QLabel(('', 'чп')[data_place == 1])
        place.setFont(QFont("CalibriLight", 8, QtGui.QFont.Normal))
        place.setStyleSheet('color: rgb(100, 255, 255);')

        cell_layout = QGridLayout()

        cell_layout.setContentsMargins(0, 0, 0, 0)
        time_of_day.setContentsMargins(0, 0, 0, 0)
        lbl_descript.setContentsMargins(0, 0, 0, 0)
        place.setContentsMargins(0, 0, 0, 0)
        lbl_empty.setContentsMargins(0, 0, 0, 0)
        hours.setContentsMargins(0, 0, 0, 0)
        team.setContentsMargins(0, 0, 0, 0)
        status.setContentsMargins(0, 0, 0, 0)
        lbl_empty.setContentsMargins(0, 0, 0, 0)
        rating.setContentsMargins(0, 0, 0, 0)

        cell_layout.setColumnStretch(0, 1)
        cell_layout.setColumnStretch(1, 1)
        cell_layout.setColumnStretch(2, 1)

        cell_layout.setAlignment(Qt.AlignHCenter)

        cell_layout.addWidget(time_of_day, 0, 0, Qt.AlignCenter)
        cell_layout.addWidget(lbl_descript, 0, 1, Qt.AlignCenter)
        cell_layout.addWidget(rating, 0, 2, Qt.AlignCenter)

        cell_layout.addWidget(lbl_empty, 1, 0, Qt.AlignCenter)
        cell_layout.addWidget(hours, 1, 1, Qt.AlignCenter)
        cell_layout.addWidget(team, 1, 2, Qt.AlignCenter)

        cell_layout.addWidget(place, 2, 0, Qt.AlignCenter)
        cell_layout.addWidget(lbl_empty, 2, 1, Qt.AlignCenter)
        cell_layout.addWidget(status, 2, 2, Qt.AlignCenter)

        cell_layout.setSpacing(0)
        widget = QWidget()
        widget.setLayout(cell_layout)
        self.setCellWidget(i, j + 3, widget)

    def generate_schedules(self):
        self.init_item_table()
        col = self.currentColumn()
        id_date = int(self.item(0, self.col).text())
        day_work = 0
        type_work = ((1, 1, 2, 2, 0, 0), (1, 2, 0, 0))
        for date in self.dates:
            if date[0] >= id_date:
                self.id_date = date[0]
                self.copy_report()
                self.buff_copy_time_of_day = type_work[self.type_scheduler][day_work]
                self.paste_report()
                self.col += 1
                day_work = (day_work + 1, 0)[day_work == len(type_work[self.type_scheduler]) - 1]
        self.check_table()
        self.setCurrentCell(self.row, col)
        self.init_item_table()
        self.click_cell()

    def clear_schedules(self):
        self.init_item_table()
        col = self.currentColumn()
        id_date = int(self.item(0, self.col).text())
        self.set_filter_table()
        for date in self.dates:
            if date[0] >= id_date:
                self.id_date = date[0]
                self.copy_report()
                self.buff_copy_time_of_day = 0
                self.paste_report()
                self.col += 1
        self.check_table()
        self.setCurrentCell(self.row, col)
        self.init_item_table()
        self.click_cell()

    def get_change_list_guild(self):
        self.wg.combo_guild.clear()
        if self.wg.combo_role.currentIndex() > 0:
            current_role = self.wg.combo_role.currentText()
            self.wg.list_guild = ['специальность'] + self.wg.dict_guilds.get(current_role)
        else:
            self.wg.list_guild = ['специальность']
        self.wg.combo_guild.addItems(self.wg.list_guild)

    def click_cell(self):
        if self.row > 0:
            self.cellClicked.emit(self.row, self.col)

    def init_item_table(self):
        self.col = self.currentColumn()
        self.row = self.currentRow()


class PermitHtml:
    def __init__(self, dat, me, pe, w, td, des, type_permit):
        super().__init__()
        self.dict_text = self.get_text_permit(
            type_permit)  # Читаем из БД текстовку для наряда электриков. Получаем 3 словаря.
        # 1 - шапка, 2 - таблица, 3 - подпись.
        self.date = dat
        self.manager_electric = me
        self.producer_electric = pe
        self.worker = w
        self.time_of_day = td
        self.description = des
        self.html_content = ''
        self.load_html()

    #   Собираем html страницу наряда.
    def load_html(self):
        line = 1
        self.html_content += '<style> p {margin-top: 0,5em; margin-bottom: 0,5em;}</style>'
        #   Заголовок
        if len(self.dict_text['1']) > 0:
            self.html_content += '<p style="font-size: 12px; font-family: arial;"><center><b>'
            for _ in self.dict_text['1'].values():
                self.html_content += _ + '<br/>'
            self.html_content += '</b><center></p>'
        #   Шапка
        if len(self.dict_text['2']) > 0:
            self.html_content += '<p style="font-size: 10px; font-family: Calibri Light;">'
            for _ in self.dict_text['2'].values():
                if _ == 'Ответственный руководитель работ:':
                    self.html_content += _ + '<u>' + self.manager_electric + '</u>' + '<br/>'
                elif _ == 'Ответственный производитель работ:':
                    self.html_content += _ + '<u>' + self.producer_electric + '</u>' + '<br/>'
                else:
                    self.html_content += _ + '<br/>'
            self.html_content += '</p>'
        #   Дата
        if len(self.dict_text['3']) > 0:
            self.html_content += '<p style="font-size: 10px; font-family: Calibri Light;">'
            for _ in self.dict_text['3'].values():
                self.html_content += '<center>' + _ + self.date + '</center>'
            self.html_content += '</p>'
        #   Исполнитель и смена работы
        if len(self.dict_text['4']) > 0:
            self.html_content += '<p style="font-size: 10px; font-family: Calibri Light;">'
            for _ in self.dict_text['4'].values():
                if _ == 'Исполнитель:':
                    self.html_content += _ + self.worker + '<br>'
                elif _ == 'Смена:':
                    self.html_content += _ + self.time_of_day + '<br>'
                else:
                    self.html_content += _ + '<br>'
            self.html_content += '</p>'
        #   Таблица
        if len(self.dict_text['5']) > 0:
            #   Шапка таблицы
            self.html_content += '<table border="1" width="100%" style="border-collapse: collapse; font-size: 8px; font-family: Calibri Light;">'
            self.html_content += '<thead>'
            self.html_content += '<tr style="font-size:60%;">'
            self.html_content += '<th style="width:3%">№<br>п/п</th>'
            self.html_content += '<th style="width:10%">Цех<br>участок</th>'
            self.html_content += '<th style="width:15%">Объект<br>ремонта</th>'
            self.html_content += '<th style="width:42%">Технологические<br>операции</th>'
            self.html_content += '<th style="width:10%">Продолжи<br>тельность</th>'
            self.html_content += '<th style="width:10%">Отметка о<br>выполнении</th>'
            self.html_content += '<th style="width:10%">Примечание</th>'
            self.html_content += '</tr>'
            self.html_content += '</thead>'
            #   Тело таблицы
            self.html_content += '<tbody>'
            for _ in self.dict_text['5'].values():
                self.html_content += '<tr style="font-size:60%;">'
                self.html_content += '<td align="center">' + str(line) + '</td>'
                self.html_content += '<td></td>'
                self.html_content += '<td></td>'
                self.html_content += '<td align="left">' + _ + '</td>'
                self.html_content += '<td></td>'
                self.html_content += '<td></td>'
                self.html_content += '<td></td>'
                self.html_content += '</tr>'
                line += 1
            if len(self.description) > 0:
                for _ in self.description:
                    self.html_content += '<tr>'
                    self.html_content += '<td align="center">' + str(line) + '</td>'
                    self.html_content += '<td></td>'
                    self.html_content += '<td></td>'
                    self.html_content += '<td align="left">' + '<em>' + '<b>' + _ + '</b>' + '</em>' + '</td>'
                    self.html_content += '<td></td>'
                    self.html_content += '<td></td>'
                    self.html_content += '<td></td>'
                    self.html_content += '</tr>'
                    line += 1
            self.html_content += '</tbody>'
            self.html_content += '</table>'
        #   Подпись
        if len(self.dict_text['6']) > 0:
            self.html_content += '<br>'
            for _ in self.dict_text['6'].values():
                self.html_content += '<p style="font-size: 10px; font-family: Calibri Light;">'
                if _ == 'Исполнитель:':
                    self.html_content += _ + ' _________________ ' + '/' + self.worker + '/' + '<br>'
                elif _ == 'Ответственный руководитель работ:':
                    manager_electric = (' '.join(self.manager_electric.split()[-2:]), self.manager_electric)[
                        self.manager_electric == '']
                    self.html_content += _ + ' _________________ ' + '/' + manager_electric + '/' + '<br>'
                elif _ == 'Ответственный производитель работ:':
                    producer_electric = (' '.join(self.producer_electric.split()[-2:]), self.producer_electric)[
                        self.producer_electric == '']
                    self.html_content += _ + ' _________________ ' + '/' + producer_electric + '/' + '<br>'
                else:
                    self.html_content += _ + '<br>'
                self.html_content += '</p>'

    def get_text_permit(self, type_permit):
        try:
            with connect(**DataBase.config(DataBase.login, DataBase.password)) as conn:
                with conn.cursor() as cursor:
                    dict_text = dict()
                    cursor.execute(DataBase.sql_read_text_permit(), (2,))
                    text_list = cursor.fetchall()
                    group = 0
                    for text in text_list:
                        if group != text[0]:
                            dict_text[str(text[0])] = dict()
                            group = text[0]
                        dict_text[str(text[0])][str(text[1])] = str(text[2])
                    return dict_text
        except:
            pass


class InputDescription(QWidget):
    def __init__(self, text):
        super().__init__()
        self.insert_signal = pyqtSignal(str)
        self.resize(500, 500)
        btn_size = QSize(200, 30)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        self.setStyleSheet("QWidget{ \
                            background-color: rgb(40, 40, 40); \
                            border: 0px outset rgb(60, 60, 60); \
                            }")

        self.main_layout = QVBoxLayout()
        self.btn_layout = QHBoxLayout()

        self.input_decription = QTextEdit(self, objectName='input_decription')
        self.input_decription.setText(text)
        self.input_decription.setFixedSize(QSize(500, 500))
        self.input_decription.setStyleSheet(Styles.input_text())
        self.input_decription.setAlignment(Qt.AlignTop)
        self.input_decription.setPlaceholderText('введите примечание...')

        self.btn_apply = QPushButton('применить')
        self.btn_apply.setFixedSize(btn_size)
        self.btn_apply.setStyleSheet(Styles.workers_btn())
        self.btn_apply.clicked.connect(self.close)
        self.btn_layout.addWidget(self.btn_apply)
        self.btn_apply.setCursor(Qt.PointingHandCursor)

        self.btn_cancel = QPushButton('отмена')
        self.btn_cancel.setFixedSize(btn_size)
        self.btn_cancel.setStyleSheet(Styles.workers_btn())
        self.btn_cancel.clicked.connect(self.close)
        self.btn_layout.addWidget(self.btn_cancel)
        self.btn_cancel.setCursor(Qt.PointingHandCursor)

        self.main_layout.addWidget(self.input_decription)
        self.main_layout.addLayout(self.btn_layout)

        self.setLayout(self.main_layout)