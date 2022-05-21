from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from ttkthemes import ThemedTk
from tkinter.ttk import Notebook
from tkcalendar import Calendar
from tkcalendar import DateEntry
from datetime import datetime
from datetime import date
import csv
import re
import uuid
import sqlite3
import rsa
from PIL import ImageTk, Image
from operator import itemgetter


publicKey, privateKey = rsa.newkeys(512)
con=sqlite3.Connection('database/HospitalDB.db')
cur=con.cursor()
query ='SELECT (DepName || ":") as name , DoctorName,DoctorSurname FROM HospitalDoctors doc JOIN HospitalDepartments dep ON dep.DepID=doc.DepID WHERE IsOnVacation = 0 ORDER BY doc.DepID'
cur.execute(query)
options_doctor = cur.fetchall()
cur.close()

def RegistrationPage():
    screen.destroy()
    import Register
    
def InfoPage():
    screen.destroy()
    import Hospital_info

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

                cur.execute("Select * from HospitalAppointments")
        
        
                results_appo = cur.fetchall()
                headers = [i[0] for i in cur.description]

       
                with open('database/HospitalAppointments.csv', 'w', newline='') as userfile:
                    csvFile = csv.writer(userfile,delimiter=',', lineterminator='\r\n', escapechar='\\') 

                    csvFile.writerow(headers)
                    csvFile.writerows(results_appo)
                    userfile.close()

                
                messagebox.showinfo(title="Error",message="Appointment to a doctor created successfully ")   
            else:
                messagebox.showwarning(title="Error",message="Warning: Enter valid login ")
                return -1


def comboclick(event):
    myLabel = Label(screen).pack()
    
    
screen = ThemedTk(theme="breeze")
screen.geometry("500x550")
screen.minsize(500, 550)
screen.maxsize(500, 550)

notebook = Notebook(screen)
frame1 = Frame(notebook, width=500, height=550)
notebook.add(frame1, text = 'Create Appointment')

frame2 = Frame(notebook, width=500, height=550)
notebook.add(frame2, text = '  My Appointment  ')

frame3 = Frame(notebook, width=500, height=550)
notebook.add(frame3, text = '   My Profile  ')

frame4 = Frame(notebook, width=500, height=550)
notebook.add(frame4, text = ' Doctors Info ')

notebook.pack(expand=1, fill='both', padx=7, pady=7)

screen.title("Appointment to a doctor")
heading = Label(frame1,text='Hospital Clinic №2',fg="#FFFFFF", bg="#4abca5", width="500", height="2")
heading.config(font=("Helvitica", 24))
heading.pack()

canvas = Canvas(frame1 ,background='#4abca5', width = 50, height = 50,highlightthickness=0, relief='ridge')      
canvas.place(x=45, y=12)
pilImage = Image.open("img\logo.png")
img = ImageTk.PhotoImage(pilImage)
imgs =canvas.create_image(0, 0, anchor=NW,image=img) 

options_timepicker = [ "10:00","10:30","11:00","11:30","12:00","12:30","13:00","14:30","15:00","15:30","16:30","16:00","16:30","17:00","17:30"]

cal = Calendar(frame1,fieldbackground='#FFFFFF',background='#4abca5',selectbackground='#4abca5',weekendbackground='#d5edec', othermonthwebackground='#d5edec', headersbackground='white',foreground='#FFFFFF',arrowcolor='white', selectmode = 'day',
               year = 2022, month = 5,
               day = 11,date_pattern='dd-mm-yyyy')

def grad_date():
    date.config(text = "Date is: " + cal.get_date())
    
date = Label(frame1, text = "")
date.place(x="100",y="342")

myCombo_timepicker = ttk.Combobox(frame1, state="readonly" ,value=options_timepicker,width="28")
myCombo_timepicker.current(0)
myCombo_timepicker.bind("<<ComboboxSelected>>",comboclick)
myCombo_timepicker.pack()

myCombo_dep = ttk.Combobox(frame1, state="readonly", values=options_doctor,width="28")
myCombo_dep.current(0)
myCombo_dep.bind("<<ComboboxSelected>>",comboclick)
myCombo_dep.pack()

user_id_text = ttk.Label(frame1,text="User ID * ", )
dep_text = Label(frame1,text="Choose doctor: * ", )
cal_text = Label(frame1,text="Choose date of visit: * ", )
time_text =Label(frame1,text="Choose time of visit: * ")

user_id = StringVar()

