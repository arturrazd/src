import json
import time
import locale
from datetime import datetime
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt, QSize, QUrl
from PyQt5.QtGui import QFont, QColor, QKeySequence, QPixmap
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import *
from psycopg2 import connect

from data_base import DataBase
from styles import Styles
from styles import AlignDelegate

locale.setlocale(category=locale.LC_ALL, locale="Russian")


class TableWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.list_role = list()
        self.list_guild = list()
        self.dict_guilds = dict()
        self.list_teams = list()

        self.list_status = ['полный день', 'б/с', 'отпуск', 'больничный', 'прогул']
        self.dict_month = self.get_list_dates()
        self.list_hours = [str(i) + ' ч.' for i in range(1, 25)]
        self.list_time_of_day = ['смена', 'день', 'ночь']
        self.list_rating = ['оценка', '1', '2', '3']
        self.list_place = ['НУФ', 'Чапаева']
        self.list_scheduler_type = ['ДД-НН-ОВ', 'ДН-ОВ']

        self.main_btn_size = QSize(35, 35)
        self.input_btn_size = QSize(200, 30)
        self.icon_size = QSize(15, 15)

        self.btn_clear_scheduler = None
        self.lbl_work_day = None
        self.btn_generate_scheduler = None
        self.combo_type_scheduler = None
        self.combo_time_of_day = None
        self.btn_insert_description = None
        self.input_decription = None
        self.combo_teams = None
        self.btn_generation_permit = None
        self.permit = None
        self.combo_place = None
        self.combo_status = None
        self.combo_hours = None
        self.combo_rating = None
        self.btn_copy = None
        self.table_report = TableReport(self)
        self.table_report.cellClicked.connect(self.show_panel)
        self.table_report.cellClicked.connect(self.table_report.fill_panel)
        self.shortcut = QShortcut(QKeySequence("Ctrl+C"), self)
        self.shortcut.activated.connect(self.table_report.copy_report)
        self.shortcut = QShortcut(QKeySequence("Ctrl+V"), self)
        self.shortcut.activated.connect(self.table_report.paste_report)
        self.shortcut = QShortcut(QKeySequence("Del"), self)
        self.shortcut.activated.connect(self.table_report.clear_report)
        self.table_report.setCursor(Qt.PointingHandCursor)

        # надпись "фильтр табеля"
        self.lbl_filter = QLabel('фильтр табеля')
        self.lbl_filter.setFont(QFont("CalibriLight", 10, QtGui.QFont.Normal))
        self.lbl_filter.setStyleSheet('color: rgb(255, 255, 255); background-color: rgb(15, 15, 15);')
        self.lbl_filter.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_filter.setFixedSize(200, 20)

        # кнопка "очистить фильтр"
        self.btn_clear_filter = QPushButton('очистить', self)
        self.btn_clear_filter.setIconSize(self.icon_size)
        self.btn_clear_filter.setFixedSize(self.input_btn_size)
        self.btn_clear_filter.setStyleSheet(Styles.workers_btn())
        self.btn_clear_filter.clicked.connect(self.clear_filter)
        self.btn_clear_filter.setCursor(Qt.PointingHandCursor)

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

        # кнопка "обновить"
        self.btn_refresh = QPushButton('', self)
        self.btn_refresh.setIcon(QtGui.QIcon('refresh.png'))
        self.btn_refresh.setIconSize(self.icon_size)
        self.btn_refresh.setFixedSize(self.main_btn_size)
        self.btn_refresh.setStyleSheet(Styles.workers_btn())
        self.btn_refresh.clicked.connect(self.table_report.check_table)
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

        self.page_layout = QHBoxLayout()
        self.page_layout.setContentsMargins(0, 0, 0, 0)
        self.panel_layout = QVBoxLayout()
        self.panel_layout.setContentsMargins(0, 0, 10, 0)
        self.button_layout = QHBoxLayout()
        self.button_layout.setContentsMargins(20, 0, 10, 0)
        self.edit_layout = QVBoxLayout()
        self.edit_layout.setContentsMargins(20, 0, 10, 0)
        self.scheduler_layout = QVBoxLayout()
        self.scheduler_layout.setContentsMargins(20, 0, 10, 0)
        self.filter_layout = QVBoxLayout()
        self.filter_layout.setContentsMargins(20, 0, 10, 2)

        self.button_layout.addWidget(self.btn_refresh)
        self.button_layout.addWidget(self.btn_copy)
        self.button_layout.addWidget(self.btn_paste)
        self.button_layout.addWidget(self.btn_clear)
        self.button_layout.setSpacing(20)

        self.filter_layout.addWidget(self.lbl_filter)
        self.filter_layout.addWidget(self.btn_clear_filter)
        self.filter_layout.addWidget(self.combo_years)
        self.filter_layout.addWidget(self.combo_month)
        self.filter_layout.addWidget(self.combo_role)
        self.filter_layout.addWidget(self.combo_guild)
        self.filter_layout.setSpacing(2)

        self.panel_layout.addLayout(self.button_layout)
        self.panel_layout.addLayout(self.edit_layout)
        self.panel_layout.addStretch(0)
        self.panel_layout.addLayout(self.scheduler_layout)
        self.panel_layout.addStretch(0)
        self.panel_layout.addLayout(self.filter_layout)
        self.panel_layout.addStretch(0)
        self.panel_layout.setSpacing(2)
        self.page_layout.addWidget(self.table_report)
        self.page_layout.addLayout(self.panel_layout)
        self.page_layout.setSpacing(2)
        self.setLayout(self.page_layout)

        self.get_list_teams()

    def show_panel(self):

        self.clear_panel()

        self.show_element_panel(self.table_report.id_worker, self.table_report.id_date)

        self.edit_layout.addWidget(self.lbl_work_day)

        if self.findChild(QComboBox, name='combo_hours') is not None:
            self.edit_layout.addWidget(self.combo_hours)
            self.combo_hours.setToolTip('отработано часов')
            self.combo_hours.setCursor(Qt.PointingHandCursor)
        if self.findChild(QComboBox, name='combo_status') is not None:
            self.edit_layout.addWidget(self.combo_status)
            self.combo_status.setToolTip('статус дня')
            self.combo_status.setCursor(Qt.PointingHandCursor)
        if self.findChild(QComboBox, name='combo_rating') is not None:
            self.edit_layout.addWidget(self.combo_rating)
            self.combo_rating.setToolTip('оценка')
            self.combo_rating.setCursor(Qt.PointingHandCursor)

        self.edit_layout.addWidget(self.input_decription)
        self.edit_layout.addWidget(self.btn_insert_description)
        self.btn_insert_description.setToolTip('записать примечание')
        self.btn_insert_description.setCursor(Qt.PointingHandCursor)

        if self.findChild(QComboBox, name='combo_time_of_day') is not None:
            self.edit_layout.addWidget(self.combo_time_of_day)
            self.combo_time_of_day.setToolTip('время рабочей смены')
            self.combo_time_of_day.setCursor(Qt.PointingHandCursor)

        if self.findChild(QComboBox, name='combo_place') is not None:
            self.edit_layout.addWidget(self.combo_place)
            self.combo_place.setToolTip('площадка предприятия')
            self.combo_place.setCursor(Qt.PointingHandCursor)

        if self.findChild(QComboBox, name='combo_teams') is not None:
            self.edit_layout.addWidget(self.combo_teams)
            self.combo_teams.setToolTip('бригада')
            self.combo_teams.setCursor(Qt.PointingHandCursor)

            self.edit_layout.addWidget(self.btn_generation_permit)
            self.btn_generation_permit.setToolTip('сгенерировать наряд')
            self.btn_generation_permit.setCursor(Qt.PointingHandCursor)

        if self.findChild(QComboBox, name='combo_type_scheduler') is not None:
            self.scheduler_layout.addWidget(self.lbl_scheduler_type)
            self.scheduler_layout.addWidget(self.combo_type_scheduler)
            self.combo_type_scheduler.setToolTip('расписание смен')
            self.combo_type_scheduler.setCursor(Qt.PointingHandCursor)

        if self.findChild(QPushButton, name='btn_generate_scheduler') is not None:
            self.scheduler_layout.addWidget(self.btn_generate_scheduler)
            self.btn_generate_scheduler.setToolTip('сгенерировать')
            self.btn_generate_scheduler.setCursor(Qt.PointingHandCursor)
            self.scheduler_layout.addWidget(self.btn_clear_scheduler)
            self.btn_clear_scheduler.setToolTip('очистить')
            self.btn_clear_scheduler.setCursor(Qt.PointingHandCursor)

    def show_element_panel(self, id_work, id_date):
        if self.table_report.col > 2:
            # надпись "настройки дня"
            self.lbl_work_day = QLabel('настройки дня')
            self.lbl_work_day.setFont(QFont("CalibriLight", 10, QtGui.QFont.Normal))
            self.lbl_work_day.setStyleSheet('color: rgb(255, 255, 255); background-color: rgb(15, 15, 15);')
            self.lbl_work_day.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.lbl_work_day.setFixedSize(200, 20)

            # отработанные часы
            self.combo_hours = QComboBox(self, objectName='combo_hours')
            self.combo_hours.setFixedSize(self.input_btn_size)
            self.combo_hours.addItems(['отработано'] + self.list_hours)
            self.combo_hours.setStyleSheet(Styles.workers_combo())
            self.combo_hours.activated.connect(self.table_report.edit_report)

            # статус работника (полный день, отгул, отпуск, больничный)
            self.combo_status = QComboBox(self, objectName='combo_status')
            self.combo_status.addItems(self.list_status)
            self.combo_status.setFixedSize(self.input_btn_size)
            self.combo_status.setStyleSheet(Styles.workers_combo())
            self.combo_status.activated.connect(self.table_report.edit_report)

            #  поле ввода примечания
            self.input_decription = QTextEdit(self, objectName='input_decription')
            self.input_decription.setFixedSize(QSize(200, 100))
            self.input_decription.setStyleSheet(Styles.input_text())
            self.input_decription.setAlignment(Qt.AlignTop)
            self.input_decription.setPlaceholderText('введите примечание...')

            # кнопка "записать примечание"
            self.btn_insert_description = QPushButton('записать примечание', self, objectName='btn_insert_description')
            self.btn_insert_description.setFixedSize(self.input_btn_size)
            self.btn_insert_description.setStyleSheet(Styles.workers_btn())
            self.btn_insert_description.clicked.connect(self.table_report.edit_report)

            if self.table_report.reports_dict[id_work][id_date]['role'] > 1:

                # оценка
                self.combo_rating = QComboBox(self, objectName='combo_rating')
                self.combo_rating.setFixedSize(self.input_btn_size)
                self.combo_rating.addItems(self.list_rating)
                self.combo_rating.setStyleSheet(Styles.workers_combo())
                self.combo_rating.activated.connect(self.table_report.edit_report)

                # смена (день/ночь)
                self.combo_time_of_day = QComboBox(self, objectName='combo_time_of_day')
                self.combo_time_of_day.addItems(self.list_time_of_day)
                self.combo_time_of_day.setFixedSize(self.input_btn_size)
                self.combo_time_of_day.setStyleSheet(Styles.workers_combo())
                self.combo_time_of_day.activated.connect(self.table_report.edit_report)

                # место работы (НУФ/Чапаева)
                self.combo_place = QComboBox(self, objectName='combo_place')
                self.combo_place.addItems(self.list_place)
                self.combo_place.setFixedSize(self.input_btn_size)
                self.combo_place.setStyleSheet(Styles.workers_combo())
                self.combo_place.activated.connect(self.table_report.edit_report)

                if self.table_report.reports_dict[id_work][id_date]['role'] > 2:
                    # бригада
                    self.combo_teams = QComboBox(self, objectName='combo_teams')
                    self.combo_teams.setFixedSize(self.input_btn_size)
                    self.combo_teams.addItems(self.list_teams)
                    self.combo_teams.setStyleSheet(Styles.workers_combo())
                    self.combo_teams.activated.connect(self.table_report.edit_report)

                    # кнопка "сгенерировать наряд"
                    self.btn_generation_permit = QPushButton('сгенерировать наряд', self,
                                                             objectName='btn_generation_permit')
                    self.btn_generation_permit.setFixedSize(self.input_btn_size)
                    self.btn_generation_permit.setStyleSheet(Styles.workers_btn())
                    self.btn_generation_permit.clicked.connect(self.show_permit)

                # надпись "расписание смен"
                self.lbl_scheduler_type = QLabel('расписание смен')
                self.lbl_scheduler_type.setFont(QFont("CalibriLight", 10, QtGui.QFont.Normal))
                self.lbl_scheduler_type.setStyleSheet('color: rgb(255, 255, 255); background-color: rgb(15, 15, 15);')
                self.lbl_scheduler_type.setAlignment(Qt.AlignmentFlag.AlignCenter)
                self.lbl_scheduler_type.setFixedSize(200, 20)

                # кнопка "сгенерировать расписание"
                self.btn_generate_scheduler = QPushButton('сгенерировать', self, objectName='btn_generate_scheduler')
                self.btn_generate_scheduler.setIconSize(self.icon_size)
                self.btn_generate_scheduler.setFixedSize(self.input_btn_size)
                self.btn_generate_scheduler.setStyleSheet(Styles.workers_btn())
                self.btn_generate_scheduler.clicked.connect(self.table_report.generate_schedules)

                # кнопка "очистить расписание"
                self.btn_clear_scheduler = QPushButton('очистить', self)
                self.btn_clear_scheduler.setIconSize(self.icon_size)
                self.btn_clear_scheduler.setFixedSize(self.input_btn_size)
                self.btn_clear_scheduler.setStyleSheet(Styles.workers_btn())
                self.btn_clear_scheduler.setCursor(Qt.PointingHandCursor)
                self.btn_clear_scheduler.clicked.connect(self.table_report.clear_schedules)

                # выбор типа расписания рабочих дней
                self.combo_type_scheduler = QComboBox(self, objectName='combo_type_scheduler')
                self.combo_type_scheduler.addItems(self.list_scheduler_type)
                self.combo_type_scheduler.setFixedSize(self.input_btn_size)
                self.combo_type_scheduler.setStyleSheet(Styles.workers_combo())

    def clear_panel(self):
        if self.findChild(QComboBox, name='combo_hours') is not None:
            self.combo_hours.deleteLater()
        if self.findChild(QComboBox, name='combo_status') is not None:
            self.combo_status.deleteLater()
        if self.findChild(QComboBox, name='combo_place') is not None:
            self.combo_place.deleteLater()
        if self.findChild(QComboBox, name='combo_time_of_day') is not None:
            self.combo_time_of_day.deleteLater()
        if self.findChild(QComboBox, name='combo_rating') is not None:
            self.combo_rating.deleteLater()
        if self.findChild(QComboBox, name='combo_type_scheduler') is not None:
            self.combo_type_scheduler.deleteLater()
            self.lbl_scheduler_type.deleteLater()
        if self.findChild(QPushButton, name='btn_generate_scheduler') is not None:
            self.btn_generate_scheduler.deleteLater()
            self.btn_clear_scheduler.deleteLater()
        if self.findChild(QComboBox, name='combo_teams') is not None:
            self.combo_teams.deleteLater()
            self.btn_generation_permit.deleteLater()
        self.edit_layout.removeWidget(self.lbl_work_day)
        self.edit_layout.removeWidget(self.input_decription)
        self.edit_layout.removeWidget(self.btn_insert_description)

    def get_list_role(self):
        try:
            with connect(**DataBase.config()) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(DataBase.sql_list_role())
                    self.list_role = cursor.fetchall()
                    combo_list_role = [role[1] for role in self.list_role]
                    return combo_list_role
        except:
            pass

    def get_list_guild(self):
        try:
            with connect(**DataBase.config()) as conn:
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
            with connect(**DataBase.config()) as conn:
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
            with connect(**DataBase.config()) as conn:
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

    def show_permit(self):
        self.permit = PermitHtml()
        for date in self.table_report.dates:
            if self.table_report.id_date in date:
                self.permit.date = ' ' + str(date[1])[-2:] + '.' + str(date[1])[5:7] + '.' + str(date[1])[:4]
        self.permit.load_html()
        self.permit.show()


