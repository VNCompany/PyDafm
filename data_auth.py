from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QMessageBox

from dbm import *


class DataAuthEditor(QDialog):
    def __init__(self, dbm: DataBaseManager):
        super(DataAuthEditor, self).__init__()
        uic.loadUi("designer/data_auth.ui", self)
        self.dbm = dbm
        self.auth_btn.clicked.connect(self.auth_clicked)
        self.login_text.setText(self.dbm.get_login())

    def auth_clicked(self):
        login = self.login_text.text()
        pw = self.pw_text.text()
        pw2 = self.pw2_text.text()
        if login != "" and pw != "" and pw2 != "":
            if self.dbm.valid_password(pw):
                self.dbm.set_auth_data(login, pw2)
                self.close()
                QMessageBox.information(self, "Данные изменены", "Логин и пароль изменены!")
            else:
                self.close()
                QMessageBox.warning(self, "Ошибка", "Введён неправильный текущий пароль!")
        elif login != "" and pw == "" and pw2 == "":
            self.dbm.edit_login(login)
            self.close()
            QMessageBox.information(self, "Данные изменены", "Логин изменён!")
        elif login == "" and pw != "" and pw2 != "":
            if self.dbm.valid_password(pw):
                self.dbm.edit_pw(pw2)
                self.close()
                QMessageBox.information(self, "Данные изменены", "Пароль изменён!")
            else:
                self.close()
                QMessageBox.warning(self, "Ошибка", "Введён неправильный текущий пароль!")
        else:
            self.close()
