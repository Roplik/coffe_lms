import sys
import sqlite3
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem


class CoffeeApp(QMainWindow):
    def __init__(self):
        super().__init__()

        uic.loadUi('main.ui', self)

        self.conn = sqlite3.connect('coffee.sqlite')
        self.cursor = self.conn.cursor()

        self.tableWidget.setColumnCount(7)
        self.tableWidget.setHorizontalHeaderLabels(
            ["ID", "Name", "Roast Level", "Ground/Beans", "Taste Description", "Price", "Package Volume"]
        )

        self.load_data()

        self.refreshButton.clicked.connect(self.load_data)

    def load_data(self):

        self.cursor.execute("SELECT * FROM coffee")
        data = self.cursor.fetchall()

        self.tableWidget.setRowCount(0)

        for row_number, row_data in enumerate(data):
            self.tableWidget.insertRow(row_number)
            for column_number, column_data in enumerate(row_data):
                self.tableWidget.setItem(
                    row_number, column_number, QTableWidgetItem(str(column_data))
                )

    def closeEvent(self, event):

        self.conn.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CoffeeApp()
    window.show()
    sys.exit(app.exec())
