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

doc_rank="""SELECT  hs.DoctorName || ' ' || hs.DoctorSurname as name,count(ha.AppointmentID) as total_appo,avg(he.Evaluation) as avg_evaluation
            FROM HospitalAppointments ha
            JOIN HospitalDoctors hs
            ON hs.DoctorID=ha.DoctorID
            JOIN HospitalAppoDocEvaluations he
            ON he.DocID = ha.DoctorID
            WHERE AppointmentStatus In("Closed","Evaluated")
            GROUP  BY  hs.DoctorName || hs.DoctorSurname
            ORDER BY total_appo Desc ,avg_evaluation DESC"""

cur.execute(doc_rank)
for doc_rank in cur.fetchall():
    print(doc_rank)


btn_page=Button(screen, text="Create Appointment",
                bg="#4abca5",fg="white",width="31",command=AppointmentPage)
btn_page.place(x=0, y=70)
btn_page.config(font=("Helvitica", 10, "bold"))

btn_page=Button(screen, text="Registration",
                bg="#4abca5", fg="white",width="30",command=RegistrationPage)
btn_page.place(x=250, y=70)
btn_page.config(font=("Helvitica", 10, "bold"))

screen.mainloop()
