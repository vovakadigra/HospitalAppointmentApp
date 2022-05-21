from  tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from ttkthemes import ThemedTk
import sqlite3
from operator import itemgetter
from PIL import ImageTk, Image
import sqlite3

def AppointmentPage():
    screen.destroy()
    import Login

def RegistrationPage():
    screen.destroy()
    import Register



con=sqlite3.Connection('database/HospitalDB.db')
cur=con.cursor()



screen = ThemedTk(theme="breeze")
screen.geometry("500x550")
screen.minsize(500, 550)
screen.maxsize(500, 550)

screen.title("Hospital Clinic №2")


heading = Label(text="Hospital Clinic №2", bg="#4abca5", fg="#FFFFFF", width="500",height=2)
heading.config(font=("Helvitica", 24))
heading.pack()


canvas = Canvas(heading ,background='#4abca5', width = 50, height = 50,highlightthickness=0, relief='ridge')      
canvas.place(x=45, y=12)

pilImage = Image.open("img\logo.png")
img = ImageTk.PhotoImage(pilImage)

imgs =canvas.create_image(0, 0, anchor=NW,image=img) 

canvas2 = Canvas(screen ,background='#4abca5', width = 210, height = 130,highlightthickness=0, relief='ridge')      
canvas2.place(x=20, y=120)
pilImage2 = Image.open("img\hospital1.jpg")
img2 = ImageTk.PhotoImage(pilImage2)

imgs2 =canvas2.create_image(0, 0, anchor=NW,image=img2)

canvas3 = Canvas(screen , width = 100, height = 340,highlightthickness=0, relief='ridge')      
canvas3.place(x=235, y=110)

var = StringVar()
var1 = StringVar()
var2 = StringVar()
label = Label( canvas3, textvariable=var,justify='left' )
label.pack( anchor="w")
label.config(font=("Helvitica", 11))

var.set("       Hospital Clinic №2, Ukraine \n"
"\n  Hospital Clinic №2 has been named\n"
"  the world’s No. 2 ranked hospital \n"
"  according to Newsweek World’s Best \n"
"  Hospital 2021 and No.1 in cardiology  \n"
"  (heart) since 1995 according to U.S.\n"
"  News & World Report.\n")
canvas5 = Canvas(screen , width = 225, height = 120,highlightthickness=0, relief='ridge')      
canvas5.place(x=250, y=275)
pilImage3 = Image.open("img\hospital.jpg")
img3 = ImageTk.PhotoImage(pilImage3)

imgs3 =canvas5.create_image(0, 0, anchor=NW,image=img3)
canvas4 = Canvas(screen ,background='#FFFFFF', width = 220, height = 200,highlightthickness=0, relief='ridge')      
canvas4.place(x=15, y=255)
label2 = Label( canvas4, textvariable=var1,justify='left' )
label2.pack( anchor="w")
label2.config(font=("Helvitica", 11))
var1.set("\nThrough this collaboration, both\n"
"organizations can pursue the\n"
"same passion to focus on needs\n"
"of each individual patients and\n"
"help patients gain clarity over\n"
"their complex medical conditions.\n")
imgs3 =canvas5.create_image(0, 0, anchor=NW,image=img3)
canvas6 = Canvas(screen , width = 220, height = 60,highlightthickness=0, relief='ridge')      
canvas6.place(x=15, y=379)
label3 = Label( canvas6,textvariable=var2,justify='left' )
label3.pack( anchor="w")
label3.config(font=("Helvitica", 11))
var2.set("Contact us:\n"
"Ukraine, Lviv, Zelena 11,\n"
"Phone: (032)-64-21-06,\n"
"Phone: (032)-64-25-12\n")

btn_page=Button(screen, text="Create Appointment",
                bg="#4abca5",fg="white",width="31",command=AppointmentPage)
btn_page.place(x=0, y=70)
btn_page.config(font=("Helvitica", 10, "bold"))

btn_page=Button(screen, text="Registration",
                bg="#4abca5", fg="white",width="30",command=RegistrationPage)
btn_page.place(x=250, y=70)
btn_page.config(font=("Helvitica", 10, "bold"))

screen.mainloop()
