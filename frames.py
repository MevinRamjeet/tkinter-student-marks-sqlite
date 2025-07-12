import sqlite3
import tkinter as tk
from tkinter import IntVar, StringVar, ttk, messagebox

import tkinter.font as tkFont

from matplotlib import pyplot as plt


conn = sqlite3.connect('studentsmarks.db')
c = conn.cursor()

c.execute('''
CREATE TABLE IF NOT EXISTS markstable (
    student_id TEXT PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    gender TEXT CHECK(gender IN ('male', 'female')),
    module_code TEXT NOT NULL,
    coursework1 INTEGER DEFAULT 0 CHECK(coursework1 BETWEEN 0 AND 100),
    coursework2 INTEGER DEFAULT 0 CHECK(coursework2 BETWEEN 0 AND 100),
    coursework3 INTEGER DEFAULT 0 CHECK(coursework3 BETWEEN 0 AND 100),
    total_marks INTEGER DEFAULT 0,
    entry_date TEXT NOT NULL
)
''')
conn.commit()


class HomeFrame(ttk.Labelframe):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.configure(text="Current Stats", padding=30)

        tk.Label(self, text='No. of Students:').grid(row=0, column=0, padx=10, pady=5)
        tk.Label(self, text='No. of Modules:').grid(row=1, column=0, padx=10, pady=5)

        students_count = StringVar(self, value=0)
        modules_count = StringVar(self, value=0)

        students_count_label = tk.Label(self, textvariable=students_count)
        students_count_label.grid(row=0, column=1, padx=10, pady=5)

        modules_count_label = tk.Label(self, textvariable=modules_count)
        modules_count_label.grid(row=1, column=1, padx=10, pady=5)
        

        def get_students():
            c.execute('SELECT COUNT(*) FROM markstable')
            st_count = c.fetchone()[0]
            students_count.set(st_count)
            students_count_label.after(2000, get_students)

        def get_modules():
            c.execute('SELECT COUNT(DISTINCT module_code) FROM markstable')
            unique_modules = c.fetchone()[0]
            modules_count.set(unique_modules)
            modules_count_label.after(2000, get_modules)


        get_students()
        get_modules()


