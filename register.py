from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5 import uic
from dbm import *
from main import Main
import os


class Registration(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi("designer/registration.ui", self)
        self.setWindowTitle("Регистрация")
        self.dbm = DataBaseManager()
        self.mn = None
        self.result = -1
        self.auth_btn.clicked.connect(self.auth_clicked)

    def auth_clicked(self):
        try:
            login = self.login_text.text()
            pw = self.pw_text.text()
            pw2 = self.pw2_text.text()
            if login != "" and pw != "" and pw2 != "":
                if pw == pw2:
                    self.dbm.create_all_tables()
                    self.dbm.create_priories()
                    self.dbm.set_auth_data(login, pw)
                    if os.path.exists("startup"):
                        os.remove("startup")
                    self.mn = Main(self.dbm)
                    self.mn.show()
                    self.hide()
                else:
                    QMessageBox.warning(self, "Ошибка", "Пароли не совпадают.")
            else:
                QMessageBox.warning(self, "Ошибка", "Заполните пустые поля!")
        except Exception as ex:
            self.dbm.log.append(LOG_ERROR, "Fatal error on registration. " + str(ex))
