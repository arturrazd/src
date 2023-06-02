from PyQt5 import QtWidgets, QtCore


class Styles:
    def __init__(self):
        super().__init__()

    @staticmethod
    def main_window():
        return "MainWindow \
                            { \
                            background-color: rgb(40, 40, 40); \
                            border: 0px outset rgb(60, 60, 60); \
                            }"

    # оформелние кнопок панели бокового меню
    @staticmethod
    def main_btn(flag):
        if flag:
            return "QPushButton \
                            { \
                            background-color: rgb(60, 60, 60); \
                            border: none; \
                            font-family: Calibri Light; \
                            color: white; \
                            font: 30px; \
                            padding: 0px; \
                            } \
                    QToolTip \
                            { \
                            font-size: 15px; \
                            font-family: Calibri Light; \
                            color: white; \
                            background-color: black; \
                            border: 0px solid gray; \
                            }"
        else:
            return "QPushButton \
                            { \
                            background-color: transparent; \
                            border: none; \
                            font-family: Calibri Light; \
                            color: gray; \
                            font: 30px; \
                            padding: 0px; \
                            } \
                    QPushButton:hover \
                            { \
                            color: white; \
                            padding: 0px; \
                            } \
                    QPushButton:pressed \
                            { \
                            padding: 0px; \
                            } \
                    QToolTip \
                            { \
                            font-size: 15px; \
                            font-family: Calibri Light; \
                            color:  white; \
                            background-color: black; \
                            border: 0px solid gray; \
                            }"

    @staticmethod
    def workers_btn():
        return "QPushButton \
                            { \
                            background-color: rgb(60, 60, 60); \
                            border: none; \
                            border-radius: 0px; \
                            font-family: Calibri Light; \
                            font: 15px; \
                            padding: 0px; \
                            color: rgb(150, 150, 150); \
                            } \
                QPushButton:hover \
                            { \
                            background-color: rgb(80, 80, 80); \
                            border: 0px outset rgb(70, 70, 70); \
                            color: rgb(180, 180, 180); \
                            } \
                QPushButton:pressed \
                            { \
                            background-color: rgb(30, 30, 30); \
                            border-style: inset; \
                            }"

    @staticmethod
    def workers_input():
        return "QLineEdit { \
                            background-color: rgb(60, 60, 60); \
                            border: none; \
                            font-family: Calibri Light; \
                            font: 15px; \
                            padding: 0px; \
                            color: rgb(200, 200, 200); \
                            padding: 5px; \
                            } \
                QLineEdit:hover \
                            { \
                            background-color: rgb(80, 80, 80); \
                            } \
                QLineEdit:focus \
                            { \
                            background-color: rgb(30, 30, 30); \
                            padding: 5px; \
                            } \
                QToolTip \
                        { \
                        font-size: 15px; \
                        font-family: CalibriLight; \
                        color: white; \
                        background-color: black; \
                        border: 0px solid gray; \
                        }"

    @staticmethod
    def table_workers():
        return "QTableWidget \
                            { \
                            background-color: rgb(45, 45, 45); \
                            border: 1px solid rgb(100, 100, 100); \
                            border-radius: 3px; \
                            font-size: 15px; \
                            font-family: Calibri Light; \
                            color: rgb(200, 200, 200); \
                            gridline-color: rgb(70, 70, 70); \
                            outline: 0; \
                            } \
                QTableWidget::item::selected \
                            { \
                            background-color: rgb(40, 40, 40); \
                            color: white; \
                            }"

    @staticmethod
    def table_table():
        return "QTableWidget \
                            { \
                            background-color: rgb(45, 45, 45); \
                            border: 1px solid rgb(100, 100, 100); \
                            border-radius: 3px; \
                            font-size: 15px; \
                            font-family: Calibri Light; \
                            color: rgb(200, 200, 200); \
                            gridline-color: rgb(70, 70, 70); \
                            outline: 0; \
                            } \
                QTableWidget::item::selected \
                            { \
                            background-color: rgb(70, 70, 70); \
                            color: white; \
                            } \
                QTableWidget::item::hover \
                            { \
                            background-color: rgb(70, 70, 70); \
                            color: white; \
                            }"

    @staticmethod
    def hor_scrollbar():
        return "QScrollBar:horizontal \
                            { \
                            border: none; \
                            background-color: black; \
                            height: 10px; \
                            margin: 0px 0px 0px 0px; \
                            } \
                QScrollBar::handle:horizontal \
                            { \
                            border: 0px solid gray; \
                            background-color: rgb(70, 70, 70); \
                            } \
                QScrollBar::handle:hover:horizontal \
                            { \
                            background: rgb(45, 45, 45); \
                            }"



    @staticmethod
    def ver_scrollbar():
        return "QScrollBar \
                            { \
                            border: none; \
                            background-color: black; \
                            width: 10px; \
                            margin: 0px 0px 0px 0px; \
                            } \
                QScrollBar::handle \
                            { \
                            border: 0px solid gray; \
                            background-color: rgb(70, 70, 70); \
                            } \
                QScrollBar::handle:hover \
                            { \
                            background: rgb(45, 45, 45); \
                            }"

    @staticmethod
    def table_header():
        return "QHeaderView::section \
                            { \
                            background-color: rgb(45, 45, 45); \
                            border: 1px solid rgb(70, 70, 70); \
                            color: rgb(200, 100, 0); \
                            font-size: 15px; \
                            font-family: Calibri Light; \
                           }"

    @staticmethod
    def workers_combo():
        return "QComboBox \
                        { \
                        background-color: rgb(60, 60, 60); \
                        border: none; \
                        font-family: Calibri Light; \
                        font: 15px; \
                        padding: 5px; \
                        color: rgb(200, 200, 200);} \
                        } \
                QComboBox::hover \
                        { \
                        background-color: rgb(80, 80, 80); \
                        } \
                QComboBox:focus \
                        { \
                        background-color: rgb(45, 45, 45); \
                        border: none; \
                        padding: 5px; \
                        } \
                QComboBox::drop-down \
                        { \
                        border: 0px; \
                        } \
                QComboBox:on \
                        { \
                        background-color: rgb(30, 30, 30); \
                        border: none; \
                        border-color: gray; \
                        padding: 5px; \
                        } \
                QComboBox QListView \
                        { \
                        font-size: 15px; \
                        font-family: Calibri Light; \
                        border: none; \
                        padding: 5px; \
                        background-color: rgb(30, 30, 30); \
                        outline: 0px; \
                        color: rgb(200, 200, 200); \
                        } \
                QComboBox QListView:item \
                        { \
                        font-size: 15px; \
                        font-family: Calibri Light; \
                        padding-left: 5px; \
                        background-color: rgb(30, 30, 30); \
                        outline: 0px; \
                        color: rgb(200, 200, 200); \
                        } \
                QComboBox QListView::item::hover \
                        { \
                        background-color: rgb(30, 30, 30); \
                        color: rgb(10, 10, 10); \
                        } \
                QToolTip \
                        { \
                        font-size: 15px; \
                        font-family: CalibriLight; \
                        color: white; \
                        background-color: black; \
                        border: 0px solid gray; \
                        }"

    @staticmethod
    def input_text():
        return "QTextEdit \
                            { \
                            background-color: rgb(60, 60, 60); \
                            border: none; \
                            font-family: Calibri Light; \
                            font: 15px; \
                            padding: 5px; \
                            color: rgb(200, 200, 200); \
                            } \
                QTextEdit::hover \
                        { \
                        background-color: rgb(80, 80, 80); \
                        } \
                QTextEdit:focus \
                            { \
                            background-color: rgb(30, 30, 30); \
                            padding: 5px; \
                            } \
                QScrollBar \
                            { \
                            background: rgb(0, 0, 0); \
                            width: 10px \
                            } \
                QScrollBar::handle \
                            { \
                            background: rgb(40, 40, 40); \
                            } \
                QScrollBar::handle::pressed \
                            { \
                            background: rgb(10, 10, 10); \
                            }"

    @staticmethod
    def color_rating(data_rating):
        rating_color = {1: 'color: red;', 2: 'color: rgb(200, 150, 0);',
                        3: 'color: rgb(80, 150, 60);'}
        return rating_color.get(data_rating, '')

    @staticmethod
    def color_status(data_status):
        status_color = {1: 'color: rgb(150, 150, 150);', 2: 'color: rgb(80, 150, 60);',
                        3: 'color: rgb(200, 20, 20);'}
        return status_color.get(data_status, '')

    @staticmethod
    def color_hours(worker_rating):
        color_dict = {0: 'transparent'}
        return "color: " + color_dict.get(worker_rating, 'rgb(255, 255, 0)')


class AlignDelegate(QtWidgets.QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super(AlignDelegate, self).initStyleOption(option, index)
        option.displayAlignment = QtCore.Qt.AlignCenter
