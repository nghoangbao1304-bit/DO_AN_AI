# Tên file: knapsack_gwo.py

import random
import math
import time
from typing import List, Tuple
from knapsack_base import KnapsackAlgorithmBase

class GreyWolfOptimizer(KnapsackAlgorithmBase):
    """
    Giải bài toán Knapsack bằng thuật toán Tối ưu hóa Bầy sói Xám (GWO).

    Thuật toán này được chuyển đổi từ không gian liên tục (của GWO gốc)
    sang không gian nhị phân (của Knapsack 0/1) bằng hàm sigmoid.
    """

    def __init__(
        self,
        item_names: List[str],
        item_values: List[int],
        item_weights: List[int],
        knapsack_capacity: int,
        max_iterations: int = 100,
        num_wolves: int = 30  # Tham số này được truyền từ ui.py
    ):
        """Khởi tạo thuật toán GWO."""
        super().__init__(item_names, item_values, item_weights, knapsack_capacity, max_iterations)
        self._num_wolves = num_wolves

        # Vị trí (liên tục) của bầy sói
        self.pack_positions: List[List[float]] = []
        
        # Giải pháp (nhị phân) tương ứng với vị trí
        self.pack_solutions: List[List[int]] = []
        
        # Fitness của mỗi giải pháp
        self.pack_fitnesses: List[int] = []

        # Các con sói đầu đàn (Alpha, Beta, Delta)
        # Chúng ta lưu cả vị trí (pos), giải pháp (solution) và fitness
        self.alpha_pos: List[float] = [0.0] * self._n
        self.alpha_solution: List[int] = [0] * self._n
        self.alpha_fitness: int = 0
        
        self.beta_pos: List[float] = [0.0] * self._n
        self.beta_solution: List[int] = [0] * self._n
        self.beta_fitness: int = 0
        
        self.delta_pos: List[float] = [0.0] * self._n
        self.delta_solution: List[int] = [0] * self._n
        self.delta_fitness: int = 0

    def _sigmoid(self, x: float) -> float:
        """Hàm Sigmoid để chuyển đổi giá trị liên tục sang xác suất (0, 1)."""
        # Giới hạn giá trị x để tránh tràn số (Overflow)
        if x < -100: return 0.0
        if x > 100: return 1.0
        return 1.0 / (1.0 + math.exp(-x))

    def _discretize(self, position: List[float]) -> List[int]:
        """
        Chuyển đổi một vector vị trí (liên tục) thành một giải pháp (nhị phân).
        Sử dụng hàm sigmoid để lấy xác suất.
        """
        solution = [0] * self._n
        for i in range(self._n):
            prob = self._sigmoid(position[i])
            if random.random() < prob:
                solution[i] = 1
        return solution

    def _init_population(self):
        """Khởi tạo quần thể bầy sói."""
        self.pack_positions = []
        self.pack_solutions = []
        self.pack_fitnesses = []

        for _ in range(self._num_wolves):
            # Khởi tạo vị trí liên tục ngẫu nhiên (ví dụ: trong khoảng [-5, 5])
            pos = [random.uniform(-5, 5) for _ in range(self._n)]
            
            # Tạo giải pháp nhị phân từ vị trí
            sol = self._discretize(pos)
            
            # Tính fitness (sử dụng hàm _fitness_value từ base class
            # để đảm bảo các giải pháp không hợp lệ (quá tải) có fitness = 0)
            fitness = self._fitness_value(sol)

            self.pack_positions.append(pos)
            self.pack_solutions.append(sol)
            self.pack_fitnesses.append(fitness)

    def _update_leaders(self):
        """Cập nhật 3 con sói đầu đàn (Alpha, Beta, Delta) dựa trên fitness."""
        
        # Tạo danh sách (fitness, index) và sắp xếp giảm dần
        sorted_wolves = sorted(
            enumerate(self.pack_fitnesses), 
            key=lambda x: x[1], 
            reverse=True
        )

        # Lấy Alpha (tốt nhất)
        alpha_idx = sorted_wolves[0][0]
        self.alpha_fitness = self.pack_fitnesses[alpha_idx]
        self.alpha_solution = self.pack_solutions[alpha_idx][:]
        self.alpha_pos = self.pack_positions[alpha_idx][:]

        # Lấy Beta (tốt nhì)
        beta_idx = sorted_wolves[1][0]
        self.beta_fitness = self.pack_fitnesses[beta_idx]
        self.beta_solution = self.pack_solutions[beta_idx][:]
        self.beta_pos = self.pack_positions[beta_idx][:]

        # Lấy Delta (tốt ba)
        delta_idx = sorted_wolves[2][0]
        self.delta_fitness = self.pack_fitnesses[delta_idx]
        self.delta_solution = self.pack_solutions[delta_idx][:]
        self.delta_pos = self.pack_positions[delta_idx][:]


    def solve(self) -> Tuple[List[str], List[str], float]:
        """Thực thi thuật toán Grey Wolf Optimizer."""
        start_time = time.time()
        
        # 1. Khởi tạo quần thể
        self._init_population()
        self._update_leaders()

        # Lưu lại giải pháp tốt nhất toàn cục
        self.best_solution = self.alpha_solution[:]
        self.best_value = self.alpha_fitness
        self.history = []

        # 2. Vòng lặp chính
        for iteration in range(self._max_iterations):
            
            # Tham số 'a' giảm tuyến tính từ 2 về 0 (điều khiển khám phá/khai thác)
            a = 2.0 - iteration * (2.0 / self._max_iterations)

            new_positions = [] # Lưu vị trí mới để cập nhật đồng bộ
            
            # Cập nhật vị trí của từng con sói (Omega)
            for i in range(self._num_wolves):
                current_pos = self.pack_positions[i]
                new_pos_dim = [] # Vị trí mới cho từng chiều (item)

                for j in range(self._n): # Từng chiều (tương ứng với mỗi vật phẩm)
                    # === Cập nhật theo Alpha ===
                    r1, r2 = random.random(), random.random()
                    A1 = 2.0 * a * r1 - a
                    C1 = 2.0 * r2
                    D_alpha = abs(C1 * self.alpha_pos[j] - current_pos[j])
                    X1 = self.alpha_pos[j] - A1 * D_alpha

                    # === Cập nhật theo Beta ===
                    r1, r2 = random.random(), random.random()
                    A2 = 2.0 * a * r1 - a
                    C2 = 2.0 * r2
                    D_beta = abs(C2 * self.beta_pos[j] - current_pos[j])
                    X2 = self.beta_pos[j] - A2 * D_beta

                    # === Cập nhật theo Delta ===
                    r1, r2 = random.random(), random.random()
                    A3 = 2.0 * a * r1 - a
                    C3 = 2.0 * r2
                    D_delta = abs(C3 * self.delta_pos[j] - current_pos[j])
                    X3 = self.delta_pos[j] - A3 * D_delta

                    # Vị trí mới là trung bình của 3 hướng
                    new_pos_j = (X1 + X2 + X3) / 3.0
                    new_pos_dim.append(new_pos_j)
                
                new_positions.append(new_pos_dim)
            
            # 3. Cập nhật đồng bộ bầy sói (vị trí, giải pháp, fitness)
            for i in range(self._num_wolves):
                self.pack_positions[i] = new_positions[i][:]
                
                # Chuyển vị trí mới thành giải pháp nhị phân
                new_solution = self._discretize(self.pack_positions[i])
                new_fitness = self._fitness_value(new_solution)
                
                # Cập nhật giải pháp và fitness của con sói
                # (Lưu ý: GWO gốc thường không so sánh trực tiếp,
                # nhưng trong B-GWO, việc này giúp giữ lại các giải pháp tốt)
                # Chúng ta sẽ cập nhật chúng và để _update_leaders sắp xếp lại
                self.pack_solutions[i] = new_solution[:]
                self.pack_fitnesses[i] = new_fitness

            # 4. Cập nhật lại 3 con đầu đàn
            self._update_leaders()

            # 5. Cập nhật giải pháp tốt nhất toàn cục
            if self.alpha_fitness > self.best_value:
                self.best_value = self.alpha_fitness
                self.best_solution = self.alpha_solution[:]

            # Ghi lại lịch sử
            self.history.append(f"Lần {iteration}: Best Value={self.best_value}")

        # 6. Kết thúc
        self.exec_time = time.time() - start_time
        
        selected_items = [self._item_names[i] for i, v in enumerate(self.best_solution) if v == 1]
        
        return selected_items, self.history, self.exec_time