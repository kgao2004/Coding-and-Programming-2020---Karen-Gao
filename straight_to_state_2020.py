"""
Community Service Hours Program
FBLA Straight to State 2020
Coding and Programming
Karen Gao
"""

# import all modules
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter.ttk import Style
import pymongo


"""Define only numbers function
- check if the inputted character is a number
- returns True or False
"""
def only_numbers(char):
    return char.isdigit()


"""Define only letters function
- check if the inputted character is a letter
- returns True or False
"""
def only_letters(str):
    return str.isalpha()


"""Check that the student number doesn't already exist (when registering new students)
- Search for student number in the database
- return True if it is not found
- return False if it is found 
"""
def check_number(number_input):
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["community_service_awards_program"]
    mycol = mydb["students"]

    # search the students in the database
    for student in mycol.find():
        # if the inputted number already exists in the database, return False
        if (student['number'] == number_input):
            return False
    return True


"""Function for cancel button
- destroys the window
"""
def cancel(window):
    window.destroy()


"""Insert student info in database into tree
- tree is the widget that displays the student information on the main window
"""
def load_database(tree):
    # load database "students"
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["community_service_awards_program"]
    mycol = mydb["students"]

    # clear the treeview widget (delete all existing entries)
    for child in tree.get_children():
        tree.delete(child)

    # insert the updated student information from the database into the tree
    for student in mycol.find():
        tree.insert('', 'end', text="{}, {}".format(student['last_name'].title(), student['first_name'].title()),
                    values=(student['number'], student['grade'], student['hours']))


"""Insert a student into the database
- load database
- insert student's first and last name all lowercase, student number, grade, and hours
"""
def insert_record(first_name, last_name, number, grade, hours):
    # load database "students"
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["community_service_awards_program"]
    mycol = mydb["students"]

    """insert the inputted student's information (first and last name are all lowercase in order to make 
    searching case-insensitive"""
    mycol.insert_one({'first_name': first_name.lower(), 'last_name': last_name.lower(), 'number': number,
                      'grade': grade, 'hours': hours})


"""Edit a student's info in the database
- load database
- student number can't be changed (or else the student won't be able to be found in the database if all of his/her info
is changed
 - everything else can be changed 
"""
def update_record(first_name, last_name, number, grade, hours):
    # load database
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["community_service_awards_program"]
    mycol = mydb["students"]

    # search for the student number and then update the information associated with that number according to the input
    mycol.update_one({'number': number}, {"$set": {'first_name': first_name.lower(), 'last_name': last_name.lower(),
                                                   'grade': grade, 'hours': hours}})


"""Delete a student from the database
- load database
- search for the student number and delete the record associated with it
"""
def delete_record(number):
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["community_service_awards_program"]
    mycol = mydb["students"]

    # search for the student number of the selected student in the database and delete the record associated it
    mycol.delete_one({'number': number})


"""Allows user to search for a student
Options:
- search by full name (first last)
- search by last name
- search by first name
"""
def search_student(name_entry, tree):
    # make all the letters lowercase in the inputted name and set equal to full_name
    full_name = name_entry.get().lower()
    # split full_name into individual names (doesn't do anything if only first or last name was inputted)
    names = full_name.split()
    # if more than two names were inputted, print error message
    if (len(names) > 2):
        messagebox.showinfo("Error Message", "Invalid name")
        return

    # load database
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["community_service_awards_program"]
    mycol = mydb["students"]

    # if nothing was inputted, display all students
    if (len(names) == 0):
        results = mycol.find()

    # if one name was inputted, search if it matches a first name or last name in the database
    elif (len(names) == 1):
        results = mycol.find({"$or": [{'first_name': full_name}, {'last_name': full_name}]})

    # if first and last name were inputted, set variable for each name and search for both in the database
    else:
        first_name = full_name[0]
        last_name = full_name[1]
        results = mycol.find({"$and": [{'first_name': first_name}, {'last_name': last_name}]})

    # if at least one result was found, display student/students on the treeview widget
    if (results.count() > 0):
        # clear all existing entries
        for child in tree.get_children():
            tree.delete(child)

        # display only the results found from the search
        for student in results:
            tree.insert('', 'end', text="{}, {}".format(student['last_name'].title(), student['first_name'].title()),
                        values=(student['number'], student['grade'], student['hours']))
    # if student was not found in the database
    else:
        messagebox.showinfo("Error Message", "Student not found")


