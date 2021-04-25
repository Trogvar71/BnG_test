import subprocess
import sys

def generate_ip_list(start, end):
    # функция генерирует диапазон IP-адресов по заданному начальному и конечному значению
    ipList = []

    # Это на случай, если введен один адрес
    if start == end:
        ipList.append(start)
        return ipList
    ipList.append(str(start))
    start_octs = start.get_octs()
    # print(start_octs)
    end_octs = end.get_octs()
    # print(end_octs)
    ipOcts = start_octs[:]
    while ipOcts != end_octs:
        ipOcts[3] += 1
        if ipOcts[3] == 256:
            ipOcts[3] = 0
            ipOcts[2] += 1
        if ipOcts[2] == 256:
            ipOcts[2] = 0
            ipOcts[1] += 1
        if ipOcts[1] == 256:
            ipOcts[1] = 0
            ipOcts[0] += 1

        ipAddr = '.'.join([str(i) for i in ipOcts])
        ipList.append(ipAddr)
    # вывод адресов проверки ради
    # print(*ipList, sep='\n')
    return ipList


def generate_commands_list(ipList):
    # эта функция берет список айпишников и делает из него команды опроса для Powershell
    commands_list = []
    commands_list.append('$list = [System.Collections.Generic.List[string]]::new()')
    for i in ipList:
        test_command = '$output = Test-Connection -IPAddress ' + i + ' -Quiet -Count 1'
        commands_list.append(test_command)
        out_command = '$list.Add($output)'
        commands_list.append(out_command)
    commands_list.append('$list | Out-File out.txt')
    # вывод списка команд для проверки
    # print(*commands_list, sep='\n')
    return commands_list


def execute_commands(commands_list):
    # функция запускает Powershell и выполняет переданный ей список команд
    p = subprocess.Popen(["powershell.exe",
                          '\n'.join(commands_list)],
                         stdout=sys.stdout)
    p.communicate()
    p.kill()
    # результаты опроса намеренно выводятся в текстовый файл, поскольку так проще, чем с subprocess.PIPE
    # оттуда они будут переданы в .csv, опять же, для целей демонстрации, а затем в TableWidget
