import sys
import sqlite3
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QMessageBox, QDialog


class AddEditCoffeeForm(QDialog):
    def __init__(self, parent=None, coffee_id=None):
        super().__init__(parent)
        uic.loadUi('addEditCoffeeForm.ui', self)

        self.coffee_id = coffee_id
        self.parent = parent

        if self.coffee_id:
            self.load_data()

        # Связывание кнопок
        self.saveButton.clicked.connect(self.save_data)
        self.cancelButton.clicked.connect(self.close)

    def load_data(self):

        self.parent.cursor.execute("SELECT * FROM coffee WHERE id=?", (self.coffee_id,))
        data = self.parent.cursor.fetchone()

        if data:
            self.nameEdit.setText(data[1])
            self.roastLevelEdit.setText(data[2])
            self.groundOrBeansCombo.setCurrentText(data[3])
            self.tasteDescriptionEdit.setText(data[4])
            self.priceEdit.setText(str(data[5]))
            self.packageVolumeEdit.setText(str(data[6]))

    def save_data(self):
        """Сохранение данных в базу."""
        name = self.nameEdit.text()
        roast_level = self.roastLevelEdit.text()
        ground_or_beans = self.groundOrBeansCombo.currentText()
        taste_description = self.tasteDescriptionEdit.text()
        price = float(self.priceEdit.text())
        package_volume = float(self.packageVolumeEdit.text())

        if self.coffee_id:
            # Редактирование существующей записи
            self.parent.cursor.execute(
                "UPDATE coffee SET name=?, roast_level=?, ground_or_beans=?, taste_description=?, price=?, package_volume=? WHERE id=?",
                (name, roast_level, ground_or_beans, taste_description, price, package_volume, self.coffee_id))
        else:
            self.parent.cursor.execute(
                "INSERT INTO coffee (name, roast_level, ground_or_beans, taste_description, price, package_volume) VALUES (?, ?, ?, ?, ?, ?)",
                (name, roast_level, ground_or_beans, taste_description, price, package_volume))

            self.parent.conn.commit()
            self.parent.load_data()
            self.close()


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
        self.addButton.clicked.connect(self.add_coffee)
        self.editButton.clicked.connect(self.edit_coffee)

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

    def add_coffee(self):

        form = AddEditCoffeeForm(self)
        form.exec()

    def edit_coffee(self):

        selected_row = self.tableWidget.currentRow()
        if selected_row >= 0:
            coffee_id = self.tableWidget.item(selected_row, 0).text()
            form = AddEditCoffeeForm(self, coffee_id)
            form.exec()
        else:
            QMessageBox.warning(self, "Warning", "Please select a row to edit.")

    def closeEvent(self, event):
        self.conn.close()



def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CoffeeApp()
    sys.excepthook = except_hook
    window.show()
    sys.exit(app.exec())
