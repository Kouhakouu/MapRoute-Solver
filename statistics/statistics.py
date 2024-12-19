import os
import time
import random
import pandas as pd
import networkx as nx
import osmnx as ox
from typing import List, Tuple
from algorithms import ALGORITHMS  # Import tất cả các thuật toán đã đăng ký
from loader.loader import load_map  # Import hàm load_map từ loader/loader.py
import logging

# Cấu hình logging
logging.basicConfig(filename='statistics_errors.log', level=logging.ERROR,
                    format='%(asctime)s:%(levelname)s:%(message)s')

def get_map_filename(ward: str, district: str, city: str, country: str) -> str:
    """
    Tạo tên file đồ thị dựa trên thông tin địa lý.
    """
    filename = f"{ward}_{district}_{city}_{country}.graphml"
    filepath = os.path.join("graphs", filename)
    return filepath

def get_csv_filename(ward: str, district: str, city: str, country: str) -> str:
    """
    Tạo tên file CSV dựa trên tên bản đồ.
    """
    filename = f"{ward}_{district}_{city}_{country}.csv"
    filepath = os.path.join("statistics", filename)
    return filepath

def select_random_coordinates(graph: nx.Graph, num_pairs: int = 100) -> List[Tuple[Tuple[float, float], Tuple[float, float]]]:
    """
    Chọn ngẫu nhiên num_pairs cặp tọa độ trong phạm vi đồ thị.
    
    Returns:
        List of tuples containing pairs of (latitude, longitude).
    """
    # Lấy các tọa độ x (longitude) và y (latitude) của tất cả các nút
    x_values = [data['x'] for _, data in graph.nodes(data=True) if 'x' in data]
    y_values = [data['y'] for _, data in graph.nodes(data=True) if 'y' in data]
    
    # Xác định phạm vi của bản đồ
    min_x, max_x = min(x_values), max(x_values)
    min_y, max_y = min(y_values), max(y_values)
    
    pairs = []
    for _ in range(num_pairs):
        # Chọn ngẫu nhiên một cặp tọa độ
        lat1 = random.uniform(min_y, max_y)
        lon1 = random.uniform(min_x, max_x)
        lat2 = random.uniform(min_y, max_y)
        lon2 = random.uniform(min_x, max_x)
        pairs.append(((lat1, lon1), (lat2, lon2)))
    return pairs

def map_coordinates_to_nodes(graph: nx.Graph, coord_pairs: List[Tuple[Tuple[float, float], Tuple[float, float]]]) -> List[Tuple[str, str]]:
    """
    Chuyển đổi các cặp tọa độ thành các cặp nút gần nhất, đảm bảo rằng Start != End.
    
    Returns:
        List of tuples containing pairs of node IDs.
    """
    node_pairs = []
    for (lat1, lon1), (lat2, lon2) in coord_pairs:
        try:
            node_A = ox.nearest_nodes(graph, X=lon1, Y=lat1)
            node_B = ox.nearest_nodes(graph, X=lon2, Y=lat2)
            if node_A != node_B:
                node_pairs.append((node_A, node_B))
            else:
                logging.error(f"Cặp nút trùng lặp: Start={node_A}, End={node_B}. Bỏ qua.")
        except Exception as e:
            logging.error(f"Lỗi khi tìm node gần nhất với tọa độ ({lat1}, {lon1}) hoặc ({lat2}, {lon2}): {e}")
    return node_pairs

def run_algorithm(algorithm_func, graph: nx.Graph, start: str, end: str, weight: str = 'length') -> Tuple[float, float, bool]:
    """
    Chạy một thuật toán tìm đường đi và thu thập thời gian chạy, độ dài đường đi và kết quả thành công.
    
    Args:
        algorithm_func: Hàm thuật toán tìm đường đi.
        graph (nx.Graph): Đồ thị.
        start (str): Node bắt đầu.
        end (str): Node kết thúc.
        weight (str): Thuộc tính trọng số của các cạnh.
    
    Returns:
        Tuple[float, float, bool]: Thời gian chạy, độ dài đường đi, và thành công hay không.
    """
    start_time = time.perf_counter()
    try:
        path = algorithm_func(graph, start, end, weight=weight)
        end_time = time.perf_counter()
        runtime = end_time - start_time
        
        if path:
            # Sử dụng OSMnx để lấy thuộc tính 'length' của từng cạnh trong đường đi
            edge_lengths = ox.utils_graph.get_route_edge_attributes(graph, path, 'length')
            path_length = sum(edge_lengths)
            success = True
        else:
            path_length = float('inf')
            success = False
    except Exception as e:
        print(f"Lỗi khi chạy thuật toán {algorithm_func.__name__} từ {start} đến {end}: {e}")
        logging.error(f"Lỗi khi chạy thuật toán {algorithm_func.__name__} từ {start} đến {end}: {e}")
        runtime = float('inf')
        path_length = float('inf')
        success = False
    
    return runtime, path_length, success

