from cryptography.fernet import Fernet
from getpass import getpass
import os,subprocess,sys
from tkinter import *

os.chdir(os.path.dirname(sys.argv[0]))

def new(preset_name,username,password,close,preset_list):
    path = "accounts/" + preset_name
    preset_list.insert(preset_list.size()+1,preset_name)
    close.destroy()
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

def login(preset_name,steam_path,close):
    close.destroy()
    path = "accounts/" + preset_name
    with open("accounts/key.key","rb") as f:
        key = f.read()
    fer = Fernet(key)
    with open(path,"r") as f:
        creds = f.read().split("|")
        username = creds[0]
        password = fer.decrypt(creds[1].encode()).decode()
    
    subprocess.call([steam_path,"-login",username,password])

def new_new(steam_path,preset_list):
    rot = Tk()
    rot.resizable(False,False)

    user_text = Label(rot,text="Username")
    pass_text = Label(rot,text="Password")
    user_entry = Entry(rot,width=20)
    pass_entry = Entry(rot,show="*",width=20)
    done_button = Button(rot,text="Done",command=lambda:new(user_entry.get(),user_entry.get(),pass_entry.get(),rot,preset_list))

    user_text.grid(row=1,column=0)
    pass_text.grid(row=1,column=1)
    user_entry.grid(row=2,column=0)
    pass_entry.grid(row=2,column=1)
    done_button.grid(row=3,column=0,columnspan=2)

    rot.mainloop()


if os.path.exists("accounts") == False:
    os.mkdir("accounts")
with open("settings.config","r") as f:
    steam_path = f.readlines()[0] + "/steam.exe"

presets = os.listdir("accounts")
try:
    presets.remove("key.key")
except:
    pass

root = Tk()
root.resizable(False,False)

preset_list = Listbox(width=30)
new_button = Button(text="New",command=lambda:new_new(steam_path,preset_list))
open_button = Button(text="Open",command=lambda:login(preset_list.get(preset_list.curselection()), steam_path,root))
x = 1
for preset in presets:
    preset_list.insert(x,preset)
    x += 1

new_button.grid(row=0,column=0)
open_button.grid(row=0,column=1)
preset_list.grid(row=1,column=0,columnspan=2)
root.mainloop()
