import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import frames


def student_marks_window():
    # main frame
    main_window = tk.Tk()
    main_window.title('Students Marks')
    # main_window.geometry('640x480')
    # main_window.configure(background='white')
    main_window.columnconfigure(1, weight=1,)

    # home, entry, display records, update, visualise
    home_frame = frames.HomeFrame(main_window)
    home_frame.grid(row=0, column=1, padx=20, pady=20, sticky='nsew')

    entry_frame = frames.EntryFormFrame(main_window) 
    display_records_frame = frames.DisplayRecordsFrame(main_window)
    visualise_frame = frames.VisualizeFrame(main_window)
    
    # buttons
    buttons_frame = ttk.Frame(main_window, )
    buttons_frame.grid(row=0, column=0, padx=10, pady=20, sticky='nsew')
    
    home_bt = ttk.Button(buttons_frame, text='Homepage', command=lambda : button_nav(home_frame), width=30)
    home_bt.grid(row=0, column=0, ipady=5, padx=5, pady=10)
    
    entry_form_bt = ttk.Button(buttons_frame, text='Registration Form', command=lambda : button_nav(entry_frame), width=30)
    entry_form_bt.grid(row=1, column=0, ipady=5, padx=5, pady=10)

    display_records_bt = ttk.Button(buttons_frame, text='View Records', command=lambda : button_nav(display_records_frame), width=30)
    display_records_bt.grid(row=2, column=0, ipady=5, padx=5, pady=10)

    visualise_bt = ttk.Button(buttons_frame, text='Visualisation', command=lambda : button_nav(visualise_frame), width=30)
    visualise_bt.grid(row=3, column=0, ipady=5, padx=5, pady=10)


    def button_nav(frame):
        home_frame.grid_remove()
        entry_frame.grid_remove()
        display_records_frame.grid_remove()
        visualise_frame.grid_remove()
        
        frame.grid(row=0, column=1,padx=20, pady=20, sticky='nsew')

    main_window.mainloop()


def validate_login(username, password):
    correct_username = "user"
    correct_password = "pass"

    if username == correct_username and password == correct_password:
        return True
    else:
        return False


def login_window():
    lw = tk.Tk()
    lw.title("Students Marks Login")
    lw.geometry("300x280")

    tk.Label(lw, text="Username:").grid(row=0, column=0,padx=60, pady=(40,0), sticky='w')
    username_entry = ttk.Entry(lw, width=30)
    username_entry.grid(row=1,column=0,padx=60, sticky='w', ipady=5)

    tk.Label(lw, text="Password:").grid(row=3, column=0, padx=60, pady=(20,0), sticky='w')
    password_entry = ttk.Entry(lw, show="*", width=30)
    password_entry.grid(row=4, column=0,padx=60, sticky='w', ipady=5)


    def on_login():
        username = username_entry.get()
        password = password_entry.get()
        if validate_login(username, password):
            messagebox.showinfo("Success", "Login Successful!")
            lw.destroy()
            student_marks_window()
        else:
            messagebox.showerror("Login Failed", "Incorrect username or password.")
    
    
    ttk.Button(lw, text="Login", command=on_login, width=30).grid(row=6, column=0, padx=60, pady=40, ipady=5)

    lw.mainloop()


def main():
    login_window()


if __name__ == '__main__':
    main()
