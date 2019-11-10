from PyQt5 import uic
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import QDate
from dbm import *
from debtor_editor import DebtorEditor


class DebtEditor(QDialog):
    def __init__(self, dbm: DataBaseManager, debt: Debt = None):
        super(DebtEditor, self).__init__()
        uic.loadUi("designer/debt_editor.ui", self)
        self.id = 0
        self.result = -1

        self.dbm = dbm

        self.debtors_list = list(map(lambda l: l.name, dbm.get_debtors()))
        self.add_items_on_dlist()

        if debt is not None:
            self.add_btn.setText("Редактировать")
            self.set_values(debt)

        self.debtor_priority.setChecked(True)
        self.priority_value.setEnabled(False)

        self.add_btn.clicked.connect(self.add_clicked)
        self.debtor_priority.stateChanged.connect(self.dp_check_changed)
        self.new_debtor_btn.clicked.connect(self.add_new_debtor)

    def set_values(self, debt: Debt):
        self.debtor_value.setCurrentText(debt.debtor)
        self.amount_value.setValue(int(debt.amount))
        self.desc_value.setPlainText(debt.description)
        self.priority_value.setCurrentIndex(debt.priority)
        self.priority_value.setEnabled(True)
        self.debtor_priority.setChecked(False)
        simple_date = QDate()
        simple_date.fromString(debt.date)
        self.date_value.setSelectedDate(simple_date)
        self.id = debt.id

    def get_values(self, debtor_priority=None):
        debtor = self.debtor_value.currentText()
        amount = int(self.amount_value.text())
        desc = self.desc_value.toPlainText()
        priority = self.priority_value.currentIndex() \
            if not self.debtor_priority.isChecked() else debtor_priority
        date = self.date_value.selectedDate().toString("yyyy-MM-dd")
        debt = Debt(self.id, debtor, amount, desc, priority, date)
        return debt

    def add_clicked(self):
        print(self.debtor_value.currentText())

    def dp_check_changed(self):
        if self.sender().isChecked():
            self.priority_value.setEnabled(False)
        else:
            self.priority_value.setEnabled(True)

    def add_items_on_dlist(self):
        self.debtor_value.clearEditText()
        self.debtor_value.clear()
        for item in self.debtors_list:
            self.debtor_value.addItem(item)

    def add_new_debtor(self):
        add_debtor = DebtorEditor(self.debtors_list)
        add_debtor.exec_()
        if add_debtor.result == 1:
            self.dbm.add_debtor(add_debtor.debtor.name, add_debtor.debtor.priority)
            self.debtors_list = list(map(lambda l: l.name, self.dbm.get_debtors()))
            self.add_items_on_dlist()
