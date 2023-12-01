import locale
from datetime import datetime
from PyQt5.QtGui import QIntValidator, QColor
from styles import AlignDelegate
from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import *
from data_base import DataBase
from data_base import select_workers, insert_worker, select_date, insert_report, update_worker, delete_worker
from styles import Styles

locale.setlocale(category=locale.LC_ALL, locale="Russian")


class WorkersWindow(QWidget):
    def __init__(self, list_roles, list_guilds, dict_guilds):
        super().__init__()

        main_btn_size = QSize(35, 35)
        input_btn_size = QSize(200, 30)
        icon_size = QSize(15, 15)

        self.list_roles = list_roles
        self.list_guilds = list_guilds
        self.dict_guilds = dict_guilds

        self.table_workers = TableWorkers(self)
        # кнопка "обновить"
        self.btn_refresh = QPushButton('', self)
        self.btn_refresh.setIcon(QtGui.QIcon('refresh.png'))
        self.btn_refresh.setIconSize(icon_size)
        self.btn_refresh.setFixedSize(main_btn_size)
        self.btn_refresh.setStyleSheet(Styles.workers_btn())
        self.btn_refresh.clicked.connect(self.table_workers.upd_table)
        self.btn_refresh.clicked.connect(self.upd_labels)
        # табельный номер
        self.input_tabel_number = QLineEdit(self)
        onlyInt = QIntValidator()
        onlyInt.setRange(0, 1000000)
        self.input_tabel_number.setValidator(onlyInt)
        self.input_tabel_number.setFixedSize(input_btn_size)
        self.input_tabel_number.setStyleSheet(Styles.workers_input())
        self.input_tabel_number.setPlaceholderText('табельный номер')
        # фамилия
        self.input_sname = QLineEdit(self)
        self.input_sname.setFixedSize(input_btn_size)
        self.input_sname.setStyleSheet(Styles.workers_input())
        self.input_sname.setPlaceholderText('фамилия')
        # имя
        self.input_fname = QLineEdit(self)
        self.input_fname.setFixedSize(input_btn_size)
        self.input_fname.setStyleSheet(Styles.workers_input())
        self.input_fname.setPlaceholderText('имя')
        # отчество
        self.input_lname = QLineEdit(self)
        self.input_lname.setFixedSize(input_btn_size)
        self.input_lname.setStyleSheet(Styles.workers_input())
        self.input_lname.setPlaceholderText('отчество')
        # должность
        self.combo_role = QComboBox(self)
        self.combo_role.addItems(['должность'] + self.list_roles)
        self.combo_role.setFixedSize(input_btn_size)
        self.combo_role.setStyleSheet(Styles.workers_combo())
        self.combo_role.activated.connect(self.table_workers.get_change_list_guild)
        # цех/служба
        self.combo_guild = QComboBox(self)
        self.combo_guild.addItem('специальность')
        self.combo_guild.setFixedSize(input_btn_size)
        self.combo_guild.setStyleSheet(Styles.workers_combo())
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
        self.combo_guild.setCursor(Qt.PointingHandCursor)
        self.btn_edit.setCursor(Qt.PointingHandCursor)
        self.table_workers.setCursor(Qt.PointingHandCursor)

        self.input_tabel_number.setToolTip('табельный номер')
        self.input_sname.setToolTip('фамилия')
        self.input_fname.setToolTip('имя')
        self.input_lname.setToolTip('отчество')
        self.combo_role.setToolTip('должность')
        self.combo_guild.setToolTip('специальность')

        self.page_layout = QHBoxLayout()
        self.page_layout.setContentsMargins(0, 0, 0, 0)
        self.panel_layout = QVBoxLayout()
        self.panel_layout.setContentsMargins(0, 0, 10, 0)
        self.button_layout = QHBoxLayout()
        self.button_layout.setContentsMargins(20, 0, 10, 0)
        self.input_layout = QVBoxLayout()
        self.input_layout.setContentsMargins(20, 0, 10, 2)

        self.button_layout.addWidget(self.btn_refresh)
        self.button_layout.addWidget(self.btn_add)
        self.button_layout.addWidget(self.btn_edit)
        self.button_layout.addWidget(self.btn_del)
        self.button_layout.setSpacing(20)

        self.input_layout.addWidget(self.input_tabel_number)
        self.input_layout.addWidget(self.input_sname)
        self.input_layout.addWidget(self.input_fname)
        self.input_layout.addWidget(self.input_lname)
        self.input_layout.addWidget(self.combo_role)
        self.input_layout.addWidget(self.combo_guild)
        self.input_layout.setSpacing(2)

        self.panel_layout.addLayout(self.button_layout)
        self.panel_layout.addLayout(self.input_layout)
        self.panel_layout.addStretch(0)
        self.panel_layout.setSpacing(2)
        self.page_layout.addWidget(self.table_workers)
        self.page_layout.addLayout(self.panel_layout)
        self.page_layout.setSpacing(0)

        self.setLayout(self.page_layout)

    # обнулить поля ввода
    def upd_labels(self):
        self.id.setText('')
        self.input_tabel_number.setText('')
        self.input_sname.setText('')
        self.input_fname.setText('')
        self.input_lname.setText('')
        self.combo_role.setCurrentIndex(0)
        self.combo_guild.clear()
        self.combo_guild.addItems(['цех/отдел'])

    def add_worker(self):
        name_guild = (self.combo_guild.currentText(), '-')[self.combo_guild.currentIndex() == -1]
        insert_id = insert_worker(self.input_sname.text(), self.input_fname.text(), self.input_lname.text(),
                                  self.combo_role.currentIndex(), name_guild, int(self.input_tabel_number.text()))
        self.table_workers.add_worker_report(insert_id)
        self.table_workers.upd_table()

    def edit_worker(self):
        name_guild = (self.combo_guild.currentText(), '-')[self.combo_guild.currentIndex() == -1]
        update_worker(self.input_sname.text(), self.input_fname.text(), self.input_lname.text(),
                      self.combo_role.currentIndex(), name_guild, self.input_tabel_number.text(),
                      int(self.id.text()))
        self.table_workers.upd_table()

    def del_worker(self):
        ids = int(self.id.text())
        delete_worker(ids)
        self.table_workers.upd_table()


