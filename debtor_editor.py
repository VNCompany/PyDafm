from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QMessageBox

from objects import Debtor


class DebtorEditor(QDialog):
    def __init__(self, debtors: list, debtor: Debtor = None):
        super(DebtorEditor, self).__init__()
        uic.loadUi("designer/add_debtor.ui", self)
        self.id = 0
        self.result = -1
        self.ignore_exists = False
        self.debtor = None

        self.debtors_list = debtors

        if debtor is not None:
            self.set_values(debtor)
            self.add_btn.setText("Изменить")
            self.ignore_exists = True

        self.add_btn.clicked.connect(self.add_clicked)

    def set_values(self, debtor: Debtor):
        self.name_value.setText(debtor.name)
        self.priority_value.setCurrentIndex(debtor.priority)
        self.id = debtor.id

    def get_values(self):
        name = self.name_value.text()
        priority = self.priority_value.currentIndex()
        id = self.id
        return Debtor(id, name, priority)

    def add_clicked(self):
        if self.name_value.text() == "":
            QMessageBox.warning(self, "Ошибка", "Введите имя должника!")
            return
        if not self.ignore_exists and self.name_value.text() in self.debtors_list:
            QMessageBox.warning(self, "Ошибка", "Должник с таким именем уже есть в базе!")
            return
        self.result = 1
        self.debtor = self.get_values()
        self.close()
