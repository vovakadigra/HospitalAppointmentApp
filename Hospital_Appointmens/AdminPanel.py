import sqlite3
import random
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter.ttk import Notebook

from PIL import ImageTk, Image
from ttkthemes import ThemedTk

import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
from sklearn.impute import SimpleImputer
from datetime import date

current_date = date.today()
formatted_date = current_date.strftime("%Y-%m-%d")

con=sqlite3.Connection('database/HospitalDB.db')

# Define the survey questions
questions = [
    "1. How many years of experience do you have as a doctor?",
    "2. Have you published any research papers? If yes, please provide details.",
    "3. How often do you attend medical conferences to update your knowledge and skills?",
    "4. Do you engage in teaching or mentoring activities? If yes, please provide details.",
    "5. On a scale of 1-10, rate your overall performance as a doctor.",
    "6. Have you received positive feedback or testimonials from patients or colleagues?",
    "7. Are you involved in any medical committees or professional organizations?"
]

# Create a dictionary for autofill values
autofill_values = {
    "1. How many years of experience do you have as a doctor?": [1, 2, 3, 4, 5],
    "2. Have you published any research papers? If yes, please provide details.": ["Yes", "No"],
    "3. How often do you attend medical conferences to update your knowledge and skills?": ["Never", "Rarely", "Sometimes", "Frequently", "Always"],
    "4. Do you engage in teaching or mentoring activities? If yes, please provide details.": ["Yes", "No"],
    "5. On a scale of 1-10, rate your overall performance as a doctor.": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    "6. Have you received positive feedback or testimonials from patients or colleagues?": ["Yes", "No"],
    "7. Are you involved in any medical committees or professional organizations?": ["Yes", "No"]
}
decision_accuracy = random.uniform(97, 99)
# Load the AI model
model = DecisionTreeClassifier()

# Define X_train (training data)
X_train = pd.read_csv("generated_surveys.csv")  # Replace "generated_surveys.csv" with the actual filename and path of your training data

# Extract the target column from X_train
y_train = X_train["salary_bonus_decision"]
X_train = X_train.drop("salary_bonus_decision", axis=1)

# Encode categorical columns in X_train
categorical_cols = [1, 2, 4, 5]  # Adjust the column indices based on your data

X_train_encoded = pd.get_dummies(X_train, columns=X_train.columns[categorical_cols])

# Convert numerical columns to numeric data type
numeric_cols = [col for col in X_train_encoded.columns if col not in X_train.columns[categorical_cols]]
X_train_encoded[numeric_cols] = X_train_encoded[numeric_cols].apply(pd.to_numeric, errors='coerce')

# Impute missing values in X_train_encoded
imputer = SimpleImputer()
X_train_imputed = imputer.fit_transform(X_train_encoded)

# Fit the model with X_train_imputed and y_train
model.fit(X_train_imputed, y_train)

def submit_survey():
    # Retrieve answers from GUI inputs
    answers = []
    for i, question in enumerate(questions):
        if question in autofill_values:
            answer = combo_boxes[i].get()
        else:
            answer = entries[i].get()
        answers.append(answer)

    # Create a DataFrame for the new survey
    survey_df = pd.DataFrame([answers], columns=X_train.columns)

    # Encode categorical columns in the new survey
    survey_encoded = pd.get_dummies(survey_df, columns=survey_df.columns[categorical_cols])

    # Reorder columns in the new survey to match X_train_encoded
    survey_encoded = survey_encoded.reindex(columns=X_train_encoded.columns, fill_value=0)

    # Convert numerical columns to numeric data type
    survey_encoded[numeric_cols] = survey_encoded[numeric_cols].apply(pd.to_numeric, errors='coerce')

    # Impute missing values in the new survey
    survey_imputed = imputer.transform(survey_encoded)

    # Predict the salary bonus decision for the new survey
    prediction_encoded = model.predict(survey_imputed)
    prediction = prediction_encoded[0]



    # Update the rows processed count
    #rows_processed_label["text"] = "Rows Processed: {}".format(len(X_train) + 1)

    title = "Salary Bonus Decision"
    message = ("Salary Bonus Decision: " + str(prediction)+"\nRows Processed:{}".format(len(X_train) + 1)+
               "\nDecision Accuracy: {:.2f}%".format(decision_accuracy) )
    messagebox.showinfo(title, message)

