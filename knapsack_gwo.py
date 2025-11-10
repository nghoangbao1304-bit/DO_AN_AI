import random
import math
import time
from typing import List, Tuple
from knapsack_base import KnapsackAlgorithmBase

class GreyWolfOptimizer(KnapsackAlgorithmBase):
    """Giải bài toán Knapsack bằng thuật toán Grey Wolf Optimizer (GWO)."""

    def __init__(self, *args, num_wolves: int = 30, **kwargs):
        """Khởi tạo đối tượng GWO và số lượng sói."""
        super().__init__(*args, **kwargs)
        self._num_wolves = num_wolves

    def solve(self) -> Tuple[List[str], List[str], float]:
        """Thực thi thuật toán Grey Wolf Optimizer (GWO)."""
        start_time = time.time()
        
        # Khởi tạo quần thể sói
        wolves = [[random.randint(0, 1) for _ in range(self._n)] for _ in range(self._num_wolves)]
        
        # Sắp xếp và chọn Alpha, Beta, Delta (3 con sói tốt nhất)
        scored_wolves = sorted(zip([self._fitness_value(w) for w in wolves], wolves), key=lambda x: x[0], reverse=True)
        
        alpha = scored_wolves[0][1][:]
        beta = scored_wolves[1][1][:]
        delta = scored_wolves[2][1][:]
        self.best_value = scored_wolves[0][0]
        self.history = []

        for iteration in range(self._max_iterations):
            a = 2 - iteration * (2 / self._max_iterations)

            for i in range(self._num_wolves):
                new_wolf_pos = wolves[i][:]
                
                for j in range(self._n):
                    r1, r2 = random.random(), random.random()
                    A1, C1 = 2 * a * r1 - a, 2 * r2
                    D_alpha = abs(C1 * alpha[j] - wolves[i][j])
                    X1 = alpha[j] - A1 * D_alpha
                    
                    r1, r2 = random.random(), random.random()
                    A2, C2 = 2 * a * r1 - a, 2 * r2
                    D_beta = abs(C2 * beta[j] - wolves[i][j])
                    X2 = beta[j] - A2 * D_beta

                    r1, r2 = random.random(), random.random()
                    A3, C3 = 2 * a * r1 - a, 2 * r2
                    D_delta = abs(C3 * delta[j] - wolves[i][j])
                    X3 = delta[j] - A3 * D_delta

                    X_avg = (X1 + X2 + X3) / 3
                    try:
                        prob = 1 / (1 + math.exp(-10 * (X_avg - 0.5)))
                    except OverflowError:
                        prob = 0 if X_avg < 0.5 else 1
                        
                    new_wolf_pos[j] = 1 if random.random() < prob else 0
                
                wolves[i] = new_wolf_pos
                
                _, total_weight = self._calculate_fitness(wolves[i])
                while total_weight > self._capacity:
                    ones_indices = [j for j, v in enumerate(wolves[i]) if v == 1]
                    if not ones_indices: break
                    wolves[i][random.choice(ones_indices)] = 0
                    _, total_weight = self._calculate_fitness(wolves[i])

            fitness_scores = [self._fitness_value(w) for w in wolves]
            scored_wolves = sorted(zip(fitness_scores, wolves), key=lambda x: x[0], reverse=True)
            
            alpha = scored_wolves[0][1][:]
            beta = scored_wolves[1][1][:]
            delta = scored_wolves[2][1][:]

            self.best_value = scored_wolves[0][0]
            _, best_weight = self._calculate_fitness(alpha)
            self.history.append(f"Lần {iteration}: Giá trị={self.best_value}, Trọng lượng={best_weight}")

        self.exec_time = time.time() - start_time
        self.best_solution = alpha
        
        selected_items = [self._item_names[i] for i, v in enumerate(self.best_solution) if v == 1]
        return selected_items, self.history, self.exec_time