import json
import os
import tkinter as tk
from tkinter import messagebox
from abc import ABC, abstractmethod

# ==========================================
# 1. СЛОЙ ИНТЕРФЕЙСА (interface.py)
# ==========================================
class ITaskStorage(ABC):
    @abstractmethod
    def load_tasks(self):
        pass

    @abstractmethod
    def save_tasks(self, tasks):
        pass


# ==========================================
# 2. СЛОЙ ХРАНЕНИЯ (storage.py)
# ==========================================
class JsonTaskStorage(ITaskStorage):
    def __init__(self, filename="tasks.json"):
        self.filename = filename

    def load_tasks(self):
        if not os.path.exists(self.filename):
            return []
        try:
            with open(self.filename, 'r', encoding='utf-8') as file:
                return json.load(file)
        except json.JSONDecodeError:
            return []

    def save_tasks(self, tasks):
        with open(self.filename, 'w', encoding='utf-8') as file:
            json.dump(tasks, file, ensure_ascii=False, indent=4)


# ==========================================
# 3. КАСТОМНЫЕ ВИДЖЕТЫ (appButton.py, appLabel.py)
# ==========================================
class AppButton(tk.Button):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.config(
            bg="#4CAF50",
            fg="white",
            font=("Arial", 10, "bold"),
            relief="flat",
            padx=10,
            pady=5
        )


class AppListbox(tk.Listbox):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.config(
            font=("Arial", 11),
            selectbackground="#2196F3",
            activestyle="none",
            height=10
        )


# ==========================================
# 4. СЛОЙ ПРЕДСТАВЛЕНИЯ (view.py)
# ==========================================
class TaskManagerView:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Manager - Layered Architecture")
        self.root.geometry("400x500")

        self.storage = JsonTaskStorage()
        self.tasks = self.storage.load_tasks()

        self.setup_ui()

    def setup_ui(self):
        self.entry_task = tk.Entry(self.root, font=("Arial", 12))
        self.entry_task.pack(pady=10, padx=10, fill=tk.X)

        self.btn_add = AppButton(self.root, text="Добавить задачу", command=self.add_task)
        self.btn_add.pack(pady=5)

        self.btn_done = AppButton(self.root, text="Отметить выполненной", command=self.toggle_done)
        self.btn_done.config(bg="#2196F3")
        self.btn_done.pack(pady=5)

        self.btn_delete = AppButton(self.root, text="Удалить задачу", command=self.delete_task)
        self.btn_delete.config(bg="#f44336")
        self.btn_delete.pack(pady=5)

        self.listbox_tasks = AppListbox(self.root)
        self.listbox_tasks.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        self.display_tasks(self.tasks)

    def add_task(self):
        task_text = self.entry_task.get().strip()
        if task_text:
            self.tasks.append({"task": task_text, "done": False})
            self.storage.save_tasks(self.tasks)
            self.entry_task.delete(0, tk.END)
            self.display_tasks(self.tasks)
        else:
            messagebox.showwarning("Внимание", "Введите текст задачи!")

    def toggle_done(self):
        try:
            index = self.listbox_tasks.curselection()[0]
            self.tasks[index]["done"] = not self.tasks[index]["done"]
            self.storage.save_tasks(self.tasks)
            self.display_tasks(self.tasks)
        except IndexError:
            messagebox.showwarning("Внимание", "Выберите задачу из списка!")

    def delete_task(self):
        try:
            index = self.listbox_tasks.curselection()[0]
            del self.tasks[index]
            self.storage.save_tasks(self.tasks)
            self.display_tasks(self.tasks)
        except IndexError:
            messagebox.showwarning("Внимание", "Выберите задачу из списка!")

    def display_tasks(self, tasks):
        self.listbox_tasks.delete(0, tk.END)
        for task in tasks:
            status = "✓ " if task.get("done") else "○ "
            self.listbox_tasks.insert(tk.END, status + task["task"])


# ==========================================
# 5. ТОЧКА ВХОДА (main.py)
# ==========================================
if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagerView(root)
    root.mainloop()
