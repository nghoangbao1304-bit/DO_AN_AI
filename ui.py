import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, Text 
from knapsack_hc import HillClimbing 
from knapsack_gwo import GreyWolfOptimizer
from data_handler import load_knapsack_data_from_csv 
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

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
        
        # Lưu kết quả của các thuật toán để vẽ biểu đồ
        self.hc_algo = None
        self.gwo_algo = None
            
        self.create_widgets()

    def create_widgets(self):
        """Thiết lập tất cả các thành phần giao diện."""
        # ========== FRAME TRÊN (Điều khiển) ==========
        top_frame = ttk.Frame(self.root)
        top_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(top_frame, text="Khối lượng tối đa:").pack(side="left", padx=5)
        self.max_w_entry = ttk.Entry(top_frame, width=8)
        self.max_w_entry.pack(side="left", padx=5)
        self.max_w_entry.insert(0, "5000") 

        ttk.Label(top_frame, text="Số lần lặp:").pack(side="left", padx=5)
        self.iter_entry = ttk.Entry(top_frame, width=8)
        self.iter_entry.insert(0, "100")
        self.iter_entry.pack(side="left", padx=5)

        self.run_button = ttk.Button(top_frame, text="Chạy Song Song", command=self.start_parallel_run)
        self.run_button.pack(side="left", padx=10)
        
        ttk.Label(top_frame, text="Chọn Dataset:").pack(side="left", padx=(10, 5))
        self.data_combobox = ttk.Combobox(
            top_frame, 
            values=self.data_files, 
            state="readonly", 
            width=22
        )
        self.data_combobox.set(self.data_files[0]) 
        self.data_combobox.pack(side="left", padx=5)
        
        ttk.Button(top_frame, text="Tải Dữ Liệu", command=self.load_selected_data).pack(side="left", padx=5)
        
        ttk.Button(top_frame, text="Xóa kết quả", command=self.clear_results).pack(side="left", padx=10)
        
        ttk.Button(top_frame, text="📊 So Sánh Biểu Đồ", command=self.show_comparison_chart).pack(side="left", padx=10)

        # ========== TABLE (Dữ liệu vật phẩm) ==========
        columns = ("Tên", "Giá trị", "Khối lượng")
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings", height=10)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=150)
        self.tree.pack(fill="x", padx=10, pady=5)
        
        # ========== FRAME DƯỚI (Kết quả & Lịch sử) ==========
        bottom_frame = ttk.Frame(self.root)
        bottom_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        hc_frame = ttk.Frame(bottom_frame)
        hc_frame.pack(side="left", fill="both", expand=True, padx=5)
        ttk.Label(hc_frame, text="HILL CLIMBING", font=("Arial", 12, "bold")).pack(pady=5)
        self.hc_result = Text(hc_frame, height=8, bg="white", fg="black", font=("Consolas", 10))
        self.hc_result.pack(fill="x", pady=5)
        ttk.Label(hc_frame, text="LỊCH SỬ HC", font=("Arial", 10, "bold")).pack(pady=5)
        self.hc_history = Text(hc_frame, bg="white", fg="black", font=("Consolas", 10))
        self.hc_history.pack(fill="both", expand=True, pady=5)
        gwo_frame = ttk.Frame(bottom_frame)
        gwo_frame.pack(side="left", fill="both", expand=True, padx=5)
        ttk.Label(gwo_frame, text="GREY WOLF OPTIMIZER", font=("Arial", 12, "bold")).pack(pady=5)
        self.gwo_result = Text(gwo_frame, height=8, bg="white", fg="black", font=("Consolas", 10))
        self.gwo_result.pack(fill="x", pady=5)
        ttk.Label(gwo_frame, text="LỊCH SỬ GWO", font=("Arial", 10, "bold")).pack(pady=5)
        self.gwo_history = Text(gwo_frame, bg="white", fg="black", font=("Consolas", 10))
        self.gwo_history.pack(fill="both", expand=True, pady=5)
        
        try:
            self.load_data_and_populate_tree(self.data_files[0])
        except Exception as e:
            messagebox.showerror("Lỗi Tải Dữ Liệu Mặc Định", f"Không thể tải '{self.data_files[0]}'.\n{e}")

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
            
        self.clear_results()
        self.root.title(f"Knapsack Optimization - {filename}")


    def clear_results(self):
        """Xóa tất cả kết quả và lịch sử."""
        self.hc_result.delete(1.0, "end"); self.gwo_result.delete(1.0, "end")
        self.hc_history.delete(1.0, "end"); self.gwo_history.delete(1.0, "end")
        self.hc_algo = None
        self.gwo_algo = None

    
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

            self.root.after(0, self._update_gui, method_name, selected, hist, t, total_val, total_w, max_w, names, values, weights, result_text, history_text, algo_instance)
            
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror(f"Lỗi {method_name}", str(e)))
            self.root.after(0, self._check_running_threads) 

    def _update_gui(self, method_name, selected, hist, t, total_val, total_w, max_w, names, values, weights, result_text, history_text, algo_instance):
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
        
        # Lưu instance để vẽ biểu đồ
        if method_name == "Hill Climbing":
            self.hc_algo = algo_instance
        elif method_name == "Grey Wolf Optimizer":
            self.gwo_algo = algo_instance
        
        self.root.update_idletasks()
        
        self._check_running_threads()

    def _check_running_threads(self):
        """Kiểm tra số lượng luồng đang chạy và bật lại nút Run."""
        if threading.active_count() <= 2: 
             self.run_button.config(state="normal")
             
    def start_parallel_run(self):
        """Khởi tạo hai luồng (Thread) để chạy Hill Climbing và GWO song song."""
        if not self.items: 
            messagebox.showerror("Lỗi", "Vui lòng tải dữ liệu trước.")
            return

        try:
            max_w = int(self.max_w_entry.get())
            max_iter = int(self.iter_entry.get())
        except ValueError:
            messagebox.showerror("Lỗi", "Tham số 'Khối lượng tối đa' hoặc 'Số lần lặp' không hợp lệ!")
            return

        names, values, weights = self.items_data['names'], self.items_data['values'], self.items_data['weights']
        
        if not names: 
            messagebox.showerror("Lỗi", "Dữ liệu vật phẩm bị rỗng, vui lòng tải lại file.")
            return
            
        self.run_button.config(state="disabled") 
        self.clear_results()

        thread_hc = threading.Thread(
            target=self._run_single_algo, 
            args=("Hill Climbing", HillClimbing, self.hc_result, self.hc_history, names, values, weights, max_w, max_iter)
        )
        thread_hc.start()

        thread_gwo = threading.Thread(
            target=self._run_single_algo, 
            args=("Grey Wolf Optimizer", GreyWolfOptimizer, self.gwo_result, self.gwo_history, names, values, weights, max_w, max_iter)
        )
        thread_gwo.start()

    def show_comparison_chart(self):
        """Hiển thị biểu đồ so sánh hai thuật toán."""
        if self.hc_algo is None or self.gwo_algo is None:
            messagebox.showwarning("Chưa có dữ liệu", "Vui lòng chạy cả hai thuật toán trước khi xem biểu đồ so sánh!")
            return
        
        # Tạo cửa sổ mới cho biểu đồ
        chart_window = tk.Toplevel(self.root)
        chart_window.title("Biểu Đồ So Sánh Thuật Toán")
        chart_window.geometry("1000x600")
        
        # Tạo figure matplotlib
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Vẽ đường cho Hill Climbing
        iterations_hc = range(len(self.hc_algo.history_values))
        ax.plot(iterations_hc, self.hc_algo.history_values, 
                label='Hill Climbing', marker='o', markersize=3, linewidth=2, color='blue')
        
        # Vẽ đường cho Grey Wolf Optimizer
        iterations_gwo = range(len(self.gwo_algo.history_values))
        ax.plot(iterations_gwo, self.gwo_algo.history_values, 
                label='Grey Wolf Optimizer', marker='s', markersize=3, linewidth=2, color='red')
        
        # Thiết lập labels và title
        ax.set_xlabel('Generation (Thế hệ)', fontsize=12)
        ax.set_ylabel('Fitness (Giá trị thích nghi)', fontsize=12)
        ax.set_title('So Sánh Hiệu Suất: Hill Climbing vs Grey Wolf Optimizer', fontsize=14, fontweight='bold')
        ax.legend(loc='best', fontsize=11)
        ax.grid(True, alpha=0.3)
        
        # Thêm thông tin cuối cùng
        final_hc = self.hc_algo.best_value
        final_gwo = self.gwo_algo.best_value
        time_hc = self.hc_algo.exec_time
        time_gwo = self.gwo_algo.exec_time
        
        info_text = f"Kết quả cuối:\nHC: {final_hc} ({time_hc:.4f}s) | GWO: {final_gwo} ({time_gwo:.4f}s)"
        ax.text(0.02, 0.98, info_text, transform=ax.transAxes, 
                verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5),
                fontsize=10)
        
        # Nhúng biểu đồ vào Tkinter window
        canvas = FigureCanvasTkAgg(fig, master=chart_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Thêm nút đóng
        close_btn = ttk.Button(chart_window, text="Đóng", command=chart_window.destroy)
        close_btn.pack(pady=10)