import subprocess
import sys


# эта функция составляет список команд, которые выполнятся через PowerShell Remoting
# на заданном списке компьютеров
# лог выполнения пишется в файл Log_remote.txt
def generate_commands_list_remoting(names, commands):
    commands_list = []
    servers = '"' + '","'.join(names) + '"'
    command = 'Start-Transcript -Path Log_remote.txt'
    commands_list.append(command)
    command = '$srv_list = @(' + servers + ')'
    commands_list.append(command)
    for c in commands:
        command = 'Invoke-Command -ScriptBlock {' + c + '} -ComputerName $srv_list'
        commands_list.append(command)
    command = 'Stop-Transcript'
    commands_list.append(command)
    return commands_list


# функция запускает Powershell и выполняет переданный ей список команд
def execute_commands_remoting(commands_list):
    p = subprocess.Popen(["powershell.exe",
                          '\n'.join(commands_list)],
                         stdout=sys.stdout)
    p.communicate()
    p.kill()
