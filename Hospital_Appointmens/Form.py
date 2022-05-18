from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from ttkthemes import ThemedTk
from tkinter import Text
import csv
import datetime
import re
import uuid
import sqlite3
from PIL import ImageTk, Image

con=sqlite3.Connection('database/HospitalDB.db')
cur=con.cursor()


with open('logs/userID.txt', 'r+') as f:
    user_id = f.read().rstrip()
    f.close()

    
def infoPage():
    screen.destroy()
    import Hospital_info
    
def AppointmentPage():
    screen.destroy()
    import Appointment
    

def save_info():
  score = visit_doctor.get()
  doctors_score = visit_doctor.get()
  comment = t.get("1.0","end")
  

  if score == 0 or doctors_score == 0:
      messagebox.showwarning(title="Visitor questiontionare ",message="Evaluation  fields can not be empty!")
  else:
      with open('logs/user_appointment.txt', 'r+') as file:
         appointment_id = file.read().rstrip()
         file.close()
      
      cur.execute("Select AppointmentID FROM  HospitalAppoEvaluations Where AppointmentID = ? ",(appointment_id,))
      if cur.fetchone():
          messagebox.showwarning(title="Visitor questiontionare ",message="You have already  created a feedback for this appointment!")
      else:
          with open('logs/user_appointment.txt', 'r+') as file:
              appointment_id = file.read().rstrip()
              file.close()
              
              k=(appointment_id,
                 user_id,
                 score,
                 comment)
              file.close()
              
          cur.execute("Insert into HospitalAppoEvaluations values(?,?,?,?)",k)
          con.commit()

          cur.execute("UPDATE HospitalAppointments SET  AppointmentStatus = 'Evaluated' WHERE AppointmentID = ?",(appointment_id,))
          con.commit()

          cur.execute("Select DoctorID FROM HospitalAppointments  WHERE AppointmentID = ?",(appointment_id,))
          doc_id =cur.fetchall()
          doc_id_withcoma="".join(map(str,doc_id))
          doctor_id = doc_id_withcoma.replace(",", "").replace("(","").replace(")","")
          
          
          score_key=(str(uuid.uuid4().fields[-1])[:7])
          
          with open('logs/user_appointment.txt', 'r+') as file:
            appointment_id = file.read().rstrip()
            file.close()
            x = (score_key,
               appointment_id,
               doctor_id,
               user_id,
               doctors_score)


          cur.execute("insert into HospitalAppoDocEvaluations values(?,?,?,?,?)",x)
          con.commit()
          
          cur.execute("UPDATE HospitalAppointments SET  AppointmentStatus = 'Evaluated' WHERE AppointmentID = ?",(appointment_id,))
          con.commit()
          cur.close()
          
          messagebox.showinfo(title="Loading data",message="Thanks for your feedback!")
          AppointmentPage()
  

screen = ThemedTk(theme="breeze")
screen.geometry("500x550")
screen.minsize(500, 550)
screen.maxsize(500, 550)
screen.title("Attender`s form")

heading = Label(screen,text='Hospital Clinic №2',fg="#FFFFFF", bg="#4abca5", width="500", height="2")
heading.config(font=("Helvitica", 24))
heading.pack()

canvas = Canvas(screen ,background='#4abca5', width = 50, height = 50,highlightthickness=0, relief='ridge')      
canvas.place(x=65, y=12)

pilImage = Image.open("img\logo.png")
img = ImageTk.PhotoImage(pilImage)
imgs =canvas.create_image(0, 0, anchor=NW,image=img) 
    

def ClearText():
  t.delete('1.0', END)
  

evald_text = Label(font=(None, 11),text="Evaluation of the doctor's work: ", )
evalh_text = Label( font=(None, 11),text="Total evaluation of the visit: ", )

comment_text = Label(text="Comments: * ", )
evald_text.place(x=260, y=151)
evalh_text.place(x=30, y=150)
comment_text.place(x=30,y=230)

visit_hospital=IntVar()
visit_doctor=IntVar()

t = Text(screen,background="white", width=20, height=3)
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
V2.place(x=300,y=180)
V3.place(x=340,y=180)
V4.place(x=380,y=180)
V5.place(x=420,y=180)

R1.place(x=30, y=180)
R2.place(x=70,y=180)
R3.place(x=110,y=180)
R4.place(x=150,y=180)
R5.place(x=190,y=180)

btn=ttk.Button(screen,width="15", text="Create", command=save_info)
btn.place(x=350,y=485)

btn=ttk.Button(screen,width="15", text="Clear", command=ClearText)
btn.place(x=210,y=485)

btn_page=Button(screen, text="Create Appointment",
                bg="#4abca5",fg="white",width="31",command=AppointmentPage)
btn_page.place(x=0, y=70)
btn_page.config(font=("Helvitica", 10, "bold"))

btn_page=Button(screen, text="Hospital Info",
                bg="#4abca5", fg="white",width="30",command=infoPage)
btn_page.place(x=250, y=70)
btn_page.config(font=("Helvitica", 10, "bold"))
                
screen.mainloop()
