import os
import sys
f = open("install.bat","a")
path = os.getcwd()
pythonpath = path.split("tasks")[0]
pythonpath += "tasks\\shared\\anaconda2\\Scripts\\easy_install.exe "
lines = open("C:\\user\\tasks\\shared\\requirements.txt").readlines()
for each in lines:
    f.write(pythonpath + each.strip() + "\n")
f.write(path.split("tasks")[0] + "tasks\\shared\\anaconda2\\Scripts\\conda.exe install azure -y \n")
f.write(path.split("tasks")[0] + "tasks\\shared\\anaconda2\\Scripts\\conda.exe install -c https://conda.anaconda.org/prkrekel azure-storage -y \n")
f.close()
os.system("install.bat")