user_id_entry = ttk.Entry(frame1,textvariable=user_id, width="29")
with open("logs/userID.txt") as f:
   fid = f.read()
   if len(fid) == 0:
       user_id_entry.insert(frame1,END,user_id)
   else:
        user_id_entry.insert(END,fid)
        user_id_entry.config( state="readonly",background='black')
        user_id_entry.config(foreground="#42474a",state="disabled")
        f.close()
        
user_id_text.place(x=260,y=130)
dep_text.place(x=260,y=200)
cal_text.place(x=20, y=130)
time_text.place(x=260, y=270)


myCombo_timepicker.place(x=260,y=300)
user_id_entry.place(x=260,y=160)
myCombo_dep.place(x=260,y=230)

cal.place(x=20, y=160,width="200",height="170" )

btn_cal=ttk.Button(frame1, text = "Select",width="8",command = grad_date)
btn_cal.place(x=20,y=340,height="25")

style2 = ttk.Style()
style2.configure('TButton', foreground='#185c4e')
btn_creation=ttk.Button(frame1,width="20", text="Create Appointment", command=save_info)
btn_creation.place(x=180,y=400)


def enabled_button2():
    button2.configure(state="enabled")
def enabled_button3():
    button3.configure(state="enabled")
    
def selectItem(a):
    curItem = tree.focus()
    if(len(curItem)==0):
       return -1

def clear_all():
   for item in tree.get_children():
      tree.delete(item) 
def vis_que():
    curItem = tree.focus()
    if(len(curItem)==0):
        messagebox.showwarning(title="Cancel Appointment ",message="Choose appointment!")
    else:
        app_checkdict = (tree.item(curItem))
        iscanceled_checker=(app_checkdict.get('values', 1))
        appost=itemgetter(4)(iscanceled_checker)
        
        appdict = (tree.item(curItem))
        b=(appdict.get('values', 5))
        appoid=itemgetter(5)(b)
        
        if appost !="Closed":
            messagebox.showwarning(title="Visitor questionnaire ",message='You can only create a visitor questionnaire'
                                  '\non field with status "Closed"')
            return -1
        else:
            f=open("logs/user_appointment.txt","w+")
            f.write(str(appoid))

            screen.destroy()
            import Form
    
def updateItem():
    curItem = tree.focus()
    if(len(curItem)==0):
        messagebox.showwarning(title="Cancel appointment ",message="Choose appointment to cancel!")
        return -1
        
    else:
        app_checkdict = (tree.item(curItem))
        iscanceled_checker=(app_checkdict.get('values', 1))
        appost=itemgetter(4)(iscanceled_checker)

        appdict = (tree.item(curItem))
        b=(appdict.get('values', 5))
        appoid=itemgetter(5)(b)
        
        if appost =="Canceled":
            
            messagebox.showwarning(title="Cancel appointment ",message="This appointment  is already canceled!")
            return -1
        else:
            MsgBox = messagebox.askquestion ('Exit Application','Are you sure that you want to cancel appointment?',icon = 'warning')
            if MsgBox == 'yes':
                cur7 = con.cursor()
                cur7.execute("UPDATE HospitalAppointments SET AppointmentStatus = 'Canceled' Where AppointmentID = ?",(appoid,))
                con.commit()
                messagebox.showinfo(title="Cancelled  appointment ",message="Your appointment  was canceled")
            
            else:
                return-1
        
def View():
    con1 = sqlite3.connect("database/HospitalDB.db")
    cur1 = con1.cursor()
    
    with open("logs/userID.txt") as f:
        user_id = f.read()
        if len(user_id) != 0:
            cur1.execute("UPDATE HospitalAppointments Set AppointmentStatus='Closed'  WHERE AppointmentDate < strftime('%d-%m-%Y', Date()) AND  AppointmentStatus Not IN('Evaluated','Canceled')")
            con.commit()
            cur1.execute("SELECT hde.DepName,(hd.DoctorName ||' '|| hd.DoctorSurname)as DoctorFullmame,AppointmentDate,AppointmentDateTime,AppointmentStatus,AppointmentID FROM HospitalAppointments ha  JOIN HospitalDoctors hd ON hd.DoctorID=ha.DoctorID JOIN HospitalDepartments hde ON ha.DepartmentID=hde.DepID WHERE ClientID = ?",(user_id,))
            rows = cur1.fetchall()
            cur1.close()
            if len(rows) == 0:
                import tkinter
                MsgBox = tkinter.messagebox.askquestion ('Exit Application','It seems like you don`t have any appointments yet.'
                                                         '\nDo you want to create one?',icon = 'warning')
                if MsgBox == 'yes':
                    screen.destroy()
                    import Appointment
                else:
                    return -1
            else:
                for row in rows:
                    tree.insert("", END, values=row)        
                    con1.close()
                    f.close()

