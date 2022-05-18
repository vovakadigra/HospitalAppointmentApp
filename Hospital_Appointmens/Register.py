from tkinter import *
from tkinter import ttk
from ttkthemes import ThemedTk
from tkinter import messagebox
from tkcalendar import Calendar
from datetime import datetime 
from datetime import date
from pytz import timezone
import csv
import re
import uuid
import sqlite3
from PIL import ImageTk, Image

ukraine_time = timezone('Europe/Kiev')
ua_time = datetime.now(ukraine_time)

con=sqlite3.Connection('database/HospitalDB.db')
cur=con.cursor()


def save_info():
    firstname_info = firstname.get()
    lastname_info = lastname.get()
    gender_info = gender.get()
    country_info = myCombo_country.get()
    phone_info = phone.get()
    date_info = cal.get_date()
    password_info = password.get()
    
    b_day = datetime.strptime(date_info, "%d-%m-%Y")
   
    if b_day.date() > ua_time.date():
        messagebox.showwarning(title="Error",message="Warning: Enter a valid Date of Birh!")
        return -1
    else:

        if(len(password_info) <6):
            messagebox.showwarning(title="Error",message="Warning: Password  should  consist of at least 6 symbols")
            return -1
        if(gender_info != "Male") and(gender_info != "Female"):
           messagebox.showwarning(title="Error",message="Choose your gender")
           return -1
        if( phone_info.isdigit()):
            output_phone = re.findall(r"^(?:(\+)?38)?(0\d{9})$",phone_info)
        else:
            messagebox.showwarning(title="Error",message="Warning: Enter a valid Phone number")
            return -1
            
        if(len(output_phone)!=1):
            messagebox.showwarning(title="Error",message="Warning: Enter a valid Phone number")
            return -1
        
        cur.execute("Select Phone From HospitalClients Where Phone = ?",(str(phone_info),))
        if cur.fetchone():
            messagebox.showwarning(title="Eror",message="This number is already registered on the app")
            return -1
        if(date_info == ""):
            messagebox.showwarning(title="Error",message="Warning: Enter a valid Date of Birth ")
            return -1
        
        if( len(firstname_info)>0):                
            firstname_info = re.sub(r'[^a-zA-Z\d\s:]', '',firstname_info)
            firstname_info = re.sub(r'[~^0-9]', '',firstname_info)
        else:
            messagebox.showwarning(title="Error",message="Warning: Enter a valid Firstname")
            return -1
            
        if(len(firstname_info)<1 and firstname_info.isnumeric()):
            messagebox.showwarning(title="Error",message="Warning: Firstname should consist at least of 2 characters")
            return -1
                        
        if( len(lastname_info)>0):                
            lastname_info = re.sub(r'[^a-zA-Z\d\s:]', '',lastname_info)
            lastname_info = re.sub(r'[~^0-9]', '',lastname_info)
        else:
            messagebox.showwarning(title="Error",message="Warning: Enter a valid Lastname")
            return -1
            
        if(len(lastname_info)<1 and lastname_info.isnumeric()):
            messagebox.showwarning(title="Error",message="Warning: Lastname should consist at least of 2 characters")
            return -1
        global key                        
        key=(str(uuid.uuid4().fields[-1])[:7])
        x = (key,
             firstname_info,
             lastname_info,
             gender_info,
             country_info,
             phone_info,
             date_info)
        
       y = (key, password_info)
        
        cur.execute("insert into HospitalClients values(?,?,?,?,?,?,?)",x)
        con.commit()

        cur.execute("insert into HospitalClientsCred values(?,?)",y)
        con.commit()

        f = open("logs/userID.txt", "w+")
        f.write(key)
        f.close()
             
        messagebox.showinfo(title="Loading data",message="Loaded data succesfully \n Your id = "+key)
        Appointment()

                                       
screen = ThemedTk(theme="breeze")
screen.geometry("500x550")
screen.minsize(500, 550)
screen.maxsize(500, 550)

screen.title("Hospital Clinic №2")


heading = Label(text="Hospital Clinic №2", bg="#4abca5", fg="#FFFFFF", width="500",height=2)
heading.config(font=("Helvitica", 24))
heading.pack()


cal = Calendar(screen,fieldbackground='#FFFFFF',background='#4abca5',selectbackground='#4abca5',weekendbackground='#d5edec', othermonthwebackground='#d5edec', headersbackground='white',foreground='#FFFFFF',arrowcolor='white', selectmode = 'day',
               year = 2022, month = 5,
               day = 10,date_pattern='dd-mm-yyyy')
