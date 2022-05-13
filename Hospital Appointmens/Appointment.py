from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime
from tkcalendar import Calendar
from tkcalendar import DateEntry
from datetime import date
import csv
import re
import uuid
import sqlite3
import rsa



publicKey, privateKey = rsa.newkeys(512)

con=sqlite3.Connection('HospitalDB.db')
cur=con.cursor()
query ='SELECT (DepName || ":") as name , DoctorName,DoctorSurname FROM HospitalDoctors doc JOIN HospitalDepartments dep ON dep.DepID=doc.DepID WHERE IsOnVacation = 0 ORDER BY doc.DepID'
cur.execute(query)
options_doctor = cur.fetchall()
cur.close()

def save_info():
    userid_info = fid
    combo_info = myCombo_dep.get()
    combo_list = combo_info.split()
    dep_list = ([combo_list [index] for index in [0]])
    docn_list = ([combo_list [index] for index in [1]])
    docs_list = ([combo_list [index] for index in [2]])
    dep_with_symbol =''.join(dep_list)
    docname ="".join(docn_list)
    docsurname="".join(docs_list)
    depname = dep_with_symbol .replace(":","")
    cur=con.cursor()
    cur.execute('SELECT DepID FROM HospitalDepartments  WHERE DepName = ? ',(depname,))
    dep_dblist = cur.fetchall()
    cur.close()
    dep_id_withcoma="".join(map(str,dep_dblist))
    department_info = dep_id_withcoma.replace(",", "").replace("(","").replace(")","")
 
    cur=con.cursor()
    cur.execute('SELECT DoctorID FROM HospitalDoctors  WHERE DoctorName = ?  AND DoctorSurname = ?',(docname,docsurname))
    doc_dblist = cur.fetchall()
    cur.close()
    doc_id_withcoma="".join(map(str,doc_dblist))
    doctor_info = doc_id_withcoma.replace(",", "").replace("(","").replace(")","")

    today = datetime.today().strftime('%d-%m-%Y')
    todayfr = today
    date_info = cal.get_date()
    time_info=myCombo_timepicker.get()
    key=(str(uuid.uuid4().fields[-1])[:10])
    status="Pending"

    if(date_info < todayfr):
        messagebox.showwarning(title="Error",message="Warning: Enter valid appointment date! ")
    else:
        
        if (not userid_info.isdigit()):
            messagebox.showwarning(title="Error",message="Warning: Enter valid login! ")
            return -1

        else:
            cur=con.cursor()
            login=cur.execute("SELECT * from HospitalAppointments  WHERE DoctorID = ? AND AppointmentDate = ? AND AppointmentDateTime = ? AND AppointmentStatus='Pending'",(doctor_info,date_info,time_info)) 
            if cur.fetchone():
                messagebox.showwarning(title="Error",message="Warning: This time is booked")
                return 1
            
            cur=con.cursor()
            login=cur.execute("SELECT * from HospitalClientsCred WHERE UserID = ?",(userid_info,)) 
            if cur.fetchone():

                z = (key,
                     department_info,
                     doctor_info,
                     userid_info,
                     date_info,
                     time_info,
                     status,
                     today)

                    
                cur=con.cursor()
                cur.execute("insert into HospitalAppointments values(?,?,?,?,?,?,?,?)",z)
                con.commit()

                
                messagebox.showinfo(title="Error",message="Appointment to a doctor created successfully ")   
            else:
                messagebox.showwarning(title="Error",message="Warning: Enter valid login ")
                return -1



def comboclick(event):
    myLabel = Label(screen).pack()
    
def AppointmentPage():
    screen.destroy()
    import Checker_appo
    
def formPage():
    screen.destroy()
    import Form

    
screen = Tk()
screen.geometry("500x550")
screen.minsize(500, 550)
screen.maxsize(500, 550)

screen.title("Appointment to a doctor")
heading = Label(text="Appointment To a Doctor", bg="#140D4F", fg="#FFFFFF",font='Times 14', width="500", height="4")
heading.pack()

options_timepicker = [ "10:00","10:30","11:00","11:30","12:00","12:30","13:00","14:30","15:00","15:30","16:30","16:00","16:30","17:00","17:30"]

cal = Calendar(screen,fieldbackground='#FFFFFF',background='#140D4F',foreground='#FFFFFF',arrowcolor='white', selectmode = 'day',
               year = 2022, month = 5,
               day = 11,date_pattern='dd-mm-yyyy')



def grad_date():
    date.config(text = "Date is: " + cal.get_date())
    
date = Label(screen, text = "")
date.place(x="100",y="330")



myCombo_timepicker = ttk.Combobox(screen, state="readonly" ,value=options_timepicker,width="30")
myCombo_timepicker.current(0)
myCombo_timepicker.bind("<<ComboboxSelected>>",comboclick)
myCombo_timepicker.pack()



myCombo_dep = ttk.Combobox(screen, state="readonly", values=options_doctor,width="30")
myCombo_dep.current(0)
myCombo_dep.bind("<<ComboboxSelected>>",comboclick)
myCombo_dep.pack()

user_id_text = Label(text="User ID * ", )
dep_text = Label(text="Choose doctor: * ", )
cal_text = Label(text="Choose date of visit: * ", )
time_text =Label(text="Choose time of visit: * ")


user_id = StringVar()



user_id_entry = Entry(textvariable=user_id, width="33",fg="grey")
with open("userID.txt") as f:
   fid = f.read()
   if len(fid) == 0:
       user_id_entry.insert(END,user_id)
   else:
        user_id_entry.insert(END,fid)
        user_id_entry.config(state=DISABLED)
        f.close()

user_id_text.place(x=260,y=130)
dep_text.place(x=260,y=200)
cal_text.place(x=20, y=130)
time_text.place(x=260, y=270)


myCombo_timepicker.place(x=260,y=300)
user_id_entry.place(x=260,y=160)
myCombo_dep.place(x=260,y=230)

cal.place(x=20, y=160,width="200",height="160" )


btn_cal=ttk.Button(screen, text = "Select",width="10",command = grad_date)
btn_cal.place(x=20,y=330)




btn=ttk.Button(screen,width="20", text="Create appointment", command=save_info)
btn.place(x=180,y=400)



btn_page=Button(screen, text="Visitor's questionnaire",width="23",
                bg="#140D4F",fg="white",font='Times 10',command=formPage)
btn_page.place(x=0, y=70)

btn_page=Button(screen, text="Appointment info",width="23",
                bg="#140D4F", fg="white",font='Times 10',command=AppointmentPage)
btn_page.place(x=167, y=70)

btn_page=Button(screen, text="Hospital Info",width="23",
                bg="#140D4F", fg="white",font='Times 10',command=AppointmentPage)
btn_page.place(x=330, y=70)
screen.mainloop()
