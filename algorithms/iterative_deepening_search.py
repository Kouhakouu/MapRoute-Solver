# algorithms/iterative_deepening_search.py

from algorithms import register_algorithm
from typing import List, Optional

def iterative_deepening_search(graph, start, end, weight=None, max_depth=100, **kwargs) -> Optional[List]:
    """
    Tìm đường đi bằng thuật toán Iterative Deepening Search.
    
    Parameters:
    - graph: Đồ thị dưới dạng đối tượng NetworkX
    - start: Nút bắt đầu
    - end: Nút kết thúc
    - max_depth: Độ sâu tối đa để tìm kiếm
    
    Returns:
    - Danh sách các nút đại diện cho đường đi. Nếu không tìm thấy đường, trả về danh sách rỗng.
    """
    def depth_limited_search(current, end, path, limit):
        if current == end:
            return path
        if limit <= 0:
            return None
        for neighbor in graph.neighbors(current):
            if neighbor not in path:
                result = depth_limited_search(neighbor, end, path + [neighbor], limit - 1)
                if result is not None:
                    return result
        return None
    
    for depth in range(max_depth + 1):
        result = depth_limited_search(start, end, [start], depth)
        if result:
            return result
    return []

# Đăng ký thuật toán vào registry
register_algorithm('Iterative Deepening Search', iterative_deepening_search)
