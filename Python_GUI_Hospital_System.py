from tkinter import *
import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry
import os
from PIL import Image, ImageTk

# Written by Emin Ayyıldız

doctors = {
    "Acıbadem": {
        "Cardiology": ["Dr. Ali", "Dr. Ayşe"],
        "Neurology": ["Dr. Mehmet", "Dr. Zeynep"],
        "Eye Diseases": ["Dr. Fatma", "Dr. İbrahim"]
    },
    "Medical Park": {
        "Cardiology": ["Dr. Esra", "Dr. Ferhat"],
        "Neurology": ["Dr. Canan", "Dr. Halil"],
        "Eye Diseases": ["Dr. Emre", "Dr. Gökhan"]
    },
    "Ankara Hospital": {
        "Cardiology": ["Dr. Merve", "Dr. Mustafa"],
        "Neurology": ["Dr. Nihal", "Dr. Özgür"],
        "Eye Diseases": ["Dr. Pınar", "Dr. Rüstem"]
    }
}

root = Tk()
root.title("***Hospital Appointment System*** DESIGNED BY EMIN AYYILDIZ")
root.geometry("900x700+0+0")

welcome_message = Label(root, text="Welcome to the hospital appointment system! We wish you healthy days", font=("times new roman", 20,"bold"))
welcome_message.pack(side=TOP, pady=15)
welcome_message.configure(background="gray")


image = Image.open("hospital.jpg")
new_image = image.resize((200, 180))
tk_image = ImageTk.PhotoImage(new_image)
image_label = Label(root, image=tk_image)
image_label.pack()

department_label = Label(root, text="Department :")
department_label.place(x=50, y=50)

department_options = ["Cardiology", "Neurology", "Eye Diseases"]
department_var = StringVar(root)
department_var.set("")

department_dropdown = OptionMenu(root, department_var, *department_options)
department_dropdown.place(x=200, y=50)

hospital_label = Label(root, text="Hospital :")
hospital_label.place(x=50, y=100)

hospital_options = ["Acıbadem", "Medical Park", "Ankara Hospital"]
hospital_var = StringVar(root)
hospital_var.set("")

hospital_dropdown = OptionMenu(root, hospital_var, *hospital_options)
hospital_dropdown.place(x=200, y=100)

doctor_label = Label(root, text="Doctor :")
doctor_label.place(x=50, y=150)

doctor_var = StringVar(root)
doctor_dropdown = OptionMenu(root, doctor_var, "")
doctor_dropdown.place(x=200, y=150)

name_label = Label(root, text="Name :")
name_label.place(x=50, y=200)

surname_label = Label(root, text="Surname :")
surname_label.place(x=50, y=250)

name_entry = Entry(root)
name_entry.place(x=120, y=200)

surname_entry = Entry(root)
surname_entry.place(x=120, y=250)

def update_doctor_options(*args):
    selected_hospital = hospital_var.get()
    selected_department = department_var.get()
    if selected_hospital and selected_department:
        doctor_dropdown['menu'].delete(0, 'end')
        if selected_hospital in doctors and selected_department in doctors[selected_hospital]:
            for doctor in doctors[selected_hospital][selected_department]:
                doctor_dropdown['menu'].add_command(label=doctor, command=lambda value=doctor: doctor_var.set(value))
        else:
            doctor_var.set("")
            doctor_dropdown['menu'].add_command(label="", command=lambda: None)
    else:
        doctor_var.set("")
        doctor_dropdown['menu'].delete(0, 'end')
        doctor_dropdown['menu'].add_command(label="", command=lambda: None)

hospital_var.trace("w", update_doctor_options)
department_var.trace("w", update_doctor_options)

update_doctor_options()


date_label = Label(root, text="Date")
date_label.pack()

date_picker = DateEntry(root, width=20, background='orange', foreground='white', borderwidth=5,font=15)
date_picker.pack()

time_label = Label(root, text="Time")
time_label.pack()

time_options = ["8:00", "8:30", "9:00", "9:30", "10:00", "10:30", "11:00", "11:30", "12:00", "12:30", "13:00", "13:30", "14:00", "14:30", "15:00", "15:30", "16:00"]
time_var = StringVar(root)
time_var.set(time_options[0])

time_picker = OptionMenu(root, time_var, *time_options)
time_picker.pack()


if os.path.exists("randevular.txt"):
    list_label = Label(root, text="Appointments:")
    list_label.pack()


    listbox = Listbox(root, width=70)
    listbox.pack()
    listbox.configure(background="gray",font=("times new roman",15,"bold"))
    f = open("randevular.txt", "r")
    lines = f.readlines()
    for line in lines:
        listbox.insert(END, line.strip())
    f.close()
def create_appointment():
    selected_hospital = hospital_var.get()
    selected_department = department_var.get()
    selected_doctor = doctor_var.get()
    appointment_time = time_var.get()
    name = name_entry.get()
    surname = surname_entry.get()
    dateee = date_picker.get()

    if name and surname and selected_hospital and selected_department and selected_doctor and appointment_time and dateee:
        with open("randevular.txt", "a") as f:
            new_appointment = f"{name} {surname} - {selected_hospital} - {selected_department} - {selected_doctor} - {dateee} - {appointment_time}"
            f.write(new_appointment + "\n")
        listbox.insert(END, new_appointment)
        messagebox.showinfo("Successfully","Your appointment has been successfully created")
        hospital_var.set('...')
        department_var.set('...')
        doctor_var.set('...')
        time_var.set('...')
        name_entry.delete(0,tk.END)
        surname_entry.delete(0, tk.END)


    else:
        messagebox.showerror("Error", "Please fill all fields!", icon = "error")

create_button = Button(root, text="CREATE AN APPOINTMENT", command=create_appointment,width=17, height=3,)
create_button.pack()
def delete_appointment():
    selected_appointment = listbox.curselection()
    if not selected_appointment:
        messagebox.showerror("Error", "Please select an appointment to delete",icon= "error")
    else:
        selected_appointment = selected_appointment[0]
        listbox.delete(selected_appointment)
        f = open("randevular.txt", "r")
        lines = f.readlines()
        f.close()
        f = open("randevular.txt", "w")
        for i, line in enumerate(lines):
            if i != selected_appointment:
                f.write(line)
        f.close()
        messagebox.showinfo("Successfully", "Appointment successfully deleted")


delete_button = Button(root, text="DELETE", command=delete_appointment,width=15, height=3)
delete_button.pack()

root.mainloop()