# класс - таблица
class TableReport(QTableWidget):
    def __init__(self, wg):
        super().__init__(wg)
        self.dates = None
        self.col = None
        self.row = None
        self.id_worker = None
        self.id_date = None
        self.buff_copy_team = None
        self.buff_copy_time_of_day = None
        self.buff_copy_description = None
        self.buff_copy_place = None
        self.filter_role = None
        self.filter_guild = None
        self.filter_month = None
        self.filter_year = None
        self.reports = None
        self.reports_dict = None
        self.buff_copy_hours = None
        self.buff_copy_rating = None
        self.buff_copy_status = None
        self.change_panel = False

        self.init_item_table()

        with open('filter.json', 'r', encoding='utf-8') as f:
            self.filter_text = json.load(f)

        self.show_panel_mode = 0
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

            with open('filter.json', 'w', encoding="utf-8") as outfile:
                json.dump(filter_write, outfile, ensure_ascii=False)

    def get_reports(self):
        with connect(**DataBase.config()) as conn:
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
                                                              'brigadier': report[15]}
                return new_reports_dict

    def get_dates(self, year, month):
        try:
            with connect(**DataBase.config()) as conn:
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
            id_worker = int(self.item(self.row, 2).text())
            id_date = int(self.item(0, self.col).text())
            self.wg.combo_hours.setCurrentIndex(self.reports_dict[id_worker][id_date]['hour'])
            if self.wg.findChild(QComboBox, name='combo_rating') is not None:
                self.wg.combo_rating.setCurrentIndex(self.reports_dict[id_worker][id_date]['rating'])
            self.wg.combo_status.setCurrentIndex(self.reports_dict[id_worker][id_date]['status'])
            if self.wg.findChild(QComboBox, name='combo_place') is not None:
                self.wg.combo_place.setCurrentIndex(self.reports_dict[id_worker][id_date]['place'])
            if self.wg.findChild(QComboBox, name='combo_time_of_day') is not None:
                self.wg.combo_time_of_day.setCurrentIndex(self.reports_dict[id_worker][id_date]['time_of_day'])
            if self.wg.findChild(QComboBox, name='combo_teams') is not None:
                self.wg.combo_teams.setCurrentText(str(self.reports_dict[id_worker][id_date]['team']) + ': ' +
                                                   self.reports_dict[id_worker][id_date]['brigadier'])
            self.wg.input_decription.setPlainText(self.reports_dict[id_worker][id_date]['description'])

    def copy_report(self):
        if self.col > 2 and self.row > 0:
            id_worker = int(self.item(self.row, 2).text())
            id_date = int(self.item(0, self.col).text())
            self.buff_copy_hours = self.reports_dict[id_worker][id_date]['hour']
            self.buff_copy_rating = self.reports_dict[id_worker][id_date]['rating']
            self.buff_copy_status = self.reports_dict[id_worker][id_date]['status']
            self.buff_copy_place = self.reports_dict[id_worker][id_date]['place']
            self.buff_copy_time_of_day = self.reports_dict[id_worker][id_date]['time_of_day']
            self.buff_copy_description = self.reports_dict[id_worker][id_date]['description']
            self.buff_copy_team = self.reports_dict[id_worker][id_date]['team']
            pass

    def paste_report(self):
        if self.col > 2 and self.row > 0:
            hour = self.buff_copy_hours
            status = self.buff_copy_status
            description = self.buff_copy_description
            id_worker = int(self.item(self.row, 2).text())
            id_date = int(self.item(0, self.col).text())

            if self.wg.findChild(QComboBox, name='combo_rating') is not None:
                rating = self.buff_copy_rating
            else:
                rating = 0

            if self.wg.findChild(QComboBox, name='combo_place') is not None:
                place = self.buff_copy_place
            else:
                place = 0

            if self.wg.findChild(QComboBox, name='combo_time_of_day') is not None:
                time_of_day = self.buff_copy_time_of_day
            else:
                time_of_day = 0

            if self.wg.findChild(QComboBox, name='combo_teams') is not None:
                team = self.buff_copy_team
            else:
                team = 0

            if hour is not None and rating is not None and status is not None:
                self.write_report(hour, rating, status, place, time_of_day, description, id_worker, id_date, team)
            self.click_cell()

    def edit_report(self):
        if self.row > 0 and self.col > 2:
            hour = self.wg.combo_hours.currentIndex()
            if self.wg.findChild(QComboBox, name='combo_rating') is not None:
                rating = self.wg.combo_rating.currentIndex()
            else:
                rating = 0
            status = self.wg.combo_status.currentIndex()
            id_worker = int(self.item(self.row, 2).text())
            id_date = int(self.item(0, self.col).text())
            if self.wg.findChild(QComboBox, name='combo_place') is not None:
                place = self.wg.combo_place.currentIndex()
            else:
                place = 0
            if self.wg.findChild(QComboBox, name='combo_time_of_day') is not None:
                time_of_day = self.wg.combo_time_of_day.currentIndex()
            else:
                time_of_day = 0
            if self.wg.findChild(QComboBox, name='combo_teams') is not None:
                team = (self.wg.combo_teams.currentText().split(":")[0], 0)[self.wg.combo_teams.currentIndex() == 0]
            else:
                team = 0
            description = self.wg.input_decription.toPlainText()
            self.write_report(hour, rating, status, place, time_of_day, description, id_worker, id_date, team)
            self.click_cell()

    def clear_report(self):
        hour = 0
        rating = 0
        status = 0
        if self.col > 2 and self.row > 0:
            id_worker = int(self.item(self.row, 2).text())
            id_date = int(self.item(0, self.col).text())
            place = 0
            time_of_day = 0
            description = ''
            team = 0
            self.write_report(hour, rating, status, place, time_of_day, description, id_worker, id_date, team)
            self.click_cell()

    def write_report(self, hour, rating, status, place, time_of_day, description, id_worker, id_date, team):
        try:
            with connect(**DataBase.config()) as conn:
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
        place = QtWidgets.QLabel(('', 'чп')[data_place == 1])
        place.setFont(QFont("CalibriLight", 8, QtGui.QFont.Normal))
        place.setStyleSheet('color: rgb(150, 150, 150);')

        # центр - лево, низ - центр (пустышка)
        lbl_empty = QtWidgets.QLabel('')

        # центр
        hours = QtWidgets.QLabel(('', str(data_hour))[data_hour != 0])
        hours.setFont(QFont("CalibriLight", 10, QtGui.QFont.Bold))
        hours.setStyleSheet('color: rgb(255, 255, 100);')

        # центр - право
        team = QtWidgets.QLabel(('', str(data_team))[data_team != 0])
        team.setFont(QFont("CalibriLight", 8, QtGui.QFont.Normal))
        team.setStyleSheet('color: rgb(100, 100, 100);')

        # низ - лево
        dict_data_status = {0: '', 1: 'б/с', 2: 'отпуск', 3: 'бл', 4: 'пр'}
        dict_color_status = {0: '',
                             1: 'color: rgb(255, 255, 100);',
                             2: 'color: rgb(0, 255, 0);',
                             3: 'color: rgb(255, 0, 0);',
                             4: 'color: rgb(255, 0, 0);'}
        status = QtWidgets.QLabel(dict_data_status.get(data_status))
        status.setFont(QFont("CalibriLight", 8, QtGui.QFont.Normal))
        status.setStyleSheet(dict_color_status.get(data_status))

        # низ - право
        rating = QtWidgets.QLabel(('', str(data_rating))[data_rating != 0])
        rating.setFont(QFont("CalibriLight", 8, QtGui.QFont.Normal))
        dict_color_rating = {0: '',
                             1: 'color: rgb(200, 0, 0);',
                             2: 'color: rgb(150, 150, 0);',
                             3: 'color: rgb(0, 150, 0);'}
        rating.setStyleSheet(dict_color_rating.get(data_rating))
        # rating.setStyleSheet('color: rgb(150, 150, 150);')

        cell_layout = QVBoxLayout()
        cell_layout.setContentsMargins(0, 0, 0, 0)

        upper_layout = QHBoxLayout()
        upper_layout.setContentsMargins(0, 0, 0, 0)
        upper_layout.addStretch(0)
        upper_layout.addWidget(time_of_day)
        upper_layout.addStretch(0)
        upper_layout.addWidget(lbl_descript)
        upper_layout.addStretch(0)
        upper_layout.addWidget(place)
        upper_layout.addStretch(0)

        center_layout = QHBoxLayout()
        center_layout.setContentsMargins(0, 0, 0, 0)
        center_layout.addStretch(0)
        center_layout.addWidget(lbl_empty)
        center_layout.addStretch(0)
        center_layout.addWidget(hours)
        center_layout.addStretch(0)
        center_layout.addWidget(team)
        center_layout.addStretch(0)

        lower_layout = QHBoxLayout()
        lower_layout.setContentsMargins(0, 0, 0, 0)
        lower_layout.addWidget(status)
        lower_layout.addStretch(0)
        lower_layout.addWidget(lbl_empty)
        lower_layout.addStretch(0)
        lower_layout.addWidget(rating)
        lower_layout.addStretch(0)

        cell_layout.addLayout(upper_layout)
        cell_layout.addLayout(center_layout)
        cell_layout.addLayout(lower_layout)
        cell_layout.setSpacing(0)
        widget = QWidget()
        widget.setLayout(cell_layout)
        self.setCellWidget(i, j + 3, widget)

    def generate_schedules(self):
        self.init_item_table()
        id_date = int(self.item(0, self.col).text())
        day_work = 0
        type_work = [[1, 1, 2, 2, 0, 0], [1, 2, 0, 0]]
        type_scheduler = self.wg.combo_type_scheduler.currentIndex()
        for date in self.dates:
            if date[0] >= id_date:
                self.copy_report()
                self.buff_copy_time_of_day = type_work[type_scheduler][day_work]
                self.paste_report()
                self.col += 1
                day_work = (day_work + 1, 0)[day_work == len(type_work[type_scheduler]) - 1]
        self.check_table()
        self.click_cell()

    def clear_schedules(self):
        self.init_item_table()
        id_date = int(self.item(0, self.col).text())
        self.set_filter_table()
        for date in self.dates:
            if date[0] >= id_date:
                self.copy_report()
                self.buff_copy_time_of_day = 0
                self.paste_report()
                self.col += 1
        self.check_table()
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
        self.init_item_table()
        if self.row > 0:
            self.cellClicked.emit(self.row, self.col)

    def init_item_table(self):
        self.col = self.currentColumn()
        self.row = self.currentRow()


class PermitHtml(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('Наряд на выполнение работ')
        self.web_view = QWebEngineView(self)
        self.web_view.setGeometry(0, 0, 800, 600)
        self.dict_text = self.get_text_permit()
        self.date = ''
        self.load_html()

    def load_html(self):
        html_content = "<html> <body> <header>"
        if len(self.dict_text['1']) > 0:
            for value in self.dict_text['1'].values():
                if value == 'Дата:':
                    html_content += '<p>' + value + self.date + '</p>'
                else:
                    html_content += '<p>' + value + '</p>'

        html_content += "</html> </body> </header>"

        self.web_view.setHtml(html_content)

    def get_text_permit(self):
        try:
            with connect(**DataBase.config()) as conn:
                with conn.cursor() as cursor:
                    dict_text = dict()
                    cursor.execute(DataBase.sql_read_text_permit())
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
