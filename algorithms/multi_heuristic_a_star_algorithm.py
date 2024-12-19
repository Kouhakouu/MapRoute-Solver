# algorithms/multi_heuristic_a_star.py

from algorithms import register_algorithm
from typing import List, Optional
import heapq
import math

def heuristic1(node, end, graph):
    """
    Hàm heuristic 1: Khoảng cách Euclidean.
    """
    x1, y1 = graph.nodes[node]['x'], graph.nodes[node]['y']
    x2, y2 = graph.nodes[end]['x'], graph.nodes[end]['y']
    return math.hypot(x2 - x1, y2 - y1)

def heuristic2(node, end, graph):
    """
    Hàm heuristic 2: Khoảng cách Manhattan.
    """
    x1, y1 = graph.nodes[node]['x'], graph.nodes[node]['y']
    x2, y2 = graph.nodes[end]['x'], graph.nodes[end]['y']
    return abs(x2 - x1) + abs(y2 - y1)

def multi_heuristic_a_star(graph, start, end, weight='length', **kwargs) -> Optional[List]:
    """
    Tìm đường đi bằng thuật toán Multi-Heuristic A*.
    
    Parameters:
    - graph: Đồ thị dưới dạng đối tượng NetworkX
    - start: Nút bắt đầu
    - end: Nút kết thúc
    - weight: Trọng số cạnh (mặc định 'length')
    
    Returns:
    - Danh sách các nút đại diện cho đường đi nếu tìm thấy, ngược lại trả về danh sách rỗng.
    """
    heuristics = [heuristic1, heuristic2]
    open_set = []
    for h in heuristics:
        heapq.heappush(open_set, (h(start, end, graph), 0, start, [start], h))
    
    closed_set = set()
    g_scores = {start: 0}
    
    while open_set:
        f, g, current, path, current_h = heapq.heappop(open_set)
        
        if current == end:
            return path
        
        if current in closed_set:
            continue
        closed_set.add(current)
        
        for neighbor in graph.neighbors(current):
            edge_weight = graph[current][neighbor].get(weight, 1)
            tentative_g = g + edge_weight
            if neighbor in g_scores and tentative_g >= g_scores[neighbor]:
                continue
            g_scores[neighbor] = tentative_g
            # Chọn heuristic tối ưu cho node kế tiếp
            h = min(h(neighbor, end, graph) for h in heuristics)
            heapq.heappush(open_set, (tentative_g + h, tentative_g, neighbor, path + [neighbor], h))
    
    return []

# Đăng ký thuật toán vào registry
register_algorithm('Multi-Heuristic A* Algorithm', multi_heuristic_a_star)