class EntryFormFrame(ttk.Labelframe):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(text="Student Registration Form", padding=30)

        # Labels
        tk.Label(self, text='Student ID (max 3 char)').grid(row=0, column=0, sticky='w')
        tk.Label(self, text='First Name').grid(row=2, column=0, pady=(20,0), sticky='w')
        tk.Label(self, text='Last Name').grid(row=4, column=0, pady=(20,0), sticky='w')
        tk.Label(self, text='Select gender').grid(row=6, column=0, pady=(20,0), sticky='w')
        tk.Label(self, text='Module Code').grid(row=8, column=0, pady=(30,0), sticky='w')
        tk.Label(self, text='Coursework 1').grid(row=10, column=0, pady=(20,0), sticky='w')
        tk.Label(self, text='Cousework 2').grid(row=12, column=0, pady=(20,0), sticky='w')
        tk.Label(self, text='Coursework 3').grid(row=14, column=0, pady=(20,0), sticky='w')
        tk.Label(self, text='Date of Entry (yyyy-mm-dd)').grid(row=16, column=0, pady=(20,0), sticky='w')

        # Entry boxes
        self.student_id = ttk.Entry(self, width=30)
        self.student_id.grid(row=1, column=0, ipady=5)
        self.first_name = ttk.Entry(self, width=30)
        self.first_name.grid(row=3, column=0, ipady=5)
        self.last_name = ttk.Entry(self, width=30)
        self.last_name.grid(row=5, column=0, ipady=5)

        self.gendervar = IntVar()
        self.male = ttk.Radiobutton(self, text='male', variable=self.gendervar, value=1)
        self.male.grid(row=7, column=0, sticky='w')
        self.female = ttk.Radiobutton(self, text='female', variable=self.gendervar, value=2)
        self.female.grid(row=7, column=0)

        self.module_code = ttk.Entry(self, width=30)
        self.module_code.grid(row=9, column=0, ipady=5)
        self.coursework1 = ttk.Entry(self, width=30)
        self.coursework1.grid(row=11, column=0, ipady=5)
        self.coursework2 = ttk.Entry(self, width=30)
        self.coursework2.grid(row=13, column=0, ipady=5)
        self.coursework3 = ttk.Entry(self, width=30)
        self.coursework3.grid(row=15, column=0, ipady=5)

        self.entry_date = ttk.Entry(self, width=30)
        self.entry_date.grid(row=17, column=0, ipady=5)

        reset_button = ttk.Button(self, text="Reset", command=self.reset_fields, width=30)
        reset_button.grid(row=18, column=0, pady=(30,0), ipady=5)
        submit_button = ttk.Button(self, text="Submit", command=self.validate_and_submit, width=30)
        submit_button.grid(row=19, column=0, ipady=5)

    def reset_fields(self, event=None):
        self.student_id.delete(0, tk.END)
        self.first_name.delete(0, tk.END)
        self.last_name.delete(0, tk.END)
        self.gendervar.set(0)
        self.module_code.delete(0, tk.END)
        self.coursework1.delete(0, tk.END)
        self.coursework2.delete(0, tk.END)
        self.coursework3.delete(0, tk.END)
        self.entry_date.delete(0, tk.END)

    
    def validate_and_submit(self, event=None):
        student_id = self.student_id.get()
        first_name = self.first_name.get()
        last_name = self.last_name.get()
        module_code = self.module_code.get()
        coursework1 = self.coursework1.get()
        coursework2 = self.coursework2.get()
        coursework3 = self.coursework3.get()
        entry_date = self.entry_date.get()

        # Validate fields
        if not student_id or len(student_id) != 3:
            messagebox.showerror("Error", "Student ID must be exactly 3 characters long.")
            return
        if not first_name:
            messagebox.showerror("Error", "First name cannot be empty.")
            return
        if not last_name:
            messagebox.showerror("Error", "Last name cannot be empty.")
            return
        if not module_code:
            messagebox.showerror("Error", "Module code cannot be empty.")
            return
        if not entry_date:
            messagebox.showerror("Error", "Date cannot be empty.")
            return
        
        try:
            coursework1 = float(coursework1)
            coursework2 = float(coursework2)
            coursework3 = float(coursework3)
        except ValueError:
            messagebox.showerror("Error", "Coursework marks must be numbers.")
            return
        if not (0 <= coursework1 <= 100) or not (0 <= coursework2 <= 100) or not (0 <= coursework3 <= 100):
            messagebox.showerror("Error", "Coursework marks must be between 0 and 100.")
            return

        if self.gendervar.get() == 1:
            gender = 'male'
        else:
            gender = 'female'

        total_marks = int(coursework1) + int(coursework2) + int(coursework3)

        c.execute('''
                  INSERT INTO markstable (student_id, first_name, last_name, gender, module_code, coursework1, coursework2, coursework3, total_marks, entry_date)
                  VALUES (?, ?, ?, ?, ?,?, ?, ?, ?, ?)''',
                  (student_id, first_name, last_name, gender, module_code, coursework1, coursework2, coursework3, total_marks, entry_date))
        conn.commit()

        self.reset_fields()
        messagebox.showinfo("Success", "Data saved successfully!")