def calculate_age(dateofbirth_clinfo):
    from datetime import date
    today = date.today() 
    return today.year - dateofbirth_clinfo.year - ((today.month, today.day) < (dateofbirth_clinfo.month, dateofbirth_clinfo.day))


global appoid
with open("logs/userID.txt") as f:
    user_idinfo = f.read()
    f.close()
    
 
cur3 = con.cursor()
rows = cur3.execute("SELECT Firstname || ' ' || Lastname as Fullname,Country,DateOfBirth,Phone,hd.UserPassword FROM HospitalClients hc  JOIN HospitalClientsCred hd ON hd.UserID=hc.CliendID  WHERE CliendID = ?",(user_idinfo,))
for rows_client in cur3.fetchall():
    fullname_cl = ([rows_client [index] for index in [0]])
    fullname_cl_withcoma="".join(map(str,fullname_cl))
    global fullname_user_cl
    fullname_user_cl = fullname_cl_withcoma.replace(",", "").replace("(","")


    country_cl = ([rows_client [index] for index in [1]])
    country_cl_withcoma="".join(map(str,country_cl))
    global coutry_user_cl
    country_user_cl = country_cl_withcoma.replace(",", "").replace("(","")
    
    dateofbirth_cl = ([rows_client [index] for index in [2]])
    dateofbirth_cl_withcoma="".join(map(str,dateofbirth_cl))
    dateofbirth_clinfo = dateofbirth_cl_withcoma.replace(",", "").replace("(","").replace(")","").replace("-","/")
    dateofbirth_clinfo = datetime.strptime(dateofbirth_clinfo,'%d/%m/%Y')
    dateofbirth_clinfo = dateofbirth_clinfo.date()
    age_user_cl = calculate_age(dateofbirth_clinfo)
    
    phone_cl = ([rows_client [index] for index in [3]])
    phone_cl_withcoma="".join(map(str,phone_cl))
    phone_user_cl = phone_cl_withcoma.replace(",", "").replace("(","")

    password_cl = ([rows_client [index] for index in [4]])
            
cur3.close()
heading = Label(frame2,text='Hospital Clinic №2',fg="#FFFFFF", bg="#4abca5", width="500", height="2")
heading.config(font=("Helvitica", 24))
heading.pack()
canvas1 = Canvas(frame2, background='#4abca5', width = 50, height = 50,highlightthickness=0, relief='ridge')    
canvas1.place(x=45, y=12)
pilImage = Image.open("img\logo.png")
img2 = ImageTk.PhotoImage(pilImage)
imgs =canvas1.create_image(0, 0, anchor=NW,image=img) 
style1 = ttk.Style(frame2)

style1.configure('Treeview.Heading',font=(None, 8))
style1.configure('Treeview',font=(None, 9))
tree = ttk.Treeview(frame2, column=("c1", "c2", "c3","c4","c5"), show='headings')
style1.map('Treeview', background=[('selected', '#4abca5')])
tree.place(x=5,y=100)

tree.column("#1", minwidth=0 ,width=90)
tree.heading("#1", text="Department")

tree.column("#2", anchor=CENTER,width=100)
tree.heading("#2", text="Doctor")

tree.column("#3", anchor=CENTER,width=90)
tree.heading("#3", text="Date")

tree.column("#4", anchor=CENTER,width=70)
tree.heading("#4", text="Time")

tree.column("#5", anchor=CENTER,width=90)
tree.heading("#5", text="Status")

tree.bind('<ButtonRelease-1>', selectItem)

button1 = ttk.Button(frame2,text="Show data",command=lambda: [clear_all(), View(),enabled_button2(),enabled_button3()],width="15")
button1.place(x=350,y=380)

button2 = ttk.Button(frame2,text="Cancel",state="disabled", command=updateItem,width="15")
button2.place(x=220,y=380)

button3 = ttk.Button(frame2,text="Rate Visit",state="disabled", command=vis_que,width="15")
button3.place(x=90,y=380)

