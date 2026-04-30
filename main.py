import tkinter as tk
from tkinter import ttk, messagebox
import random
import json
import os
from datetime import datetime

DEFAULT_TASKS = [
    {"name": "Прочитать статью", "type": "учёба"},
    {"name": "Сделать зарядку", "type": "спорт"},
    {"name": "Написать отчёт", "type": "работа"},
    {"name": "Выучить 10 новых слов", "type": "учёба"},
    {"name": "Пробежка 3 км", "type": "спорт"},
    {"name": "Позвонить клиенту", "type": "работа"},
    {"name": "Посмотреть вебинар", "type": "учёба"},
    {"name": "Отжимания 20 раз", "type": "спорт"},
    {"name": "Составить план", "type": "работа"}
]

class TaskGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Task Generator")
        self.root.geometry("650x550")
        self.root.resizable(True, True)

        self.history = []
        self.filtered_history = []
        self.current_filter = "все"

        self.load_history()
        self.create_widgets()
        self.update_history_listbox()

    def create_widgets(self):
        frame_top = ttk.LabelFrame(self.root, text="Генератор", padding=10)
        frame_top.pack(fill="x", padx=10, pady=5)

        self.generate_btn = ttk.Button(frame_top, text="Сгенерировать задачу", command=self.generate_task)
        self.generate_btn.pack(side="left", padx=5)

        self.task_var = tk.StringVar()
        self.task_label = ttk.Label(frame_top, textvariable=self.task_var, font=("Arial", 12, "bold"), foreground="blue")
        self.task_label.pack(side="left", padx=20)

        frame_filter = ttk.LabelFrame(self.root, text="Фильтр по типу", padding=10)
        frame_filter.pack(fill="x", padx=10, pady=5)

        ttk.Label(frame_filter, text="Тип задачи:").pack(side="left", padx=5)
        self.filter_var = tk.StringVar(value="все")
        filter_combo = ttk.Combobox(frame_filter, textvariable=self.filter_var, 
                                    values=["все", "учёба", "спорт", "работа"], 
                                    state="readonly", width=15)
        filter_combo.pack(side="left", padx=5)
        filter_combo.bind("<<ComboboxSelected>>", self.apply_filter)

        self.counter_label = ttk.Label(frame_filter, text="Всего: 0")
        self.counter_label.pack(side="right", padx=10)

        frame_history = ttk.LabelFrame(self.root, text="История задач", padding=10)
        frame_history.pack(fill="both", expand=True, padx=10, pady=5)

        history_frame = ttk.Frame(frame_history)
        history_frame.pack(fill="both", expand=True)

        self.history_listbox = tk.Listbox(history_frame, height=15, font=("Courier", 9))
        scrollbar = ttk.Scrollbar(history_frame, orient="vertical", command=self.history_listbox.yview)
        self.history_listbox.configure(yscrollcommand=scrollbar.set)
        self.history_listbox.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        frame_add = ttk.LabelFrame(self.root, text="Добавить новую задачу", padding=10)
        frame_add.pack(fill="x", padx=10, pady=5)

        ttk.Label(frame_add, text="Название:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.new_task_entry = ttk.Entry(frame_add, width=35)
        self.new_task_entry.grid(row=0, column=1, padx=5, pady=5)
        self.new_task_entry.bind('<Return>', lambda e: self.add_custom_task())

        ttk.Label(frame_add, text="Тип:").grid(row=0, column=2, padx=5, pady=5, sticky="e")
        self.new_type_combo = ttk.Combobox(frame_add, values=["учёба", "спорт", "работа"], 
                                           state="readonly", width=12)
        self.new_type_combo.grid(row=0, column=3, padx=5, pady=5)
        self.new_type_combo.set("учёба")

        self.add_btn = ttk.Button(frame_add, text="Добавить", command=self.add_custom_task)
        self.add_btn.grid(row=0, column=4, padx=10, pady=5)

        self.clear_btn = ttk.Button(frame_add, text="Очистить историю", command=self.clear_history)
      self.clear_btn.grid(row=0, column=5, padx=10, pady=5)

    def load_history(self):
        if os.path.exists("tasks.json"):
            try:
                with open("tasks.json", "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.history = data.get("history", [])
            except Exception as e:
                print(f"Ошибка загрузки: {e}")
                self.history = []
        else:
            self.history = []

    def save_history(self):
        try:
            with open("tasks.json", "w", encoding="utf-8") as f:
                json.dump({"history": self.history}, f, ensure_ascii=False, indent=2)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить историю: {e}")

    def get_all_tasks(self):
        all_tasks = DEFAULT_TASKS.copy()
        for item in self.history:
            task_data = {"name": item["task"], "type": item["type"]}
            if task_data not in all_tasks:
                all_tasks.append(task_data)
        return all_tasks

    def generate_task(self):
        all_tasks = self.get_all_tasks()
        
        if not all_tasks:
            messagebox.showwarning("Нет задач", "Добавьте хотя бы одну задачу!")
            return

        selected = random.choice(all_tasks)
        task_name = selected["name"]
        task_type = selected["type"]

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.history.append({
            "task": task_name,
            "type": task_type,
            "timestamp": now
        })
        self.save_history()

        self.task_var.set(f"{task_name} [{task_type}]")
        self.apply_filter()

    def add_custom_task(self):
        task_name = self.new_task_entry.get().strip()
        task_type = self.new_type_combo.get()

        if not task_name:
            messagebox.showerror("Ошибка", "Название задачи не может быть пустым!")
            return

        if len(task_name) > 100:
            messagebox.showerror("Ошибка", "Название задачи слишком длинное (макс. 100 символов)!")
            return

        for item in self.history:
            if item["task"].lower() == task_name.lower() and item["type"] == task_type:
                if not messagebox.askyesno("Повтор", "Такая задача уже есть в истории. Всё равно добавить?"):
                    return

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.history.append({
            "task": task_name,
            "type": task_type,
            "timestamp": now
        })
        self.save_history()
        self.new_task_entry.delete(0, tk.END)
        self.apply_filter()
        messagebox.showinfo("Успех", f"Задача '{task_name}' добавлена!")

    def apply_filter(self, event=None):
        self.current_filter = self.filter_var.get()
        if self.current_filter == "все":
            self.filtered_history = self.history.copy()
        else:
            self.filtered_history = [item for item in self.history if item["type"] == self.current_filter]
        self.update_history_listbox()
        self.update_counter()

    def update_counter(self):
        total = len(self.filtered_history)
        self.counter_label.config(text=f"Показано: {total}")

    def update_history_listbox(self):
        self.history_listbox.delete(0, tk.END)
        if not self.filtered_history:
            self.history_listbox.insert(tk.END, "Нет задач для отображения")
        else:
            for item in reversed(self.filtered_history):
                display = f"{item['timestamp']}  |  {item['task']:<30}  |  [{item['type']}]"
                self.history_listbox.insert(tk.END, display)

    def clear_history(self):
        if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите очистить всю историю?\nЭто действие нельзя отменить!"):
            self.history = []
            self.save_history()
            self.apply_filter()
            self.task_var.set("")
          messagebox.showinfo("Готово", "История очищена")

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskGenerator(root)
    root.mainloop()
