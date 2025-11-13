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
        # Xoá nội dung của các ô Text hiển thị kết quả và lịch sử
        try:
            self.hc_result.delete('1.0', tk.END)
            self.hc_history.delete('1.0', tk.END)
            self.gwo_result.delete('1.0', tk.END)
            self.gwo_history.delete('1.0', tk.END)
        except Exception:
            # Nếu widget chưa được tạo hoặc có lỗi, bỏ qua
            return

    def _run_single_algo(self, method_name, algo_class, result_text, history_text, names, values, weights, max_w, max_iter):
        """
        Worker chạy trong thread phụ: khởi tạo thuật toán, gọi .solve(), tính tổng giá trị/trọng lượng
        và gửi kết quả về GUI thread qua self.root.after.
        """
        try:
            # Khởi tạo thuật toán; constructor các thuật toán phù hợp với thứ tự:
            # (item_names, item_values, item_weights, knapsack_capacity, max_iterations)
            algo = algo_class(names, values, weights, max_w, max_iter)

            selected_items, history, exec_time = algo.solve()

            # Lấy tổng giá trị và trọng lượng từ nghiệm tốt nhất lưu trong đối tượng thuật toán
            try:
                total_val, total_w = algo._calculate_fitness(algo.best_solution)
            except Exception:
                # Dự phòng: tính lại bằng danh sách selected_items
                total_val = 0
                total_w = 0
                name_to_index = {n: i for i, n in enumerate(names)}
                for n in selected_items:
                    idx = name_to_index.get(n)
                    if idx is not None:
                        total_val += values[idx]
                        total_w += weights[idx]

            # Đẩy kết quả về GUI thread một cách an toàn
            self.root.after(0, lambda: self._update_gui(
                method_name, selected_items, history, exec_time, total_val, total_w, max_w,
                names, values, weights, result_text, history_text
            ))

        except Exception as e:
            # Nếu có lỗi trong thread, hiển thị messagebox trên GUI thread
            self.root.after(0, lambda: messagebox.showerror(f"Lỗi {method_name}", str(e)))

    def _update_gui(self, method_name, selected, hist, t, total_val, total_w, max_w, names, values, weights, result_text, history_text):
        """
        Cập nhật các widget Text trên GUI (chạy trên main thread).
        - result_text: Text widget để in kết quả tóm tắt
        - history_text: Text widget để in lịch sử iteration
        """
        try:
            # Cập nhật phần kết quả tóm tắt
            result_text.config(state='normal')
            result_text.delete('1.0', tk.END)
            header = f"{method_name} - Kết quả\n"
            meta = f"Tổng giá trị: {total_val}    Tổng trọng lượng: {total_w} / {max_w}\n"
            time_line = f"Thời gian: {t:.4f} giây\n"
            items_line = "Chọn: " + (', '.join(selected) if selected else 'Không có') + "\n"
            result_text.insert(tk.END, header + meta + time_line + items_line)
            result_text.config(state='disabled')

            # Cập nhật lịch sử
            history_text.config(state='normal')
            history_text.delete('1.0', tk.END)
            if hist:
                if isinstance(hist, list):
                    history_text.insert(tk.END, "\n".join(hist))
                else:
                    history_text.insert(tk.END, str(hist))
            history_text.config(state='disabled')

        except Exception as e:
            # Hiển thị lỗi nhỏ trong messagebox nếu cập nhật GUI thất bại
            messagebox.showerror("Lỗi cập nhật GUI", str(e))
    def _check_running_threads(self):
        pass 
    def start_parallel_run(self):

        pass 
