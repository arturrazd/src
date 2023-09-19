from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget, QHBoxLayout, QStackedLayout
from workers_window import WorkersWindow
from table_window import TableWindow
from styles import Styles


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Collective")
        self.setWindowIcon(QtGui.QIcon('icon.png'))
        self.setStyleSheet(Styles.main_window())
        self.main_btn_size = QSize(200, 50)
        self.workers_window = WorkersWindow()
        self.table_window = TableWindow()

        # создание кнопок панели бокового меню
        self.btn_1 = QPushButton('табель', self)
        self.btn_1.clicked.connect(self.table_window.table_report.check_table)
        self.btn_1.clicked.connect(self.table_window.table_report.click_cell)
        self.btn_2 = QPushButton('сотрудники', self)
        self.btn_3 = QPushButton('отчеты', self)
        # всплывающие подсказки для кнопок
        self.btn_1.setToolTip('табель')
        self.btn_2.setToolTip('список сотрудников')
        self.btn_3.setToolTip('отчеты')
        # размеры кнопок
        self.btn_1.setFixedSize(self.main_btn_size)
        self.btn_2.setFixedSize(self.main_btn_size)
        self.btn_3.setFixedSize(self.main_btn_size)
        # курсоры для кнопок
        self.btn_1.setCursor(Qt.PointingHandCursor)
        self.btn_2.setCursor(Qt.PointingHandCursor)
        self.btn_3.setCursor(Qt.PointingHandCursor)
        # сыбытия нажатий на кнопоки
        self.btn_1.clicked.connect(self.button1)
        self.btn_2.clicked.connect(self.button2)
        self.btn_3.clicked.connect(self.button3)

        self.page_layout = QVBoxLayout()
        self.page_layout.setContentsMargins(0, 0, 0, 0)
        self.button_layout = QHBoxLayout()

        self.button_layout.addWidget(self.btn_1)
        self.button_layout.addWidget(self.btn_2)
        self.button_layout.addWidget(self.btn_3)
        self.button_layout.addStretch(0)

        self.page_layout.addLayout(self.button_layout)

        self.stack_layout = QStackedLayout()
        self.page_layout.addLayout(self.stack_layout)
        self.stack_layout.addWidget(self.table_window)
        self.stack_layout.addWidget(self.workers_window)


        self.page_layout.setContentsMargins(0, 0, 0, 0)

        self.main_widget = QWidget()
        self.main_widget.setLayout(self.page_layout)
        self.setCentralWidget(self.main_widget)
        # при запуске активируем нажатие первой кнопки
        self.button1()

    def button1(self):
        self.stack_layout.setCurrentIndex(0)
        self.btn_1.setStyleSheet(Styles.main_btn(True))
        self.btn_2.setStyleSheet(Styles.main_btn(False))
        self.btn_3.setStyleSheet(Styles.main_btn(False))

    def button2(self):
        self.stack_layout.setCurrentIndex(1)
        self.btn_1.setStyleSheet(Styles.main_btn(False))
        self.btn_2.setStyleSheet(Styles.main_btn(True))
        self.btn_3.setStyleSheet(Styles.main_btn(False))

    def button3(self):
        self.stack_layout.setCurrentIndex(2)
        self.btn_1.setStyleSheet(Styles.main_btn(False))
        self.btn_2.setStyleSheet(Styles.main_btn(False))
        self.btn_3.setStyleSheet(Styles.main_btn(True))


