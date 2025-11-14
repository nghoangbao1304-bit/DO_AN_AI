import time
import csv
from typing import List, Tuple, Dict
from abc import ABC, abstractmethod

class KnapsackAlgorithmBase(ABC):
    """
    Class cơ sở trừu tượng cho các thuật toán giải bài toán Knapsack (0/1).

    Đóng gói dữ liệu đầu vào và định nghĩa giao diện chung (solve) cho các Class con.
    """
    def __init__(
        self,
        item_names: List[str],
        item_values: List[int],
        item_weights: List[int],
        knapsack_capacity: int,
        max_iterations: int = 100
    ):
        """Khởi tạo đối tượng thuật toán cơ sở."""
        self._item_names = item_names
        self._item_values = item_values
        self._item_weights = item_weights
        self._capacity = knapsack_capacity
        self._max_iterations = max_iterations
        self._n = len(item_names)
        self.history = []
        self.history_values = []  # Lưu giá trị tốt nhất theo từng iteration
        self.best_solution = []
        self.best_value = 0
        self.exec_time = 0.0

    def _calculate_fitness(self, sol: List[int]) -> Tuple[int, int]:
        """Tính tổng giá trị và trọng lượng của một nghiệm."""
        total_value = sum(self._item_values[i] * sol[i] for i in range(self._n))
        total_weight = sum(self._item_weights[i] * sol[i] for i in range(self._n))
        return total_value, total_weight

    def _fitness_value(self, sol: List[int]) -> int:
        """Trả về giá trị Fitness của nghiệm. Trả về 0 nếu nghiệm không hợp lệ (quá tải)."""
        total_value, total_weight = self._calculate_fitness(sol)
        return total_value if total_weight <= self._capacity else 0

    @abstractmethod
    def solve(self) -> Tuple[List[str], List[str], float]:
        """Phương thức trừu tượng, phải được Class con ghi đè để chạy thuật toán."""
        pass