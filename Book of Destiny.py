import os
import sys
import shutil
import sqlite3
import datetime
from PyQt5 import uic
from random import choice
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QImage, QBrush, QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QInputDialog, QWidget, QDialog, \
    QListWidgetItem, QDialogButtonBox, QVBoxLayout, QLabel, QPlainTextEdit


class OwnWindow(QMainWindow):
    def __init__(self, db):
        self.db = db
        super().__init__()
        self.setWindowIcon(QIcon('logo.ico'))
        self.folder = ['folder', 'main']
        self.name_window = ''
        uic.loadUi('interface/diary.ui', self)
        self.setWindowTitle("Book of Destiny")
        self.tabWidget.setStyleSheet("background-color: rgb(255, 255, 255, 100);")
        # настройка компонентов:
        # База данных
        self.con = sqlite3.connect(db)
        # настройка кнопок
        self.leave.clicked.connect(self._leave)
        self.settings.clicked.connect(self._settings)
        self.del_b_1.clicked.connect(self._del)
        self.open_b_1.clicked.connect(self._open)
        self.add_b_1.clicked.connect(self._create)
        self.sort_b_1.clicked.connect(self._sort)
        self.del_b_2.clicked.connect(self._delFolder)
        self.add_in_f.clicked.connect(self._add_in_Folder)
        self.open_b_2.clicked.connect(self._openFolder)
        self.add_b_2.clicked.connect(self._createFolder)
        self.sort_b_2.clicked.connect(self._sortFolder)
        self.open_b_3.clicked.connect(self._openThisFolder)
        self.sort_b_3.clicked.connect(self._sortThisFolder)
        self.del_b_3.clicked.connect(self._delThisFolder)
        self.order = "Дате создания"
        self.order_f = "Дате создания"
        self.order_one_f = "Дате создания"
        self.show_()

    def _sort(self):
        argument, ok_pressed = QInputDialog.getItem(self, "Сортировка", "Отсортировать по", ("Дате создания", "Имени"),
                                                    0, False)
        if ok_pressed:
            self.order = argument
        self.show_()

    def _sortFolder(self):
        argument, ok_pressed = QInputDialog.getItem(self, "Сортировка", "Отсортировать по", ("Дате создания", "Имени"),
                                                    0, False)
        if ok_pressed:
            self.order_f = argument
        self.show_()

    def _sortThisFolder(self):
        argument, ok_pressed = QInputDialog.getItem(self, "Сортировка", "Отсортировать по", ("Дате создания", "Имени"),
                                                    0, False)
        if ok_pressed:
            self.order_f = argument
            self._openFolder(self.label_f.text()[37:-18])

    def _del(self):
        cur = self.con.cursor()
        try:
            item = self.listWidget.currentItem().text()
        except Exception:
            try:
                self.listWidget.setCurrentRow(0)
                item = self.listWidget.currentItem().text()
            except Exception:
                return
        dialog = Confirm_(f"Вы действительно хотите безвозвратно удалить {item}?", "Удаление")
        if dialog.exec():
            cur.execute(f"""DELETE FROM main WHERE name = '{item}'""").fetchone()
            self.con.commit()
        self.show_()

    def _delFolder(self):
        cur = self.con.cursor()
        try:
            folder = self.listWidget_1.currentItem().text()
        except Exception:
            try:
                self.listWidget_1.setCurrentRow(0)
                folder = self.listWidget_1.currentItem().text()
            except Exception:
                return
        dialog = Confirm_(f"Вы действительно хотите безвозвратно удалить папку {folder}? "
                          f"Записи в ней НЕ будут удалены.", "Удаление папки")
        if dialog.exec():
            cur.execute(f"""DELETE FROM folder WHERE name = '{folder}'""")
            self.con.commit()
        self.show_()

    def _delThisFolder(self):
        cur = self.con.cursor()
        try:
            item = self.listWidget_folder.currentItem().text()
        except Exception:
            try:
                self.listWidget_folder.setCurrentRow(0)
                item = self.listWidget_folder.currentItem().text()
            except Exception:
                return
        dialog = Confirm_(f"Вы действительно хотите удалить запись {item} из папки "
                          f"{self.label_f.text()[37:-18]}? "
                          f"Она больше не будет входить в данную папку, но останется доступной.", "Удаление папки")
        if dialog.exec():
            old_folder = cur.execute(f"""Select folder from {self.folder[-1]} WHERE name = '{item}'""").fetchone()[
                0].split('_')
            old_folder.pop(old_folder.index(str(cur.execute(
                f"""SELECT id FROM {self.folder[-2]} WHERE name = '{self.label_f.text()[37:-18]}'""").fetchone()[0])))
            cur.execute(f"""UPDATE main SET folder = '{'_'.join(old_folder)}' WHERE name = '{item}'""")
            self.con.commit()
            self._openFolder(self.label_f.text()[37:-18])

    def _open(self):
        global lE, tE
        cur = self.con.cursor()
        try:
            lE = self.listWidget.currentItem().text()
        except Exception:
            try:
                self.listWidget.setCurrentRow(0)
                lE = self.listWidget.currentItem().text()
            except Exception:
                return
        tE = cur.execute(f"""SELECT record FROM main WHERE name = '{lE}'""").fetchone()[0]
        self.name_window = 'write'
        self.close()

    def _openFolder(self, name_f=None):
        cur = self.con.cursor()
        if not name_f:
            try:
                name_f = self.listWidget_1.currentItem().text()
            except Exception:
                try:
                    self.listWidget_1.setCurrentRow(0)
                    name_f = self.listWidget_1.currentItem().text()
                except Exception:
                    return
        self.label_f.setText(f'<html><head/><body><p align="center">{name_f}</p></body></html>')
        id_f = cur.execute(f"""SELECT id FROM {self.folder[-2]} WHERE name = '{name_f}'""").fetchone()[0]
        self.listWidget_folder.clear()
        n = []
        for i in cur.execute(f"""SELECT name, date_creation, folder FROM {self.folder[-1]}""").fetchall():
            if i[-1] and str(id_f) in i[-1].split('_'):
                n += [i[:-1]]
        for i in sorted(n, key=lambda x: x[int(self.order_one_f == "Дате создания")]):
            i = i[0]
            item = QListWidgetItem()
            item.setText(i)
            self.listWidget_folder.addItem(item)
        self.tabWidget.setCurrentIndex(2)
        self.listWidget_folder.show()

    def _openThisFolder(self):
        global lE, tE
        cur = self.con.cursor()
        try:
            lE = self.listWidget_folder.currentItem().text()
        except Exception:
            try:
                self.listWidget_folder.setCurrentRow(0)
                lE = self.listWidget_folder.currentItem().text()
            except Exception:
                return
        tE = cur.execute(f"""SELECT record FROM main WHERE name = '{lE}'""").fetchone()[0]
        self.name_window = 'write'
        self.close()

    def _settings(self):
        self.settings = WindowSetting(self)
        self.settings.show()

    def _leave(self):
        self.name_window = 'hello'
        self.close()

    def getData(self):
        return self.name_window,

    def resizeEvent(self, event):
        global background_image
        if not background_image:
            background_image = "interface/default.jpg"
        try:
            palette = QPalette()
            img = QImage(background_image)
            scaled = img.scaled(self.size(), Qt.KeepAspectRatioByExpanding, transformMode=Qt.SmoothTransformation)
            palette.setBrush(QPalette.Window, QBrush(scaled))
            self.setPalette(palette)
        except Exception:
            pass

    def _create(self):
        self.name_window = 'write'
        self.close()

    def _createFolder(self):
        name, ok_pressed = QInputDialog.getText(self, "Новая папка",
                                                "Введите название для новой папки")
        if ok_pressed:
            cur = self.con.cursor()
            if not cur.execute(f"""Select id from folder where name = '{name}'""").fetchone():
                cur.execute(f"""INSERT INTO folder (name)
                VALUES ('{name}')""")
                self.con.commit()
                self.show_()
            else:
                self.label.setStyleSheet("background-color: rgba(255, 255, 255, 200);")
                self.label.setText('Папка с таким именем уже существует.')

    def show_(self):
        cur = self.con.cursor()
        # Вывод списка записей
        self.listWidget.clear()
        for i in sorted([j for j in cur.execute(f"""Select name, date_creation 
                from {self.folder[-1]}""").fetchall()], key=lambda x: x[int(self.order == "Дате создания")]):
            i = i[0]
            item = QListWidgetItem()
            item.setText(i)
            self.listWidget.addItem(item)
        self.listWidget.show()
        # Вывод списка папок
        self.listWidget_1.clear()
        for i in sorted([j for j in cur.execute(f"""Select id, name from {self.folder[-2]}""").fetchall()],
                        key=lambda x: x[int(self.order_f != "Дате создания")]):
            item = QListWidgetItem()
            item.setText(i[1])
            self.listWidget_1.addItem(item)
        self.listWidget_1.show()
        self.label.setText('')
        self.label.setStyleSheet("background-color: rgba(255, 255, 255, 0);")

    def _add_in_Folder(self):
        cur = self.con.cursor()
        try:
            item = self.listWidget.currentItem().text()
        except Exception:
            try:
                self.listWidget.setCurrentRow(0)
                item = self.listWidget.currentItem().text()
            except Exception:
                return
        folder, ok_pressed = QInputDialog.getItem(
            self, "Выберите папку для сохранения", "Добавить запись в",
            tuple(
                i[1] for i in sorted([j for j in cur.execute(f"""Select id, name from {self.folder[-2]}""").fetchall()],
                                     key=lambda x: x[0])), 0, False)
        if ok_pressed:
            f = str(cur.execute(f"""Select id from {self.folder[-2]} WHERE name = '{folder}'""").fetchone()[0])
            try:
                old_folder = cur.execute(f"""Select folder from {self.folder[-1]} WHERE name = '{item}'""").fetchone()
                inp_folder = '_'.join(sorted(list(set(old_folder[0].split('_') + [f]))))
            except sqlite3.OperationalError:
                inp_folder = f
            finally:
                cur.execute(f"""UPDATE main SET folder = '{inp_folder}' WHERE name = '{item}'""")
                self.con.commit()

    def closeEvent(self, event):
        if not self.name_window:
            self.name_window = 'hello'


