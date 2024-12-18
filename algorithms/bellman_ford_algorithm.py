# algorithms/bellman_ford.py

from algorithms import register_algorithm
from typing import List, Optional

def bellman_ford(graph, start, end, weight='length', **kwargs) -> Optional[List]:
    """
    Tìm đường đi bằng thuật toán Bellman-Ford.

    Parameters:
    - graph: Đồ thị dưới dạng đối tượng NetworkX
    - start: Nút bắt đầu
    - end: Nút kết thúc
    - weight: Trọng số cạnh (mặc định 'length')

    Returns:
    - Danh sách các nút đại diện cho đường đi nếu không có chu trình trọng số âm.
      Nếu có chu trình trọng số âm hoặc không tìm thấy đường đi, trả về danh sách rỗng.
    """
    # Initialize distances and predecessors
    distance = {node: float('inf') for node in graph.nodes()}
    predecessor = {node: None for node in graph.nodes()}
    
    distance[start] = 0
    
    # Relax edges repeatedly
    for _ in range(len(graph.nodes()) - 1):
        updated = False
        for u, v, data in graph.edges(data=True):
            w = data.get(weight, 1)
            if distance[u] + w < distance[v]:
                distance[v] = distance[u] + w
                predecessor[v] = u
                updated = True
        if not updated:
            break
    
    # Check for negative-weight cycles
    for u, v, data in graph.edges(data=True):
        w = data.get(weight, 1)
        if distance[u] + w < distance[v]:
            print("Graph contains a negative-weight cycle")
            return []
    
    # Reconstruct path
    path = []
    current = end
    while current is not None:
        path.append(current)
        current = predecessor[current]
    path = path[::-1]
    
    if path[0] == start:
        return path
    else:
        return []

# Đăng ký thuật toán vào registry
register_algorithm('Bellman-Ford Algorithm', bellman_ford)
