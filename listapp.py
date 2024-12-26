import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import json

class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List Application")
        self.root.geometry("600x500")
        self.tasks = []

        # Task Entry
        self.task_label = tk.Label(root, text="Task:", font=("Arial", 12), bg="#f0f0f0", fg="#2a2a2a")
        self.task_label.pack()

        self.task_entry = tk.Entry(root, font=("Arial", 14), width=30)
        self.task_entry.pack(pady=10)

        # Due Date Entry
        self.due_label = tk.Label(root, text="Due Date (YYYY-MM-DD):", font=("Arial", 12), bg="#f0f0f0", fg="#2a2a2a")
        self.due_label.pack()

        self.due_entry = tk.Entry(root, font=("Arial", 14), width=30)
        self.due_entry.pack(pady=10)

        # Priority Dropdown
        self.priority_label = tk.Label(root, text="Priority:", font=("Arial", 12), bg="#f0f0f0", fg="#2a2a2a")
        self.priority_label.pack()

        self.priority_var = tk.StringVar(root)
        self.priority_var.set("Medium")  # Default priority

        self.priority_menu = tk.OptionMenu(root, self.priority_var, "High", "Medium", "Low")
        self.priority_menu.pack(pady=10)

        # Category Dropdown
        self.category_label = tk.Label(root, text="Category:", font=("Arial", 12), bg="#f0f0f0", fg="#2a2a2a")
        self.category_label.pack()

        self.category_var = tk.StringVar(root)
        self.category_var.set("Work")  # Default category

        self.category_menu = tk.OptionMenu(root, self.category_var, "Work", "Personal", "Other")
        self.category_menu.pack(pady=10)

        # Add Task Button
        self.add_button = tk.Button(root, text="Add Task", font=("Arial", 14), bg="#4CAF50", fg="white", command=self.add_task)
        self.add_button.pack(pady=10)

        # Search Bar
        self.search_label = tk.Label(root, text="Search:", font=("Arial", 12), bg="#f0f0f0", fg="#2a2a2a")
        self.search_label.pack()

        self.search_entry = tk.Entry(root, font=("Arial", 14), width=30)
        self.search_entry.pack(pady=10)

        # Task Listbox
        self.task_listbox = tk.Listbox(root, font=("Arial", 12), width=50, height=10)
        self.task_listbox.pack(pady=10)

        # Sort Buttons
        self.sort_due_button = tk.Button(root, text="Sort by Due Date", font=("Arial", 12), command=self.sort_tasks_by_due_date)
        self.sort_due_button.pack(pady=5)

        self.sort_priority_button = tk.Button(root, text="Sort by Priority", font=("Arial", 12), command=self.sort_tasks_by_priority)
        self.sort_priority_button.pack(pady=5)

        # Load tasks on startup
        self.load_tasks()

        # Bind search function to search entry
        self.search_entry.bind("<KeyRelease>", lambda event: self.search_tasks())

    def add_task(self):
        task = self.task_entry.get()
        due_date = self.due_entry.get()
        priority = self.priority_var.get()
        category = self.category_var.get()

        if task and due_date:
            try:
                datetime.strptime(due_date, "%Y-%m-%d")  # Validate date format
                self.tasks.append({"task": task, "due_date": due_date, "priority": priority, "category": category, "completed": False})
                self.update_task_listbox()
                self.task_entry.delete(0, tk.END)
                self.due_entry.delete(0, tk.END)
            except ValueError:
                messagebox.showwarning("Date Error", "Invalid date format. Please enter the date in YYYY-MM-DD format.")
        else:
            messagebox.showwarning("Input Error", "Please enter both task and due date.")

    def update_task_listbox(self):
        self.task_listbox.delete(0, tk.END)
        for task in self.tasks:
            task_str = f"{task['task']} | Due: {task['due_date']} | Priority: {task['priority']} | Category: {task['category']}"
            self.task_listbox.insert(tk.END, task_str)

    def mark_completed(self, index):
        self.tasks[index]["completed"] = True
        self.update_task_listbox()

    def search_tasks(self):
        search_term = self.search_entry.get().lower()
        filtered_tasks = [task for task in self.tasks if search_term in task["task"].lower()]
        self.update_filtered_task_listbox(filtered_tasks)

    def update_filtered_task_listbox(self, tasks):
        self.task_listbox.delete(0, tk.END)
        for task in tasks:
            task_str = f"{task['task']} | Due: {task['due_date']} | Priority: {task['priority']} | Category: {task['category']}"
            self.task_listbox.insert(tk.END, task_str)

    def sort_tasks_by_due_date(self):
        self.tasks.sort(key=lambda x: x["due_date"])
        self.update_task_listbox()

    def sort_tasks_by_priority(self):
        priority_order = {"High": 0, "Medium": 1, "Low": 2}
        self.tasks.sort(key=lambda x: priority_order[x["priority"]])
        self.update_task_listbox()

    def save_tasks(self):
        with open("tasks.json", "w") as f:
            json.dump(self.tasks, f)

    def load_tasks(self):
        try:
            with open("tasks.json", "r") as f:
                self.tasks = json.load(f)
                self.update_task_listbox()
        except FileNotFoundError:
            pass

    def on_closing(self):
        self.save_tasks()
        self.root.quit()

# Main Loop
root = tk.Tk()
app = ToDoApp(root)
root.protocol("WM_DELETE_WINDOW", app.on_closing)
root.mainloop()
