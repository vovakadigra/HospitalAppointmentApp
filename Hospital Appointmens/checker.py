from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sqlite3
import rsa
import getpass


con=sqlite3.Connection('HospitalDB.db')
cur=con.cursor()
publicKey, privateKey = rsa.newkeys(512)


def Registration():
    screen.destroy()
    import RegistrationForm  

def AppointmentPage():
    screen.destroy()
    import AppointmentInfo 

def check_info():
    userid_info = user_id.get()
    password_info = password.get()

    

    if len(userid_info)== 0 and len(password_info)>=6:
        messagebox.showwarning(title="Error",message="Warning: Enter valid login and password!")
        return -1
    if not userid_info.isdigit():
        messagebox.showwarning(title="Error",message="Warning: Id consist only of numbers!")
        return -1

    else:
        login=cur.execute("SELECT * from HospitalClientsCred WHERE UserID = ? AND UserPassword = ? ",(userid_info,password_info))
        
        if cur.fetchone(): 
            print(userid_info)
            AppointmentPage()
            
            
            
        else:
             messagebox.showwarning(title="Error",message="Warning: Enter valid login and password ")
             return -1    

screen = Tk()
screen.geometry("350x300")
screen.title("Registration form")
heading = Label(text="Private Clinic №2", bg="#140D4F", fg="#FFFFFF",font='Times 15', width="500", height="4")
heading.pack()

id_text = Label(text="Client ID * ", )
password_text=Label(text="Password *,  ",)

id_text.place(x=90, y=110)
password_text.place(x=90,y=170)

password = StringVar()
user_id = StringVar()


    
user_id_entry = ttk.Entry(textvariable=user_id, width="30")
with open("userID.txt") as f:
    fid = f.read()
    if len(fid) == 0:
        user_id_entry.insert(END,user_id)
        f.close()
    else:
        user_id_entry.insert(END,fid)
        f.close()

password_entry = ttk.Entry(textvariable=password,show="*", width="30")

user_id_entry.place(x=90, y=140)
password_entry.place(x=90, y=200)


btn=ttk.Button(screen,width="15", text="Login",command=check_info)
btn.place(x=135,y=240)

btn=ttk.Button(screen,width="5", text="<<",command=Registration)
btn.place(x=90,y=240)

