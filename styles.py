

class Styles:
    def __init__(self):
        super().__init__()

    # оформелние кнопок панели бокового меню
    @staticmethod
    def main_btn():
        return "QPushButton { \
                            background-color: rgba(150, 150, 150, 255); \
                            border: 1px outset gray; \
                            border-radius: 20px; \
                            font-family: Calibri Light; \
                            font: 15px; \
                            min-width: 5em; \
                            padding: 5px;} \
                QPushButton:hover   { \
                                    ackground-color: rgba(200, 200, 200, 255); \
                                    min-width: 5em; \
                                    padding: 5px;} \
                QPushButton:focus   { \
                                    background-color: white;\
                                    border-style: inset; \
                                    min-width: 5em; \
                                    padding: 5px;}"

    @staticmethod
    def workres_btn():
        return "QPushButton { \
                            background-color: rgba(70, 70, 70, 255); \
                            border: 1px outset gray; \
                            border-radius: 5px; \
                            font-family: Calibri Light; \
                            font: 15px; \
                            min-width: 5em; \
                            padding: 5px; \
                            color: rgb(150, 150, 150);} \
                QPushButton:hover   { \
                                    background-color: rgba(60, 60, 60, 255); \
                                    min-width: 5em; \
                                    padding: 5px;} \
                QPushButton:pressed { \
                                    background-color: gray; \
                                    border-style: inset; \
                                    min-width: 5em; \
                                    padding: 5px;}"

    @staticmethod
    def workers_input():
        return "QLineEdit { \
                            background-color: rgb(50, 50, 50); \
                            border: 1px solid gray; \
                            border-radius: 1px; \
                            font-family: Calibri Light; \
                            font: 15px; \
                            min-width: 5em; \
                            padding: 5px; \
                            color: rgb(150, 150, 150);} \
                QLineEdit:hover { \
                                background-color: rgb(40, 40, 40); \
                                min-width: 5em; \
                                padding: 5px;} \
                QLineEdit:focus { \
                                background-color: rgb(40, 40, 40); \
                                border-color: white; \
                                min-width: 5em; \
                                padding: 5px;}"
    @staticmethod
    def pages():
        return "QWidget \
                        { \
                        background-color: rgb(60, 60, 60);  \
                        border: 1px outset gray; \
                        border-style: solid;  \
                        border-width: 1px; \
                        border-radius: 0px; \
                        border-color: darkgray; \
                        font-family: Calibri Light; \
                        font: 15px; \
                        min-width: 900px; \
                        padding: 0px; \
                        }"

    @staticmethod
    def workers_table():
        return "QHeaderView::section \
                            { \
                            background:transparent; \
                            border:none; \
                            color: rgb(150, 150, 150); \
                            margin-left:0px; \
                            padding - left: 0px; \
                            }\
               QTableWidget \
                            { \
                            background-color: rgb(60, 60, 60); \
                            border:1px; \
                            font-size: 15px; \
                            font-family: Calibri Light; \
                            color: rgb(180, 180, 180); \
                            } \
                QTableWidget::item::selected \
                            { \
                            background-color: rgb(80, 80, 80); \
                            } \
                QTableWidget::item::hover \
                            { \
                            background-color: rgb(80, 80, 80); \
                            }"
    @staticmethod
    def workers_combo():
        return "QComboBox \
                        { \
                        background-color: rgb(50, 50, 50); \
                        border: 1px solid gray; \
                        border-radius: 1px; \
                        padding-left: 10px; \
                        min-width: 6em; \
                        color: rgb(150, 150, 150); \
                        } \
                QComboBox::hover \
                        { \
                        border-color: rgba(50, 50, 50, 0); \
                        } \
                QComboBox::drop-down \
                        { \
                        border: 0px; \
                        } \
                QComboBox:on \
                        { \
                        border: 1px solid gray; \
                        } \
                QComboBox QListView \
                        { \
                        font-size: 15px; \
                        border: 1px solid gray; \
                        padding: 5px; \
                        background-color: rgba(60, 60, 60, 255); \
                        outline: 0px; \
                        min-width: 6em; \
                        color: rgb(150, 150, 150); \
                        } \
                QComboBox QListView:item \
                        { \
                        padding-left: 10px; \
                        background-color: rgba(60, 60, 60, 255); \
                        } \
                QComboBox QListView::item:hover \
                        { \
                        background - color: rgba(60, 60, 60, 255); \
                        }"