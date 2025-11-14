import ttkbootstrap as ttkb
from ui import KnapsackApp 

if __name__ == "__main__":
    """Điểm khởi chạy chính của ứng dụng."""
    root = ttkb.Window(themename="darkly") 
    app = KnapsackApp(root)
    root.mainloop()