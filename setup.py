#!/usr/bin/env python

import subprocess
import os
from spider.__init__ import __name__, __version__, __author__



__NAME__ = r"""
            ________                        _______       _     __
   / ____/ /____  _________  ____ _/ / ___/____  (_)___/ /__  _____
  / __/ / __/ _ \/ ___/ __ \/ __ `/ /\__ \/ __ \/ / __  / _ \/ ___/
 / /___/ /_/  __/ /  / / / / /_/ / /___/ / /_/ / / /_/ /  __/ /    
/_____/\__/\___/_/  /_/ /_/\__,_/_//____/ .___/_/\__,_/\___/_/     
                                       /_/

"""



def shellSetup():
    import ctypes

    # ft = Figlet(font='slant')
    ctypes.windll.kernel32.SetConsoleTitleW(ctypes.c_wchar_p(f"{__name__}{__version__}_by_{__author__}"))
    print(f"\033[1;5;7;37;40m{__name__}\033[0mv{__version__}\nBy {__author__}\n\
        {__NAME__}\
        \n注意:下载后的文件保存在根目录下的Download文件夹中\
        \n\033[0;32m-----用`Ctrl+C` 退出下载-----\033[0m")
    subprocess.call("python .\\spider\\main.py")

def common_shell_setup():
    path = os.getcwd()
    print(f"\033[1;5;7;37;40m{__name__}\033[0mv{__version__}\nBy {__author__}\n\
        {__NAME__}\
        \n注意:下载后的文件保存在根目录下的Download文件夹中\
        \n\033[0;32m-----用`exit()` 退出下载-----\033[0m")
    subprocess.call(f"python {path}/spider/main.py")




import sys
if sys.platform.startswith("win"):
    shellSetup()
else: 
    common_shell_setup()
    
    