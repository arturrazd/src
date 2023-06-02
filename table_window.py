import time
import locale
from datetime import datetime, timedelta
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QIcon, QColor, QKeySequence, QPixmap
from PyQt5.QtWidgets import *
from psycopg2 import connect
from data_base import DataBase
from styles import Styles
from styles import AlignDelegate

locale.setlocale(category=locale.LC_ALL, locale="Russian")


class TableWindow(QWidget):
    def __init__(self):
        super().__init__()

        main_btn_size = QSize(30, 30)
        input_btn_size = QSize(150, 25)
        icon_size = QSize(15, 15)

        self.btn_generate_scheduler = None
        self.combo_type_scheduler = None
        self.combo_time_of_day = None
        self.btn_insert_description = None
        self.input_decription = None
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
        # фильтр по должности
        self.combo_role = QComboBox(self, objectName='combo_role')
        self.list_role = self.get_list_role()
        self.combo_role.addItems(self.list_role)
        self.combo_role.setFixedSize(input_btn_size)
        self.combo_role.setStyleSheet(Styles.workers_combo())
        self.combo_role.activated.connect(self.table_report.set_filter_table)
        self.combo_role.activated.connect(self.table_report.check_table)
        # фильтр по отделу/цеху
        self.combo_gild = QComboBox(self, objectName='combo_gild')
        self.list_gild = self.get_list_gild()
        self.combo_gild.addItems(self.list_gild)
        self.combo_gild.setFixedSize(input_btn_size)
        self.combo_gild.setStyleSheet(Styles.workers_combo())
        self.combo_gild.activated.connect(self.table_report.set_filter_table)
        self.combo_gild.activated.connect(self.table_report.check_table)
        # выбор года
        self.combo_years = QComboBox(self, objectName='combo_years')
        self.list_years = list(self.get_list_dates().keys())
        self.combo_years.addItems(self.list_years)
        self.combo_years.setCurrentText(str(datetime.now().date().year))
        self.combo_years.setFixedSize(input_btn_size)
        self.combo_years.setStyleSheet(Styles.workers_combo())
        self.combo_years.activated.connect(self.change_list_month)
        self.combo_years.activated.connect(self.table_report.set_filter_table)
        self.combo_years.activated.connect(self.table_report.bild_table)
        # выбор месяца
        self.combo_month = QComboBox(self, objectName='combo_month')
        self.dict_month = self.get_list_dates()
        self.list_month = list(self.dict_month[self.combo_years.currentText()].values())
        self.combo_month.addItems(self.list_month)
        current_month = datetime.strptime(str(datetime.now().date()), "%Y-%m-%d").strftime("%B")
        self.combo_month.setCurrentText(current_month)
        self.combo_month.setFixedSize(input_btn_size)
        self.combo_month.setStyleSheet(Styles.workers_combo())
        self.combo_month.activated.connect(self.table_report.set_filter_table)
        self.combo_month.activated.connect(self.table_report.bild_table)
        # кнопка "обновить"
        self.btn_refresh = QPushButton('', self)
        self.btn_refresh.setIcon(QtGui.QIcon('refresh.png'))
        self.btn_refresh.setIconSize(icon_size)
        self.btn_refresh.setFixedSize(main_btn_size)
        self.btn_refresh.setStyleSheet(Styles.workers_btn())
        self.btn_refresh.clicked.connect(self.table_report.check_table)
        # кнопка "копировать"
        self.btn_copy = QPushButton('', self)
        self.btn_copy.setIcon(QtGui.QIcon('copy_report.png'))
        self.btn_copy.setIconSize(icon_size)
        self.btn_copy.setFixedSize(main_btn_size)
        self.btn_copy.setStyleSheet(Styles.workers_btn())
        self.btn_copy.clicked.connect(self.table_report.copy_report)
        # кнопка "вставить"
        self.btn_paste = QPushButton('', self)
        self.btn_paste.setIcon(QtGui.QIcon('paste_report.png'))
        self.btn_paste.setIconSize(icon_size)
        self.btn_paste.setFixedSize(main_btn_size)
        self.btn_paste.setStyleSheet(Styles.workers_btn())
        self.btn_paste.clicked.connect(self.table_report.paste_report)
        # кнопка "очистить"
        self.btn_clear = QPushButton('', self)
        self.btn_clear.setIcon(QtGui.QIcon('delete_report.png'))
        self.btn_clear.setIconSize(icon_size)
        self.btn_clear.setFixedSize(main_btn_size)
        self.btn_clear.setStyleSheet(Styles.workers_btn())
        self.btn_clear.clicked.connect(self.table_report.clear_report)

        self.page_layout = QHBoxLayout()
        self.page_layout.setContentsMargins(0, 0, 0, 0)
        self.panel_layout = QVBoxLayout()
        self.panel_layout.setContentsMargins(0, 0, 10, 0)
        self.button_layout = QHBoxLayout()
        self.button_layout.setContentsMargins(0, 0, 0, 0)
        self.edit_layout = QVBoxLayout()
        self.edit_layout.setContentsMargins(0, 0, 0, 0)
        self.scheduler_layout = QVBoxLayout()
        self.scheduler_layout.setContentsMargins(0, 0, 0, 0)
        self.filter_layout = QVBoxLayout()
        self.filter_layout.setContentsMargins(0, 0, 0, 0)

        self.button_layout.addWidget(self.btn_refresh)
        self.button_layout.addWidget(self.btn_copy)
        self.button_layout.addWidget(self.btn_paste)
        self.button_layout.addWidget(self.btn_clear)
        self.button_layout.setSpacing(10)

        self.filter_layout.addWidget(self.combo_years)
        self.filter_layout.addWidget(self.combo_month)
        self.filter_layout.addWidget(self.combo_role)
        self.filter_layout.addWidget(self.combo_gild)
        self.filter_layout.setSpacing(10)

        self.panel_layout.addLayout(self.button_layout)
        self.panel_layout.addLayout(self.edit_layout)
        self.panel_layout.addStretch(0)
        self.panel_layout.addLayout(self.scheduler_layout)
        self.panel_layout.addStretch(0)
        self.panel_layout.addLayout(self.filter_layout)
        self.panel_layout.setSpacing(10)
        self.page_layout.addWidget(self.table_report)
        self.page_layout.addLayout(self.panel_layout)
        self.page_layout.setSpacing(10)

        self.setLayout(self.page_layout)

    def show_panel(self):
        self.clear_panel()
        # отработанные часы
        self.combo_hours = QComboBox(self, objectName='combo_hours')
        self.combo_hours.setFixedSize(self.input_btn_size)
        self.combo_hours.addItem('отработано')
        [self.combo_hours.addItem(str(i) + 'ч.') for i in range(1, 25)]
        self.combo_hours.setStyleSheet(Styles.workers_combo())
        self.combo_hours.activated.connect(self.table_report.edit_report)
        # статус работника (полный день, отгул, отпуск, больничный)
        self.combo_status = QComboBox(self, objectName='combo_status')
        list_status = ['полный день', 'б/с', 'отпуск', 'больничный', 'прогул']
        self.combo_status.addItems(list_status)
        self.combo_status.setFixedSize(self.input_btn_size)
        self.combo_status.setStyleSheet(Styles.workers_combo())
        self.combo_status.activated.connect(self.table_report.edit_report)
        #  поле ввода примечания
        self.input_decription = QTextEdit(self)
        self.input_decription.setFixedSize(QSize(150, 200))
        self.input_decription.setStyleSheet(Styles.input_text())
        self.input_decription.setAlignment(Qt.AlignTop)
        self.input_decription.setPlaceholderText('введите перечень работ.')
        # кнопка "записать примечание"
        self.btn_insert_description = QPushButton('записать', self)
        self.btn_insert_description.setIconSize(self.icon_size)
        self.btn_insert_description.setFixedSize(self.input_btn_size)
        self.btn_insert_description.setStyleSheet(Styles.workers_btn())
        self.btn_insert_description.clicked.connect(self.table_report.edit_report)

        self.edit_layout.addWidget(self.combo_hours)

        if self.table_report.show_panel_mode == 1:
            # смена (день/ночь)
            self.combo_time_of_day = QComboBox(self, objectName='combo_time_of_day')
            list_time_of_day = ['смена', 'день', 'ночь']
            self.combo_time_of_day.addItems(list_time_of_day)
            self.combo_time_of_day.setFixedSize(self.input_btn_size)
            self.combo_time_of_day.setStyleSheet(Styles.workers_combo())
            self.combo_time_of_day.activated.connect(self.table_report.edit_report)
            self.edit_layout.addWidget(self.combo_time_of_day)
            # оценка
            self.combo_rating = QComboBox(self, objectName='combo_rating')
            self.combo_rating.setFixedSize(self.input_btn_size)
            self.combo_rating.addItems(['оценка', '1', '2', '3'])
            self.combo_rating.setStyleSheet(Styles.workers_combo())
            self.combo_rating.activated.connect(self.table_report.edit_report)
            self.edit_layout.addWidget(self.combo_rating)
            # место работы (НУФ/Чапаева)
            self.combo_place = QComboBox(self, objectName='combo_place')
            self.combo_place.addItems(['НУФ', 'Чапаева'])
            self.combo_place.setFixedSize(self.input_btn_size)
            self.combo_place.setStyleSheet(Styles.workers_combo())
            self.combo_place.activated.connect(self.table_report.edit_report)
            self.edit_layout.addWidget(self.combo_place)
            # выбор типа расписания рабочих дней
            self.combo_type_scheduler = QComboBox(self, objectName='combo_type_scheduler')
            self.combo_type_scheduler.addItems(['ДД-НН-ОВ', 'ДН-ОВ', 'очистить'])
            self.combo_type_scheduler.setFixedSize(self.input_btn_size)
            self.combo_type_scheduler.setStyleSheet(Styles.workers_combo())
            self.combo_type_scheduler.activated.connect(self.table_report.edit_report)
            self.scheduler_layout.addWidget(self.combo_type_scheduler)
            # кнопка "сгенерировать расписание"
            self.btn_generate_scheduler = QPushButton('сгенерировать', self, objectName='btn_generate_scheduler')
            self.btn_generate_scheduler.setIconSize(self.icon_size)
            self.btn_generate_scheduler.setFixedSize(self.input_btn_size)
            self.btn_generate_scheduler.setStyleSheet(Styles.workers_btn())
            self.btn_generate_scheduler.clicked.connect(self.table_report.generate_schedules)
            self.scheduler_layout.addWidget(self.btn_generate_scheduler)
            #  подсказки
            self.combo_rating.setToolTip('оценка')
            self.combo_place.setToolTip('площадка')
            self.combo_type_scheduler.setToolTip('тип расписания')
            self.combo_time_of_day.setToolTip('смена')
            #  курсоры
            self.combo_rating.setCursor(Qt.PointingHandCursor)
            self.combo_place.setCursor(Qt.PointingHandCursor)
            self.combo_type_scheduler.setCursor(Qt.PointingHandCursor)
            self.btn_generate_scheduler.setCursor(Qt.PointingHandCursor)
            self.combo_time_of_day.setCursor(Qt.PointingHandCursor)

        self.edit_layout.addWidget(self.combo_status)
        self.edit_layout.addWidget(self.input_decription)
        self.edit_layout.addWidget(self.btn_insert_description)

        # курсоры
        self.btn_refresh.setCursor(Qt.PointingHandCursor)
        self.btn_paste.setCursor(Qt.PointingHandCursor)
        self.btn_clear.setCursor(Qt.PointingHandCursor)
        self.btn_copy.setCursor(Qt.PointingHandCursor)
        self.combo_hours.setCursor(Qt.PointingHandCursor)
        self.combo_status.setCursor(Qt.PointingHandCursor)
        self.btn_insert_description.setCursor(Qt.PointingHandCursor)
        self.combo_years.setCursor(Qt.PointingHandCursor)
        self.combo_month.setCursor(Qt.PointingHandCursor)
        self.combo_role.setCursor(Qt.PointingHandCursor)
        self.combo_gild.setCursor(Qt.PointingHandCursor)

        #  подсказки
        self.combo_hours.setToolTip('отработано часов')
        self.combo_month.setToolTip('фильтр по месяцу')
        self.combo_years.setToolTip('фильтр по году')
        self.combo_role.setToolTip('фильтр по должности')
        self.combo_gild.setToolTip('фильтр по цеху/отделу')
        self.combo_status.setToolTip('статус дня')

    def get_list_role(self):
        try:
            with connect(**DataBase.config()) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(DataBase.sql_list_role())
                    list_role_out = ['Все сотрудники'] + [item for t in cursor.fetchall() for item in t if
                                                          isinstance(item, str)]
                    return list_role_out
        except:
            pass

    def get_list_gild(self):
        try:
            with connect(**DataBase.config()) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(DataBase.sql_list_gild())
                    list_role_out = ['Все цеха/отделы'] + [item for t in cursor.fetchall() for item in t if
                                                           isinstance(item, str)]
                    return list_role_out
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
                        all_date_dict[str(date[0])][str(date[1])] = str(date[2])
                    return all_date_dict
        except:
            pass

    def change_list_month(self):
        self.combo_month.clear()
        self.list_month = list(self.get_list_dates()[self.combo_years.currentText()].values())
        self.combo_month.addItems(self.list_month)

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
        if self.findChild(QPushButton, name='btn_generate_scheduler') is not None:
            self.btn_generate_scheduler.deleteLater()

        self.edit_layout.removeWidget(self.input_decription)
        self.edit_layout.removeWidget(self.btn_insert_description)


