import csv
import sys
import subprocess

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QLineEdit
from classes import IPaddress
from nettester import generate_ip_list, generate_commands_list, execute_commands

# в main.py описано в основном взаимодействие с интерфейсом и внешними файлами.
# все, что касается внутренней работы - формирование списка IP-адресов и команд,
# я вынес в отдельный файл nettester.py порядка ради
class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.RunButton.clicked.connect(self.run)
        self.TestButton.clicked.connect(self.generate)
        self.commands_list = []
        self.ipList = []

    def run(self):
        execute_commands(self.commands_list)
        # вот эти вот строки - это вынужденная мера, потому что Powershell крайне странно пишет в текстовый файл
        # в итоге в query_results попадет список из True/False, соответствующий пингам по IP-адресам
        out = open('out.txt').readlines()
        query_results = [str(i.strip()) for i in out if len(i) > 3]
        query_results[0] = query_results[0][2:]
        res = []
        for i in query_results:
            word = [_ for _ in i if _.isalpha()]
            res.append(''.join(word))

        # дальше будем выполнять запись в .csv, а потом считаем из него же в таблицу
        # этот маневр можно было вообще опустить, он сделан только ради демонстрации работы с .csv для проекта
        data = []
        for i in range(len(self.ipList)):
            d = {
                'IPAddress': self.ipList[i],
                'Connection': str(res[i])
            }
            data.append(d)
        # print(data)

        with open('result.csv', 'w', newline='') as f:
            writer = csv.DictWriter(
                f, fieldnames=list(data[0].keys()),
                delimiter=';', quoting=csv.QUOTE_NONNUMERIC)
            writer.writeheader()
            for d in data:
                writer.writerow(d)
            f.close()
        # а теперь считаем.
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
        self.ResultTable.resizeColumnsToContents()
        csvfile.close()

    def generate(self):
        start = IPaddress(self.IP_start_input.text())
        end = IPaddress(self.IP_end_input.text())

        if start.is_correct() and end.is_correct():
            # print('IP-адреса корректны')
            self.Error_Label.setText('IP-адреса корректны')
            if start < end:
                ipList = generate_ip_list(start, end)
            else:
                ipList = generate_ip_list(end, start)
            self.ipList = ipList
            commands_list = generate_commands_list(ipList)
            # print('Список опроса успешно сформирован')
            self.Test_Label.setText('Список успешно сформирован')
            self.RunButton.setEnabled(True)
            self.commands_list = commands_list
        else:
            self.Error_Label.setText('Введите корректные адреса')
            # print('Введите корректные адреса и попробуйте снова')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())