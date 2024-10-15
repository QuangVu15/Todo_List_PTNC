import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from tkinter.ttk import Combobox
import psycopg2
from idlelib.tooltip import Hovertip

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ngô Quang Vũ")
        self.root.iconbitmap("python-misc-32.ico")  # Set the icon for the window
        
        # Menu bar
        menu_bar = tk.Menu(root)
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Save", command=self.save_data)
        file_menu.add_command(label="Load", command=self.load_data)
        menu_bar.add_cascade(label="File", menu=file_menu)
        root.config(menu=menu_bar)
        
        # Tabbed Widgets
        tab_control = ttk.Notebook(root)
        
        # Tab 1: To-Do List
        tab1 = ttk.Frame(tab_control)
        tab_control.add(tab1, text='To-Do List')
        
        # Tab 2: Settings
        tab2 = ttk.Frame(tab_control)
        tab_control.add(tab2, text='Settings')
        tab_control.pack(expand=1, fill='both')
        
        # Label Frame for To-Do Entry
        label_frame = ttk.LabelFrame(tab1, text="New Task")
        label_frame.grid(column=0, row=0, padx=10, pady=10)

        # Task Entry
        ttk.Label(label_frame, text="Task:").grid(column=0, row=0)
        self.task_entry = ttk.Entry(label_frame, width=30)
        self.task_entry.grid(column=1, row=0)

        # Priority Spinbox
        ttk.Label(label_frame, text="Priority:").grid(column=0, row=1)
        self.priority_spinbox = ttk.Spinbox(label_frame, from_=1, to=5, width=5)
        self.priority_spinbox.grid(column=1, row=1)

        # Combo Box for Category
        ttk.Label(label_frame, text="Category:").grid(column=0, row=2)
        self.category_combobox = Combobox(label_frame)
        self.category_combobox['values'] = ("Work", "Home", "Study", "Other")
        self.category_combobox.grid(column=1, row=2)

        # Radio Button for Status
        ttk.Label(label_frame, text="Status:").grid(column=0, row=3)
        self.status_var = tk.StringVar()
        ttk.Radiobutton(label_frame, text="Pending", variable=self.status_var, value="Pending").grid(column=1, row=3)
        ttk.Radiobutton(label_frame, text="Completed", variable=self.status_var, value="Completed").grid(column=2, row=3)

        # ScrolledText for Task List
        self.scrolled_text = scrolledtext.ScrolledText(tab1, width=40, height=10)
        self.scrolled_text.grid(column=0, row=1, padx=10, pady=10)

        # Add Task Button
        add_task_btn = ttk.Button(label_frame, text="Add Task", command=self.add_task)
        add_task_btn.grid(column=1, row=4)
        
        # Tooltip for Add Task Button
        Hovertip(add_task_btn, "Click to add a new task.")

    def add_task(self):
        task = self.task_entry.get()
        priority = self.priority_spinbox.get()
        category = self.category_combobox.get()
        status = self.status_var.get()
        if task:
            task_entry = f"{task} | Priority: {priority} | Category: {category} | Status: {status}\n"
            self.scrolled_text.insert(tk.END, task_entry)
        else:
            messagebox.showwarning("Input Error", "Task cannot be empty")

    def save_data(self):
        task = self.task_entry.get()
        priority = self.priority_spinbox.get()
        category = self.category_combobox.get()
        status = self.status_var.get()
        
        connection, cursor = self.connect_to_db()
        if connection is not None:
            insert_query = """INSERT INTO tasks (task_name, priority, category, status)
                              VALUES (%s, %s, %s, %s)"""
            cursor.execute(insert_query, (task, priority, category, status))
            connection.commit()
            cursor.close()
            connection.close()
            messagebox.showinfo("Success", "Task saved successfully!")
        else:
            messagebox.showerror("Error", "Could not connect to the database.")

    def load_data(self):
        connection, cursor = self.connect_to_db()
        if connection is not None:
            select_query = "SELECT task_name, priority, category, status FROM tasks"
            cursor.execute(select_query)
            records = cursor.fetchall()
            self.scrolled_text.delete(1.0, tk.END)
            for record in records:
                task_entry = f"{record[0]} | Priority: {record[1]} | Category: {record[2]} | Status: {record[3]}\n"
                self.scrolled_text.insert(tk.END, task_entry)
            cursor.close()
            connection.close()
        else:
            messagebox.showerror("Error", "Could not connect to the database.")

    def connect_to_db(self):
        try:
            connection = psycopg2.connect(
                user="your_user",
                password="your_password",
                host="localhost",
                port="5432",
                database="your_database"
            )
            cursor = connection.cursor()
            return connection, cursor
        except Exception as error:
            print("Error while connecting to PostgreSQL", error)
            return None, None


if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()
