from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidget, QTableWidgetItem, QAction
from PyQt5.QtWidgets import QHeaderView
from PyQt5.QtGui import QColor, QIcon
from PyQt5.QtCore import Qt
from PyQt5 import uic

from dbm import *
from custom_dialog import CustomDialog


class Main(QMainWindow):
    def __init__(self, database: DataBaseManager):
        super().__init__()
        uic.loadUi("./designer/main.ui", self)
        self.dbm = database
        self.priorities = self.dbm.get_priorities()
        self.setWindowIcon(QIcon("content/icon.ico"))

        self.update_monitor()

        self.sorting_list.currentIndexChanged.connect(self.sorting_type_changed)
        self.refresh_btn.clicked.connect(self.update_monitor)

        # Header width
        self.monitor_table.setColumnWidth(0, 50)
        self.monitor_table.setColumnWidth(1, 100)
        self.monitor_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.monitor_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.monitor_table.horizontalHeader().setSectionResizeMode(4, QHeaderView.Stretch)
        self.monitor_table.setColumnWidth(5, 100)

        # Context menu
        act = QAction("Удалить", self)
        act.triggered.connect(self.delete_trigger)

        self.monitor_table.addAction(act)

    def update_monitor(self, debts=None):
        if debts is None:
            debts = self.dbm.get_debts(sorting=self.sorting_list.currentIndex())

        self.monitor_table.setRowCount(len(debts))
        for i, debt in enumerate(debts):
            for j, cell in enumerate([debt.id, self.priorities[debt.priority].name,
                                      debt.debtor,
                                      str(debt.amount) + " р",
                                      debt.description,
                                      self.dbm.strd_from_str(debt.date)]):
                table_item = QTableWidgetItem()
                table_item.setText(str(cell))
                item_color = QColor()
                item_color.setNamedColor(self.priorities[debt.priority].color)
                table_item.setBackground(item_color)
                table_item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsDragEnabled)
                self.monitor_table.setItem(i, j, table_item)
        self.update_statistic(debts)

    def update_statistic(self, debts=None):
        if debts is None:
            debts = self.dbm.get_debts()
        amount_iterator = list(map(lambda l: l.amount, debts))

        if len(amount_iterator) > 0:
            self.sum_amount.setText(str(sum(amount_iterator)) + " р")
            self.max_amount.setText(str(max(amount_iterator)) + " р")
            self.min_amount.setText(str(min(amount_iterator)) + " р")
        else:
            self.sum_amount.setText("0" + " р")
            self.max_amount.setText("0" + " р")
            self.min_amount.setText("0" + " р")

        self.debtors_count.setText(str(self.dbm.get_debtors_count()))
        self.debts_count.setText(str(len(amount_iterator)))

    def sorting_type_changed(self):
        self.update_monitor()

    def delete_trigger(self):
        sel_items = self.monitor_table.selectedItems()
        if len(sel_items) > 0:
            dlg = CustomDialog()
            dlg.exec_()
            if dlg.result == dlg.CUSTOM_DIALOG_RESULT_OK:
                self.delete_debt(sel_items[0])

    def delete_debt(self, selectedItem: QTableWidgetItem):
        if selectedItem is not None:
            row = selectedItem.row()
            id = self.monitor_table.item(row, 0).text()
            self.dbm.delete_debt(id)
            self.monitor_table.removeRow(row)
            self.update_statistic()

    def search(self, all_debts, search_string: str, columns, case_sensitive: bool):
        searcher = []
        if case_sensitive:
            search_string = search_string.lower()
        for debt in all_debts:
            if columns == 0:
                if search_string == str(debt.id) or \
                        search_string in debt.debtor or \
                        search_string == str(debt.amount) or \
                        search_string in debt.description or \
                        search_string in PRIORITIES_LIST2[int(debt.priority)] or \
                        search_string in self.dbm.strd_from_str(debt.date):
                    searcher.append(debt)
            elif columns == 1 and search_string == str(debt.id):
                searcher.append(debt)
            elif columns == 2 and search_string in PRIORITIES_LIST2[int(debt.priority)]:
                searcher.append(debt)
            elif columns == 3 and search_string in debt.debtor:
                searcher.append(debt)
            elif columns == 4 and search_string == str(debt.amount):
                searcher.append(debt)
            elif columns == 5 and search_string in str(debt.description):
                searcher.append(debt)
            elif columns == 6 and (search_string in self.dbm.strd_from_str(debt.date) or
                                   search_string in debt.date):
                searcher.append(debt)
        return searcher