class WindowGreeting(QMainWindow):
    def __init__(self):
        self.name_window = ''
        super().__init__()
        self.setWindowIcon(QIcon('logo.ico'))
        uic.loadUi('interface/hello.ui', self)
        self.setWindowTitle("Book of Destiny: Добро пожаловать")
        # Настройки кнопок
        [i.clicked.connect(self.run) for i in [self.select, self.create, self.settings]]
        self.resizeEvent(self)
        self.label.setStyleSheet('background-color: rgba(255, 255, 255, 200);')
        self.statusBar().setStyleSheet('background-color: rgba(255, 255, 255, 200);')
        with open('interface/quote.txt', encoding='utf8') as quote:
            self.statusBar().showMessage(choice(quote.readlines()).strip())

    def run(self):
        if self.sender().text() == 'Создать книгу':
            self.name_window = 'createBook'
            self.close()
        elif self.sender().text() == 'Выбрать книгу':
            self.name_window = 'selectBook'
            self.close()
        elif self.sender().text() == 'Настройки':
            self.second_window = WindowSetting(self)
            self.second_window.show()

    def getData(self):
        return self.name_window,

    def resizeEvent(self, event):
        global background_image
        if not background_image:
            background_image = "interface/default.jpg"
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
        self.setWindowIcon(QIcon('logo.ico'))
        self.name_window = ''
        uic.loadUi('interface/selectBook.ui', self)
        self.setWindowTitle("Book of Destiny: Выбрать")
        # Настройки кнопок
        self.Put.setStyleSheet("background-color: rgba(255, 255, 255, 100);")
        self.dialog_sel.clicked.connect(self._filedialog)
        self.cancel.clicked.connect(self._leave)
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
                self.label.setStyleSheet("background-color: rgba(255, 255, 255, 200);")
                self.label.setText("База данных не найдена.")
        else:
            self.label.setStyleSheet("background-color: rgba(255, 255, 255, 200);")
            self.label.setText("Не правильное имя базы данных.")

    def closeEvent(self, event):
        if not self.name_window:
            self.name_window = 'hello'

    def _leave(self):
        self.name_window = 'hello'
        self.close()

    def getData(self):
        return self.name_window, self.database

    def resizeEvent(self, event):
        global background_image
        if not background_image:
            background_image = "interface/default.jpg"
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
        self.setWindowIcon(QIcon('logo.ico'))
        self.name_window = ''
        uic.loadUi('interface/createBook.ui', self)
        self.setWindowTitle("Book of Destiny: Создать")
        [i.setStyleSheet("background-color: rgba(255, 255, 255, 100);") for i in [self.name_2, self.put_2]]
        [i.setStyleSheet("background-color: rgba(255, 255, 255, 200);") for i in [self.label_8, self.label_10]]
        self.createButton_2.clicked.connect(self.create_db)
        self.dialog_sel.clicked.connect(self._filedialog)
        self.cancel_2.clicked.connect(self._leave)
        self.database = None

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
        if len(name) > 0 and all([i not in name for i in r'/\:*?<>|']):
            try:
                if not name.endswith('.db'):
                    name = name + '.db'
                f = open(name, mode='r', encoding='utf8')
                f.close()
            except FileNotFoundError:
                sqlite_connection = sqlite3.connect(name)
                cur = sqlite_connection.cursor()
                cur.execute(f"""Create table main (
                id INTEGER PRIMARY KEY NOT NULL, 
                name TEXT UNIQUE NOT NULL,
                record TEXT,
                date_creation DATETIME NOT NULL,
                folder TEXT)""")
                cur.execute(f"""Create table folder (
                id INTEGER PRIMARY KEY NOT NULL, 
                name TEXT UNIQUE NOT NULL)""")
                sqlite_connection.commit()
                sqlite_connection.close()
                self.database = name
                self.name_window = 'diary'
                self.close()
        self.label.setStyleSheet("background-color: rgba(255, 255, 255, 200);")
        self.label.setText('Некорректное имя!!')

    def _filedialog(self):
        self.put_2.setText(QFileDialog.getExistingDirectory(self, 'Выберете папку',
                                                     '',
                                                     QFileDialog.ShowDirsOnly
                                                     | QFileDialog.DontResolveSymlinks))


    def resizeEvent(self, event):
        global background_image
        if not background_image:
            background_image = "interface/default.jpg"
        try:
            palette = QPalette()
            img = QImage(background_image)
            scaled = img.scaled(self.size(), Qt.KeepAspectRatioByExpanding, transformMode=Qt.SmoothTransformation)
            palette.setBrush(QPalette.Window, QBrush(scaled))
            self.setPalette(palette)
        except Exception:
            pass


