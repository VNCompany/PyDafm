from PyQt5 import uic
from PyQt5.QtWidgets import QDialog


class CustomDialog(QDialog):
    CUSTOM_DIALOG_RESULT_CANCEL = 0
    CUSTOM_DIALOG_RESULT_OK = 1
    CUSTOM_DIALOG_RESULT_NO = 2

    def __init__(self):
        super(CustomDialog, self).__init__()
        uic.loadUi("designer/dialog_delete.ui", self)
        self.result = -1
        self.finished.connect(self.finish_click)
        self.ok_btn.clicked.connect(self.ok_click)
        self.no_btn.clicked.connect(self.no_click)

    def set_headers(self, title, text, yes_text, no_text):
        self.setWindowTitle(str(title))
        self.label_2.setText(str(title))
        self.label.setText(str(text))
        self.ok_btn.setText(str(yes_text))
        self.ok_btn.setFocus()
        self.no_btn.setText(str(no_text))

    def ok_click(self):
        self.result = 1
        self.close()

    def no_click(self):
        self.result = 2
        self.close()

    def finish_click(self):
        if self.result == -1:
            self.result = 0
