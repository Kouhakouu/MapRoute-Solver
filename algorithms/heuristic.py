import math

def heuristic(node, end, graph):
    """
    Hàm heuristic cho thuật toán A* (sử dụng khoảng cách Euclidean).
    
    Parameters:
    - node: Nút hiện tại
    - end: Nút kết thúc
    - graph: Đồ thị
    
    Returns:
    - Khoảng cách ước tính từ node đến end.
    """
    x1, y1 = graph.nodes[node]['x'], graph.nodes[node]['y']
    x2, y2 = graph.nodes[end]['x'], graph.nodes[end]['y']
    return math.hypot(x2 - x1, y2 - y1)