canvas = Canvas(heading ,background='#4abca5', width = 50, height = 50,highlightthickness=0, relief='ridge')      
canvas.place(x=45, y=12)
pilImage = Image.open("img\logo.png")
img = ImageTk.PhotoImage(pilImage)

imgs =canvas.create_image(0, 0, anchor=NW,image=img) 

 
def grad_date():
    date.config(text = "Date is: " + cal.get_date())
    
date = Label(screen, text = "")
date.place(x="265",y="390")

btn_cal=ttk.Button(screen, text = "Select",command = grad_date)
btn_cal.place(x=390,y=390,width="80",height="25")

def Appointment():
    screen.destroy()
    import Appointment
    
def infoPage():
    screen.destroy()
    import Hospital_info
    
def AppointmentPage():
    screen.destroy()
    import Login


option_country =[
    'Afghanistan', 'Aland Islands', 'Albania', 'Algeria', 'American Samoa', 'Andorra', 'Angola', 'Anguilla', 'Antarctica', 'Antigua and Barbuda', 'Argentina', 'Armenia', 'Aruba', 'Australia', 'Austria', 'Azerbaijan', 'Bahamas', 'Bahrain', 'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Belize', 'Benin', 'Bermuda', 'Bhutan', 'Bolivia, Plurinational State of', 'Bonaire, Sint Eustatius and Saba', 'Bosnia and Herzegovina', 'Botswana', 'Bouvet Island', 'Brazil', 'British Indian Ocean Territory', 'Brunei Darussalam', 'Bulgaria', 'Burkina Faso', 'Burundi', 'Cambodia', 'Cameroon', 'Canada', 'Cape Verde', 'Cayman Islands', 'Central African Republic', 'Chad', 'Chile', 'China', 'Christmas Island', 'Cocos (Keeling) Islands', 'Colombia', 'Comoros', 'Congo', 'Congo, The Democratic Republic of the', 'Cook Islands', 'Costa Rica', "Côte d'Ivoire", 'Croatia', 'Cuba', 'Curaçao', 'Cyprus', 'Czech Republic', 'Denmark', 'Djibouti', 'Dominica', 'Dominican Republic', 'Ecuador', 'Egypt', 'El Salvador', 'Equatorial Guinea', 'Eritrea', 'Estonia', 'Ethiopia', 'Falkland Islands (Malvinas)', 'Faroe Islands', 'Fiji', 'Finland', 'France', 'French Guiana', 'French Polynesia', 'French Southern Territories', 'Gabon', 'Gambia', 'Georgia', 'Germany', 'Ghana', 'Gibraltar', 'Greece', 'Greenland', 'Grenada', 'Guadeloupe', 'Guam', 'Guatemala', 'Guernsey', 'Guinea', 'Guinea-Bissau', 'Guyana', 'Haiti', 'Heard Island and McDonald Islands', 'Holy See (Vatican City State)', 'Honduras', 'Hong Kong', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Iran, Islamic Republic of', 'Iraq', 'Ireland', 'Isle of Man', 'Israel', 'Italy', 'Jamaica', 'Japan', 'Jersey', 'Jordan', 'Kazakhstan', 'Kenya', 'Kiribati', "Korea, Democratic People's Republic of", 'Korea, Republic of', 'Kuwait', 'Kyrgyzstan', "Lao People's Democratic Republic", 'Latvia', 'Lebanon', 'Lesotho', 'Liberia', 'Libya', 'Liechtenstein', 'Lithuania', 'Luxembourg', 'Macao', 'Macedonia, Republic of', 'Madagascar', 'Malawi', 'Malaysia', 'Maldives', 'Mali', 'Malta', 'Marshall Islands', 'Martinique', 'Mauritania', 'Mauritius', 'Mayotte', 'Mexico', 'Micronesia, Federated States of', 'Moldova, Republic of', 'Monaco', 'Mongolia', 'Montenegro', 'Montserrat', 'Morocco', 'Mozambique', 'Myanmar', 'Namibia', 'Nauru', 'Nepal', 'Netherlands', 'New Caledonia', 'New Zealand', 'Nicaragua', 'Niger', 'Nigeria', 'Niue', 'Norfolk Island', 'Northern Mariana Islands', 'Norway', 'Oman', 'Pakistan', 'Palau', 'Palestinian Territory, Occupied', 'Panama', 'Papua New Guinea', 'Paraguay', 'Peru', 'Philippines', 'Pitcairn', 'Poland', 'Portugal', 'Puerto Rico', 'Qatar', 'Réunion', 'Romania', 'Russian Federation', 'Rwanda', 'Saint Barthélemy', 'Saint Helena, Ascension and Tristan da Cunha', 'Saint Kitts and Nevis', 'Saint Lucia', 'Saint Martin (French part)', 'Saint Pierre and Miquelon', 'Saint Vincent and the Grenadines', 'Samoa', 'San Marino', 'Sao Tome and Principe', 'Saudi Arabia', 'Senegal', 'Serbia', 'Seychelles', 'Sierra Leone', 'Singapore', 'Sint Maarten (Dutch part)', 'Slovakia', 'Slovenia', 'Solomon Islands', 'Somalia', 'South Africa', 'South Georgia and the South Sandwich Islands', 'Spain', 'Sri Lanka', 'Sudan', 'Suriname', 'South Sudan', 'Svalbard and Jan Mayen', 'Swaziland', 'Sweden', 'Switzerland', 'Syrian Arab Republic', 'Taiwan, Province of China', 'Tajikistan', 'Tanzania, United Republic of', 'Thailand', 'Timor-Leste', 'Togo', 'Tokelau', 'Tonga', 'Trinidad and Tobago', 'Tunisia', 'Turkey', 'Turkmenistan', 'Turks and Caicos Islands', 'Tuvalu', 'Uganda', 'Ukraine', 'United Arab Emirates', 'United Kingdom', 'United States', 'United States Minor Outlying Islands', 'Uruguay', 'Uzbekistan', 'Vanuatu', 'Venezuela, Bolivarian Republic of', 'Viet Nam', 'Virgin Islands, British', 'Virgin Islands, U.S.', 'Wallis and Futuna', 'Yemen', 'Zambia', 'Zimbabwe']

def comboclick(event):
    myLabel = Label(screen).pack()
    
def clear_entry(event, phone_entry):
    phone_entry.delete(0, END)
    phone_entry.unbind('<Button-1>)')


   
myCombo_country = ttk.Combobox(screen,state="readonly",value=option_country)
myCombo_country.bind("<<ComboboxSelected>>",comboclick)
myCombo_country.pack()


firstname_text = Label(text="Firstname * ", )
lastname_text = Label(text="Lastname * ", )
country_text = Label(text="Country * ", )
phone_text = Label(text="Phone * ", )
male_text = Label(text="Gender: * ", )
age_text=Label(text="Date of birth * ",)
password_text=Label(text="Password * ",)

firstname_text.place(x=20, y=110)
lastname_text.place(x=20, y=180)
country_text.place(x=20, y=320)
phone_text.place(x=20, y=250)
age_text.place(x=265,y=180)
password_text.place(x=265,y=110)

firstname = StringVar()
lastname = StringVar()
phone = StringVar()
password =StringVar()
gender = StringVar(None,0)


R1 = Radiobutton(screen,state=NORMAL,text="Male", variable=gender, value="Male")
R2 = Radiobutton(screen,state=NORMAL, text="Female", variable=gender, value="Female")

firstname_entry = ttk.Entry(textvariable=firstname, width="28")
lastname_entry = ttk.Entry(textvariable=lastname, width="28")
phone_entry = ttk.Entry(textvariable=phone, width="28")
password_entry= ttk.Entry(textvariable=password,show="*", width="28")

placeholder_text = 'Format 380XXXXXXXXX'
phone_entry.insert(0, placeholder_text)

phone_entry.bind("<Button-1>", lambda event: clear_entry(event, phone_entry))


firstname_entry.place(x=20, y=140)
lastname_entry.place(x=20, y=210)
myCombo_country.place(x=20, y=350,width="207",height="27")
phone_entry.place(x=20, y=280)
password_entry.place(x=265, y=140)
cal.place(x=265, y=210,width="207",height="167")
R1.place(x=30, y=390)
R2.place(x=120,y=390)


btn=ttk.Button(screen, text="Register", command=save_info)
btn=ttk.Button(screen,width="20", text="Register", command=save_info)
btn.place(x=180,y=445)

btn_page=Button(screen, text="Create Appointment",
                bg="#4abca5",fg="white",width="31",command=AppointmentPage)
btn_page.place(x=0, y=70)
btn_page.config(font=("Helvitica", 10, "bold"))

btn_page=Button(screen, text="Hospital Info",
                bg="#4abca5", fg="white",width="30",command=infoPage)
btn_page.place(x=250, y=70)
btn_page.config(font=("Helvitica", 10, "bold"))
screen.mainloop()

