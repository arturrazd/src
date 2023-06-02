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
                            background-color: rgb(80, 80, 80); \
                            border: 1px solid gray; \
                            border-radius: 3px; \
                            font-family: Calibri Light; \
                            font: 15px; \
                            padding: 5px; \
                            } \
                    QToolTip \
                            { \
                            font-size: 15px; \
                            font-family: Calibri Light; \
                            color:  white; \
                            background-color: black; \
                            border: 0px solid gray; \
                            }"
        else:
            return "QPushButton \
                            { \
                            background-color: rgb(45, 45, 45); \
                            border: 1px solid rgb(100, 100, 100); \
                            border-radius: 3px; \
                            padding: 5px; \
                            } \
                    QPushButton:hover \
                            { \
                            background-color: rgb(70, 70, 70); \
                            padding: 5px; \
                            } \
                    QPushButton:pressed \
                            { \
                            background-color: rgb(120, 120, 120); \
                            padding: 5px; \
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
    def workres_btn():
        return "QPushButton \
                            { \
                            background-color: rgb(45, 45, 45); \
                            border: 1px outset rgb(60, 60, 60); \
                            border-radius: 3px; \
                            font-family: Calibri Light; \
                            font: 15px; \
                            padding: 0px; \
                            color: rgb(150, 150, 150); \
                            } \
                QPushButton:hover \
                            { \
                            border: 1px outset rgb(70, 70, 70); \
                            color: rgb(180, 180, 180); \
                            } \
                QPushButton:pressed \
                            { \
                            background-color: rgb(45, 45, 45); \
                            border-style: inset; \
                            }"

    @staticmethod
    def workers_input():
        return "QLineEdit { \
                            background-color: rgb(45, 45, 45); \
                            border: 1px outset rgb(60, 60, 60); \
                            border-radius: 3px; \
                            font-family: Calibri Light; \
                            font: 15px; \
                            padding: 0px; \
                            color: rgb(200, 200, 200);} \
                QLineEdit:hover \
                            { \
                            border: 1px outset rgb(70, 70, 70); \
                            } \
                QLineEdit:focus \
                            { \
                            background-color: rgb(30, 30, 30); \
                            border: 1px inset rgb(60, 60, 60); \
                            border-color: gray; \
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
                            color: rgb(200, 100, 0); \
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
    def table_header():
        return "QHeaderView::section \
                            { \
                            background-color: rgb(45, 45, 45); \
                            border: 1px solid rgb(70, 70, 70); \
                            color: rgb(200, 100, 0); \
                            font-size: 15px; \
                            font-family: Calibri Light; \
                           } \
                QHeaderView::selected \
                            { \
                            color: red; \
                            }"
    @staticmethod
    def workers_combo():
        return "QComboBox \
                        { \
                        background-color: rgb(45, 45, 45); \
                        border: 1px outset rgb(60, 60, 60); \
                        border-radius: 3px; \
                        font-family: Calibri Light; \
                        font: 15px; \
                        padding: 0px; \
                        color: rgb(200, 200, 200);} \
                        } \
                QComboBox::hover \
                        { \
                        border: 1px outset rgb(70, 70, 70); \
                        } \
                QComboBox:focus \
                        { \
                        background-color: rgb(45, 45, 45); \
                        border: 1px outset rgb(60, 60, 60); \
                        border-color: gray; \
                        padding: 0px; \
                        } \
                QComboBox::drop-down \
                        { \
                        border: 0px; \
                        } \
                QComboBox:on \
                        { \
                        background-color: rgb(30, 30, 30); \
                        border: 1px inset rgb(60, 60, 60); \
                        border-color: gray; \
                        padding: 0px; \
                        } \
                QComboBox QListView \
                        { \
                        font-size: 15px; \
                        font-family: Calibri Light; \
                        border: 1px outset rgb(60, 60, 60); \
                        padding: 5px; \
                        background-color: rgb(30, 30, 30); \
                        outline: 0px; \
                        color: rgb(200, 200, 200); \
                        } \
                QComboBox QListView:item \
                        { \
                        font-size: 15px; \
                        font-family: Calibri Light; \
                        padding-left: 10px; \
                        background-color: rgb(30, 30, 30); \
                        outline: 0px; \
                        color: rgb(200, 200, 200); \
                        } \
                QComboBox QListView::item::hover \
                        { \
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
    def color_rating(data_rating):
        rating_color = {1: 'color: rgb(255, 150, 0);', 2: 'color: rgb(200, 150, 0);',
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