class DisplayRecordsFrame(ttk.Labelframe):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(text="Students Records", padding=30)

        # Function to populate the treeview
        def populate_treeview():
            for item in self.treeview.get_children():
                self.treeview.delete(item)

            c.execute("SELECT * FROM markstable")
            rows = c.fetchall()
            for row in rows:
                self.treeview.insert("", "end", values=row)

        # Function to select a record and display in entry boxes
        def treeview_select(event):
            try:
                selected_item = self.treeview.selection()[0]
                item = self.treeview.item(selected_item)
                values = item['values']
                self.student_id.delete(0, tk.END)
                self.student_id.insert(0, values[0])
                self.first_name.delete(0, tk.END)
                self.first_name.insert(0, values[1])
                self.last_name.delete(0, tk.END)
                self.last_name.insert(0, values[2])
                self.gender.delete(0, tk.END)
                self.gender.insert(0, values[3])
                self.module_code.delete(0, tk.END)
                self.module_code.insert(0, values[4])
                self.coursework1.delete(0, tk.END)
                self.coursework1.insert(0, values[5])
                self.coursework2.delete(0, tk.END)
                self.coursework2.insert(0, values[6])
                self.coursework3.delete(0, tk.END)
                self.coursework3.insert(0, values[7])
                self.entry_date.delete(0, tk.END)
                self.entry_date.insert(0,values[9])
            except IndexError:
                self.student_id.delete(0, tk.END)
                self.first_name.delete(0, tk.END)
                self.last_name.delete(0, tk.END)
                self.gender.delete(0, tk.END)
                self.module_code.delete(0, tk.END)
                self.coursework1.delete(0, tk.END)
                self.coursework2.delete(0, tk.END)
                self.coursework3.delete(0, tk.END)
                self.entry_date.delete(0, tk.END)

        # Function to update the record
        def update_record():
            try:
                selected_item = self.treeview.selection()[0]
                student_id = self.student_id.get()
                first_name = self.first_name.get()
                last_name = self.last_name.get()
                gender = self.gender.get()
                module_code = self.module_code.get()
                coursework1 = self.coursework1.get()
                coursework2 = self.coursework2.get()
                coursework3 = self.coursework3.get()
                total_marks = int(coursework1) + int(coursework2) + int(coursework3)
                entry_date = self.entry_date.get()

                # Validate fields
                if not student_id or len(student_id) != 3:
                    messagebox.showerror("Error", "Student ID must be exactly 3 characters long.")
                    return
                if not first_name:
                    messagebox.showerror("Error", "First name cannot be empty.")
                    return
                if not last_name:
                    messagebox.showerror("Error", "Last name cannot be empty.")
                    return
                if not module_code:
                    messagebox.showerror("Error", "Module code cannot be empty.")
                    return
                if not entry_date:
                    messagebox.showerror("Error", "Date cannot be empty.")
                    return
                
                if not gender:
                    messagebox.showerror("Error", "Gender can cannot be empty.")
                    return                   
                
                if gender != 'male' and gender != 'female':
                    messagebox.showerror("Error", "Gender can only be either male or female.")
                    return
                
                try:
                    coursework1 = float(coursework1)
                    coursework2 = float(coursework2)
                    coursework3 = float(coursework3)
                except ValueError:
                    messagebox.showerror("Error", "Coursework marks must be numbers.")
                    return
                if not (0 <= coursework1 <= 100) or not (0 <= coursework2 <= 100) or not (0 <= coursework3 <= 100):
                    messagebox.showerror("Error", "Coursework marks must be between 0 and 100.")
                    return

                c.execute("UPDATE markstable SET student_id=?, first_name=?, last_name=?, gender=?, module_code=?, coursework1=?, coursework2=?, coursework3=?, total_marks=?, entry_date=? WHERE student_id=?",
                            (student_id, first_name, last_name, gender, module_code, coursework1, coursework2, coursework3, total_marks, entry_date, self.treeview.item(selected_item)['values'][0]))
                conn.commit()

                populate_treeview()
                self.student_id.delete(0, tk.END)
                self.first_name.delete(0, tk.END)
                self.last_name.delete(0, tk.END)
                self.gender.delete(0, tk.END)
                self.module_code.delete(0, tk.END)
                self.coursework1.delete(0, tk.END)
                self.coursework2.delete(0, tk.END)
                self.coursework3.delete(0, tk.END)
                self.entry_date.delete(0, tk.END)
            except IndexError:
                tk.messagebox.showerror("Error", "Please select a record to update.") 

        # Create the treeview
        self.treeview = ttk.Treeview(self, columns=("student_id",
                                                     "first_name",
                                                     "last_name",
                                                     "gender",
                                                     "module_code",
                                                     "coursework1",
                                                     "coursework2",
                                                     "coursework3",
                                                     "total_marks",
                                                     "entry_date"), show="headings")
        
        self.treeview.heading("student_id", text="Student ID")
        self.treeview.heading("first_name", text="First Name")
        self.treeview.heading("last_name", text="Last Name")
        self.treeview.heading("gender", text="Gender")
        self.treeview.heading("module_code", text="Module Code")
        self.treeview.heading("coursework1", text="Coursework1")
        self.treeview.heading("coursework2", text="Coursework2")
        self.treeview.heading("coursework3", text="Coursework3")
        self.treeview.heading("total_marks", text="Total Marks")
        self.treeview.heading("entry_date", text="Entry Date")

        self.treeview.grid(row=0, column=0, columnspan=2)
        self.treeview.bind("<ButtonRelease-1>", treeview_select)

        # Set column widths
        self.treeview.column("student_id", width=80, anchor='center')
        self.treeview.column("first_name", width=100, anchor='center')
        self.treeview.column("last_name", width=100, anchor='center')
        self.treeview.column("gender", width=100, anchor='center')
        self.treeview.column("module_code", width=100, anchor='center')
        self.treeview.column("coursework1", width=100, anchor='center')
        self.treeview.column("coursework2", width=100, anchor='center')
        self.treeview.column("coursework3", width=100, anchor='center')
        self.treeview.column("total_marks", width=100, anchor='center')
        self.treeview.column("entry_date", width=100, anchor='center')

        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Arial", 10, "bold")) 
        style.configure("Treeview", rowheight=30, font=("Arial", 10))


        # Create a vertical scrollbar
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.treeview.yview)
        self.treeview.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(sticky="NS",row=0, column=2)

        # Labels
        tk.Label(self, text='Student ID (max 3 char)').grid(sticky="e", row=1, column=0, pady=10)
        tk.Label(self, text='First Name').grid(sticky="E",row=2, column=0, pady=10)
        tk.Label(self, text='Last Name').grid(sticky="E",row=3, column=0, pady=10)
        tk.Label(self, text='Gender').grid(sticky="E",row=4, column=0, pady=10)
        tk.Label(self, text='Module Code').grid(sticky="E",row=6, column=0, pady=10)
        tk.Label(self, text='Coursework 1').grid(sticky="E",row=7, column=0, pady=10)
        tk.Label(self, text='Coursework 2').grid(sticky="E",row=8, column=0, pady=10)
        tk.Label(self, text='Coursework 3').grid(sticky="E",row=9, column=0, pady=10)
        tk.Label(self, text='Date of Entry (yyyy-mm-dd)').grid(sticky="E",row=10, column=0, pady=10)

        # Entry boxes
        self.student_id = ttk.Entry(self)
        self.student_id.grid(sticky="w",row=1, column=1, padx=10, pady=10, ipady=3)
        self.first_name = ttk.Entry(self)
        self.first_name.grid(sticky="W",row=2, column=1, padx=10, pady=10, ipady=3)
        self.last_name = ttk.Entry(self)
        self.last_name.grid(sticky="W",row=3, column=1, padx=10, pady=10, ipady=3)
        
        self.gender = ttk.Entry(self)
        self.gender.grid(sticky="W",row=4, column=1, padx=10, pady=10, ipady=3)

        self.module_code = ttk.Entry(self)
        self.module_code.grid(sticky="W",row=6, column=1, padx=10, pady=10, ipady=3)
        self.coursework1 = ttk.Entry(self)
        self.coursework1.grid(sticky="W",row=7, column=1, padx=10, pady=10, ipady=3)
        self.coursework2 = ttk.Entry(self)
        self.coursework2.grid(sticky="W",row=8, column=1, padx=10, pady=10, ipady=3)
        self.coursework3 = ttk.Entry(self)
        self.coursework3.grid(sticky="W",row=9, column=1, padx=10, pady=10, ipady=3)
        self.entry_date = ttk.Entry(self)
        self.entry_date.grid(sticky="W",row=10, column=1, padx=10, pady=10, ipady=3)

        update_button = ttk.Button(self, text="Update", command=update_record, width=30)
        update_button.grid(row=11, column=0, columnspan=2, ipady=5, padx=5, pady=10)

        populate_treeview()


