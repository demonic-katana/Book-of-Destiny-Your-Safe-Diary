import sys
import sqlite3

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QImage, QBrush
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QInputDialog, QWidget, QDialog, QListWidget, \
    QListWidgetItem
from PyQt5 import uic


class OwnWindow(QMainWindow):
    def __init__(self, db):
        self.db = db
        super().__init__()
        self.listWidget = QListWidget()
        self.folder = ['main']
        self.name_window = ''
        uic.loadUi('interface/diary.ui', self)
        self.setWindowTitle("Book of Destiny")
        # настройка компонентов:
        # База данных
        self.con = sqlite3.connect(db)
        # настройка кнопок
        self.leave.clicked.connect(self._leave)
        self.settings.clicked.connect(self._settings)
        self.show_()

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

    def create_(self):
        # creating
        self.show_()

    def show_(self):
        self.listWidget.clear()
        cur = self.con.cursor()
        for i in [i[0] for i in cur.execute(f"""Select name from {self.folder[-1]}""").fetchall()]:
            item = QListWidgetItem()
            cur.execute(f"""Select record from {self.folder[-1]} where name = '{i}'""").fetchone()
            item.setText(i)
            self.listWidget.addItem(item)
        self.listWidget.show()


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


class WindowSelect(QMainWindow):
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

    def resizeEvent(self, event):
        try:
            palette = QPalette()
            img = QImage(background_image)
            scaled = img.scaled(self.size(), Qt.KeepAspectRatioByExpanding, transformMode=Qt.SmoothTransformation)
            palette.setBrush(QPalette.Window, QBrush(scaled))
            self.setPalette(palette)
        except Exception:
            pass


class WindowCreate(QWidget):
    def __init__(self):
        super().__init__()
        self.name_window = ''
        uic.loadUi('interface/createBook.ui', self)
        self.setWindowTitle("Book of Destiny: Создать")
        self.needPassword_2.clicked.connect(self._needPassword)
        self.createButton_2.clicked.connect(self.create_db)
        self.cancel_2.clicked.connect(self._leave)
        self._needPassword()
        self.database = None

    def _needPassword(self):
        if self.needPassword_2.isChecked():
            [i.setEnabled(True) for i in [self.password_2, self.question_2, self.answer_2]]
        else:
            [i.setEnabled(False) for i in [self.password_2, self.question_2, self.answer_2]]

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

    def create_db(self):
        name = self.name_2.text()
        if len(name) > 3 and name.split('.')[-1] == 'db' and '.' in name:
            try:
                f = open(name, mode='r', encoding='utf8')
                f.close()
            except FileNotFoundError:
                sqlite_connection = sqlite3.connect(name)
                cur = sqlite_connection.cursor()
                cur.execute(f"""Create table main (
                id INTEGER PRIMARY KEY NOT NULL, 
                name TEXT UNIQUE NOT NULL,
                record BLOB)""")
                sqlite_connection.commit()
                sqlite_connection.close()
                self.database = name
                self.name_window = 'diary'
                self.close()

    def resizeEvent(self, event):
        try:
            palette = QPalette()
            img = QImage(background_image)
            scaled = img.scaled(self.size(), Qt.KeepAspectRatioByExpanding, transformMode=Qt.SmoothTransformation)
            palette.setBrush(QPalette.Window, QBrush(scaled))
            self.setPalette(palette)
        except Exception:
            pass


class WindowSetting(QDialog):
    def __init__(self):
        self.name_window = ''
        super().__init__()
        uic.loadUi('interface/diary_settings.ui', self)
        self.setWindowTitle("Book of Destiny: Настройки")
        self.cancel.clicked.connect(self._leave)
        # self.b_w_theme.clicked.connect(self._create)

    def _sort(self):
        argument, ok_pressed = QInputDialog.getItem(
            self, "Выберите как отсортировать записи", "Параметр сортировки записей:",
            ("ID", "Название", "Дата создания"), 0, False)
        if ok_pressed:
            print(argument)

    def _leave(self):
        self.name_window = 'hello'
        self.close()

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
            elif name_window == 'createBook':
                db = data[1]
            name_window = data[0]
        except Exception as es:
            sys.exit(es)
    sys.exit(0)
