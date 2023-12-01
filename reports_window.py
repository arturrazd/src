import locale

from PyQt5 import QtWebEngineWidgets, QtCore, QtGui, QtPrintSupport
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtPrintSupport import QPrintPreviewDialog
from PyQt5.QtWidgets import *
from styles import Styles
from data_base import DataBase

locale.setlocale(category=locale.LC_ALL, locale="Russian")


class ReportsWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.main_btn_size = QSize(35, 35)
        self.input_btn_size = QSize(200, 30)
        self.icon_size = QSize(15, 15)

        self.report_view = QtWebEngineWidgets.QWebEngineView()
        self.report_view.setContentsMargins(0, 0, 0, 0)

        self.panel_layout = QVBoxLayout()
        self.panel_layout.setContentsMargins(0, 0, 0, 0)

        self.btn_layout = QGridLayout()
        self.btn_layout.setContentsMargins(0, 0, 0, 0)

        self.panel_layout.addLayout(self.btn_layout)

        self.page_layout = QHBoxLayout()
        self.page_layout.setContentsMargins(0, 0, 0, 0)
        self.page_layout.addWidget(self.report_view)
        self.page_layout.addLayout(self.panel_layout)

        self.report_dict = dict()

        #self.workers_list =

        self.html_content = ''

        self.show_element_panel()

        self.setLayout(self.page_layout)

    def show_element_panel(self):
        self.create_btn_report_hours()
        self.create_btn_report_place()
        self.create_btn_print()

    def create_btn_report_hours(self):
        btn_report_hours = QPushButton('отработанное время', self)
        btn_report_hours.setIconSize(self.icon_size)
        btn_report_hours.setFixedSize(self.input_btn_size)
        btn_report_hours.setStyleSheet(Styles.workers_btn())
        btn_report_hours.clicked.connect(self.show_report_hour)
        btn_report_hours.setCursor(Qt.PointingHandCursor)
        self.btn_layout.addWidget(btn_report_hours, 1, Qt.AlignCenter)

    def create_btn_report_place(self):
        btn_report_place = QPushButton('площадка работы', self)
        btn_report_place.setIconSize(self.icon_size)
        btn_report_place.setFixedSize(self.input_btn_size)
        btn_report_place.setStyleSheet(Styles.workers_btn())
        btn_report_place.clicked.connect(self.show_report_place)
        btn_report_place.setCursor(Qt.PointingHandCursor)
        self.btn_layout.addWidget(btn_report_place, 2, Qt.AlignCenter)

    def create_btn_print(self):
        btn_print = QPushButton('печать', self)
        btn_print.setIconSize(self.icon_size)
        btn_print.setFixedSize(self.input_btn_size)
        btn_print.setStyleSheet(Styles.workers_btn())
        btn_print.clicked.connect(self.print_report)
        btn_print.setCursor(Qt.PointingHandCursor)
        self.panel_layout.addStretch()
        self.panel_layout.addWidget(btn_print)

    def show_report_hour(self):

        for key, value in self.report_dict.items():
            pass
            # self.html_content += '<table>'
            # self.html_content += '<tr>'
            # self.html_content += '<td></td>'
            # self.html_content +=
            # self.html_content +=
            # self.html_content +=
            # self.html_content +=
            # self.html_content +=
            # self.html_content +=




    def show_report_place(self):
        self.report_view.setHtml(self.html_content)

    def print_report(self):
        printer = QtPrintSupport.QPrinter(QtPrintSupport.QPrinter.PrinterResolution)
        printer.setOutputFormat(QtPrintSupport.QPrinter.PdfFormat)
        printer.setPaperSize(QtPrintSupport.QPrinter.A4)
        printer.setOrientation(QtPrintSupport.QPrinter.Portrait)

        self.doc = QtGui.QTextDocument()

        self.doc.setHtml(self.html_content)
        self.doc.setPageSize(QtCore.QSizeF(printer.pageRect().size()))

        permit_preview = QPrintPreviewDialog()
        permit_preview.setFixedSize(1000, 1000)

        permit_preview.paintRequested.connect(self.print_preview)

        permit_preview.exec_()

    def print_preview(self, printer):
        document = self.doc
        document.print_(printer)

