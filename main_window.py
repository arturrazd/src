from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget, QHBoxLayout, QLabel, QStackedLayout, QFrame
from workers_window import WorkersWindow
from table_window import TableWindow
from styles import Styles as styles


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.right_widget = None
        self.setWindowTitle("Collective")
        self.setWindowIcon(QtGui.QIcon('icon.png'))
        self.setStyleSheet(styles.main_window())
        self.workers_window = WorkersWindow()
        self.table_window = TableWindow()

        # создание кнопок панели бокового меню
        self.btn_1 = QPushButton('', self)
        self.btn_2 = QPushButton('', self)
        self.btn_3 = QPushButton('', self)

        # всплывающие подсказки для кнопок
        self.btn_1.setToolTip('табель')
        self.btn_2.setToolTip('список сотрудников')
        self.btn_3.setToolTip('отчеты')
        # икноки для кнопок
        self.btn_1.setFixedSize(40, 40)
        self.btn_1.setIcon(QtGui.QIcon('icon_btn1.png'))
        self.btn_1.setIconSize(QtCore.QSize(20, 20))
        self.btn_2.setFixedSize(40, 40)
        self.btn_2.setIcon(QtGui.QIcon('icon_btn2.png'))
        self.btn_2.setIconSize(QtCore.QSize(20, 20))
        self.btn_3.setFixedSize(40, 40)
        self.btn_3.setIcon(QtGui.QIcon('icon_btn3.png'))
        self.btn_3.setIconSize(QtCore.QSize(20, 20))
        # курсоры для кнопок
        self.btn_1.setCursor(Qt.PointingHandCursor)
        self.btn_2.setCursor(Qt.PointingHandCursor)
        self.btn_3.setCursor(Qt.PointingHandCursor)
        # сыбытия нажатий на кнопоки
        self.btn_1.clicked.connect(self.button1)
        self.btn_2.clicked.connect(self.button2)
        self.btn_3.clicked.connect(self.button3)

        self.page_layout = QVBoxLayout()
        self.button_layout = QHBoxLayout()

        self.button_layout.addWidget(self.btn_1)
        self.button_layout.addWidget(self.btn_2)
        self.button_layout.addWidget(self.btn_3)
        self.button_layout.addStretch(0)
        self.button_layout.setSpacing(10)

        self.page_layout.addLayout(self.button_layout)

        self.stack_layout = QStackedLayout()
        self.page_layout.addLayout(self.stack_layout)

        self.stack_layout.addWidget(self.table_window)
        self.stack_layout.addWidget(self.workers_window)

        self.main_widget = QWidget()
        self.main_widget.setLayout(self.page_layout)
        self.setCentralWidget(self.main_widget)
        # при запуске активируем нажатие первой кнопки
        self.button1()

    def button1(self):
        self.stack_layout.setCurrentIndex(0)
        self.btn_1.setStyleSheet(styles.main_btn(True))
        self.btn_2.setStyleSheet(styles.main_btn(False))
        self.btn_3.setStyleSheet(styles.main_btn(False))

    def button2(self):
        self.stack_layout.setCurrentIndex(1)
        self.btn_1.setStyleSheet(styles.main_btn(False))
        self.btn_2.setStyleSheet(styles.main_btn(True))
        self.btn_3.setStyleSheet(styles.main_btn(False))

    def button3(self):
        self.stack_layout.setCurrentIndex(2)
        self.btn_1.setStyleSheet(styles.main_btn(False))
        self.btn_2.setStyleSheet(styles.main_btn(False))
        self.btn_3.setStyleSheet(styles.main_btn(True))


