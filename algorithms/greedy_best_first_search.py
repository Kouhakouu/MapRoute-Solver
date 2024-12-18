import heapq
from .heuristic import heuristic
from algorithms import register_algorithm

def greedy(graph, start, end, weight=None):
    """
    Tìm đường đi bằng thuật toán Greedy Best-First Search.
    
    Parameters:
    - graph: Đồ thị dưới dạng đối tượng NetworkX
    - start: Nút bắt đầu
    - end: Nút kết thúc
    
    Returns:
    - Danh sách các nút đại diện cho đường đi. Nếu không tìm thấy đường, trả về danh sách rỗng.
    """
    queue = []
    heapq.heappush(queue, (heuristic(start, end, graph), start))
    visited = {start}
    previous = {start: None}

    while queue:
        _, current_node = heapq.heappop(queue)

        if current_node == end:
            break

        for neighbor in graph.neighbors(current_node):
            if neighbor not in visited:
                visited.add(neighbor)
                previous[neighbor] = current_node
                heapq.heappush(queue, (heuristic(neighbor, end, graph), neighbor))

    # Khôi phục đường đi
    path = []
    node = end
    while node is not None:
        path.append(node)
        node = previous.get(node)
    path = path[::-1]

    if path[0] == start:
        return path
    else:
        return []

register_algorithm('Greedy Best-First Search', greedy)