def update_info():
    MsgBox = messagebox.askquestion ('Exit Application','Are you sure that you want to update your data?',icon = 'warning')
    if MsgBox == 'no':
        return -1
    else:
        updated_phone=phone.get()
        old_pwd =old_password.get()
        new_pwd =new_password.get()

        if(len(str(old_pwd)) <6) and (len(str(new_pwd)) <6):
            messagebox.showwarning(title="Error",message="Warning: Password  should  consist of 6 symbols")
            return -1
        
        with open("logs/userID.txt") as f:
            user_id_info = f.read()
            f.close()
        if( updated_phone.isdigit()):
            output_phone = re.findall(r"^(?:(\+)?38)?(0\d{9})$",updated_phone)
        else:
            messagebox.showwarning(title="Error",message="Warning: Enter a valid Phone number")
            return -1
        if(len(output_phone)!=1):
            messagebox.showwarning(title="Error",message="Warning: Enter a valid Phone number")
            return -1
        cur4=con.cursor()
        cur4.execute("Select Phone,CliendID From HospitalClients Where Phone = ? And CliendID != ?",(str(updated_phone),str(user_id_info),))
        if cur4.fetchone():
            messagebox.showwarning(title="Eror",message="This number is already registered on the app")
            return -1
        cur4.close()
        
        cur5=con.cursor()
        cur5.execute("Select UserID From HospitalClientsCred Where UserID = ? And UserPassword = ?",(str(user_id_info),str(old_pwd),))
        if cur5.fetchone():
            cur5.execute("UPDATE HospitalClientsCred SET UserPassword = ? Where UserID = ?",(str(new_pwd),str(user_id_info),))
            cur5.execute("UPDATE HospitalClients SET Phone = ? WhERE CliendID = ?",(str(updated_phone),str(user_id_info)))
            con.commit()                                                                            

            messagebox.showinfo(title="Updating data",message="Updated data succesfully")
            delete_entry()                                                                        
        else:
            return -1
def enable_update():
    button6.config(state="enabled")
        
def delete_entry():
    user_new_password.forget()
    user_old_password.forget()
    pass_entry.forget()
    pass_entry_old.forget()
    
def recover_label():
    user_new_password.pack()
    user_old_password.pack()
    pass_entry_old.pack()
    pass_entry.pack()

    user_old_password.place(x=250,y=230)
    user_new_password.place(x=250,y=285)
    pass_entry_old.place(x=250,y=250)
    pass_entry.place(x=250,y=305)
    
def enable_editing():
    phone_entry.config( state="enabled")

heading = Label(frame3,text='Hospital Clinic №2',fg="#FFFFFF", bg="#4abca5", width="500", height="2")
heading.config(font=("Helvitica", 24))
heading.pack()

canvas1 = Canvas(frame3, background='#4abca5', width = 50, height = 50,highlightthickness=0, relief='ridge')    
canvas1.place(x=45, y=12)

pilImage = Image.open("img\logo.png")
img2 = ImageTk.PhotoImage(pilImage)
imgs =canvas1.create_image(0, 0, anchor=NW,image=img2) 

canvas1 = Canvas(frame3, width = 120, height = 120,highlightthickness=0, relief='ridge')    
canvas1.place(x=67, y=105)
pilImage = Image.open("img\icon.png")
img3 = ImageTk.PhotoImage(pilImage)
imgs =canvas1.create_image(0, 0, anchor=NW,image=img3) 

name = StringVar()
age = StringVar()
country = StringVar()
phone = StringVar()
old_password=StringVar()
new_password=StringVar()
gender = StringVar()

user_name = ttk.Label(frame3,text="Username:  ", )
user_age = ttk.Label(frame3,text="Age:  ", )
user_country = ttk.Label(frame3,text="Country:  ", )
user_idcl = ttk.Label(frame3,text="User ID:  ", )
user_phone = ttk.Label(frame3,text="Phone:  ", )
user_new_password = ttk.Label(frame3,text="New Password :  ", )
user_old_password = ttk.Label(frame3,text="Old Password :  ", )

user_new_password.pack()
user_old_password.pack()

user_name.place(x=16,y=225)
user_age.place(x=16,y=340)
user_country.place(x=16,y=285)

user_idcl.place(x=250,y=115)
user_phone.place(x=250,y=175)

user_identry = ttk.Entry(frame3,textvariable=user_id, width="29")
user_identry.place(x=250,y=140)
user_identry.config( foreground="#42474a",state="disabled")

phone_entry = ttk.Entry(frame3,textvariable=phone, width="29")
phone_entry.place(x=250,y=195)
phone_entry.insert(END,phone_user_cl)
phone_entry.config( foreground="#42474a",state="disabled")

pass_entry = ttk.Entry(frame3,show='*',textvariable=new_password, width="29")
pass_entry.pack()

