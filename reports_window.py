import locale
import threading

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
        self.workers_dict = dict()
        self.dates = tuple()
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

        self.html_content = ''

        dates_dict = {1: 'пн', 2: 'вт', 3: 'ср', 4: 'чт', 5: 'пт', 6: 'сб', 7: 'вс'}

        self.html_content += '<table border="1" width="100%" style="border-collapse: collapse; font-size: 5px; font-family: Calibri Light;">'

        self.html_content += '<thead>'
        self.html_content += '<tr valign=middle style="font-size:100%;">'
        self.html_content += '<th valign=middle style="width:2%">№<br>п/п</th>'
        self.html_content += '<th valign=middle style="width:5%">ФИО</th>'
        for i in range(len(self.dates)):
            self.html_content += '<th valign=middle style="width:2%">' + (str(i + 1) + '<br>' + dates_dict[self.dates[i][2]]) + '</th>'
        self.html_content += '</tr>'
        self.html_content += '</thead>'

        self.html_content += '<tbody>'
        i = 1
        for id_w, worker in self.workers_dict.items():
            self.html_content += '</tr>'
            self.html_content += '<td>' + str(i) + '</td>'
            self.html_content += '<td>' + worker + '</td>'
            for report in self.report_dict[id_w].values():
                self.html_content += '<td>' + str(report['hour']) + '</td>'
            self.html_content += '</tr>'
            i += 1
        self.html_content += '</tbody>'
        self.html_content += '</table>'
        self.report_view.setHtml(self.html_content)

    def show_report_place(self):
        self.report_view.setHtml(self.html_content)

    def print_report(self):
        printer = QtPrintSupport.QPrinter(QtPrintSupport.QPrinter.PrinterResolution)
        printer.setOutputFormat(QtPrintSupport.QPrinter.PdfFormat)
        printer.setPaperSize(QtPrintSupport.QPrinter.A4)
        printer.setOrientation(QtPrintSupport.QPrinter.Landscape)

        self.doc = QtGui.QTextDocument()
        self.doc.setHtml(self.html_content)
        self.doc.setPageSize(QtCore.QSizeF(printer.pageRect().size()))

        permit_preview = QPrintPreviewDialog()
        permit_preview.setFixedSize(1000, 1000)

        th = threading.Thread(target=self.show_report(permit_preview))
        th.start()

    def show_report(self, permit_preview):
        permit_preview.paintRequested.connect(self.print_preview)
        permit_preview.exec_()

    def print_preview(self, printer):
        document = self.doc
        document.print_(printer)

