import sys
from PyQt5.QtWidgets import QApplication
from forms.main import Main


# Главное вхождение программы
if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = Main()
    main_window.show()
    sys.exit(app.exec_())