pass_entry_old = ttk.Entry(frame3,show='*',textvariable=old_password, width="29")
pass_entry_old.pack()

delete_entry()

button5 = ttk.Button(frame3,text="Edit",command=lambda: [recover_label(),enable_editing(),enable_update()],width="11")
button5.place(x=250,y=425)

button6 = ttk.Button(frame3,text="Update",state="disabled",command=update_info,width="11")
button6.place(x=367,y=425)

username_entry = ttk.Entry(frame3,textvariable=name, width="29")
username_entry.place(x=15,y=250)
username_entry.insert(END,fullname_user_cl)
username_entry.config(foreground="#42474a",state="disabled")


age_entry = ttk.Entry(frame3,textvariable=age, width="29")
age_entry.place(x=15,y=360)
age_entry.insert(END,age_user_cl)
age_entry.config(foreground="#42474a",state="disabled")

country_entry = ttk.Entry(frame3,textvariable=country, width="29")
country_entry.place(x=15,y=305)
country_entry.insert(END,country_user_cl)
country_entry.config( foreground="#42474a",state="disabled")


btn_page=Button(screen, text="Hospital Info",
                bg="#4abca5",fg="white",width="30",command=InfoPage)
btn_page.place(x=6, y=100)
btn_page.config(font=("Helvitica", 10, "bold"))

btn_page=Button(screen, text="Registration",
                bg="#4abca5", fg="white",width="29",command=RegistrationPage)
btn_page.place(x=250, y=100)
btn_page.config(font=("Helvitica", 10, "bold"))

def View2():
    con9 = sqlite3.connect("database/HospitalDB.db")
    cur9 = con9.cursor()
    doc_rank="""with cte as(
                    SELECT DoctorID,
                    count(AppointmentID) as total_appo
                    FROM HospitalAppointments 
                    GROUP by DoctorID),
                    cte1 as(SELECT ha.DoctorID,
                            avg(he.Evaluation) as avg_evaluation
                            FROM HospitalAppointments ha
                            JOIN HospitalAppoDocEvaluations he
                            ON he.DocID = ha.DoctorID
                            WHERE AppointmentStatus In("Closed","Evaluated")
                            GROUP  BY  ha.DoctorID)
                    SELECT DoctorName || ' '  || DoctorSurname as DocName,DepName,total_appo,
                    IFNULL(avg_evaluation, 'No score')avg_evaluation FROM cte
                    LEFT JOIN cte1
                    ON cte.DoctorID=cte1.DoctorID
                    JOIN HospitalDoctors hd
                    ON hd.DoctorID =cte.DoctorID
                    JOIN HospitalDepartments hde
                    ON hd.DepID=hde.DepID
                    ORDER By total_appo DESC"""
    
    cur9.execute(doc_rank)
    rows_doc = cur9.fetchall()
    
    for rows_doc in rows_doc:
        tree2.insert("", END, values=rows_doc)        
        con9.close()
        
def clear_all2():
   for item in tree2.get_children():
      tree2.delete(item)

      
def selectItem2(a):
    curItem = tree2.focus()
    if(len(curItem)==0):
       return -1

heading = Label(frame4,text='Hospital Clinic №2',fg="#FFFFFF", bg="#4abca5", width="500", height="2")
heading.config(font=("Helvitica", 24))
heading.pack()

canvas = Canvas(frame4 ,background='#4abca5', width = 50, height = 50,highlightthickness=0, relief='ridge')      
canvas.place(x=45, y=12)

pilImage = Image.open("img\logo.png")
img4 = ImageTk.PhotoImage(pilImage)
imgs =canvas.create_image(0, 0, anchor=NW,image=img4)

tree2 = ttk.Treeview(frame4, column=("c1", "c2", "c3","c4"), show='headings')
style1.map('Treeview', background=[('selected', '#4abca5')])
tree2.place(x=5,y=100)

tree2.column("#1", minwidth=0 ,width=110)
tree2.heading("#1", text="Doctor Name")

tree2.column("#2", minwidth=0 ,width=110)
tree2.heading("#2", text="Department")

tree2.column("#3",width=110)
tree2.heading("#3", text="Total Appointments")

tree2.column("#4",width=110)
tree2.heading("#4", text="AVG Score")

button1 = ttk.Button(frame4,text="Show data",command=lambda: [clear_all2(), View2()],width="15")
button1.place(x=180,y=380)

tree.bind('<ButtonRelease-1>', selectItem2)
screen.mainloop()
