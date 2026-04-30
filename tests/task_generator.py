import unittest
import json
import os
import tempfile
from datetime import datetime
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import TaskGenerator
import tkinter as tk

class TestTaskGenerator(unittest.TestCase):
    
    def setUp(self):
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.json')
        self.temp_file.close()
        self.original_tasks_file = "tasks.json"
        
        self.root = tk.Tk()
        self.app = TaskGenerator(self.root)
        
        self.app.save_history = lambda: None
    
    def tearDown(self):
        self.root.destroy()
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)
    
    def test_add_custom_task_empty_name(self):
        self.app.new_task_entry.delete(0, tk.END)
        self.app.new_task_entry.insert(0, "   ")
        old_len = len(self.app.history)
        import tkinter.messagebox
        original_showerror = tkinter.messagebox.showerror
        tkinter.messagebox.showerror = lambda *args: None
        try:
            self.app.add_custom_task()
        finally:
            tkinter.messagebox.showerror = original_showerror
        self.assertEqual(len(self.app.history), old_len)
    
    def test_add_custom_task_valid(self):
        self.app.new_task_entry.delete(0, tk.END)
        self.app.new_task_entry.insert(0, "Тестовая задача")
        self.app.new_type_combo.set("учёба")
        old_len = len(self.app.history)
        
        import tkinter.messagebox
        original_showinfo = tkinter.messagebox.showinfo
        tkinter.messagebox.showinfo = lambda *args: None
        try:
            self.app.add_custom_task()
        finally:
            tkinter.messagebox.showinfo = original_showinfo
            
        self.assertEqual(len(self.app.history), old_len + 1)
        self.assertEqual(self.app.history[-1]["task"], "Тестовая задача")
        self.assertEqual(self.app.history[-1]["type"], "учёба")
    
    def test_generate_task(self):
        old_len = len(self.app.history)
        self.app.generate_task()
        self.assertEqual(len(self.app.history), old_len + 1)
        self.assertTrue("task" in self.app.history[-1])
        self.assertTrue("timestamp" in self.app.history[-1])
    
    def test_filter_by_type(self):
        self.app.history = [
            {"task": "Задача 1", "type": "учёба", "timestamp": "2024-01-01 10:00:00"},
            {"task": "Задача 2", "type": "спорт", "timestamp": "2024-01-01 11:00:00"},
            {"task": "Задача 3", "type": "работа", "timestamp": "2024-01-01 12:00:00"},
        ]
        self.app.filter_var.set("учёба")
        self.app.apply_filter()
        self.assertEqual(len(self.app.filtered_history), 1)
        self.assertEqual(self.app.filtered_history[0]["type"], "учёба")
    
    def test_clear_history(self):
        self.app.history = [{"task": "Тест", "type": "учёба", "timestamp": "2024-01-01 10:00:00"}]
        self.app.clear_history()
        self.assertEqual(len(self.app.history), 0)
    
    def test_get_all_tasks(self):
        self.app.history = [
            {"task": "Новая задача", "type": "учёба", "timestamp": "2024-01-01 10:00:00"}
        ]
        all_tasks = self.app.get_all_tasks()
        self.assertTrue(len(all_tasks) > len(self.app.history))
        self.assertTrue(any(t["name"] == "Новая задача" for t in all_tasks))
    
    def test_save_and_load_json(self):
        test_history = [
            {"task": "Тест 1", "type": "учёба", "timestamp": "2024-01-01 10:00:00"},
            {"task": "Тест 2", "type": "спорт", "timestamp": "2024-01-01 11:00:00"}
        ]
        self.app.history = test_history
        self.app.save_history()
        
        new_app = TaskGenerator(self.root)
        new_app.load_history()
        self.assertEqual(len(new_app.history), len(test_history))

if __name__ == "__main__":
    unittest.main()