class WindowSetting(QDialog):
    def __init__(self, parent):
        self.name_window = ''
        super().__init__()
        self.setWindowIcon(QIcon('logo.ico'))
        uic.loadUi('interface/diary_settings.ui', self)
        self.setWindowTitle("Book of Destiny: Настройки")
        self.parent = parent
        self.custom_theme.clicked.connect(self._background_image)
        self.del_custom_theme.clicked.connect(self._del_custom_theme)
        self.about_author.clicked.connect(self._about_author)
        self.label.setStyleSheet("background-color: rgba(255, 255, 255, 200);")

    def _background_image(self):
        global background_image
        del_background_image = background_image
        background_image = QFileDialog.getOpenFileName(
            self, 'Выбрать картинку', '', 'Картинка (*.jpg);;Картинка (*.png);;Все файлы (*)')[0]
        if del_background_image == "interface/default.jpg":
            del_background_image = ""
        if del_background_image and background_image and del_background_image not in background_image:
            os.remove(del_background_image)
        if background_image:
            shutil.copy(background_image, 'photo/')
            background_image = 'photo/' + os.listdir("photo")[0] if os.listdir("photo") else ''
            self.resizeEvent(self)
            self.parent.resizeEvent(self.parent)
        else:
            background_image = del_background_image

    def _del_custom_theme(self):
        global background_image
        if background_image and background_image != "interface/default.jpg":
            os.remove(background_image)
        background_image = "interface/default.jpg"
        self.resizeEvent(self)
        self.parent.resizeEvent(self.parent)

    def _leave(self):
        self.name_window = 'hello'
        self.close()

    def _about_author(self):
        self.textEdit_about_author = QPlainTextEdit(open('interface/about_author.txt', encoding='utf8').read())
        self.textEdit_about_author.show()

    def closeEvent(self, event):
        self.name_window = 'hello'

    def resizeEvent(self, event):
        global background_image
        if not background_image:
            background_image = "interface/default.jpg"
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