"""Add a new student into the database
- create a new window
- allows you to add a new student:
    first name
    last name
    student number
    grade
    hours
- register and cancel button
"""
def register_new_student(tree):
    # open new window
    register_window = Toplevel()
    # set title of window to "Register New Student"
    register_window.title("Register New Student")

    # create a top frame
    top_frame = Frame(register_window)
    top_frame.pack(side=TOP, fill=BOTH)

    # create a center frame
    center_frame = Frame(register_window)
    center_frame.pack(side=TOP, fill=BOTH)

    # allow columns to fill the space
    Grid.columnconfigure(center_frame, 0, weight=1)
    Grid.columnconfigure(center_frame, 1, weight=1)

    # create a label: "REGISTER NEW STUDENT"
    edit_info_title = Label(top_frame, text="REGISTER NEW STUDENT", font='verdana 18 bold', bg='yellow')
    edit_info_title.pack(padx=30, pady=30)

    # label for first name
    first_name_label = Label(center_frame, text="First Name", font='verdana 18 bold')
    first_name_label.grid(row=0, column=0, sticky=E, padx=30, pady=30)

    # label for last name
    last_name_label = Label(center_frame, text="Last Name", font='verdana 18 bold')
    last_name_label.grid(row=1, column=0, sticky=E, padx=30, pady=30)

    # label for student number
    number_label = Label(center_frame, text="Student Number", font='verdana 18 bold')
    number_label.grid(row=2, column=0, sticky=E, padx=30, pady=30)

    # label for grade
    grade_label = Label(center_frame, text="Grade", font='verdana 18 bold')
    grade_label.grid(row=3, column=0, sticky=E, padx=30, pady=30)

    # label for hours
    hours_label = Label(center_frame, text="Hours", font='verdana 18 bold')
    hours_label.grid(row=4, column=0, sticky=E, padx=30, pady=30)

    # make sure that the user can only input letters into first name entry
    first_name_validation = center_frame.register(only_letters)
    """create entry box for inputting first name
    - validate: any keystroke in the entry triggers the validation
    - %S: pass the inserted/deleted character into the function only_letters
    """
    first_name_entry = Entry(center_frame, validate="key", validatecommand=(first_name_validation, '%S'),
                             font='verdana 18')
    first_name_entry.grid(row=0, column=1, sticky=W, padx=30, pady=30)

    # make sure that the user can only input letters into last name entry
    last_name_validation = center_frame.register(only_letters)
    last_name_entry = Entry(center_frame, validate="key", validatecommand=(last_name_validation, '%S'),
                            font='verdana 18')
    last_name_entry.grid(row=1, column=1, sticky=W, padx=30, pady=30)

    # make sure that the user can only input numbers into the student number entry and the number is 10 characters
    number_validation = center_frame.register(only_numbers)
    number_entry = Entry(center_frame, validate="key", validatecommand=(number_validation, '%S'), font='verdana 18')
    number_entry.grid(row=2, column=1, sticky=W, padx=30, pady=30)

    # call class StringVar which allow you to easily track the variable "grades", center_frame is its master widget
    grades = StringVar(center_frame)
    # set the initial value that shows up on the option menu to an empty string
    grades.set("")
    # create option menu widget for selecting the grade level
    grade_entry = OptionMenu(center_frame, grades, "9", "10", "11", "12")
    grade_entry.grid(row=3, column=1, sticky=W, padx=30, pady=30)

    # make sure that the user can only input numbers into the hours entry
    hours_validation = center_frame.register(only_numbers)
    hours_entry = Entry(center_frame, validate="key", validatecommand=(hours_validation, '%S'), font='verdana 18')
    hours_entry.grid(row=4, column=1, sticky=W, padx=30, pady=30)

    """create register button
    - input student info, the register window, and tree into the function confirm_input when the button is clicked
    """
    register_button = Button(center_frame, text="Register", command=lambda: confirm_input(
        first_name_entry, last_name_entry, number_entry, grades, hours_entry, register_window, tree),
                             font='verdana 18 bold')
    register_button.grid(row=5, column=0, sticky=E, padx=30, pady=30)

    # cancel button which exits the window and doesn't apply the input to the database
    cancel_button = Button(center_frame, text="Cancel", command=lambda: cancel(register_window), font='verdana 18 bold')
    cancel_button.grid(row=5, column=1, sticky=W, padx=30, pady=30)

    # keep window open and running until destroyed
    register_window.mainloop()


