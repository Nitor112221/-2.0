import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem
from PyQt5 import uic
import sqlite3


class CoffeeInfo(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        conn = sqlite3.connect('coffee.sqlite')
        cursor = conn.cursor()
        rows = cursor.execute("SELECT * FROM coffee").fetchall()
        self.tableWidget.setRowCount(len(rows))
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setHorizontalHeaderLabels(
            ["ID", "Название сорта", "Степень обжарки", "Молотый/в зернах", "Описание вкуса", "Цена", "Объем упаковки"])
        for i, row in enumerate(rows):
            for j, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                self.tableWidget.setItem(i, j, item)
        conn.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CoffeeInfo()
    ex.show()
    sys.exit(app.exec_())
