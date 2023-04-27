from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget, QTabWidget, QHBoxLayout, QLabel
from workers_window import WorkersWindow as ww
from styles import Styles as styles



class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.right_widget = None
        self.setWindowTitle("Collective")
        self.setWindowIcon(QtGui.QIcon('icon.png'))
        self.setStyleSheet("MainWindow { background: rgb(50, 50, 50) }")
        self.WorkersWindow = ww()


        # создание кнопок панели бокового меню
        self.btn_1 = QPushButton('', self)
        self.btn_2 = QPushButton('', self)
        self.btn_3 = QPushButton('', self)
        self.btn_4 = QPushButton('', self)

        # оформелние кнопок панели бокового меню
        self.btn_1.setStyleSheet(styles.main_btn())
        self.btn_2.setStyleSheet(styles.main_btn())
        self.btn_3.setStyleSheet(styles.main_btn())
        self.btn_4.setStyleSheet(styles.main_btn())

        # икноки для кнопок
        self.btn_1.setFixedSize(64, 100)
        self.btn_1.setIcon(QtGui.QIcon('icon_btn1.png'))
        self.btn_1.setIconSize(QtCore.QSize(64, 64))
        self.btn_2.setFixedSize(64, 100)
        self.btn_2.setIcon(QtGui.QIcon('icon_btn2.png'))
        self.btn_2.setIconSize(QtCore.QSize(64, 64))
        self.btn_3.setFixedSize(64, 100)
        self.btn_3.setIcon(QtGui.QIcon('icon_btn3.png'))
        self.btn_3.setIconSize(QtCore.QSize(64, 64))
        self.btn_4.setFixedSize(64, 100)
        self.btn_4.setIcon(QtGui.QIcon('icon_btn4.png'))
        self.btn_4.setIconSize(QtCore.QSize(64, 64))

        # курсоры для кнопок
        self.btn_1.setCursor(Qt.PointingHandCursor)
        self.btn_2.setCursor(Qt.PointingHandCursor)
        self.btn_3.setCursor(Qt.PointingHandCursor)
        self.btn_4.setCursor(Qt.PointingHandCursor)

        # сыбытия нажатий на кнопоки
        self.btn_1.clicked.connect(self.button1)
        self.btn_2.clicked.connect(self.button2)
        self.btn_3.clicked.connect(self.button3)
        self.btn_4.clicked.connect(self.button4)

        # создание боковых вкладок
        self.tab1 = self.page1()
        self.tab2 = self.page2()
        self.tab3 = self.page3()
        self.tab4 = self.page4()

        self.initUI()

    def initUI(self):
        left_layout = QVBoxLayout()
        left_layout.addWidget(self.btn_1)
        left_layout.addWidget(self.btn_2)
        left_layout.addWidget(self.btn_3)
        left_layout.addWidget(self.btn_4)
        left_widget = QWidget()
        left_widget.setLayout(left_layout)

        self.right_widget = QTabWidget()
        self.right_widget.tabBar().setObjectName("mainTab")
        self.right_widget.addTab(self.tab1, '')
        self.right_widget.addTab(self.tab2, '')
        self.right_widget.addTab(self.tab3, '')
        self.right_widget.addTab(self.tab4, '')
        self.right_widget.setCurrentIndex(0)
        self.right_widget.setStyleSheet('QTabBar::tab{width: 0; \
            height: 0; margin: 0; padding: 0; border: none;}')

        main_layout = QHBoxLayout()
        main_layout.addWidget(left_widget)
        main_layout.addWidget(self.right_widget)
        main_layout.setStretch(0, 5)
        main_layout.setStretch(1, 300)
        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        main_widget.setStyleSheet("border:none;")
        self.setCentralWidget(main_widget)

    def button1(self):
        self.right_widget.setCurrentIndex(0)

    def button2(self):
        self.right_widget.setCurrentIndex(1)

    def button3(self):
        self.right_widget.setCurrentIndex(2)

    def button4(self):
        self.right_widget.setCurrentIndex(3)

    def page1(self):
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.WorkersWindow)
        main = QWidget()
        main.setLayout(main_layout)
        main.setStyleSheet(styles.pages())
        return main

    def page2(self):
        main_layout = QVBoxLayout()
        main_layout.addWidget(QLabel('page 2'))
        main_layout.addStretch(5)
        main = QWidget()
        main.setLayout(main_layout)
        return main

    def page3(self):
        main_layout = QVBoxLayout()
        main_layout.addWidget(QLabel('page 3'))
        main_layout.addStretch(5)
        main = QWidget()
        main.setLayout(main_layout)
        return main

    def page4(self):
        main_layout = QVBoxLayout()
        main_layout.addWidget(QLabel('page 4'))
        main_layout.addStretch(5)
        main = QWidget()
        main.setLayout(main_layout)
        return main
