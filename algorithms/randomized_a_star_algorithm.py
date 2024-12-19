# algorithms/randomized_a_star.py

from algorithms import register_algorithm
from typing import List, Optional
import heapq
import math
import random
from .heuristic import heuristic

def randomized_a_star(graph, start, end, weight='length', randomness=0.1, **kwargs) -> Optional[List]:
    """
    Tìm đường đi bằng thuật toán Randomized A*.
    
    Parameters:
    - graph: Đồ thị dưới dạng đối tượng NetworkX
    - start: Nút bắt đầu
    - end: Nút kết thúc
    - weight: Trọng số cạnh (mặc định 'length')
    - randomness: Tỷ lệ ngẫu nhiên (0 ≤ randomness ≤ 1)
    
    Returns:
    - Danh sách các nút đại diện cho đường đi nếu tìm thấy, ngược lại trả về danh sách rỗng.
    """
    open_set = []
    heapq.heappush(open_set, (0 + heuristic(start, end, graph), 0, start, [start]))
    
    closed_set = set()
    g_scores = {start: 0}
    
    while open_set:
        f, g, current, path = heapq.heappop(open_set)
        
        if current == end:
            return path
        
        if current in closed_set:
            continue
        closed_set.add(current)
        
        neighbors = list(graph.neighbors(current))
        random.shuffle(neighbors)  # Xáo trộn thứ tự các láng giềng
        
        for neighbor in neighbors:
            edge_weight = graph[current][neighbor].get(weight, 1)
            tentative_g = g + edge_weight
            if neighbor in g_scores and tentative_g >= g_scores[neighbor]:
                continue
            g_scores[neighbor] = tentative_g
            # Thêm yếu tố ngẫu nhiên vào hàm heuristic
            h = heuristic(neighbor, end, graph) * (1 - randomness) + random.uniform(0, heuristic(neighbor, end, graph)) * randomness
            heapq.heappush(open_set, (tentative_g + h, tentative_g, neighbor, path + [neighbor]))
    
    return []

# Đăng ký thuật toán vào registry
register_algorithm('Randomized A* Algorithm', randomized_a_star)