def main():
    # Thông tin địa lý
    ward_name = "Dien Bien Ward"  # Tên phường
    district_name = "Ba Dinh District"  # Tên quận
    city_name = "Ha Noi City"  # Tên thành phố
    country_name = "Vietnam"  # Tên quốc gia
    
    # Tạo tên file đồ thị và file CSV
    map_filepath = get_map_filename(ward_name, district_name, city_name, country_name)
    csv_filepath = get_csv_filename(ward_name, district_name, city_name, country_name)
    
    # Kiểm tra sự tồn tại của file đồ thị
    if not os.path.exists(map_filepath):
        print(f"File đồ thị không tồn tại: {map_filepath}")
        return
    
    # Tải đồ thị sử dụng hàm load_map từ loader/loader.py
    graph = load_map(" ".join([ward_name, district_name, city_name, country_name]), filepath=map_filepath)
    print("Đã tải đồ thị thành công.")
    
    # Chọn 100 cặp tọa độ ngẫu nhiên
    num_pairs = 100
    coord_pairs = select_random_coordinates(graph, num_pairs)
    print(f"Đã chọn {num_pairs} cặp tọa độ ngẫu nhiên.")
    
    # Chuyển đổi các cặp tọa độ thành các cặp nút, đảm bảo Start != End
    node_pairs = map_coordinates_to_nodes(graph, coord_pairs)
    print(f"Đã chuyển đổi các cặp tọa độ thành {len(node_pairs)} cặp nút (Start != End).")
    
    # Nếu số cặp nút sau khi lọc không đủ, tiếp tục chọn thêm
    if len(node_pairs) < num_pairs:
        additional_needed = num_pairs - len(node_pairs)
        print(f"Chỉ có thể chọn được {len(node_pairs)} cặp nút khác nhau. Đang chọn thêm {additional_needed} cặp nút...")
        while additional_needed > 0:
            extra_coord_pairs = select_random_coordinates(graph, additional_needed)
            extra_node_pairs = map_coordinates_to_nodes(graph, extra_coord_pairs)
            # Chọn thêm các cặp nút không trùng lặp và khác với các cặp nút đã có
            for pair in extra_node_pairs:
                if pair not in node_pairs:
                    node_pairs.append(pair)
                    additional_needed -=1
                    if additional_needed ==0:
                        break
        print(f"Đã chọn đủ {len(node_pairs)} cặp nút khác nhau.")
    
    # Kiểm tra tất cả các cặp nút đã có Start != End
    for start, end in node_pairs:
        assert start != end, f"Cặp nút không hợp lệ: Start={start}, End={end}"
    
    # Chuẩn bị dữ liệu cho CSV
    data = []
    
    # Lấy danh sách các thuật toán từ registry
    algorithms = ALGORITHMS  # Được định nghĩa trong algorithms/__init__.py
    algorithm_names = list(algorithms.keys())
    
    print(f"Đang chạy {len(algorithm_names)} thuật toán trên {len(node_pairs)} cặp điểm...")
    
    # Duyệt qua từng cặp điểm
    for idx, (start, end) in enumerate(node_pairs, 1):
        print(f"Chạy cho cặp {idx}/{num_pairs}: Start={start}, End={end}")
        for algo_name, algo_info in algorithms.items():
            func = algo_info['func']
            runtime, path_length, success = run_algorithm(func, graph, start, end, weight='length')
            data.append({
                'Pair_ID': idx,
                'Start_Node': start,
                'End_Node': end,
                'Algorithm': algo_name,
                'Runtime_Seconds': runtime,
                'Path_Length_Meters': path_length,
                'Success': success
            })
    
    # Tạo DataFrame và lưu vào CSV
    df = pd.DataFrame(data)
    df.to_csv(csv_filepath, index=False)
    print(f"Đã lưu kết quả vào file CSV: {csv_filepath}")

if __name__ == "__main__":
    main()