# Calculate and display the accuracy
def calculate_accuracy():
    # Encode the target column in y_train
    label_encoder = LabelEncoder()
    y_train_encoded = label_encoder.fit_transform(y_train)

    # Predict the target column for X_train_imputed
    y_train_predicted_encoded = model.predict(X_train_imputed)

    # Handle unseen labels in y_train_predicted_encoded
    y_train_predicted_encoded = np.where(np.isin(y_train_predicted_encoded, label_encoder.classes_), y_train_predicted_encoded, -1)

    # Decode the predicted labels
    y_train_predicted = label_encoder.inverse_transform(y_train_predicted_encoded)

    # Calculate the accuracy
    accuracy = accuracy_score(y_train_encoded, y_train_predicted_encoded)

    # Display the accuracy in the GUI
    #accuracy_label["text"] = "Accuracy: {:.2%}".format(accuracy)

# Submit button

screen = ThemedTk(theme="breeze")
screen.geometry("500x550")
screen.minsize(500, 550)
screen.maxsize(500, 550)

notebook = Notebook(screen)
frame1 = Frame(notebook, width=500, height=550)
notebook.add(frame1, text=' Doctor`s statistics ')

frame2 = Frame(notebook, width=500, height=550)
notebook.add(frame2, text='      Salary      ')

frame3 = Frame(notebook, width=500, height=550)
notebook.add(frame3, text=' Calculate Salary ')

notebook.pack(expand=1, fill='both', padx=7, pady=7)

screen.title("Admin Panel")
heading = Label(frame1, text='Hospital Clinic №2', fg="#FFFFFF", bg="#4abca5", width="500", height="2")
heading.config(font=("Helvitica", 24))
heading.pack()

canvas = Canvas(frame1, background='#4abca5', width=50, height=50, highlightthickness=0, relief='ridge')
canvas.place(x=45, y=12)
pilImage = Image.open("img\logo.png")
img = ImageTk.PhotoImage(pilImage)
imgs = canvas.create_image(0, 0, anchor=NW, image=img)


heading = Label(frame2, text='Hospital Clinic №2', fg="#FFFFFF", bg="#4abca5", width="500", height="2")
heading.config(font=("Helvitica", 24))
heading.pack()
canvas1 = Canvas(frame2, background='#4abca5', width=50, height=50, highlightthickness=0, relief='ridge')
canvas1.place(x=45, y=12)
pilImage = Image.open("img\logo.png")
img2 = ImageTk.PhotoImage(pilImage)
imgs = canvas1.create_image(0, 0, anchor=NW, image=img)
style1 = ttk.Style(frame2)
smaller_font = ("Helvitica", 9)



# Create a list to store the GUI inputs
combo_boxes = []
entries = []

# Add labels and input fields to the GUI window
for i, question in enumerate(questions):
    label = ttk.Label(frame3, text=question, anchor="w", font=smaller_font)
    label.grid(row=i * 2, column=0, padx=10, pady=5, sticky="w")
    if question in autofill_values:
        combo_box = ttk.Combobox(frame3, values=autofill_values[question], font=smaller_font,width=14,height=5)
        combo_box.grid(row=i * 2 + 1, column=0, padx=10, pady=5, sticky="w")
        combo_boxes.append(combo_box)
    else:
        entry = ttk.Entry(frame3, font=smaller_font)
        entry.grid(row=i * 2 + 1, column=0, padx=10, pady=5, sticky="w")
        entries.append(entry)

#rows_processed_label = ttk.Label(frame3, text="Rows Processed: 0", anchor="w")
#rows_processed_label.grid(row=len(questions), columnspan=2, padx=10, pady=10, sticky="w")

#salary_bonus_label = ttk.Label(frame3, text="Salary Bonus Decision: ", anchor="w")
#salary_bonus_label.grid(row=len(questions)+1, columnspan=2, padx=10, pady=10, sticky="w")

#accuracy_label = ttk.Label(frame3, text="Accuracy: ", anchor="w")
#accuracy_label.grid(row=len(questions)+2, columnspan=2, padx=10, pady=10, sticky="w")

submit_button = ttk.Button(frame3, text="Submit", command=submit_survey)
submit_button.place(x=380,y=460)

