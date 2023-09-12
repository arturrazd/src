import calendar
import locale
from datetime import datetime, timedelta
from styles import AlignDelegate
from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import *
from psycopg2 import connect
from data_base import DataBase
from styles import Styles

locale.setlocale(category=locale.LC_ALL, locale="Russian")


class WorkersWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.list_gild = None
        main_btn_size = QSize(30, 30)
        input_btn_size = QSize(150, 30)
        icon_size = QSize(15, 15)

        self.dict_gilds = dict()
        self.list_role = list()
        self.table_workers = TableWorkers(self)
        # кнопка "обновить"
        self.btn_refresh = QPushButton('', self)
        self.btn_refresh.setIcon(QtGui.QIcon('refresh.png'))
        self.btn_refresh.setIconSize(icon_size)
        self.btn_refresh.setFixedSize(main_btn_size)
        self.btn_refresh.setStyleSheet(Styles.workers_btn())
        self.btn_refresh.clicked.connect(self.table_workers.upd_table)
        self.btn_refresh.clicked.connect(self.upd_lables)
        # фамилия
        self.input_sname = QLineEdit(self)
        self.input_sname.setFixedSize(input_btn_size)
        self.input_sname.setStyleSheet(Styles.workers_input())
        # имя
        self.input_fname = QLineEdit(self)
        self.input_fname.setFixedSize(input_btn_size)
        self.input_fname.setStyleSheet(Styles.workers_input())
        # отчество
        self.input_lname = QLineEdit(self)
        self.input_lname.setFixedSize(input_btn_size)
        self.input_lname.setStyleSheet(Styles.workers_input())
        # должность
        self.combo_role = QComboBox(self)
        combo_list_role = self.get_list_role()
        self.combo_role.addItems(combo_list_role)
        self.combo_role.setFixedSize(input_btn_size)
        self.combo_role.setStyleSheet(Styles.workers_combo())
        self.combo_role.activated.connect(self.get_change_list_gild)
        # цех/служба
        self.combo_gild = QComboBox(self)
        self.get_list_gild()
        self.combo_gild.addItem('цех/отдел')
        self.combo_gild.setFixedSize(input_btn_size)
        self.combo_gild.setStyleSheet(Styles.workers_combo())
        # идентификатор (скрыт)
        self.id = QLineEdit(self)
        self.id.setFixedSize(input_btn_size)
        self.id.setStyleSheet(Styles.workers_input())
        self.id.setReadOnly(True)
        self.id.setVisible(False)
        # кнопка изменить запись
        self.btn_edit = QPushButton('', self)
        self.btn_edit.setIcon(QtGui.QIcon('edit_worker.png'))
        self.btn_edit.setIconSize(icon_size)
        self.btn_edit.setFixedSize(main_btn_size)
        self.btn_edit.setStyleSheet(Styles.workers_btn())
        self.btn_edit.clicked.connect(self.edit_worker)
        self.btn_edit.clicked.connect(self.table_workers.upd_table)
        # кнопка добавить запись
        self.btn_add = QPushButton('', self)
        self.btn_add.setIcon(QtGui.QIcon('add_worker.png'))
        self.btn_add.setIconSize(icon_size)
        self.btn_add.setFixedSize(main_btn_size)
        self.btn_add.setStyleSheet(Styles.workers_btn())
        self.btn_add.clicked.connect(self.add_worker)
        self.btn_add.clicked.connect(self.table_workers.upd_table)
        # кнопка удалить запись
        self.btn_del = QPushButton('', self)
        self.btn_del.setIcon(QtGui.QIcon('del_worker.png'))
        self.btn_del.setIconSize(icon_size)
        self.btn_del.setFixedSize(main_btn_size)
        self.btn_del.setStyleSheet(Styles.workers_btn())
        self.btn_del.clicked.connect(self.del_worker)
        self.btn_del.clicked.connect(self.table_workers.upd_table)
        # курсоры
        self.btn_refresh.setCursor(Qt.PointingHandCursor)
        self.btn_add.setCursor(Qt.PointingHandCursor)
        self.btn_del.setCursor(Qt.PointingHandCursor)
        self.combo_role.setCursor(Qt.PointingHandCursor)
        self.combo_gild.setCursor(Qt.PointingHandCursor)
        self.btn_edit.setCursor(Qt.PointingHandCursor)
        self.table_workers.setCursor(Qt.PointingHandCursor)

        self.input_sname.setToolTip('фамилия')
        self.input_fname.setToolTip('имя')
        self.input_lname.setToolTip('отчество')
        self.combo_role.setToolTip('должность')
        self.combo_gild.setToolTip('цех/отдел')

        self.page_layout = QHBoxLayout()
        self.page_layout.setContentsMargins(0, 0, 0, 0)
        self.panel_layout = QVBoxLayout()
        self.panel_layout.setContentsMargins(0, 0, 10, 0)
        self.button_layout = QHBoxLayout()
        self.button_layout.setContentsMargins(0, 0, 0, 0)
        self.input_layout = QVBoxLayout()
        self.input_layout.setContentsMargins(0, 0, 0, 0)

        self.button_layout.addWidget(self.btn_refresh)
        self.button_layout.addWidget(self.btn_add)
        self.button_layout.addWidget(self.btn_edit)
        self.button_layout.addWidget(self.btn_del)
        self.button_layout.setSpacing(10)

        self.input_layout.addWidget(self.input_sname)
        self.input_layout.addWidget(self.input_fname)
        self.input_layout.addWidget(self.input_lname)
        self.input_layout.addWidget(self.combo_role)
        self.input_layout.addWidget(self.combo_gild)
        self.input_layout.setSpacing(10)

        self.panel_layout.addLayout(self.button_layout)
        self.panel_layout.addLayout(self.input_layout)
        self.panel_layout.addStretch(0)
        self.panel_layout.setSpacing(10)
        self.page_layout.addWidget(self.table_workers)
        self.page_layout.addLayout(self.panel_layout)
        self.page_layout.setSpacing(10)

        self.setLayout(self.page_layout)

    # обнулить поля ввода
    def upd_lables(self):
        self.id.setText('')
        self.input_sname.setText('')
        self.input_fname.setText('')
        self.input_lname.setText('')
        self.combo_role.setCurrentIndex(0)
        self.combo_gild.clear()
        self.combo_gild.addItems(['цех/отдел'])

    def add_worker(self):
        index_role = self.combo_role.currentIndex()
        index_gild = self.combo_gild.currentIndex()
        try:
            with connect(**DataBase.config()) as conn:
                conn.autocommit = True
                with conn.cursor() as cursor:
                    cursor.execute(DataBase.sql_add_worker(), (self.input_sname.text(), self.input_fname.text(),
                                                               self.input_lname.text(), index_role,
                                                               index_gild))
                    insert_id = cursor.fetchone()

            self.table_workers.add_worker_report(insert_id)
            self.table_workers.upd_table()
        except:
            pass

    def edit_worker(self):
        index_role = self.combo_role.currentIndex()
        index_gild = self.combo_gild.currentIndex()
        try:
            with connect(**DataBase.config()) as conn:
                conn.autocommit = True
                with conn.cursor() as cursor:
                    cursor.execute(DataBase.sql_edit_worker(), (self.input_sname.text(), self.input_fname.text(),
                                                                self.input_lname.text(), index_role,
                                                                index_gild, int(self.id.text())))
        except:
            pass
        self.table_workers.upd_table()

    def del_worker(self):
        try:
            ids = int(self.id.text())
            with connect(**DataBase.config()) as conn:
                conn.autocommit = True
                with conn.cursor() as cursor:
                    cursor.execute(DataBase.sql_del_worker(), (ids,))
        except:
            pass
        self.table_workers.upd_table()

    def get_list_role(self):
        try:
            with connect(**DataBase.config()) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(DataBase.sql_list_role())
                    list_role = cursor.fetchall()
                    self.list_role = list_role
                    combo_list_role = ['должность'] + [item for t in self.list_role for item in t if
                                                       isinstance(item, str)]
                    return combo_list_role
        except:
            pass

    def get_list_gild(self):
        try:
            with connect(**DataBase.config()) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(DataBase.sql_list_gild())
                    self.list_gild = cursor.fetchall()
                    for role in self.list_role:
                        self.dict_gilds[role[1]] = []
                        for gild in self.list_gild:
                            if role[0] == gild[2]:
                                self.dict_gilds[role[1]].append(gild[1])
        except:
            pass

    def get_change_list_gild(self):
        self.combo_gild.clear()
        if self.combo_role.currentIndex() > 0:
            current_role = self.combo_role.currentText()
            current_list = self.dict_gilds.get(current_role)
        else:
            current_list = ['цех/отдел']
        self.combo_gild.addItems(current_list)


