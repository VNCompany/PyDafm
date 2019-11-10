from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QMessageBox


class Searcher(QDialog):
    def __init__(self):
        super(Searcher, self).__init__()
        uic.loadUi("designer/search.ui", self)
        self.calendar.setVisible(False)

        self.search_list.currentIndexChanged.connect(self.selected_index_changed)
        self.calendar.selectionChanged.connect(self.calendar_selection_changed)
        self.search_btn.clicked.connect(self.search_clicked)

        self.result = 0
        self.search_string = ""
        self.case_im = False
        self.search_columns = 0

    def selected_index_changed(self, index: int):
        if index == 6:
            if not self.calendar.isVisible():
                self.calendar.setVisible(True)
        else:
            if self.calendar.isVisible():
                self.calendar.setVisible(False)

    def calendar_selection_changed(self):
        self.search_text.setText(self.calendar.selectedDate().toString("yyyy-MM-dd"))

    def search_clicked(self):
        if self.search_text.text() != "":
            self.result = 1
            self.search_string = self.search_text.text()
            self.case_im = self.search_case.isChecked()
            self.search_columns = self.search_list.currentIndex()
            self.close()
        else:
            QMessageBox.warning(self, "Ошибка", "Введите строку поиска!")
