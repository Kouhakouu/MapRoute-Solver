from algorithms import register_algorithm
from collections import deque

def bfs(graph, start, end, weight=None):
    """
    Tìm đường đi bằng thuật toán BFS.
    
    Parameters:
    - graph: Đồ thị dưới dạng đối tượng NetworkX
    - start: Nút bắt đầu
    - end: Nút kết thúc
    
    Returns:
    - Danh sách các nút đại diện cho đường đi. Nếu không tìm thấy đường, trả về danh sách rỗng.
    """
    queue = deque([start])
    visited = {start}
    previous = {start: None}

    while queue:
        current = queue.popleft()
        if current == end:
            break
        for neighbor in graph.neighbors(current):
            if neighbor not in visited:
                visited.add(neighbor)
                previous[neighbor] = current
                queue.append(neighbor)

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

register_algorithm('Breadth-First Search', bfs)