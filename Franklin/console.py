from cryptography.fernet import Fernet
from getpass import getpass
import os,subprocess,sys

os.chdir(os.path.dirname(sys.argv[0]))

def new(preset_name):
    path = "accounts/" + preset_name
    username = input("Steam username\n:")
    password = getpass("Steam password (Input hidden)\n:")
    if os.path.exists("accounts/key.key") == False:
        key = Fernet.generate_key()
        with open("accounts/key.key","wb") as f:
            f.write(key)
    else:
        with open("accounts/key.key","rb") as f:
            key = f.read()
    fer = Fernet(key)
    with open(path,"w") as f:
        f.write(username + "|" + fer.encrypt(password.encode()).decode())
    input("Done")

def login(preset_name,steam_path):
    path = "accounts/" + preset_name
    with open("accounts/key.key","rb") as f:
        key = f.read()
    fer = Fernet(key)
    with open(path,"r") as f:
        creds = f.read().split("|")
        username = creds[0]
        password = fer.decrypt(creds[1].encode()).decode()
    
    subprocess.call([steam_path,"-login",username,password])

if os.path.exists("accounts") == False:
    os.mkdir("accounts")


with open("settings.config","r") as f:
    steam_path = f.readlines()[0] + "/steam.exe"

preset_name = input("Preset name\n:")
loin = "1" == input("Login:1 | New preset:2\n:")

if loin:
    login(preset_name, steam_path)
else:
    new(preset_name)
