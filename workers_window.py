from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QPushButton, QWidget, QLineEdit, QTableWidget, QTableWidgetItem, QComboBox
from psycopg2 import connect
from data_base import DataBase as db
from styles import Styles as styles


class WorkersWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.TableWorkers = TableWorkers(self)
        self.TableWorkers.upd_table()
        # кнопка "обновить"
        self.btn_refresh = QPushButton('обновить', self)
        self.btn_refresh.resize(150, 30)
        self.btn_refresh.move(1000, 10)
        self.btn_refresh.setStyleSheet(styles.workres_btn())
        self.btn_refresh.clicked.connect(self.TableWorkers.upd_table)
        self.btn_refresh.clicked.connect(self.upd_lables)
        # фамилия
        self.input_sname = QLineEdit(self)
        self.input_sname.resize(150, 30)
        self.input_sname.move(1000, 60)
        self.input_sname.setStyleSheet(styles.workers_input())
        # имя
        self.input_fname = QLineEdit(self)
        self.input_fname.resize(150, 30)
        self.input_fname.move(1000, 110)
        self.input_fname.setStyleSheet(styles.workers_input())
        # отчество
        self.input_lname = QLineEdit(self)
        self.input_lname.resize(150, 30)
        self.input_lname.move(1000, 160)
        self.input_lname.setStyleSheet(styles.workers_input())
        # должность
        self.combo_role = QComboBox(self)
        self.list_role = self.list_role()
        self.combo_role.addItems(self.list_role)
        self.combo_role.resize(150, 30)
        self.combo_role.move(1000, 210)
        self.combo_role.setStyleSheet(styles.workers_combo())
        # цех/служба
        self.combo_gild = QComboBox(self)
        self.list_gild = self.list_gild()
        self.combo_gild.addItems(self.list_gild)
        self.combo_gild.resize(150, 30)
        self.combo_gild.move(1000, 260)
        self.combo_gild.setStyleSheet(styles.workers_combo())
        # идентификатор
        self.id = QLineEdit(self)
        self.id.resize(150, 30)
        self.id.move(1000, 310)
        self.id.setStyleSheet(styles.workers_input())
        self.id.setReadOnly(True)
        #self.id.setVisible(False)
        # кнопка изменить запись
        self.btn_edit = QPushButton('изменить', self)
        self.btn_edit.resize(150, 30)
        self.btn_edit.move(1000, 310)
        self.btn_edit.setStyleSheet(styles.workres_btn())
        self.btn_edit.clicked.connect(self.edit_worker)
        # кнопка добавить запись
        self.btn_add = QPushButton('добавить', self)
        self.btn_add.resize(150, 30)
        self.btn_add.move(1000, 360)
        self.btn_add.setStyleSheet(styles.workres_btn())
        self.btn_add.clicked.connect(self.add_worker)
        # кнопка удалить запись
        self.btn_del = QPushButton('удалить', self)
        self.btn_del.resize(150, 30)
        self.btn_del.move(1000, 410)
        self.btn_del.setStyleSheet(styles.workres_btn())
        self.btn_del.clicked.connect(self.del_worker)
        # курсоры
        self.btn_refresh.setCursor(Qt.PointingHandCursor)
        self.btn_add.setCursor(Qt.PointingHandCursor)
        self.btn_del.setCursor(Qt.PointingHandCursor)
        self.combo_role.setCursor(Qt.PointingHandCursor)
        self.combo_gild.setCursor(Qt.PointingHandCursor)

    # обнулить поля ввода
    def upd_lables(self):
        self.id.setText('')
        self.input_sname.setText('')
        self.input_fname.setText('')
        self.input_lname.setText('')
        self.combo_role.setCurrentIndex(0)
        self.combo_gild.setCurrentIndex(0)

    def add_worker(self):
        index_role = self.combo_role.currentIndex()
        index_gild = self.combo_gild.currentIndex()
        try:
            with connect(**db.config()) as conn:
                with conn.cursor() as cur:
                    cur.execute(db.sql_add_worker(), (self.input_sname.text(), self.input_fname.text(),
                                                      self.input_lname.text(), index_role,
                                                      index_gild))
        except:
            pass
        self.TableWorkers.upd_table()

    def edit_worker(self):
        index_role = self.combo_role.currentIndex()
        index_gild = self.combo_gild.currentIndex()
        try:
            with connect(**db.config()) as conn:
                with conn.cursor() as cur:
                    cur.execute(db.sql_edit_worker(), (self.input_sname.text(), self.input_fname.text(),
                                                       self.input_lname.text(), index_role,
                                                       index_gild, self.id.text()))
        except:
            pass
        self.TableWorkers.upd_table()

    def del_worker(self):
        try:
            ids = int(self.id.text())
        except:
            return
        with connect(**db.config()) as conn:
            with conn.cursor() as cur:
                cur.execute(db.sql_del_worker(), (ids,))
        self.TableWorkers.upd_table()

    def list_role(self):
        try:
            with connect(**db.config()) as conn:
                with conn.cursor() as cur:
                    cur.execute(db.sql_list_role())
                    list_role_out = [''] + [item for t in cur.fetchall() for item in t if
                                                     isinstance(item, str)]
                    return list_role_out
        except:
            pass

    def list_gild(self):
        try:
            with connect(**db.config()) as conn:
                with conn.cursor() as cur:
                    cur.execute(db.sql_list_gild())
                    list_gild_out = [''] + [item for t in cur.fetchall() for item in t if
                                                      isinstance(item, str)]
                    return list_gild_out
        except:
            pass


# класс - таблица
class TableWorkers(QTableWidget):
    def __init__(self, wg):
        self.wg = wg
        super().__init__(wg)
        self.setGeometry(10, 10, 300, 900)
        self.setColumnCount(5)
        self.setStyleSheet(styles.workers_table())
        self.verticalHeader().hide()
        self.setEditTriggers(QTableWidget.NoEditTriggers)  # запретить изменять поля
        self.cellClicked.connect(self.click_table)  # установить обработчик щелча мыши в таблице

    # обработка щелчка мыши по таблице
    def click_table(self, row, col):  # row - номер строки, col - номер столбца
        self.wg.TableWorkers.selectRow(row)
        #self.wg.id.setText(self.item(row, 5).text())
        #TableWorkers.ids = self.item(row, 5).text()
        self.wg.input_sname.setText(self.item(row, 0).text().strip())
        self.wg.input_fname.setText(self.item(row, 1).text().strip())
        self.wg.input_lname.setText(self.item(row, 2).text().strip())
        self.wg.combo_role.setCurrentIndex(int(self.item(row, 3).text()))
        self.wg.combo_gild.setCurrentIndex(int(self.item(row, 4).text()))

    # обновление таблицы
    def upd_table(self):
        self.clear()
        self.setRowCount(0)
        self.setHorizontalHeaderLabels(
            ['Фамилия', 'Имя', 'Отчество', 'Должность', 'Цех/Служба', 'Идентификатор'])
        with connect(**db.config()) as conn:
            with conn.cursor() as cur:
                cur.execute(db.sql_read_workers())
                rows = cur.fetchall()
            i = 0
            for row in rows:
                self.setRowCount(self.rowCount() + 1)
                j = 0
                for elem in row:
                    self.setItem(i, j, QTableWidgetItem(str(elem).strip()))
                    j += 1
                i += 1
        self.resizeColumnsToContents()
