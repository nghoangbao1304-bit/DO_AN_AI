# File: ui.py (Do Dev 1 tạo ban đầu)

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, Text
from knapsack_hc import HillClimbing
from knapsack_gwo import GreyWolfOptimizer
from data_handler import load_knapsack_data_from_csv

import threading
from typing import List, Tuple

class KnapsackApp:
    """Class chính quản lý giao diện người dùng và điều phối các thuật toán tối ưu."""
    def __init__(self, root):
        """Khởi tạo ứng dụng Knapsack."""
        self.root = root
        self.root.title("Knapsack Optimization - Hill Climbing & GWO Song Song")
        self.root.geometry("1400x800")

        self.data_files = [
            'dataset_500.csv',
            'dataset_1000.csv',
            'products.csv'
        ]

        self.items_data = {'names': [], 'values': [], 'weights': []}
        self.items: List[Tuple[str, int, int]] = []

        self.create_widgets()

    def create_widgets(self):
 
        self.max_w_entry = ttk.Entry(self.root)
        self.iter_entry = ttk.Entry(self.root)
        self.run_button = ttk.Button(self.root, text="Chạy (Chưa gán lệnh)") 
        
        self.data_combobox = ttk.Combobox(self.root, values=self.data_files)
        self.tree = ttk.Treeview(self.root)
        
        self.hc_result = Text(self.root, height=8)
        self.hc_history = Text(self.root)
        self.gwo_result = Text(self.root, height=8)
        self.gwo_history = Text(self.root)
       
        try:
            self.load_data_and_populate_tree(self.data_files[0])
        except Exception as e:
            pass 
    def load_selected_data(self):
        pass 
    def load_data_and_populate_tree(self, filename: str):
        pass 
    def clear_results(self):
        """Xóa tất cả kết quả và lịch sử."""
        self.hc_result.delete(1.0, "end"); self.gwo_result.delete(1.0, "end")
        self.hc_history.delete(1.0, "end"); self.gwo_history.delete(1.0, "end")

    def _run_single_algo(self, method_name, algo_class, result_text, history_text, names, values, weights, max_w, max_iter):
        """Hàm chạy thuật toán trong một luồng riêng biệt (luồng worker)."""
        try:
            if method_name == "Grey Wolf Optimizer":
                 algo_instance = algo_class(names, values, weights, max_w, max_iter, num_wolves=30)
            else:
                 algo_instance = algo_class(names, values, weights, max_w, max_iter)

            selected, hist, t = algo_instance.solve()

            total_val = sum(values[i] for i, n in enumerate(names) if n in selected)
            total_w = sum(weights[i] for i, n in enumerate(names) if n in selected)

            self.root.after(0, self._update_gui, method_name, selected, hist, t, total_val, total_w, max_w, names, values, weights, result_text, history_text)

        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror(f"Lỗi {method_name}", str(e)))
            self.root.after(0, self._check_running_threads) # Gọi hàm của Dev 3

    def _update_gui(self, method_name, selected, hist, t, total_val, total_w, max_w, names, values, weights, result_text, history_text):
        """Cập nhật giao diện an toàn trên luồng chính của Tkinter."""
        result_text.delete(1.0, "end")
        history_text.delete(1.0, "end")

        result_text.insert("end", f"Thuật toán: {method_name}\n")
        result_text.insert("end", f"Tổng giá trị: {total_val}\nTổng khối lượng: {total_w}/{max_w}\n")
        result_text.insert("end", f"Số vật phẩm được chọn: {len(selected)}\nThời gian: {t:.4f}s\n\n")

        for i, name in enumerate(selected, 1):
            idx = names.index(name)
            result_text.insert("end", f"{i:2d}. {name} ({values[idx]} - {weights[idx]})\n")

        history_text.insert("end", "\n".join(hist))

        self.root.update_idletasks()

        self._check_running_threads() # Gọi hàm của Dev 3
    def _check_running_threads(self):
        pass 
    def start_parallel_run(self):

        pass 
    def load_selected_data(self):
        """Lấy tên file từ Combobox và tải dữ liệu."""
        filename = self.data_combobox.get()
        if not filename:
            messagebox.showwarning("Chưa chọn file", "Vui lòng chọn một dataset từ danh sách.")
            return

        try:
            self.load_data_and_populate_tree(filename)
        except Exception as e:
            messagebox.showerror("Lỗi Tải File", f"Không thể tải file: {filename}\n{e}")

    def load_data_and_populate_tree(self, filename: str):
        """Tải dữ liệu từ file CSV được chỉ định và hiển thị lên Treeview."""
        self.items_data = load_knapsack_data_from_csv(filename)

        if not self.items_data['names']:
             messagebox.showerror("Lỗi", f"Không tìm thấy dữ liệu hoặc file '{filename}' bị lỗi.")
             self.items = []
             return

        self.items = list(zip(self.items_data['names'], self.items_data['values'], self.items_data['weights']))

        for item in self.tree.get_children():
            self.tree.delete(item)

        for name, val, w in self.items:
            self.tree.insert("", "end", values=(name, val, w))

        self.clear_results() # Gọi hàm của Dev 4
        self.root.title(f"Knapsack Optimization - {filename}")