# класс - таблица
class TableWorkers(QTableWidget):
    def __init__(self, wg):
        self.wg = wg
        super().__init__(wg)
        self.setColumnCount(8)
        self.setColumnHidden(1, True)  # скрываем 2 столбец с идентификатором работника
        self.verticalHeader().hide()
        self.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents)
        self.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeToContents)
        self.horizontalHeader().setSectionResizeMode(6, QHeaderView.Stretch)
        self.horizontalHeader().setSectionResizeMode(7, QHeaderView.Stretch)
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
        self.upd_table()

    # обработка щелчка мыши по таблице
    def click_table(self, row, col):  # row - номер строки, col - номер столбца
        self.wg.id.setText(self.item(row, 1).text())
        self.wg.input_tabel_number.setText(self.item(row, 2).text().strip())
        self.wg.input_sname.setText(self.item(row, 3).text().strip())
        self.wg.input_fname.setText(self.item(row, 4).text().strip())
        self.wg.input_lname.setText(self.item(row, 5).text().strip())
        self.wg.combo_role.setCurrentText(self.item(row, 6).text())
        self.get_change_list_guild()
        self.wg.combo_guild.setCurrentText(self.item(row, 7).text())

    # обновление таблицы
    def upd_table(self):
        current_row = self.currentRow()
        current_col = self.currentColumn()
        self.clear()
        self.setRowCount(0)
        self.setHorizontalHeaderLabels(
            ['№', '', 'Табельный \nномер', 'Фамилия', 'Имя', 'Отчество', 'Должность', 'Цех/Отдел'])
        delegate = AlignDelegate(self)
        self.setItemDelegateForColumn(0, delegate)
        self.setItemDelegateForColumn(2, delegate)
        self.setItemDelegateForColumn(6, delegate)
        self.setItemDelegateForColumn(7, delegate)
        i = 0
        rows = select_workers()
        for row in rows:
            self.setRowCount(self.rowCount() + 1)
            self.setItem(i, 0, QTableWidgetItem(str(i + 1)))
            j = 1
            for elem in row:
                self.setItem(i, j, QTableWidgetItem(str(elem).strip()))
                if j in [3, 4, 5]:
                    self.item(i, j).setForeground(QColor(200, 150, 0, 255))
                j += 1
            self.setRowHeight(i, 26)
            i += 1
        self.setCurrentCell(current_row, current_col)

    def add_worker_report(self, new_worker_id):
        cur_year = datetime.now().date().year
        cur_month = datetime.now().date().month
        for date in select_date(cur_year, cur_month):
            insert_report(date[0], new_worker_id)

    def get_change_list_guild(self):
        self.wg.combo_guild.clear()
        if self.wg.combo_role.currentIndex() > 0:
            current_role = self.wg.combo_role.currentText()
            current_list = self.wg.dict_guilds.get(current_role)
        else:
            current_list = ['специальность']
        self.wg.combo_guild.addItems(current_list)
