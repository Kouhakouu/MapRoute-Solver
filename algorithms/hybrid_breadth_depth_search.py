# algorithms/hybrid_bfs_dfs.py

from algorithms import register_algorithm
from typing import List, Optional
from collections import deque
import random

def hybrid_bfs_dfs(graph, start, end, weight=None, toggle_prob=0.5, max_steps=1000, **kwargs) -> Optional[List]:
    """
    Tìm đường đi bằng thuật toán Hybrid BFS-DFS.

    Parameters:
    - graph: Đồ thị dưới dạng đối tượng NetworkX
    - start: Nút bắt đầu
    - end: Nút kết thúc
    - weight: Trọng số cạnh (không sử dụng trong Hybrid BFS-DFS)
    - toggle_prob: Xác suất chuyển đổi giữa BFS và DFS
    - max_steps: Số bước tối đa để tìm kiếm

    Returns:
    - Danh sách các nút đại diện cho đường đi nếu tìm thấy, ngược lại trả về danh sách rỗng.
    """
    queue = deque([(start, [start], 'BFS')])  # ('BFS' hoặc 'DFS')
    visited = set([start])
    steps = 0

    while queue and steps < max_steps:
        current, path, mode = queue.popleft()

        if current == end:
            return path

        neighbors = list(graph.neighbors(current))
        random.shuffle(neighbors)  # Xáo trộn thứ tự các láng giềng

        for neighbor in neighbors:
            if neighbor not in visited:
                visited.add(neighbor)
                new_path = path + [neighbor]
                steps += 1
                if steps >= max_steps:
                    break
                # Chọn chế độ tiếp theo dựa trên toggle_prob
                if random.random() < toggle_prob:
                    next_mode = 'DFS' if mode == 'BFS' else 'BFS'
                else:
                    next_mode = mode
                queue.append((neighbor, new_path, next_mode))
                
    return []

# Đăng ký thuật toán vào registry
register_algorithm('Hybrid Breadth-Depth First Search', hybrid_bfs_dfs)
