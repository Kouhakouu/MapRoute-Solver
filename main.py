import tkinter as tk

from gui.app import MapApp
from loader.loader import load_map
from algorithms import *

def main():
    ward_name = "Dien Bien Ward"  # Tên phường
    district_name = "Ba Dinh District"  # Tên quận
    city_name = "Ha Noi City"  # Tên thành phố
    country_name = "Vietnam"  # Tên quốc gia

    place_name = f"{ward_name}, {district_name}, {city_name}, {country_name}"  # Tên địa điểm
    graph_filepath = f'graphs/{ward_name}_{district_name}_{city_name}_{country_name}.graphml'  # Đường dẫn lưu đồ thị

    G = load_map(place_name, filepath=graph_filepath)

    if G.is_directed():
        print("Đồ thị có hướng")

    if G.is_multigraph():
        print("Đồ thị có nhiều cạnh giữa hai đỉnh")

    root = tk.Tk()
    app = MapApp(root, G)
    root.mainloop()
    
if __name__ == "__main__":
    main()
