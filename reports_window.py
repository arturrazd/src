import locale

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QColor
from PyQt5.QtWidgets import *
from psycopg2 import connect

from data_base import DataBase
from styles import Styles

locale.setlocale(category=locale.LC_ALL, locale="Russian")


class ReportsWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.main_btn_size = QSize(35, 35)
        self.input_btn_size = QSize(200, 30)
        self.icon_size = QSize(15, 15)

        self.list_role = list()
        self.list_guild = list()
        self.dict_guilds = dict()

        self.reports_tree = ReportsTree()

        self.btn_report = QPushButton('выбор', self, objectName='btn_report')
        self.btn_report.setFixedSize(self.input_btn_size)
        self.btn_report.setStyleSheet(Styles.workers_btn())

        self.page_layout = QHBoxLayout()
        self.page_layout.setContentsMargins(0, 0, 0, 0)
        self.panel_layout = QVBoxLayout()
        self.panel_layout.setContentsMargins(0, 0, 10, 0)
        self.input_layout = QVBoxLayout()
        self.input_layout.setContentsMargins(20, 0, 10, 2)

        self.input_layout.addWidget(self.btn_report)
        self.input_layout.setSpacing(2)

        self.panel_layout.addLayout(self.input_layout)
        self.panel_layout.addStretch(0)
        self.panel_layout.setSpacing(2)
        self.page_layout.addWidget(self.reports_tree)
        self.page_layout.addLayout(self.panel_layout)
        self.page_layout.setSpacing(0)

        self.setLayout(self.page_layout)

# класс - таблица
class ReportsTree(QTreeView):
    def __init__(self):
        super().__init__()

        self.dict_guilds = None
        self.list_role = None
        self.list_guild = None

        list_role = self.get_list_role()

        self.treeview = QtWidgets.QTreeView()
        self.treeview.setHeaderHidden(True)

        treeModel = QStandardItemModel()
        rootNode = treeModel.invisibleRootItem()


    def get_list_role(self):
        try:
            with connect(**DataBase.config()) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(DataBase.sql_list_role())
                    list_role = cursor.fetchall()
                    self.list_role = list_role
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