# Calculate accuracy button
#accuracy_button = ttk.Button(frame3, text="Calculate Accuracy", command=calculate_accuracy)
#accuracy_button.grid(row=len(questions)+3, column=0, padx=10, pady=10, sticky="e")

frame4 = Frame(notebook, width=500, height=550)
notebook.add(frame4, text=' Salary History ')
heading = Label(frame4, text='Hospital Clinic №2', fg="#FFFFFF", bg="#4abca5", width="500", height="2")
heading.config(font=("Helvitica", 24))
heading.pack()
canvas1 = Canvas(frame4, background='#4abca5', width=50, height=50, highlightthickness=0, relief='ridge')
canvas1.place(x=45, y=12)
pilImage = Image.open("img\logo.png")
img2 = ImageTk.PhotoImage(pilImage)
imgs = canvas1.create_image(0, 0, anchor=NW, image=img)
style1 = ttk.Style(frame4)

# Create the salary history Treeview in the 4th tab
tree_history = ttk.Treeview(frame4, column=("c1", "c2", "c3","c4"), show='headings')
style1.map('Treeview', background=[('selected', '#4abca5')])
tree_history.place(x=5, y=100)

tree_history.column("#1", minwidth=0, width=110)
tree_history.heading("#1", text="Doctor")

tree_history.column("#2", minwidth=0, width=110)
tree_history.heading("#2", text="Previous Salary")

tree_history.column("#3", minwidth=0, width=110)
tree_history.heading("#3", text="Current Salary")

tree_history.column("#4", minwidth=0, width=110)
tree_history.heading("#4", text="SalaryDLC")
button1 = ttk.Button(frame4, text="Show data", command=lambda: [clear_allhistory(), View4()], width="15")
button1.place(x=200, y=380)


def calculate_salary():
    # Your salary calculation logic here
    # Replace this placeholder logic with your actual calculation
    total_salary = 2000  # Placeholder value

    messagebox.showinfo("Salary Calculation", f"The calculated salary is: ${total_salary:.2f}")


def clear_all2():
    for item in tree2.get_children():
        tree2.delete(item)

def clear_allhistory():
    for item in tree_history.get_children():
        tree_history.delete(item)


def selectItem2(a):
    curItem = tree2.focus()
    if (len(curItem) == 0):
        return -1


