import os
import osmnx as ox

def load_map(place_name, filepath='graph.graphml'):
    if os.path.exists(filepath):
        print(f"Tải đồ thị từ file: {filepath}")
        G = ox.load_graphml(filepath)
    else:
        print(f"Tải bản đồ từ OpenStreetMap cho: {place_name}")
        G = ox.graph_from_place(place_name, network_type='walk')
        print(f"Lưu đồ thị vào file: {filepath}")
        ox.save_graphml(G, filepath)
    return G