class VisualizeFrame(ttk.LabelFrame):

    def __init__(self, parent):
        super().__init__(parent)
        self.configure(text="Student Records Charts", padding=60)

        gender_chart_bt = ttk.Button(self, text='View Students Gender Distribution', command=lambda : display_gender_chart(), width=60)
        gender_chart_bt.grid(row=0, column=0, ipady=5, pady=15)

        avgmarks_chart_bt = ttk.Button(self, text='View Average Marks by Coursework', command=lambda : display_avgmarks_chart(), width=60)
        avgmarks_chart_bt.grid(row=1, column=0, ipady=5, pady=15)

        
        def display_gender_chart():
            c.execute("SELECT gender, COUNT(*) FROM markstable GROUP BY gender")
            data = c.fetchall()

            labels = [row[0] for row in data]
            sizes = [row[1] for row in data]
            
            fig, ax = plt.subplots()
            ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
            ax.axis('equal')
            
            plt.title('Students Distribution by Gender')
            plt.show()


        def display_avgmarks_chart():
            c.execute("SELECT coursework1, coursework2, coursework3 FROM markstable")
            data = c.fetchall()

            # Calculate the averages
            c1_avg = sum(row[0] for row in data) / len(data)
            c2_avg = sum(row[1] for row in data) / len(data)
            c3_avg = sum(row[2] for row in data) / len(data)

            # Prepare the data for the bar chart
            averages = [c1_avg, c2_avg, c3_avg]
            fields = ['coursework1', 'coursework2', 'coursework3']

            # Create the bar chart
            plt.figure(figsize=(6,6))
            plt.bar(fields, averages, width=0.4)
            plt.xlabel('Courseworks', labelpad=10)
            plt.ylabel('Average Values', labelpad=10)
            plt.title('Average Marks of Courseworks', pad=20)
            # Annotate the averages on top of the bars
            for i, avg in enumerate(averages):
                plt.text(i, avg, f'{avg:.2f}', ha='center', va='bottom')

            plt.tight_layout() 
            plt.show()