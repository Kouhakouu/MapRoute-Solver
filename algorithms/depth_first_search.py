from algorithms import register_algorithm

def dfs(graph, start, end, weight=None):
    """
    Tìm đường đi bằng thuật toán DFS.
    
    Parameters:
    - graph: Đồ thị dưới dạng đối tượng NetworkX
    - start: Nút bắt đầu
    - end: Nút kết thúc
    
    Returns:
    - Danh sách các nút đại diện cho đường đi. Nếu không tìm thấy đường, trả về danh sách rỗng.
    """
    stack = [start]
    visited = set()
    previous = {start: None}

    while stack:
        current = stack.pop()
        if current == end:
            break
        if current not in visited:
            visited.add(current)
            for neighbor in graph.neighbors(current):
                if neighbor not in visited:
                    previous[neighbor] = current
                    stack.append(neighbor)

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

register_algorithm('Depth-First Search', dfs)