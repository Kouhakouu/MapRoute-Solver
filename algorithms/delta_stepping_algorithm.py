# algorithms/delta_stepping.py

from algorithms import register_algorithm
from typing import List, Optional
from collections import defaultdict
import heapq

def delta_stepping(graph, start, end, weight='length', delta=1, **kwargs) -> Optional[List]:
    """
    Tìm đường đi bằng thuật toán Delta-Stepping.

    Parameters:
    - graph: Đồ thị dưới dạng đối tượng NetworkX
    - start: Nút bắt đầu
    - end: Nút kết thúc
    - weight: Trọng số cạnh (mặc định 'length')
    - delta: Khoảng delta để chia bucket

    Returns:
    - Danh sách các nút đại diện cho đường đi. Nếu không tìm thấy đường, trả về danh sách rỗng.
    """
    distance = {node: float('inf') for node in graph.nodes()}
    predecessor = {node: None for node in graph.nodes()}
    distance[start] = 0
    
    buckets = defaultdict(list)
    buckets[0].append(start)
    
    bucket_index = 0
    
    while True:
        if bucket_index not in buckets:
            break
        current_bucket = buckets[bucket_index]
        if not current_bucket:
            bucket_index += 1
            continue
        
        while current_bucket:
            u = current_bucket.pop(0)
            for v in graph.neighbors(u):
                edge_weight = graph[u][v].get(weight, 1)
                new_dist = distance[u] + edge_weight
                if new_dist < distance[v]:
                    distance[v] = new_dist
                    predecessor[v] = u
                    b_index = new_dist // delta
                    buckets[b_index].append(v)
        
        bucket_index += 1
    
    # Khôi phục đường đi
    path = []
    node = end
    while node is not None:
        path.append(node)
        node = predecessor.get(node)
    path = path[::-1]
    
    if path[0] == start:
        return path
    else:
        return []

# Đăng ký thuật toán vào registry
register_algorithm('Delta-Stepping', delta_stepping)
