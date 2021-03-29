import csv
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.RunButton.clicked.connect(self.run)

    def run(self):
        with open('result.csv', encoding="utf8") as csvfile:
            reader = csv.reader(csvfile,
                                delimiter=';', quotechar='"')
            title = next(reader)

            self.ResultTable.setColumnCount(len(title))
            self.ResultTable.setHorizontalHeaderLabels(title)
            self.ResultTable.setRowCount(0)

            for i, row in enumerate(reader):
                self.ResultTable.setRowCount(
                    self.ResultTable.rowCount() + 1)
                for j, elem in enumerate(row):
                    self.ResultTable.setItem(
                        i, j, QTableWidgetItem(elem))

        # self.ResultTable.resizeColumnsToContents()     этого может и не стоит делать


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())