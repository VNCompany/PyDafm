import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidget, QTableWidgetItem, QAction
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt
from PyQt5 import uic


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("./designer/main.ui", self)
