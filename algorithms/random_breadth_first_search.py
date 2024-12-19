# algorithms/random_bfs.py

from algorithms import register_algorithm
from typing import List, Optional
from collections import deque
import random

def random_bfs(graph, start, end, weight=None, max_steps=1000, **kwargs) -> Optional[List]:
    """
    Tìm đường đi bằng thuật toán Random Breadth-First Search.

    Parameters:
    - graph: Đồ thị dưới dạng đối tượng NetworkX
    - start: Nút bắt đầu
    - end: Nút kết thúc
    - weight: Trọng số cạnh (không sử dụng trong Random BFS)
    - max_steps: Số bước tối đa để tìm kiếm

    Returns:
    - Danh sách các nút đại diện cho đường đi nếu tìm thấy, ngược lại trả về danh sách rỗng.
    """
    queue = deque([(start, [start])])
    visited = set([start])
    steps = 0

    while queue and steps < max_steps:
        current, path = queue.popleft()
        if current == end:
            return path

        neighbors = list(graph.neighbors(current))
        random.shuffle(neighbors)  # Xáo trộn thứ tự các láng giềng

        for neighbor in neighbors:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))
                steps += 1
                if steps >= max_steps:
                    break

    return []

# Đăng ký thuật toán vào registry
register_algorithm('Random Breadth-First Search', random_bfs)
