import random
import time
from typing import List, Tuple
from knapsack_base import KnapsackAlgorithmBase

class HillClimbing(KnapsackAlgorithmBase):
    """Giải bài toán Knapsack bằng thuật toán Hill Climbing."""

    def _generate_neighbor(self, sol: List[int]) -> List[int]:
        """Tạo lân cận bằng cách đảo bit ngẫu nhiên tại một vị trí."""
        new_sol = sol[:]
        i = random.randint(0, self._n - 1)
        new_sol[i] = 1 - new_sol[i] 
        return new_sol

    def solve(self) -> Tuple[List[str], List[str], float]:
        """Thực thi thuật toán Hill Climbing để tìm nghiệm tối ưu."""
        start_time = time.time()
        
        current_solution = [random.randint(0, 1) for _ in range(self._n)]
        current_value, current_weight = self._calculate_fitness(current_solution)

        while current_weight > self._capacity:
            ones_indices = [i for i, v in enumerate(current_solution) if v == 1]
            if not ones_indices: break
            
            idx = random.choice(ones_indices)
            current_solution[idx] = 0
            current_value, current_weight = self._calculate_fitness(current_solution)

        self.best_solution = current_solution[:]
        self.best_value, best_weight = current_value, current_weight
        self.history = []
        self.history_values = []

        for iteration in range(self._max_iterations):
            neighbor = self._generate_neighbor(current_solution)
            value, weight = self._calculate_fitness(neighbor)

            if weight <= self._capacity and value > current_value:
                current_solution = neighbor[:]
                current_value, current_weight = value, weight
                if current_value > self.best_value:
                    self.best_solution = current_solution[:]
                    self.best_value, best_weight = current_value, current_weight

            self.history.append(f"Lần {iteration}: Giá trị={current_value}, Trọng lượng={current_weight}")
            self.history_values.append(self.best_value)  # Lưu giá trị tốt nhất

        self.exec_time = time.time() - start_time
        
        selected_items = [self._item_names[i] for i, v in enumerate(self.best_solution) if v == 1]
        return selected_items, self.history, self.exec_time