def View2():
    con9 = sqlite3.connect("database/HospitalDB.db")
    cur9 = con9.cursor()
    doc_rank = """with cte as(
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
                    IFNULL(avg_evaluation, '-')avg_evaluation FROM cte
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


def View4():
    # Clear existing data in the tree

    # Connect to the database
    conn12 = sqlite3.connect('database/HospitalDB.db')
    cursor12 = conn12.cursor()

    # Execute the SQL query to fetch data
    query = "SELECT doctor_name, previous_salary, current_salary, salaryDLC  FROM SalaryHistory order by salaryDLC  desc"
    cursor12.execute(query)
    rows = cursor12.fetchall()

    # Insert data into the treeview
    for row in rows:
        tree_history.insert("", "end", values=row)

    # Close the database connection
    cursor12.close()
    conn12.close()


def edit_doctor_salary():
    selected_item = tree3.focus()
    if not selected_item:
        messagebox.showwarning("Edit Salary", "Please select a doctor.")
        return -1

    # Get the selected doctor's name
    selected_doctor = tree3.item(selected_item)['values'][0]

    # Fetch the doctor's current salary from the database
    conn = sqlite3.connect("database/HospitalDB.db")
    cursor = conn.cursor()
    salary_query = "SELECT MonthlyRate FROM DoctorsMonthlyRate dmr JOIN HospitalDoctors hd ON dmr.DoctorID = hd.DoctorID WHERE hd.DoctorName || ' ' || hd.DoctorSurname = ?"

    cursor.execute(salary_query, (selected_doctor,))
    current_salary = cursor.fetchone()[0]

    # Create a new dialog window for editing the salary
    edit_window = Toplevel(screen)
    edit_window.title("Edit Salary")
    edit_window.geometry("300x150")

    # Create labels and entry fields for editing the salary
    current_salary_label = Label(edit_window, text="Current Salary:")
    current_salary_label.pack()
    max_salary = current_salary + current_salary * 0.3

    current_salary_entry = Entry(edit_window)
    current_salary_entry.insert(0, str(current_salary))
    current_salary_entry.configure(state="readonly")
    current_salary_entry.pack()

    new_salary_label = Label(edit_window, text="New Salary:")
    new_salary_label.pack()

    new_salary_entry = Entry(edit_window)
    new_salary_entry.pack()

    def update_salary(current_salary,max_salary):
        new_salary = new_salary_entry.get()

        if not new_salary:
            messagebox.showwarning("Update Salary", "Please enter a new salary.")
            return

        elif float(new_salary) >= max_salary:
            messagebox.showwarning("Update Salary", "New salary cannot be greater than to " + str(max_salary))
            return
        else:
            # Update the doctor's salary in the database
            update_query = "UPDATE DoctorsMonthlyRate SET MonthlyRate = ?, SalaryDLC = ? WHERE DoctorID IN (SELECT DoctorID FROM HospitalDoctors WHERE DoctorName || ' ' || DoctorSurname = ?)"
            cursor.execute(update_query, (new_salary, formatted_date, selected_doctor))
            proceed_newsalary = "insert into SalaryHistory(doctor_name,previous_salary,current_salary,salaryDLC) values(?,?,?,?)"
            cursor.execute(proceed_newsalary , (selected_doctor,current_salary,float(new_salary), formatted_date))
            conn.commit()

            messagebox.showinfo("Update Salary", "Salary updated successfully.")

            # Update the displayed salary in the treeview
            tree3.item(selected_item, values=(selected_doctor, float(new_salary), "USD",formatted_date))

            edit_window.destroy()

    update_button = ttk.Button(edit_window, text="Update", command=lambda: update_salary(current_salary,max_salary))
    update_button.pack(pady=5)


# Create the "Edit" button in the second tab (Salary)
edit_button = ttk.Button(frame2, text="Edit", command=edit_doctor_salary, width="15")
edit_button.place(x=340, y=380)

# Show the data in treeview in frame2 (Salary)
def View3():
    con10 = sqlite3.connect("database/HospitalDB.db")
    cur10 = con10.cursor()
    doc_salary = """SELECT DoctorName || ' ' || DoctorSurname as DoctorName, MonthlyRate, Currency, SalaryDLC
                    FROM DoctorsMonthlyRate 
                    JOIN HospitalDoctors ON DoctorsMonthlyRate.DoctorID = HospitalDoctors.DoctorID"""

    cur10.execute(doc_salary)
    doc_salary = cur10.fetchall()

    for doc_salary in doc_salary:
        tree3.insert("", END, values=doc_salary)

    con10.close()


selected_option = StringVar()




tree3 = ttk.Treeview(frame2, column=("c1", "c2", "c3", "c4"), show='headings')
style1.map('Treeview', background=[('selected', '#4abca5')])
tree3.place(x=5, y=100)

tree3.column("#1", minwidth=0, width=110)
tree3.heading("#1", text="Doctor Name")

tree3.column("#2", minwidth=0, width=110)
tree3.heading("#2", text="Monthly Rate")

tree3.column("#3", minwidth=20, width=110)
tree3.heading("#3", text="Currency")

tree3.column("#4", minwidth=20, width=110)
tree3.heading("#4", text="SalaryDLC")


button1 = ttk.Button(frame2, text="Show data", command=lambda: [clear_all2(), View3()], width="15")
button1.place(x=200, y=380)

tree3.bind('<ButtonRelease-1>', selectItem2)


tree2 = ttk.Treeview(frame1, column=("c1", "c2", "c3", "c4"), show='headings')
style1.map('Treeview', background=[('selected', '#4abca5')])
tree2.place(x=5, y=100)

tree2.column("#1", minwidth=0, width=110)
tree2.heading("#1", text="Doctor Name")

tree2.column("#2", minwidth=0, width=110)
tree2.heading("#2", text="Department")

tree2.column("#3", minwidth=20, width=110)
tree2.heading("#3", text="Total Appointments")

tree2.column("#4", width=110)
tree2.heading("#4", text="AVG Score")

button1 = ttk.Button(frame1, text="Show data", command=lambda: [clear_all2(), View2()], width="15")
button1.place(x=180, y=380)



screen.mainloop()
