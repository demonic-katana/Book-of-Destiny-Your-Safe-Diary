import sys
import sqlite3

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QImage, QBrush
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QInputDialog, QWidget, QDialog
from PyQt5 import uic


class OwnWindow(QMainWindow):
    def __init__(self, db):
        self.db = db
        super().__init__()
        self.name_window = ''
        uic.loadUi('interface/diary.ui', self)
        self.setWindowTitle("Book of Destiny")
        # настройка компонентов:
        # настройка кнопок
        self.leave.clicked.connect(self._leave)
        self.settings.clicked.connect(self._settings)

    def _settings(self):
        self.settings = WindowSetting()
        self.settings.show()

    def _leave(self):
        self.name_window = 'hello'
        self.close()

    def getData(self):
        return self.name_window,

    def resizeEvent(self, event):
        try:
            palette = QPalette()
            img = QImage(background_image)
            scaled = img.scaled(self.size(), Qt.KeepAspectRatioByExpanding, transformMode=Qt.SmoothTransformation)
            palette.setBrush(QPalette.Window, QBrush(scaled))
            self.setPalette(palette)
        except Exception:
            pass


class WindowGreeting(QMainWindow):
    def __init__(self):
        self.name_window = ''
        super().__init__()
        uic.loadUi('interface/hello.ui', self)
        self.setWindowTitle("Book of Destiny: Добро пожаловать")
        # Настройки кнопок
        [i.clicked.connect(self.run) for i in [self.select, self.create, self.settings]]

    def run(self):
        if self.sender().text() == 'Создать':
            self.name_window = 'createBook'
            self.close()
        elif self.sender().text() == 'Выбрать':
            self.name_window = 'selectBook'
            self.close()
        elif self.sender().text() == 'Настройки':
            self.second_window = WindowSetting()
            self.second_window.show()

    def getData(self):
        return self.name_window,

    def resizeEvent(self, event):
        try:
            palette = QPalette()
            img = QImage(background_image)
            scaled = img.scaled(self.size(), Qt.KeepAspectRatioByExpanding, transformMode=Qt.SmoothTransformation)
            palette.setBrush(QPalette.Window, QBrush(scaled))
            self.setPalette(palette)
        except Exception:
            pass


class WindowSelect(QWidget):
    def __init__(self):
        super().__init__()
        self.name_window = ''
        uic.loadUi('interface/selectBook.ui', self)
        self.setWindowTitle("Book of Destiny: Выбрать")
        # Настройки кнопок
        self.dialog_sel.clicked.connect(self._filedialog)
        self.cancel.clicked.connect(self._cancel)
        self.select.clicked.connect(self._select)
        self.database = None

    def _filedialog(self):
        self.Put.setText(QFileDialog.getOpenFileName(self, 'Выбрать книгу',
                                                           '',
                                                           'Data Base file (*.db);;Все файлы (*)')[0])

    def _select(self):
        database = self.Put.text()
        if len(database) > 3 and database.split('.')[-1] == 'db' and '.' in database:
            try:
                f = open(database, mode='r', encoding='utf8')
                f.close()
                self.database = database
                self.name_window = 'diary'
                self.close()
            except Exception:
                self.statusBar().showMessage("База данных не найдена.")
        else:
            self.statusBar().showMessage("Не правильное имя базы данных.")

    def closeEvent(self, event):
        if not self.name_window:
            self.name_window = 'hello'

    def _cancel(self):
        self.name_window = 'hello'
        self.close()

    def _leave(self):
        self.name_window = 'hello'
        self.close()

    def getData(self):
        return self.name_window, self.database


class WindowCreate(QWidget):
    def __init__(self):
        super().__init__()
        self.name_window = ''
        uic.loadUi('interface/createBook.ui', self)
        self.setWindowTitle("Book of Destiny: Создать")


    def _cancel(self):
        self.name_window = 'hello'
        self.close()

    def _leave(self):
        self.name_window = 'hello'
        self.close()

    def closeEvent(self, event):
        if not self.name_window:
            self.name_window = 'hello'

    def getData(self):
        return self.name_window, self.database


class WindowSetting(QDialog):
    def __init__(self):
        self.name_window = ''
        super().__init__()
        uic.loadUi('interface/diary_settings.ui', self)
        self.setWindowTitle("Book of Destiny: Настройки")
        # self.b_w_theme.clicked.connect(self._create)

    def _sort(self):
        argument, ok_pressed = QInputDialog.getItem(
            self, "Выберите как отсортировать записи", "Параметр сортировки записей:",
            ("ID", "Название", "Дата создания"), 0, False)
        if ok_pressed:
            print(argument)

    def _background_image(self):
        global background_image
        background_image = QFileDialog.getOpenFileName(
            self, 'Выбрать картинку', '', 'Картинка (*.jpg);;Картинка (*.png);;Все файлы (*)')[0]

    def closeEvent(self, event):
        self.name_window = 'hello'

    def resizeEvent(self, event):
        try:
            palette = QPalette()
            img = QImage(background_image)
            scaled = img.scaled(self.size(), Qt.KeepAspectRatioByExpanding, transformMode=Qt.SmoothTransformation)
            palette.setBrush(QPalette.Window, QBrush(scaled))
            self.setPalette(palette)
        except Exception:
            pass

    def getData(self):
        return self.name_window,


def excepthook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    name_window = 'hello'
    background_image = r'interface\911045.png'
    sys.excepthook = excepthook
    while name_window != '':
        try:
            if name_window == 'hello':
                window = WindowGreeting()
            elif name_window == 'selectBook':
                window = WindowSelect()
            elif name_window == 'createBook':
                window = WindowCreate()
            elif name_window == 'diary':
                window = OwnWindow(db)
            window.show()
            s = app.exec()
            data = window.getData()
            if name_window == 'selectBook':
                db = data[1]
            name_window = data[0]
        except Exception as es:
            sys.exit(es)
    sys.exit(0)
