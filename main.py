import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem
from PyQt5 import uic
import sqlite3
from PyQt5.QtWidgets import QDialog


class CoffeeInfo(QMainWindow):
    def __init__(self):
        super().__init__()
        self.addEditForm = None
        uic.loadUi('main.ui', self)
        self.conn = sqlite3.connect('coffee.sqlite')
        cursor = self.conn.cursor()
        rows = cursor.execute("SELECT * FROM coffee").fetchall()
        self.tableWidget.setRowCount(len(rows))
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setHorizontalHeaderLabels(
            ["ID", "Название сорта", "Степень обжарки", "Молотый/в зернах", "Описание вкуса", "Цена", "Объем упаковки"])
        for i, row in enumerate(rows):
            for j, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                self.tableWidget.setItem(i, j, item)
        self.addbutton.clicked.connect(self.open_add_edit_coffee_form)

    def open_add_edit_coffee_form(self):
        self.addEditForm = Form(self)
        self.addEditForm.show()

    def updatetable(self):
        # Обновление таблицы после добавления или редактирования записи
        self.tableWidget.clear()
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setHorizontalHeaderLabels(
            ["ID", "Название сорта", "Степень обжарки", "Молотый/в зернах", "Описание вкуса", "Цена", "Объем упаковки"])
        rows = self.conn.cursor().execute("SELECT * FROM coffee").fetchall()
        self.tableWidget.setRowCount(len(rows))
        for i, row in enumerate(rows):
            for j, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                self.tableWidget.setItem(i, j, item)

    def closeEvent(self, event):
        self.conn.close()
        event.accept()


class Form(QDialog):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.connection = sqlite3.connect("coffee.sqlite")
        self.cancel.clicked.connect(self.close)
        self.save.clicked.connect(self.save_action)
        self.index = self.parent.tableWidget.selectedIndexes()
        if self.index:
            self.name.setText(self.parent.tableWidget.model().data(self.index[1]))
            self.roasting.setText(self.parent.tableWidget.model().data(self.index[2]))
            self.ground_beans.setText(self.parent.tableWidget.model().data(self.index[3]))
            self.discribe.setText(self.parent.tableWidget.model().data(self.index[4]))
            self.price.setText(self.parent.tableWidget.model().data(self.index[5]))
            self.volume.setText(self.parent.tableWidget.model().data(self.index[6]))

    def save_action(self):
        name = self.name.text()
        roast = self.roasting.text()
        ground_or_whole = self.ground_beans.text()
        description = self.discribe.text()
        price = self.price.text()
        volume = self.volume.text()
        if self.index:
            id_row = self.parent.tableWidget.model().data(self.index[0])
            self.connection.cursor().execute("""UPDATE coffee
            SET sort_name = ?, degree_roasting = ?, ground_beans = ?, description_taste = ?, price = ?, size = ?
            WHERE id = ?""", (name, roast, ground_or_whole, description, price, volume, id_row))
        else:
            self.connection.cursor().execute(
                """INSERT INTO coffee(sort_name, degree_roasting, ground_beans, description_taste, price, size)
                VALUES(?, ?, ?, ?, ?, ?)""", (name, roast, ground_or_whole, description, price, volume))
        self.connection.commit()
        self.connection.close()
        self.parent.updatetable()
        self.close()

    def closeEvent(self, event):
        self.connection.close()
        event.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CoffeeInfo()
    ex.show()
    sys.exit(app.exec_())