# класс - таблица
class TableReport(QTableWidget):
    def __init__(self, wg):
        super().__init__(wg)
        self.row = self.currentRow()
        self.col = self.currentColumn()
        self.buff_copy_time_of_day = None
        self.buff_copy_description = None
        self.buff_copy_place = None
        self.filter_role = None
        self.filter_gild = None
        self.filter_month = None
        self.filter_year = None
        self.reports = None
        self.reports_dict = None
        self.buff_copy_hours = None
        self.buff_copy_rating = None
        self.buff_copy_status = None
        self.change_panel = False

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
            self.filter_role = 'rs.role'
            self.filter_gild = 'gd.gild'
            self.filter_year = str(datetime.now().date().year)
            self.filter_month = str(datetime.now().date().month)
        else:
            months = {'Январь': '1', 'Февраль': '2', 'Март': '3', 'Апрель': '4', 'Май': '5', 'Июнь': '6',
                      'Июль': '7', 'Август': '8', 'Сентябрь': '9', 'Октябрь': '10', 'Ноябрь': '11', 'Декабрь': '12'}
            combo_role_text = self.wg.combo_role.currentText()
            self.filter_role = ("'" + combo_role_text + "'", 'rs.role')[combo_role_text == 'Все сотрудники']
            combo_gild_text = self.wg.combo_gild.currentText()
            self.filter_gild = ("'" + combo_gild_text + "'", 'gd.gild')[combo_gild_text == 'Все цеха/отделы']
            self.filter_year = self.wg.combo_years.currentText()
            self.filter_month = months[self.wg.combo_month.currentText()]

    def get_reports(self):
        try:
            with connect(**DataBase.config()) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        DataBase.sql_read_workers_report(self.filter_role, self.filter_year, self.filter_month,
                                                         self.filter_gild))
                    self.reports = cursor.fetchall()
                    id_report = 0
                    new_reports_dict = dict()
                    for report in self.reports:
                        if id_report != report[7]:
                            new_reports_dict[report[7]] = dict()
                            id_report = report[7]
                        new_reports_dict[report[7]][report[8]] = {'role': report[13], 'hour': report[4], 'rating': report[5], 'status': report[6], 'place': report[10], 'time_of_day': report[11], 'description': report[12]}
                    return new_reports_dict
        except:
            pass

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
            id_worker = int(self.item(row, 2).text())
            id_date = int(self.item(0, col).text())
            if self.reports_dict[id_worker][id_date]['role'] in [2, 3]:
                self.show_panel_mode = 1
            else:
                self.show_panel_mode = 2

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

    def paste_report(self):
        if self.col > 2 and self.row > 0:
            hour = self.buff_copy_hours
            if self.wg.findChild(QComboBox, name='combo_rating') is not None:
                rating = self.buff_copy_rating
            else:
                rating = 0
            status = self.buff_copy_status
            if self.wg.findChild(QComboBox, name='combo_place') is not None:
                place = self.buff_copy_place
            else:
                place = 0
            if self.wg.findChild(QComboBox, name='combo_time_of_day') is not None:
                time_of_day = self.buff_copy_time_of_day
            else:
                time_of_day = 0
            description = self.buff_copy_description
            id_worker = int(self.item(self.row, 2).text())
            id_date = int(self.item(0, self.col).text())
            if hour is not None and rating is not None and status is not None:
                self.write_report(hour, rating, status, place, time_of_day, description, id_worker, id_date)

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
            description = self.wg.input_decription.toPlainText()
            self.write_report(hour, rating, status, place, time_of_day, description, id_worker, id_date)

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
            self.write_report(hour, rating, status, place, time_of_day, description, id_worker, id_date)

    def write_report(self, hour, rating, status, place, time_of_day, description, id_worker, id_date):
        try:
            with connect(**DataBase.config()) as conn:
                conn.autocommit = True
                with conn.cursor() as cursor:
                    cursor.execute(DataBase.sql_edit_table(),
                                   (hour, rating, status, place, time_of_day, description, id_worker, id_date))
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
        current_row = self.currentRow()
        current_col = self.currentColumn()
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
        self.setCurrentCell(current_row, current_col)

    # обновление таблицы
    def bild_table(self):
        start_time = time.time()
        scroll = self.verticalScrollBar()
        old_position_scroll = scroll.value() / (scroll.maximum() or 1)
        self.setColumnCount(0)
        self.setRowCount(0)
        dates = self.get_dates(self.filter_year, self.filter_month)
        self.reports_dict = self.get_reports()

        fio_dict = {report[7]: report[0] + ' ' + report[1][:1] + '. ' + report[2][:1] + '.' for report in
                    self.reports}

        dates_dict = {1: 'пн', 2: 'вт', 3: 'ср', 4: 'чт', 5: 'пт', 6: 'сб', 7: 'вс'}
        i = 0
        for i in range(len(dates) + 3):
            self.setColumnCount(self.columnCount() + 1)
            self.horizontalHeader().setSectionResizeMode(i, QHeaderView.Stretch)
            self.setHorizontalHeaderItem(i, QTableWidgetItem(str(i - 2) + '\n' + dates_dict[dates[i - 3][2]]))
        self.setRowCount(self.rowCount() + 1)

        i = 3
        for date in dates:
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

        worker_hours = QtWidgets.QLabel(('', str(data_hour))[data_hour != 0])
        worker_hours.setFont(QFont("CalibriLight", 12, QtGui.QFont.Bold))
        worker_hours.setStyleSheet(Styles.color_hours(data_hour))

        worker_place = QtWidgets.QLabel(('', 'чп')[data_place == 1])
        worker_place.setFont(QFont("CalibriLight", 10, QtGui.QFont.Normal))
        worker_place.setStyleSheet('color: rgb(100, 100, 100);')

        cell_layout = QVBoxLayout()
        cell_layout.setContentsMargins(1, 1, 1, 1)

        upper_layout = QHBoxLayout()
        upper_layout.setContentsMargins(0, 0, 0, 0)

        dict_data_status = {'0': '', '1': 'бс', '2': 'от', '3': 'бл', '4': 'пр'}
        worker_status = QtWidgets.QLabel(dict_data_status.get(data_status))
        worker_status.setFont(QFont("CalibriLight", 10, QtGui.QFont.Normal))
        worker_status.setStyleSheet('color: rgb(150, 150, 150);')
        upper_layout.addStretch(0)

        if data_description is not None and data_description != '':
            lbl_descript = QLabel()
            lbl_descript.setPixmap(self.pix_descript)
            upper_layout.addStretch(0)
            upper_layout.addWidget(lbl_descript)
            upper_layout.addStretch(0)

        upper_layout.addStretch(0)

        if data_rating > 0:
            worker_rating = QtWidgets.QLabel(('', str(data_rating))[data_rating != 0])
            worker_rating.setFont(QFont("CalibriLight", 10, QtGui.QFont.Normal))
            worker_rating.setStyleSheet('color: rgb(150, 150, 150);')
            upper_layout.addWidget(worker_rating)

            upper_layout.addStretch(0)

        center_layout = QHBoxLayout()
        center_layout.setContentsMargins(0, 0, 0, 0)
        center_layout.addStretch(0)
        center_layout.addWidget(worker_hours)
        center_layout.addStretch(0)

        lower_layout = QHBoxLayout()
        lower_layout.setContentsMargins(0, 0, 0, 0)
        lower_layout.addWidget(worker_place)
        lower_layout.addStretch(0)

        if data_time_of_day > 0:
            time_of_day = QtWidgets.QLabel(('', str(data_time_of_day))[data_time_of_day != 0])
            time_of_day.setFont(QFont("CalibriLight", 10, QtGui.QFont.Normal))
            time_of_day.setStyleSheet('color: rgb(150, 150, 150);')

            lower_layout.addWidget(time_of_day)

        cell_layout.addLayout(upper_layout)
        cell_layout.addLayout(center_layout)
        cell_layout.addLayout(lower_layout)
        cell_layout.setSpacing(0)
        widget = QWidget()
        widget.setLayout(cell_layout)
        self.setCellWidget(i, j + 3, widget)

    def generate_schedules(self):
        id_worker = int(self.item(self.row, 2).text())
        id_date = int(self.item(0, self.col).text())
        self.set_filter_table()
        dates = self.get_dates(self.filter_year, self.filter_month)
        work_day = 1
        work_type = [6, 4, 0]
        type_scheduler = self.wg.combo_type_scheduler.currentIndex()
        for date in dates:
            if date[0] >= id_date:
                if type_scheduler != 2:
                    self.copy_report()
                    if work_day in ([1, 2], [1])[type_scheduler == 0]:
                        self.buff_copy_time_of_day = 1
                    elif work_day in ([3, 4], [2])[type_scheduler == 0]:
                        self.buff_copy_time_of_day = 2
                    else:
                        self.buff_copy_time_of_day = 0
                else:
                    self.buff_copy_time_of_day = 0
                self.paste_report()
                self.col += 1
                work_day = (work_day + 1, 1)[work_day == work_type[type_scheduler]]
        self.check_table()
        pass