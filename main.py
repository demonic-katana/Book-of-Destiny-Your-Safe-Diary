import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QAction, QFileDialog, QDialog, QDialogButtonBox, \
    QLabel, QVBoxLayout
from PyQt5 import uic


class OwnWindow(QMainWindow):
    def __init__(self, db):
        self.db = db
        super().__init__()
        self._window = ''
        uic.loadUi('interface\\diary.ui', self)
        # настройка компонентов:
        # настройка кнопок
        self.leave.clicked.connect(self._leave)

    def _leave(self):
        self._window = 'hello'
        self.close()

    def getData(self):
        return self._window,


class WindowSelect(QMainWindow):
    def __init__(self):
        super().__init__()
        self._window = ''
        uic.loadUi('interface\\selectBook.ui', self)
        self.setWindowTitle("Book of Destiny")
        # Настройки кнопок
        self.dialog_sel.clicked.connect(self._filedialog)
        self.cancel.clicked.connect(self._cancel)
        self.select.clicked.connect(self._select)
        self.database = None

    def _filedialog(self):
        self.Put.setText(QFileDialog.getOpenFileName(self,
                                                          'Выбрать книгу',
                                                          '',
                                                          'Data Base file (*.db);;Все файлы (*)')[0])

    def _select(self):
        database = self.Put.text()
        if len(database) > 3 and database.split('.')[-1] == 'db' and '.' in database:
            try:
                f = open(database, mode='r', encoding='utf8')
                f.close()
                self.database = database
                self._window = 'diary'
                self.close()
            except Exception:
                self.statusBar().showMessage("База данных не найдена.")
        else:
            self.statusBar().showMessage("Не правильное имя базы данных.")

    def _cancel(self):
        self._window = 'hello'
        self.close()

    def getData(self):
        return self._window, self.database

class WindowGreeting(QMainWindow):
    def __init__(self):
        self._window = ''
        super().__init__()
        uic.loadUi('interface\\hello.ui', self)
        self.setWindowTitle("Book of Destiny")
        # Настройки кнопок
        self.select.clicked.connect(self._select)
        self.create.clicked.connect(self._create)
        self.settings.clicked.connect(self._settings)

    def _select(self):
        self._window = 'selectBook'
        self.close()

    def _create(self):
        self._window = 'createBook'
        self.close()

    def _settings(self):
        self._window = 'settings_h'
        self.close()

    def getData(self):
        return self._window,

if __name__ == '__main__':
    app = QApplication(sys.argv)
    _window = 'hello'
    while _window != '':
        try:
            if _window == 'hello':
                window = WindowGreeting()
            elif _window == 'selectBook':
                window = WindowSelect()
            elif _window == 'createBook':
                pass
            elif _window == 'settings_h':
                pass
            elif _window == 'diary':
                window = OwnWindow(db)
            window.show()
            s = app.exec()
            data = window.getData()
            if _window == 'selectBook':
                db = data[1]
            _window = data[0]
        except Exception as es:
            sys.exit(es)
    sys.exit(0)
