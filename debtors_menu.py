from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QAction
from PyQt5.QtGui import QKeyEvent
from PyQt5.QtCore import Qt

from dbm import *
from custom_dialog import CustomDialog
from debtor_editor import DebtorEditor


class DebtorsMenu(QDialog):
    def __init__(self, dbm: DataBaseManager):
        super(DebtorsMenu, self).__init__()
        uic.loadUi("designer/debtors_menu.ui", self)
        self.dbm = dbm
        self.debtors = []
        self.update_debtors_list()
        self.set_items_to_list()
        self.update_main_list = False

        self.edit_search.textChanged.connect(self.searching)

        act_delete = QAction("Удалить должника", self)
        act_delete.triggered.connect(self.delete_element)

        act_edit = QAction("Изменить", self)
        act_edit.triggered.connect(self.edit_element)

        self.list_debtors.addAction(act_delete)
        self.list_debtors.addAction(act_edit)

    def update_debtors_list(self):
        self.debtors = self.dbm.get_debtors()

    def get_string_debtors(self):
        return [str(item) for item in self.debtors]

    def set_items_to_list(self, items: list = None):
        self.list_debtors.clear()
        self.list_debtors.addItems(items if items is not None else self.get_string_debtors())

    def searching(self):
        searched_elements = []
        s_text = self.edit_search.text()
        for i in self.get_string_debtors():
            if str(s_text).lower() in str(i).lower():
                searched_elements.append(i)
        self.set_items_to_list(searched_elements)

    def delete_element(self):
        if len(self.list_debtors.selectedItems()) == 1:
            cd = CustomDialog()
            cd.set_headers("Вы уверены?", "Удаление должника может повлечь за "
                                          "собой удаление \n"
                                          "всех его долгов. \n Удалить "
                                          "должника и все его задолжности?",
                           "Да", "Нет")
            cd.exec_()
            if cd.result == cd.CUSTOM_DIALOG_RESULT_OK:
                item = self.list_debtors.currentItem()
                self.dbm.delete_debtor(item.text())
                self.list_debtors.takeItem(self.list_debtors.currentRow())
                self.update_debtors_list()

    def edit_element(self):
        if len(self.list_debtors.selectedItems()) == 1:
            debtor = list(filter(lambda l: l.name == self.list_debtors.currentItem().text(),
                                 self.debtors))[0]
            de = DebtorEditor(self.get_string_debtors(), debtor)
            de.exec_()
            if de.result == 1:
                self.dbm.edit_debtor(de.debtor, debtor.name)
                self.update_debtors_list()
                self.set_items_to_list()
                self.update_main_list = True

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key_Delete:
            self.delete_element()
