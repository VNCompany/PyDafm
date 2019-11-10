from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5 import uic
from dbm import *
from main import Main


class Authorization(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi("designer/authorization.ui", self)
        self.setWindowTitle("Вход")
        self.dbm = DataBaseManager()
        self.mn = Main(self.dbm)
        self.auth_btn.clicked.connect(self.auth_clicked)

    def auth_clicked(self):
        login = self.login_text.text()
        pw = self.pw_text.text()
        if self.dbm.auth(login, pw):
            self.mn.show()
            self.hide()
        else:
            QMessageBox.warning(self, "Ошибка входа", "Неверный логин или пароль!")
