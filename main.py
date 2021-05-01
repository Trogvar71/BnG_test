import csv
import sys
import sqlite3
import subprocess

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QLineEdit, QTextEdit
from classes import IPaddress
from nettester import generate_ip_list, generate_commands_list, execute_commands
from remoting import generate_commands_list_remoting, execute_commands_remoting


# в main.py описано в основном взаимодействие с интерфейсом и внешними файлами.
# все, что касается внутренней работы - формирование списка IP-адресов и команд,
# я вынес в отдельный файл nettester.py порядка ради
# также вся работа с "математикой" IP-адресов вынесена в отдельный класс
# в файле classes.py
class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.RunButton.clicked.connect(self.run_tester)
        self.TestButton.clicked.connect(self.generate_tester)
        self.RunButton2.clicked.connect(self.run_remoting)
        self.ApplyButton.clicked.connect(self.apply_remoting)
        self.commands_list = []
        self.ipList = []
        self.connection = sqlite3.connect('pc.sqlite')

    # эта функция выполняет команду Test-Connection из PowerShell на заданном диапазоне IP-адресов
    # и записывает результаты в файл out.txt, а также выводит в виджет
    def run_tester(self):
        execute_commands(self.commands_list)
        # вот эти вот строки - это вынужденная мера, потому что Powershell крайне странно пишет в текстовый файл
        # в query_results попадет список из True/False, соответствующий пингам по IP-адресам
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

    # эта функция берет начальный и конечный айпишники и, если они корректные,
    # формирует список адресов для другой функции
    # сами проверки и создание диапазона с учетом особенностей IP-адреса вынесены в отдельный класс
    def generate_tester(self):
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

    # эта функция формирует список имен компютеров по выставленным галочкам,
    # и составляет запрос к БД.
    # имена берутся из БД и имитируют имена компьютеров из моей школы
    def apply_remoting(self):
        floors = []
        floor = ''
        res = ''
        if self.floor_1_box.isChecked():
            floors.append('floor = 1')
        if self.floor_2_box.isChecked():
            floors.append('floor = 2')
        if self.floor_3_box.isChecked():
            floors.append('floor = 3')
        if floors:
            floor = ' OR '.join(floors)

        types = []
        type = ''
        if self.pupil_box.isChecked():
            types.append('is_pupil = 1')
        if self.teacher_box.isChecked():
            types.append('is_teacher = 1')
        if types:
            type = ' OR '.join(types)

        query = 'SELECT name FROM stations'
        if type or floor:
            query += ' WHERE '
            if floor and type:
                query += type
                query += ' AND '
                query += floor
            elif floor:
                query += floor
            elif type:
                query += type
        else:
            query = None
            self.Error_Label2.setText('Выберите хотя бы одно!')

        print(query)
        if query:
            res = self.connection.cursor().execute(query).fetchall()
            print(res)

        text_out = []
        if res:
            for i in res:
                text_out.append(str(i[0]))
        out = '\n'.join(text_out)
        self.NamesInput.setPlainText(out)

    # эта функция берет из текстовых полей список имен компов и
    # список команд и передает это все функции, которая силами PowerShell выполнит
    # заданные команды на заданном списке компьютеров
    def run_remoting(self):
        self.names = self.NamesInput.toPlainText().split()
        self.commands = self.CommandsInput.toPlainText().split()
        if len(self.names) > 0 and len(self.commands) > 0:
            commands_list = generate_commands_list_remoting(self.names, self.commands)
            execute_commands_remoting(commands_list)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())