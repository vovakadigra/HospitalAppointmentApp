from tkinter import *
from tkinter import ttk
from ttkthemes import ThemedTk
from tkinter import messagebox
import sqlite3
import rsa
import getpass

con=sqlite3.Connection('database/HospitalDB.db')
cur=con.cursor()
publicKey, privateKey = rsa.newkeys(512)


def Registration():
    screen.destroy()
    import Register  

def AppointmentPage():
    screen.destroy()
    import Appointment

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
            f = open("logs/userID.txt", "w+")
            f.write(userid_info)
            f.close()
            AppointmentPage()
            
            
            
        else:
             messagebox.showwarning(title="Error",message="Warning: Enter valid login and password ")
             return -1    

screen = ThemedTk(theme="breeze")
screen.geometry("300x270")
screen.title("Registration form")

heading = Label(text="Private Clinic №2", bg="#4abca5", fg="#FFFFFF", width="500", height="2")
heading.config(font=("Helvitica", 22))
heading.pack()

id_text = Label(text="Client ID * ", )
password_text=Label(text="Password *,  ",)

id_text.place(x=50, y=90)
password_text.place(x=50,y=145)

password = StringVar()
user_id = StringVar()


    
user_id_entry = ttk.Entry(textvariable=user_id, width="28")
with open("logs/userID.txt") as f:
    fid = f.read()
    if len(fid) == 0:
        user_id_entry.insert(END,user_id)
        f.close()
    else:
        user_id_entry.insert(END,fid)
        f.close()

password_entry = ttk.Entry(textvariable=password,show="*", width="28")

user_id_entry.place(x=50, y=115)
password_entry.place(x=50, y=170)


btn=ttk.Button(screen,width="12", text="Login",command=check_info)
btn.place(x=110,y=215)

btn=ttk.Button(screen,width="4", text="<<",command=Registration)
btn.place(x=50,y=215)
screen.mainloop()
