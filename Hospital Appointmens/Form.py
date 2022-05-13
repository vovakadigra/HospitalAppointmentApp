from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import Text
import csv
import datetime
import re
import uuid
import sqlite3
import os

con=sqlite3.Connection('HospitalDB.db')
cur=con.cursor()

with open('user_appointment.txt', 'r+') as file:
    global appointment_id
    appointment_id = file.read().rstrip()
    file.close()
with open('userID.txt', 'r+') as f:
    global user_id
    user_id = f.read().rstrip()
    print(user_id)
    f.close()

def AppointmentPage():
    screen.destroy()
    import checker

def save_info():
  score = visit_doctor.get()
  comment = t.get("1.0","end")
  
  
  k=(appointment_id,
     user_id,
     score,
     comment)
  
  cur.execute("insert into HospitalAppoEvaluations values(?,?,?,?)",k)
  con.commit()

  cur.execute("UPDATE HospitalAppointments SET  AppointmentStatus = 'Evaluated' WHERE AppointmentID = ?",(appointment_id,))
  con.commit()

  cur.execute("Select DoctorID FROM HospitalAppointments  WHERE AppointmentID = ?",(appointment_id,))
  doc_id =cur.fetchall()
  doc_id_withcoma="".join(map(str,doc_id))
  doctor_id = doc_id_withcoma.replace(",", "").replace("(","").replace(")","")
  
  doctors_score = visit_doctor.get()
  score_key=(str(uuid.uuid4().fields[-1])[:7])
  x = (score_key,
       appointment_id,
       doctor_id,
       user_id,
       doctors_score)


  cur.execute("insert into HospitalAppoDocEvaluations values(?,?,?,?,?)",x)
  con.commit()
  cur.close()
  
  
  messagebox.showinfo(title="Loading data",message="Thanks for your feedback!")
  import AppointmentInfo
  

    

screen = Tk()
screen.geometry("500x580")
screen.title("Attender`s form")
heading = Label(text="Private Hospital Clinic №2", bg="#140D4F", fg="#FFFFFF",font='Times 14', width="500", height="3")
heading.pack()

    
    

def ClearText():
  t.delete('1.0', END)





evald_text = Label(text="Evaluation of the doctor's work * ", )
evalh_text = Label(text="Evaluation of the hospital * ", )
comment_text = Label(text="Comments: * ", )
evald_text.place(x=260, y=150)
evalh_text.place(x=30, y=150)
comment_text.place(x=30,y=230)



visit_hospital=IntVar()
visit_doctor=IntVar()


t = Text(screen, width=20, height=3)
scroll = Scrollbar(screen)
t.configure(yscrollcommand=scroll.set)
t.place(x=30,y=260, width=440,height=200)
  
scroll.config(command=t.yview)
scroll.pack(side=RIGHT, fill=Y)


V1 = ttk.Radiobutton(screen,state=NORMAL,text="1", variable=visit_doctor, value="1")
V2 = ttk.Radiobutton(screen,state=NORMAL, text="2", variable=visit_doctor, value="2")
V3 = ttk.Radiobutton(screen,state=NORMAL, text="3", variable=visit_doctor, value="3")
V4 = ttk.Radiobutton(screen,state=NORMAL, text="4", variable=visit_doctor, value="4")
V5 = ttk.Radiobutton(screen,state=NORMAL, text="5", variable=visit_doctor, value="5")


R1 = ttk.Radiobutton(screen,state=NORMAL,text="1", variable=visit_hospital, value="1")
R2 = ttk.Radiobutton(screen,state=NORMAL, text="2", variable=visit_hospital, value="2")
R3 = ttk.Radiobutton(screen,state=NORMAL, text="3", variable=visit_hospital, value="3")
R4 = ttk.Radiobutton(screen,state=NORMAL, text="4", variable=visit_hospital, value="4")
R5 = ttk.Radiobutton(screen,state=NORMAL, text="5", variable=visit_hospital, value="5")


V1.place(x=260, y=180)
V2.place(x=290,y=180)
V3.place(x=320,y=180)
V4.place(x=350,y=180)
V5.place(x=380,y=180)

R1.place(x=30, y=180)
R2.place(x=60,y=180)
R3.place(x=90,y=180)
R4.place(x=120,y=180)
R5.place(x=150,y=180)



btn=ttk.Button(screen,width="15", text="Run", command=save_info)
btn.place(x=370,y=485)

btn=ttk.Button(screen,width="15", text="Clear", command=ClearText)
btn.place(x=260,y=485)

btn_page=Button(screen, text="Visitor's questionnaire",width="23",
                bg="#140D4F",fg="white",font='Times 10',command=AppointmentPage)
btn_page.place(x=0, y=70)

btn_page=Button(screen, text="Visit to a doctor",width="23",
                bg="#140D4F", fg="white",font='Times 10',command=AppointmentPage)
btn_page.place(x=167, y=70)

btn_page=Button(screen, text="Info",width="23",
                bg="#140D4F",fg="white",font='Times 10',command=AppointmentPage)
btn_page.place(x=330, y=70)






    













    
