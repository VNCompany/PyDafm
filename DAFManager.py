import sys
from PyQt5.QtWidgets import QApplication
from auth import Authorization
from register import Registration
import os.path


# Главное вхождение программы
if __name__ == '__main__':
    app = QApplication(sys.argv)
    if not os.path.exists("startup"):
        main_form = Authorization()
        main_form.show()
    else:
        main_form = Registration()
        main_form.show()
    sys.exit(app.exec_())