"""Validate the user input in register window
- for each entry, check if it meets certain requirements
- if it doesn't create a messagebox that explains the error
"""
def confirm_input(first_name_entry, last_name_entry, number_entry, grades, hours_entry, register_window, tree):
    # if nothing was entered in the first name entry
    if (len(first_name_entry.get()) == 0):
        register_window.wm_attributes("-topmost", 0)
        messagebox.showinfo("Error Message", "Please type in the first name")
        register_window.wm_attributes("-topmost", 1)
    # if nothing was entered in the last name entry
    elif (len(last_name_entry.get()) == 0):
        register_window.wm_attributes("-topmost", 0)
        messagebox.showinfo("Error Message", "Please type in the last name")
        register_window.wm_attributes("-topmost", 1)
    # if nothing was entered in the student number entry
    elif (len(number_entry.get()) == 0):
        register_window.wm_attributes("-topmost", 0)
        messagebox.showinfo("Error Message", "Please type in the student number")
        register_window.wm_attributes("-topmost", 1)
    # if student number is not 10 characters long
    elif (len(number_entry.get()) != 10):
        register_window.wm_attributes("-topmost", 0)
        messagebox.showinfo("Error Message", "Student number must contain 10 digits.")
        register_window.wm_attributes("-topmost", 1)
    # if nothing was entered in the grades option menu
    elif (len(grades.get()) == 0):
        register_window.wm_attributes("-topmost", 0)
        messagebox.showinfo("Error Message", "Please select a grade")
        register_window.wm_attributes("-topmost", 1)
    # if nothing was entered in the hours entry
    elif (len(hours_entry.get()) == 0):
        register_window.wm_attributes("-topmost", 0)
        messagebox.showinfo("Error Message", "Please type in the number of hours")
        register_window.wm_attributes("-topmost", 1)
    # check if the student number already exists in the database (it shouldn't)
    elif (not check_number(number_entry.get())):
        register_window.wm_attributes("-topmost", 0)
        messagebox.showinfo("Error Message", "Student number is already registered")
        register_window.wm_attributes("-topmost", 1)
    # if all the input meets the requirements, then add the student info to the database and destroy register window
    else:
        insert_record(first_name_entry.get(), last_name_entry.get(), number_entry.get(), grades.get(),
                      hours_entry.get())
        register_window.destroy()
        load_database(tree)


