from PyQt5 import QtWidgets
from psycopg2 import connect
from data_base import DataBase as db
from data_base import select_requests
from main_window import MainWindow


class Login(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(Login, self).__init__(parent)
        self.list_app_users = list()
        self.first_connect()
        self.combo_name = QtWidgets.QComboBox(self)
        [self.combo_name.addItem(a[0]) for a in self.list_app_users]

        self.textPass = QtWidgets.QLineEdit(self)
        self.buttonLogin = QtWidgets.QPushButton('Login', self)
        self.buttonLogin.clicked.connect(self.handle_login)
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.combo_name)
        layout.addWidget(self.textPass)
        layout.addWidget(self.buttonLogin)

    def first_connect(self):
        try:
            login = 'col_engineer'
            password = 'coll'
            with connect(**db.init_connection(login, password)) as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT usename FROM pg_catalog.pg_user WHERE usename like 'col_%' ORDER BY usename")
                    self.list_app_users = cursor.fetchall()
        except:
            pass

    def handle_login(self):

        try:
            with connect(**db.init_connection(self.combo_name.currentText(), self.textPass.text())) as conn:
                self.accept()
                db.login = self.combo_name.currentText()
                db.password = self.textPass.text()
                select_requests()
        except:
            QtWidgets.QMessageBox.warning(self, 'Ошибка', 'Неверный пароль')


class Window(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    login = Login()
    if login.exec_() == QtWidgets.QDialog.Accepted:
        MainWindow = MainWindow()
        MainWindow.showMaximized()
        sys.exit(app.exec_())