class Confirm_(QDialog):
    def __init__(self, question, title):
        super().__init__()
        self.setWindowIcon(QIcon('logo.ico'))
        self.setWindowTitle("Book of Destiny: " + title)
        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        self.layout = QVBoxLayout()
        lable = QLabel(question)
        self.layout.addWidget(lable)
        self.layout.addWidget(self.buttons)
        self.setLayout(self.layout)


class WriteRecord(QWidget):
    def __init__(self):
        global lE, tE
        super().__init__()
        self.setWindowIcon(QIcon('logo.ico'))
        self.name_window = ''
        self.con = sqlite3.connect(db)
        uic.loadUi('interface/write.ui', self)
        self.setWindowTitle("Book of Destiny: Запись")
        self.lineEdit.setText(str(lE))
        self.lineEdit.setStyleSheet("background-color: rgba(255, 255, 255, 100);")
        self.lineEdit.setPlaceholderText('Введите название')
        self.textEdit.setText(str(tE))
        self.textEdit.setStyleSheet("background-color: rgba(255, 255, 255, 100);")
        self.textEdit.setPlaceholderText('Введите текст')
        self.lE_, self.tE_, lE, tE = lE, tE, '', ''
        self.save.clicked.connect(self._save)

    def resizeEvent(self, event):
        global background_image
        if not background_image:
            background_image = "interface/default.jpg"
        try:
            palette = QPalette()
            img = QImage(background_image)
            scaled = img.scaled(self.size(), Qt.KeepAspectRatioByExpanding, transformMode=Qt.SmoothTransformation)
            palette.setBrush(QPalette.Window, QBrush(scaled))
            self.setPalette(palette)
        except Exception:
            pass


    def closeEvent(self, event):
        if self._save():
            event.ignore()
        self.name_window = 'diary'

    def _save(self):
        now = datetime.datetime.now()
        self.lE_n, self.tE_n = self.lineEdit.text().strip(), self.textEdit.toPlainText().strip()
        cur = self.con.cursor()
        check = cur.execute(f"""Select record from main where name = '{self.lE_n}'""").fetchone()
        if (not self.lE_n and not self.lE_n) or (self.lE_ == self.lE_n and self.tE_ == self.tE_n):
            return False
        elif not self.lE_n:
            self.label.setText("Название не может быть пустым, для сохранения укажите название.")
            return True
        elif not check:
            dialog = Confirm_(f"Сохранить запись?", "Сохранение")
            if dialog.exec():
                if self.lE_:
                    folder = cur.execute(f"""Select folder from main where name = '{self.lE_}'""").fetchone()[0]
                else:
                    folder = ''
                if cur.execute(f"""Select date_creation from main where name = '{self.lE_}'""").fetchone():
                    time = cur.execute(f"""Select date_creation from main where name = '{self.lE_}'""").fetchone()[0]
                else:
                    time = now.strftime("%Y/%m/%d %H:%M:%S")
                cur.execute(f"""INSERT INTO main (name, record, date_creation, folder) 
                VALUES ('{self.lE_n}', '{self.tE_n}', '{time}', '{folder}')""")
                self.after_save()
            return False
        elif self.lE_ == self.lE_n and self.lE_n:
            dialog = Confirm_(f"Сохранить изменения?", "Сохранение")
            if dialog.exec():
                cur.execute(f"""UPDATE main SET record = '{self.tE_n}' WHERE name = '{self.lE_n}'""")
                self.after_save()
            return False
        else:
            self.label.setText("Запись с таким названием уже существует, для сохранения измените название.")
            return True

    def after_save(self):
        cur = self.con.cursor()
        if self.lE_ != self.lE_n:
            cur.execute(f"""DELETE FROM main WHERE name = '{self.lE_}'""")
        self.lE_, self.tE_ = self.lE_n, self.tE_n
        self.con.commit()

    def getData(self):
        return self.name_window,


def excepthook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    lE, tE = '', ''
    name_window = 'hello'
    background_image = 'photo/' + n[0] if (n := os.listdir("photo")) else ''
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
            elif name_window == 'write':
                window = WriteRecord()
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