"""Edit student information window
- creates a window similar to the register window, but already displays the names in the entry
- allows you to edit existing student information
"""
def edit_info(tree):
    # create new window
    edit_window = Toplevel()
    # set title of window to "Edit Student Information"
    edit_window.title("Edit Student Information")

    # if no student is selected, show error message
    if (len(tree.selection()) == 0):
        messagebox.showinfo("Error Message", "No student selected")
        return
    # if a student is selected, set some variables equal to the name, number, etc. of that student
    else:
        # set index to first student selected (treeview allows multiple selections, but it is disabled on this program)
        index = tree.selection()[0]

        # set full_name to the name in the database (it is formatted like last name, first name)
        full_name = tree.item(index, 'text')
        # split into first and last name
        names = full_name.split()
        first_name = names[1]
        old_last_name = names[0]
        # delete comma in last name
        last_name = old_last_name.replace(",", "")

        # extract remaining values
        values = tree.item(index, 'values')
        # set the student number equal to "number"
        number = values[0]
        # set the grade equal to "grade"
        grade = values[1]
        # set the hours equal to "hours"
        hours = values[2]

    # create a top frame
    top_frame = Frame(edit_window)
    top_frame.pack(side=TOP, fill=BOTH)

    # create a center frame
    center_frame = Frame(edit_window)
    center_frame.pack(side=TOP, fill=BOTH)

    # allow columns to fill the space
    Grid.columnconfigure(center_frame, 0, weight=1)
    Grid.columnconfigure(center_frame, 1, weight=1)

    # create a label: "EDIT STUDENT INFORMATION"
    edit_info_title = Label(top_frame, text="EDIT STUDENT INFORMATION", font='verdana 18 bold', bg='yellow')
    edit_info_title.pack(padx=30, pady=30)

    # label for first name
    first_name_label = Label(center_frame, text="First Name", font='verdana 18 bold')
    first_name_label.grid(row=0, column=0, sticky=E, padx=30, pady=30)

    # label for last name
    last_name_label = Label(center_frame, text="Last Name", font='verdana 18 bold')
    last_name_label.grid(row=1, column=0, sticky=E, padx=30, pady=30)

    # label for student number
    number_label = Label(center_frame, text="Student Number", font='verdana 18 bold')
    number_label.grid(row=2, column=0, sticky=E, padx=30, pady=30)

    # label for grade
    grade_label = Label(center_frame, text="Grade", font='verdana 18 bold')
    grade_label.grid(row=3, column=0, sticky=E, padx=30, pady=30)

    # label for hours
    hours_label = Label(center_frame, text="Hours", font='verdana 18 bold')
    hours_label.grid(row=4, column=0, sticky=E, padx=30, pady=30)

    # make sure that the user can only input letters into first name entry
    first_name_validation = center_frame.register(only_letters)
    first_name_entry = Entry(center_frame, validate="key", validatecommand=(first_name_validation, '%S'),
                             font='verdana 18')
    first_name_entry.grid(row=0, column=1, sticky=W, padx=30, pady=30)
    first_name_entry.insert(INSERT, first_name)

    # make sure that the user can only input letters into last name entry
    last_name_validation = center_frame.register(only_letters)
    last_name_entry = Entry(center_frame, validate="key", validatecommand=(last_name_validation, '%S'),
                            font='verdana 18')
    last_name_entry.grid(row=1, column=1, sticky=W, padx=30, pady=30)
    last_name_entry.insert(INSERT, last_name)

    # make sure that the user can only input numbers into the student number entry and the number is 10 characters
    number_validation = center_frame.register(only_numbers)
    number_entry = Entry(center_frame, validate="key", validatecommand=(number_validation, '%S'), font='verdana 18')
    number_entry.grid(row=2, column=1, sticky=W, padx=30, pady=30)
    number_entry.insert(INSERT, number)
    number_entry['state'] = 'disabled'

    # call class StringVar which allow you to easily track the variable "grades", center_frame is its master widget
    grades = StringVar(center_frame)
    # set the initial value that shows up on the option menu to an empty string
    grades.set(grade)
    # create option menu widget for selecting the grade level
    grade_entry = OptionMenu(center_frame, grades, "9", "10", "11", "12")
    grade_entry.grid(row=3, column=1, sticky=W, padx=30, pady=30)

    # make sure that the user can only input numbers into the hours entry
    hours_validation = center_frame.register(only_numbers)
    hours_entry = Entry(center_frame, validate="key", validatecommand=(hours_validation, '%S'), font='verdana 18')
    hours_entry.grid(row=4, column=1, sticky=W, padx=30, pady=30)
    hours_entry.insert(INSERT, hours)

    """create change button
    - input student info, the edit window, and tree into the function edit_record when the button is clicked
    """
    change_button = Button(center_frame, text="Change", command=lambda: edit_record(
        first_name_entry, last_name_entry, number_entry, grades, hours_entry, edit_window, tree),
                           font='verdana 18 bold')
    change_button.grid(row=5, column=0, sticky=E, padx=30, pady=30)

    # cancel button which exits the window and doesn't apply the input to the database
    cancel_button = Button(center_frame, text="Cancel", command=lambda: cancel(edit_window), font='verdana 18 bold')
    cancel_button.grid(row=5, column=1, sticky=W, padx=30, pady=30)

    # keep window open and running until destroyed
    edit_window.mainloop()


