# -*- coding: iso-8859-1 -*-
import subprocess, sys



# p = subprocess.Popen(["powershell.exe",
#               "write-output 'test' \n write-output 'test2'"],
#               stdout=subprocess.PIPE)

# result = p.stdout.readlines()

# p.communicate()
# p.kill()
# print(*result, sep='\n')

p = subprocess.Popen(["powershell.exe",
              "write-output 'test' \n write-output 'test2'"],
              stdout=sys.stdout)

p.communicate()
p.kill()




