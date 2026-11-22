import json
import os
import uuid
from datetime import datetime
import tkinter as tk
from tkinter import messagebox

# ==========================================
# 1. КЛАСС TASK (Модель данных)
# ==========================================
class Task:
    def __init__(self, title, description="", status="new", author="User", task_id=None, created_at=None):
        self.id = task_id if task_id else str(uuid.uuid4())
        self.title = title
        self.description = description
        self.status = status
        self.author = author
        self.created_at = created_at if created_at else datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status,
            "author": self.author,
            "created_at": self.created_at
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            title=data.get("title"),
            description=data.get("description", ""),
            status=data.get("status", "new"),
            author=data.get("author", "User"),
            task_id=data.get("id"),
            created_at=data.get("created_at")
        )

# ==========================================
# 2. КЛАСС STORAGEMANAGER (Работа с JSON)
# ==========================================
class StorageManager:
    def __init__(self, filename="tasks.json"):
        self.filename = filename

    def load(self):
        if not os.path.exists(self.filename):
            return []
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return [Task.from_dict(item) for item in data]
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def save(self, tasks):
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump([task.to_dict() for task in tasks], f, ensure_ascii=False, indent=4)

    def add(self, task, tasks):
        tasks.append(task)
        self.save(tasks)

    def update(self, task_id, updated_data, tasks):
        for task in tasks:
            if task.id == task_id:
                task.title = updated_data.get("title", task.title)
                task.description = updated_data.get("description", task.description)
                task.status = updated_data.get("status", task.status)
                break
        self.save(tasks)

    def delete(self, task_id, tasks):
        tasks[:] = [t for t in tasks if t.id != task_id]
        self.save(tasks)

# ==========================================
# 3. КЛАСС INTERFACE (Прослойка к Tkinter)
# ==========================================
class Interface:
    def __init__(self, root):
        self.root = root
        self.root.title("Менеджер задач v0.2.0")
        self.root.geometry("600x500")

        # Поле ввода названия
        tk.Label(root, text="Название задачи:", font=("Arial", 10)).pack(pady=(10, 0), anchor="w", padx=10)
        self.entry_title = tk.Entry(root, font=("Arial", 11))
        self.entry_title.pack(padx=10, fill=tk.X)

        # Поле ввода описания
        tk.Label(root, text="Описание:", font=("Arial", 10)).pack(pady=(10, 0), anchor="w", padx=10)
        self.entry_desc = tk.Entry(root, font=("Arial", 11))
        self.entry_desc.pack(padx=10, fill=tk.X)

        # Кнопки
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10, fill=tk.X, padx=10)

        self.btn_add = tk.Button(btn_frame, text="Добавить", bg="#4CAF50", fg="white")
        self.btn_add.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)

        self.btn_edit = tk.Button(btn_frame, text="Редактировать", bg="#2196F3", fg="white")
        self.btn_edit.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)

        self.btn_delete = tk.Button(btn_frame, text="Удалить", bg="#f44336", fg="white")
        self.btn_delete.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)

        self.btn_toggle = tk.Button(btn_frame, text="Сменить статус", bg="#FF9800", fg="white")
        self.btn_toggle.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)

        # Список задач
        self.listbox = tk.Listbox(root, font=("Arial", 11), selectbackground="#2196F3")
        self.listbox.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    def get_input(self):
        return self.entry_title.get().strip(), self.entry_desc.get().strip()

    def show_tasks(self, tasks):
        self.listbox.delete(0, tk.END)
        for task in tasks:
            status_icon = "✓" if task.status == "done" else "○"
            display_text = f"[{status_icon}] {task.title} ({task.created_at})"
            self.listbox.insert(tk.END, display_text)

    def ask_confirm(self, message):
        return messagebox.askyesno("Подтверждение", message)

    def show_error(self, message):
        messagebox.showerror("Ошибка", message)

    def clear_inputs(self):
        self.entry_title.delete(0, tk.END)
        self.entry_desc.delete(0, tk.END)

    def get_selected_index(self):
        selection = self.listbox.curselection()
        return selection[0] if selection else None

# ==========================================
# 4. КЛАСС TASKMANAGER (Фасад / Логика)
# ==========================================
class TaskManager:
    def __init__(self, root):
        self.storage = StorageManager()
        self.ui = Interface(root)
        self.tasks = self.storage.load()

        # Привязка событий (Binding)
        self.ui.btn_add.config(command=self.create_task)
        self.ui.btn_edit.config(command=self.edit_task)
        self.ui.btn_delete.config(command=self.delete_task)
        self.ui.btn_toggle.config(command=self.toggle_status)

        self.refresh_ui()

    def refresh_ui(self):
        self.ui.show_tasks(self.tasks)

    def create_task(self):
        title, desc = self.ui.get_input()
        if not title:
            self.ui.show_error("Название задачи не может быть пустым!")
            return
        
        new_task = Task(title=title, description=desc)
        self.storage.add(new_task, self.tasks)
        self.ui.clear_inputs()
        self.refresh_ui()

    def edit_task(self):
        idx = self.ui.get_selected_index()
        if idx is None:
            self.ui.show_error("Выберите задачу для редактирования!")
            return

        title, desc = self.ui.get_input()
        if not title:
            self.ui.show_error("Название не может быть пустым!")
            return

        task_id = self.tasks[idx].id
        updated_data = {"title": title, "description": desc}
        
        self.storage.update(task_id, updated_data, self.tasks)
        self.ui.clear_inputs()
        self.refresh_ui()

    def delete_task(self):
        idx = self.ui.get_selected_index()
        if idx is None:
            self.ui.show_error("Выберите задачу для удаления!")
            return

        task_id = self.tasks[idx].id
        if self.ui.ask_confirm("Вы уверены, что хотите удалить эту задачу?"):
            self.storage.delete(task_id, self.tasks)
            self.refresh_ui()

    def toggle_status(self):
        idx = self.ui.get_selected_index()
        if idx is None:
            self.ui.show_error("Выберите задачу для смены статуса!")
            return

        task = self.tasks[idx]
        new_status = "done" if task.status == "new" else "new"
        self.storage.update(task.id, {"status": new_status}, self.tasks)
        self.refresh_ui()

    def run(self):
        self.ui.root.mainloop()

# ==========================================
# ТОЧКА ВХОДА
# ==========================================
if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManager(root)
    app.run()