"""Validating input in the edit student information window
- creating a window that allows you to edit an existing student's information
"""
def edit_record(first_name_entry, last_name_entry, number_entry, grades, hours_entry, register_window, tree):
    # if nothing was entered in the first name entry
    if (len(first_name_entry.get()) == 0):
        register_window.wm_attributes("-topmost", 0)
        messagebox.showinfo("Error Message", "Please type in the first name")
        register_window.wm_attributes("-topmost", 1)
    # if nothing was entered in the last name entry
    elif (len(last_name_entry.get()) == 0):
        register_window.wm_attributes("-topmost", 0)
        messagebox.showinfo("Error Message", "Please type in the last name")
        register_window.wm_attributes("-topmost", 1)
    # if nothing was entered in the number entry
    elif (len(number_entry.get()) == 0):
        register_window.wm_attributes("-topmost", 0)
        messagebox.showinfo("Error Message", "Please type in the student number")
        register_window.wm_attributes("-topmost", 1)
    # if student number is not 10 characters long
    elif (len(number_entry.get()) != 10):
        register_window.wm_attributes("-topmost", 0)
        messagebox.showinfo("Error Message", "Student number must contain 10 digits.")
        register_window.wm_attributes("-topmost", 1)
    # if nothing was entered in the grades option menu
    elif (len(grades.get()) == 0):
        register_window.wm_attributes("-topmost", 0)
        messagebox.showinfo("Error Message", "Please select a grade")
        register_window.wm_attributes("-topmost", 1)
    # if nothing was entered in the hours entry
    elif (len(hours_entry.get()) == 0):
        register_window.wm_attributes("-topmost", 0)
        messagebox.showinfo("Error Message", "Please type in the number of hours")
        register_window.wm_attributes("-topmost", 1)
    # if input meets all requirements, then update student info, destroy the window, and display the new info on tree
    else:
        update_record(first_name_entry.get(), last_name_entry.get(), number_entry.get(), grades.get(),
                      hours_entry.get())
        register_window.destroy()
        load_database(tree)


"""Delete an existing student from the database
- allows you to select a student and delete them from the database when the delete button is clicked
"""
def delete_student(tree):
    # if no student is selected, show error message
    if (len(tree.selection()) == 0):
        messagebox.showinfo("Error Message", "No student selected")
        return
    # check to confirm deletion with a messagebox
    else:
        msg_box = messagebox.askquestion('Message', 'Are you sure you want to delete this student',
                                         icon='warning')
        if (not msg_box == 'yes'):
            return

        # set the first selected student equal to index
        index = tree.selection()[0]
        # access values of the student
        values = tree.item(index, 'values')
        # retrieve the student number
        number = values[0]

        # function that finds the student with that number and deletes it from the database
        delete_record(number)
        # refreshes the treeview widget with the new information
        load_database(tree)


def treeview_sort_name_column(tree, col, reverse):
    students_list = [(tree.item(student)['text'], student) for student in tree.get_children()]
    students_list.sort(key=lambda t: t[0], reverse=reverse)

    for index, (full_name, student) in enumerate(students_list):
        tree.move(student, '', index)

    tree.heading(col, command=lambda: treeview_sort_name_column(tree, col, not reverse))


def treeview_sort_number_column(tree, col, reverse, value):
    students_list = [(tree.item(student)['values'][value], student) for student in tree.get_children()]
    students_list.sort(key=lambda t: t[0], reverse=reverse)

    for index, (full_name, student) in enumerate(students_list):
        tree.move(student, '', index)

    tree.heading(col, command=lambda: treeview_sort_number_column(tree, col, not reverse, value))


