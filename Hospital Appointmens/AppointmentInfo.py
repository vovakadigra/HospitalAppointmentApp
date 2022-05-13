import tkinter
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sqlite3
from operator import itemgetter
  
    
def formPage():
    screen.destroy()
    import Form
    
def AppointmentPage():
    screen.destroy()
    import checker
    
 
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
        messagebox.showwarning(title="Cancel appointment ",message="Choose appointment!")
    else:
        app_checkdict = (tree.item(curItem))
        iscanceled_checker=(app_checkdict.get('values', 1))
        appost=itemgetter(5)(iscanceled_checker)
        
        appdict = (tree.item(curItem))
        b=(appdict.get('values', 6))
        appoid=itemgetter(6)(b)
        
        if appost =="Canceled":
            messagebox.showwarning(title="Cancel appointment ",message="You can not create visitors questionare on canceled appointment!")
            return -1
        else:
            f=open("user_appointment.txt","w+")
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
        appost=itemgetter(5)(iscanceled_checker)

        appdict = (tree.item(curItem))
        b=(appdict.get('values', 6))
        appoid=itemgetter(6)(b)


        
        if appost =="Canceled":
            messagebox.showwarning(title="Cancel appointment ",message="This appointment  is already canceled!")
            return -1
        else:
            MsgBox = tkinter.messagebox.askquestion ('Exit Application','Are you sure that you want to cancel appointment?',icon = 'warning')
            if MsgBox == 'yes':
                con1 = sqlite3.connect("HospitalDB.db")
                cur1 = con1.cursor()
                cur1.execute("UPDATE HospitalAppointments SET AppointmentStatus = 'Canceled' Where AppointmentID = ?",(appoid,))
                con1.commit()
                messagebox.showinfo(title="Cancelled  appointment ",message="Your appointment  was canceled")
            
            else:
                return-1
        
def View():
    con1 = sqlite3.connect("HospitalDB.db")
    cur1 = con1.cursor()
    
    with open("userID.txt") as f:
        user_id = f.read()
        if len(user_id) != 0:

            cur1.execute("SELECT hde.DepName,(hd.DoctorName ||' '|| hd.DoctorSurname)as DoctorFullmame,AppointmentDate,AppointmentDateTime,CreationDate,AppointmentStatus,AppointmentID FROM HospitalAppointments ha  JOIN HospitalDoctors hd ON hd.DoctorID=ha.DoctorID JOIN HospitalDepartments hde ON ha.DepartmentID=hde.DepID WHERE ClientID = ?",(user_id,))
            rows = cur1.fetchall()
            print(rows)
            if len(rows) == 0:
                import tkinter
                MsgBox = tkinter.messagebox.askquestion ('Exit Application','It seems like you don`t have a appointments yet.'
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




global appoid
screen = Tk()
screen.geometry("650x500")
screen.minsize(650, 500)
screen.maxsize(650, 500)
screen.title("My appointments list")
heading = Label(screen,text="My Appointments List", bg="#140D4F", fg="#FFFFFF",font='Times 15', width="400", height="3")
heading.pack()
label = ttk.Label(screen, text="Chose your appointment:",background="#f0f0f0",foreground="black",font='Times 16', width="500")
label.place(x=20,y=125)
style=ttk.Style()
style.theme_use('clam')

tree = ttk.Treeview(screen, column=("c1", "c2", "c3","c4","c5","c6"), show='headings')
tree.pack(expand=YES)
tree.column("#1", minwidth=0 ,anchor=CENTER,width=100)

tree.heading("#1", text="Dep.Name")

tree.column("#2", anchor=CENTER,width=125)

tree.heading("#2", text="Doctor Name")

tree.column("#3", anchor=CENTER,width=125)

tree.heading("#3", text="Appointment Date")

tree.column("#4", anchor=CENTER,width=50)

tree.heading("#4", text="Time")

tree.column("#5", anchor=CENTER,width=100)

tree.heading("#5", text="Creation date")

tree.column("#6", anchor=CENTER,width=100)

tree.heading("#6", text="Status")


tree.pack()

tree.bind('<ButtonRelease-1>', selectItem)

button1 = ttk.Button(text="Show data",command=lambda: [clear_all(), View()],width="20")
button1.place(x=490,y=420)

button1 = ttk.Button(text="Cancel", command=updateItem,width="20")
button1.place(x=340,y=420)
button1 = ttk.Button(text="Clear", command=clear_all,width="20")
button1.place(x=190,y=420)

button1 = ttk.Button(text="Visitor questionnare", command=vis_que,width="20")


button1.place(x=40,y=420)
btn_page=Button(screen, text="Visitor's questionnaire",width="30",
                bg="#140D4F",fg="white",font='Times 10',command=formPage)
btn_page.place(x=0, y=70)

btn_page=Button(screen, text="Visit to a doctor",width="30",
                bg="#140D4F", fg="white",font='Times 10',command=AppointmentPage)
btn_page.place(x=220, y=70)

btn_page=Button(screen, text="Info",width="30",
                bg="#140D4F",fg="white",font='Times 10',command=AppointmentPage)
btn_page.place(x=440, y=70)

btn_page=Button(screen, text="Info",width="30",
                bg="#140D4F",fg="white",font='Times 10',command=AppointmentPage)
btn_page.place(x=440, y=70)

