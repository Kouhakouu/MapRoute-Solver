# algorithms/random_dfs.py

from algorithms import register_algorithm
from typing import List, Optional
import random

def random_dfs(graph, start, end, weight=None, max_depth=1000, **kwargs) -> Optional[List]:
    """
    Tìm đường đi bằng thuật toán Random Depth-First Search.

    Parameters:
    - graph: Đồ thị dưới dạng đối tượng NetworkX
    - start: Nút bắt đầu
    - end: Nút kết thúc
    - weight: Trọng số cạnh (không sử dụng trong Random DFS)
    - max_depth: Độ sâu tối đa để tìm kiếm

    Returns:
    - Danh sách các nút đại diện cho đường đi nếu tìm thấy, ngược lại trả về danh sách rỗng.
    """
    stack = [(start, [start])]
    visited = set()

    while stack:
        current, path = stack.pop()
        if current == end:
            return path
        if current in visited:
            continue
        visited.add(current)

        neighbors = list(graph.neighbors(current))
        random.shuffle(neighbors)  # Xáo trộn thứ tự các láng giềng

        for neighbor in neighbors:
            if neighbor not in path and len(path) < max_depth:
                stack.append((neighbor, path + [neighbor]))

    return []

# Đăng ký thuật toán vào registry
register_algorithm('Random Depth-First Search', random_dfs)
