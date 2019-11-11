from PyQt5 import uic
from PyQt5.QtWidgets import QDialog

from dbm import *


class DebtInfo(QDialog):
    def __init__(self, dbm: DataBaseManager, debt: Debt):
        try:
            super(DebtInfo, self).__init__()
            uic.loadUi("designer/debt_info.ui", self)
            self.dbm = dbm
            self.debt = debt
            self.amount = debt.amount

            self.payment_btn.clicked.connect(self.payment_btn_clicked)
            self.initial_values()
        except Exception as ex:
            print(ex)

    def initial_values(self):
        self.debtor_value.setText(self.debt.debtor)
        self.amount_value.setText(str(self.debt.amount))
        self.priority_value.setText(PRIORITIES_LIST2[self.debt.priority])
        self.date_value.setText(DataBaseManager.strd_from_str(self.debt.date))
        self.description_value.setPlainText(self.debt.description)

    def payment_btn_clicked(self):
        try:
            self.dbm.add_payment(self.debt.id, self.payment)
        except Exception as ex:
            print(str(ex))

    def payment(self, amount):
        amount = int(amount)
        if (amount - int(self.payment_value.value())) >= 0:
            val = amount - int(self.payment_value.value())
            self.amount = int(val)
            self.amount_value.setText(str(self.amount))
            return str(val)
        else:
            return str(amount)
