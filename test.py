# -*- coding: iso-8859-1 -*-
import subprocess, sys



# p = subprocess.Popen(["powershell.exe",
#               "write-output 'test' \n write-output 'test2'"],
#               stdout=subprocess.PIPE)

# result = p.stdout.readlines()

# p.communicate()
# p.kill()
# print(*result, sep='\n')
command_list = ['$output = Test-Connection -IPAddress 127.0.0.1 -Count 1', '$output | Out-File out.txt']

p = subprocess.Popen(["powershell.exe",
              '\n'.join(command_list)],
              stdout=sys.stdout)

p.communicate()
p.kill()




