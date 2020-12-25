import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog
from login import Login

if __name__ == "__main__":
    app = QApplication(sys.argv)
    login = Login()
    main = None
    login.show()
    sys.exit(app.exec_())

'''
    D:
    cd "D://programming//python//softWare_PP//Server"
    python -u "serverCore copy.py"
'''
