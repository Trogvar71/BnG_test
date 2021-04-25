# сюда я складываю ненужный код


#  реализация работы с айпишниками нездорового человека
def check_IPs(start, end):
    start_octs = start.split('.')
    if not all(i.isdigit() for i in start_octs):
        print('Некорректные символы в адресе', start)
        return 'Некорректные символы в адресе'
    elif len(start_octs) != 4:
        print('Неверный формат адреса', start)
        return 'Неверный формат адреса'
    elif not all(0 <= int(i) <= 255 for i in start_octs):
        print('Выход за допустимый диапазон', start)
        return 'Выход за допустимый диапазон'
    else:
        start_correct = True

    end_octs = end.split('.')
    if not all(i.isdigit() for i in end_octs):
        print('Некорректные символы в адресе', end)
        return 'Некорректные символы в адресе'
    elif len(end_octs) != 4:
        print('Неверный формат адреса', end)
        return 'Неверный формат адреса'
    elif not all(0 <= int(i) <= 255 for i in end_octs):
        print('Выход за допустимый диапазон', end)
        return 'Выход за допустимый диапазон'
    else:
        end_correct = True

    # пока не знаю, как это лучше сделать
    if start_correct and end_correct:
        endNum = int(end_octs[3]) + int(end_octs[2] * 256) + int(end_octs[1] * (256 ** 2)) + int(end_octs[0] * (256 ** 3))
        print(endNum)
        startNum = int(start_octs[3]) + int(start_octs[2] * 256) + int(start_octs[1] * (256 ** 2)) + int(start_octs[0] * (256 ** 3))
        if endNum - startNum > 0:
            print('Неверный порядок адресов')
            return 'Неверный порядок адресов'
    return 'OK'





# команды для павершелл
command_list = ['$list = [System.Collections.Generic.List[string]]::new()',
                '$output = Test-Connection -IPAddress 127.0.0.1 -Quiet -Count 1',
                '$list.Add($output)',
                '$output = Test-Connection -IPAddress 127.0.0.1 -Quiet -Count 1',
                '$list.Add($output)',
                '$list | Out-File ',
                ]

p = subprocess.Popen(["powershell.exe",
              '\n'.join(command_list)],
              stdout=a)

p.communicate()
p.kill()