# класс - таблица
class TableWorkers(QTableWidget):
    def __init__(self, wg):
        self.wg = wg
        super().__init__(wg)
        self.setColumnCount(7)
        self.setColumnHidden(6, True)  # скрываем 7 столбец с идентификатором работника
        self.verticalHeader().hide()
        self.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.horizontalHeader().setSectionResizeMode(4, QHeaderView.Stretch)
        self.horizontalHeader().setSectionResizeMode(5, QHeaderView.Stretch)
        self.horizontalHeader().setSectionsClickable(False)
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setStyleSheet(Styles.table_workers())
        self.horizontalScrollBar().setStyleSheet(Styles.hor_scrollbar())
        self.verticalScrollBar().setStyleSheet(Styles.ver_scrollbar())
        self.horizontalHeader().setStyleSheet(Styles.table_header())
        self.setEditTriggers(QTableWidget.NoEditTriggers)  # запретить изменять поля
        self.cellClicked.connect(self.click_table)  # установить обработчик щелча мыши в таблице
        self.setMinimumSize(500, 500)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.add_month()
        self.upd_table()

    # обработка щелчка мыши по таблице
    def click_table(self, row, col):  # row - номер строки, col - номер столбца
        self.wg.id.setText(self.item(row, 6).text())
        self.wg.input_sname.setText(self.item(row, 1).text().strip())
        self.wg.input_fname.setText(self.item(row, 2).text().strip())
        self.wg.input_lname.setText(self.item(row, 3).text().strip())
        self.wg.combo_role.setCurrentText(self.item(row, 4).text())
        self.get_change_list_gild()
        self.wg.combo_gild.setCurrentText(self.item(row, 5).text())

    # обновление таблицы
    def upd_table(self):
        self.clear()
        self.setRowCount(0)
        self.setHorizontalHeaderLabels(
            ['№', 'Фамилия', 'Имя', 'Отчество', 'Должность', 'Цех/Отдел'])
        with connect(**DataBase.config()) as conn:
            with conn.cursor() as cursor:
                cursor.execute(DataBase.sql_read_workers_1())
                rows = cursor.fetchall()
                delegate = AlignDelegate(self)
                self.setItemDelegateForColumn(0, delegate)
                i = 0
                for row in rows:
                    self.setRowCount(self.rowCount() + 1)
                    self.setItem(i, 0, QTableWidgetItem(str(i + 1)))
                    j = 1
                    for elem in row:
                        self.setItem(i, j, QTableWidgetItem(str(elem).strip()))
                        j += 1
                    self.setRowHeight(i, 26)
                    i += 1

    def add_month(self):
        try:
            with connect(**DataBase.config()) as conn:
                conn.autocommit = True
                with conn.cursor() as cursor:
                    cur_year = datetime.now().date().year
                    cur_month = datetime.now().date().month
                    cursor.execute(DataBase.sql_read_date_report(), (cur_year, cur_month,))
                    date_list = cursor.fetchall()
                    if len(date_list) == 0:
                        monthrange = calendar.monthrange(cur_year, cur_month)
                        cursor.execute(DataBase.sql_read_date_report(), (cur_year, cur_month,))
                        date_list = cursor.fetchall()
                        cursor.execute(DataBase.sql_read_workers_2())
                        worker_list = cursor.fetchall()
                        first_number_day = monthrange[0] + 1
                        first_day = datetime.today().replace(day=1)
                        for day in range(monthrange[1]):
                            cursor.execute(DataBase.sql_insert_date_report(),
                                           (first_day + timedelta(days=day), first_number_day))
                            first_number_day = (first_number_day + 1, 1)[first_number_day > 6]
                            if len(worker_list) != 0:
                                for worker in worker_list:
                                    for date in date_list:
                                        cursor.execute(DataBase.sql_insert_workers_report(),
                                                       (date[0], worker[0], 0, 0, 0))
        except:
            pass

    def add_worker_report(self, new_worker_id):
        with connect(**DataBase.config()) as conn:
            conn.autocommit = True
            with conn.cursor() as cursor:
                cur_year = datetime.now().date().year
                cur_month = datetime.now().date().month
                cursor.execute(DataBase.sql_read_date_report(), (cur_year, cur_month,))
                date_list = cursor.fetchall()
                for date in date_list:
                    cursor.execute(DataBase.sql_insert_workers_report(), (date[0], new_worker_id, 0, 0, 0, 0, 0, '', 0))

    def get_change_list_gild(self):
        self.wg.combo_gild.clear()
        if self.wg.combo_role.currentIndex() > 0:
            current_role = self.wg.combo_role.currentText()
            current_list = self.wg.dict_gilds.get(current_role)
        else:
            current_list = ['цех/отдел']
        self.wg.combo_gild.addItems(current_list)