"""Main window
- can search for student names
- displays students registered in the database on a treeview widget
- can delete students
- can edit students
- can register students
"""
def main():
    # instantiate tkinter object root
    root = Tk()
    # set title of window to "Community Service Hours Program"
    root.title("Community Service Hours Program")
    # maximize window on the screen
    root.wm_state('zoomed')

    # create top frame
    top_frame = Frame(root)
    top_frame.pack(side=TOP, fill=BOTH)

    # create a top frame inside the first top frame
    top_top_frame = Frame(top_frame)
    top_top_frame.pack(side=TOP, fill=BOTH)

    # create a bottom frame inside the first top frame
    top_bottom_frame = Frame(top_frame)
    top_bottom_frame.pack(side=BOTTOM, fill=BOTH)

    # allow columns and the row in top_bottom frame to expand/fill the space
    Grid.columnconfigure(top_bottom_frame, 0, weight=1)
    Grid.columnconfigure(top_bottom_frame, 1, weight=1)
    Grid.rowconfigure(top_bottom_frame, 0, weight=1)

    # create a center frame
    center_frame = Frame(root)
    center_frame.pack(fill=BOTH, expand=TRUE)

    # create a bottom frame
    bottom_frame = Frame(root)
    bottom_frame.pack(side=BOTTOM, fill=BOTH)

    # create title label: "COMMUNITY SERVICE HOURS PROGRAM"
    title_label = Label(top_top_frame, text="COMMUNITY SERVICE HOURS PROGRAM", font='verdana 18 bold', bg='yellow')
    title_label.pack()

    # create student name entry where you can search for student name
    search_name_entry = Entry(top_bottom_frame, font='verdana 14')
    search_name_entry.grid(row=0, column=0, sticky=E, padx=30, pady=30)

    # instantiate style object to edit style of the treeview widget in the center frame
    style = Style(center_frame)
    # set row height to 50 **the appearance of the rows in treeview is dependent on the device
    style.configure('Treeview', rowheight=50)
    # disable multi-selection in treeview (so only one item can be selected at a time)
    tree = ttk.Treeview(center_frame, selectmode="browse")

    # create search button
    search_button = Button(top_bottom_frame, text="Search for Student Name",
                           command=lambda: search_student(search_name_entry, tree), font='verdana 14 bold')
    search_button.grid(row=0, column=1, sticky=W, padx=30, pady=30)

    # create the column headers of the treeview widget
    tree["columns"] = ("one", "two", "three")
    tree.column("#0")
    tree.column("one")
    tree.column("two")
    tree.column("three")

    # naming the column headers
    tree.heading("#0", command=lambda: treeview_sort_name_column(tree, "#0", False), text="Student Name", anchor=tk.W)
    tree.heading("one", command=lambda: treeview_sort_number_column(tree, "one", False, 0), text="Student Number", anchor=tk.W)
    tree.heading("two", command=lambda: treeview_sort_number_column(tree, "two", False, 1), text="Grade", anchor=tk.W)
    tree.heading("three", command=lambda: treeview_sort_number_column(tree, "three", False, 2), text="Hours", anchor=tk.W)

    # load the database info onto tree
    load_database(tree)

    # display tree on the window
    tree.pack(fill=BOTH, expand=TRUE, padx=30, pady=30)

    # creating a scrollbar on the right side of tree
    scrollbar = Scrollbar(tree)
    scrollbar.pack(side=RIGHT, fill=Y)
    scrollbar.configure(command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)

    # create edit button
    edit_button = Button(bottom_frame, text="Edit Student Information",
                         command=lambda: edit_info(tree), font='verdana 14 bold')
    edit_button.pack(side=TOP, padx=30, pady=30)

    # create delete button
    delete_button = Button(bottom_frame, text="Delete Student",
                           command=lambda: delete_student(tree), font='verdana 14 bold')
    delete_button.pack(side=TOP, padx=30, pady=30)

    # create register button
    register_button = Button(bottom_frame, text="Register New Student",
                             command=lambda: register_new_student(tree), font='verdana 14 bold')
    register_button.pack(side=TOP, padx=30, pady=30)

    # keeps root window running until destroyed
    root.mainloop()

# run main() method
if (__name__ == "__main__"):
    main()
