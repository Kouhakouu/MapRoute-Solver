import heapq
from .heuristic import heuristic
from algorithms import register_algorithm

def a_star(graph, start, end, weight='length'):
    """
    Tìm đường đi bằng thuật toán A*.
    
    Parameters:
    - graph: Đồ thị dưới dạng đối tượng NetworkX
    - start: Nút bắt đầu
    - end: Nút kết thúc
    - weight: Thuộc tính của cạnh dùng làm trọng số (mặc định là 'length')
    
    Returns:
    - Danh sách các nút đại diện cho đường đi ngắn nhất. Nếu không tìm thấy đường, trả về danh sách rỗng.
    """
    queue = []
    heapq.heappush(queue, (0 + heuristic(start, end, graph), 0, start))
    distances = {start: 0}
    previous = {start: None}

    while queue:
        estimated_total, current_distance, current_node = heapq.heappop(queue)

        if current_node == end:
            break

        for neighbor in graph.neighbors(current_node):
            edge_data = graph.get_edge_data(current_node, neighbor)
            if isinstance(edge_data, dict):
                weight_values = [data.get(weight, 1) for data in edge_data.values()]
                edge_weight = min(weight_values)
            else:
                edge_weight = edge_data.get(weight, 1)

            distance = current_distance + edge_weight
            estimated = distance + heuristic(neighbor, end, graph)

            if neighbor not in distances or distance < distances[neighbor]:
                distances[neighbor] = distance
                previous[neighbor] = current_node
                heapq.heappush(queue, (estimated, distance, neighbor))

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

register_algorithm('A*', a_star)