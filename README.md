# DO_AN_AI - Knapsack Optimization

Ứng dụng tối ưu hóa bài toán Knapsack (0/1) sử dụng hai thuật toán: **Hill Climbing** và **Grey Wolf Optimizer (GWO)**.

## Tính năng

- ✅ Chạy song song 2 thuật toán tối ưu hóa: Hill Climbing và Grey Wolf Optimizer
- ✅ Giao diện đồ họa thân thiện với ttkbootstrap
- ✅ Hỗ trợ nhiều dataset khác nhau (500, 1000 items, và custom)
- ✅ Hiển thị kết quả chi tiết và lịch sử tối ưu hóa
- ✅ **Biểu đồ so sánh trực quan** giữa 2 thuật toán

## Cài đặt

### 1. Yêu cầu hệ thống
- Python 3.7 trở lên
- pip

### 2. Cài đặt dependencies

```bash
pip install -r requirements.txt
```

Hoặc cài đặt thủ công:

```bash
pip install ttkbootstrap matplotlib
```

## Cách sử dụng

### 1. Chạy ứng dụng

```bash
python main.py
```

### 2. Các bước sử dụng

1. **Chọn Dataset**: Chọn file dữ liệu từ dropdown (dataset_500.csv, dataset_1000.csv, hoặc products.csv)
2. **Tải Dữ Liệu**: Click "Tải Dữ Liệu" để load dataset
3. **Thiết lập tham số**:
   - **Khối lượng tối đa**: Dung lượng ba lô (mặc định: 5000)
   - **Số lần lặp**: Số vòng lặp cho thuật toán (mặc định: 100)
4. **Chạy Song Song**: Click "Chạy Song Song" để thực thi cả 2 thuật toán
5. **Xem Biểu Đồ**: Click "📊 So Sánh Biểu Đồ" để xem so sánh trực quan

### 3. Hiểu kết quả

- **Panel Hill Climbing**: Hiển thị kết quả và lịch sử của thuật toán Hill Climbing
- **Panel Grey Wolf Optimizer**: Hiển thị kết quả và lịch sử của GWO
- **Biểu Đồ So Sánh**: Hiển thị đường cong tối ưu hóa theo từng iteration, so sánh hiệu suất 2 thuật toán

## Cấu trúc Project

```
DO_AN_AI/
├── main.py                 # Entry point
├── ui.py                   # Giao diện người dùng
├── knapsack_base.py        # Abstract base class cho các thuật toán
├── knapsack_hc.py          # Hill Climbing implementation
├── knapsack_gwo.py         # Grey Wolf Optimizer implementation
├── data_handler.py         # Xử lý load dữ liệu CSV
├── dataset_500.csv         # Dataset 500 items
├── dataset_1000.csv        # Dataset 1000 items
├── products.csv            # Dataset custom
├── requirements.txt        # Python dependencies
└── README.md               # Tài liệu này
```

## Thuật toán

### Hill Climbing
- Thuật toán leo đồi cơ bản
- Bắt đầu từ nghiệm ngẫu nhiên
- Tìm kiếm lân cận tốt hơn trong mỗi iteration
- Nhanh nhưng dễ rơi vào local optimum

### Grey Wolf Optimizer (GWO)
- Mô phỏng hành vi săn mồi của bầy sói xám
- Sử dụng quần thể 30 con sói
- Alpha, Beta, Delta dẫn đầu quần thể
- Khả năng thoát local optimum tốt hơn

## Dataset Format

File CSV cần có format:

```csv
Tên,Giá trị,Khối lượng
Item1,100,50
Item2,200,75
...
```

## Khắc phục sự cố

### Lỗi "ModuleNotFoundError"
```bash
pip install -r requirements.txt
```

### Biểu đồ không hiển thị
- Đảm bảo đã chạy cả 2 thuật toán trước khi click "So Sánh Biểu Đồ"
- Kiểm tra matplotlib đã được cài đặt

### GUI không mở
- Kiểm tra ttkbootstrap đã được cài đặt
- Đảm bảo có môi trường đồ họa (không phải SSH headless)

## Tác giả

Đồ án AI - 2025

## License

MIT License