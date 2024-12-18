# algorithms/beam_search.py

from algorithms import register_algorithm
import math
from typing import List, Optional
from .heuristic import heuristic
from collections import deque

def beam_search(graph, start, end, weight=None, beam_width=100, **kwargs) -> Optional[List]:
    """
    Tìm đường đi bằng thuật toán Beam Search.
    
    Parameters:
    - graph: Đồ thị dưới dạng đối tượng NetworkX
    - start: Nút bắt đầu
    - end: Nút kết thúc
    - beam_width: Số lượng nút tối đa tại mỗi cấp độ
    
    Returns:
    - Danh sách các nút đại diện cho đường đi. Nếu không tìm thấy đường, trả về danh sách rỗng.
    """
    queue = deque()
    queue.append([start])
    visited = set()
    visited.add(start)
    
    while queue:
        # Lấy tất cả các đường đi ở cấp độ hiện tại
        current_level = []
        while queue:
            current_level.append(queue.popleft())
        
        # Mở rộng tất cả các đường đi
        all_candidates = []
        for path in current_level:
            last_node = path[-1]
            neighbors = list(graph.neighbors(last_node))
            for neighbor in neighbors:
                if neighbor not in path:  # Tránh vòng lặp
                    new_path = path + [neighbor]
                    all_candidates.append(new_path)
        
        # Sắp xếp các đường đi theo heuristic của nút cuối
        all_candidates.sort(key=lambda path: heuristic(path[-1], end, graph))
        
        # Giới hạn beam width
        limited_candidates = all_candidates[:beam_width]
        
        for candidate in limited_candidates:
            last_node = candidate[-1]
            if last_node == end:
                return candidate
            queue.append(candidate)
            visited.add(last_node)
    
    return []

# Đăng ký thuật toán vào registry
register_algorithm('Beam Search', beam_search)
