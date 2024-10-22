import os
import osmnx as ox
from algorithm import shortest_path
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import messagebox

# Bước 1: Tải và xử lý dữ liệu bản đồ, với khả năng lưu và tải lại từ file
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

# Bước 2: Xây dựng giao diện người dùng để chọn hai điểm
class MapApp:
    def __init__(self, master, graph):
        self.master = master
        self.master.title("Tìm Đường Đi Ngắn Nhất")
        self.graph = graph
        self.points = []
        self.route = []
        self.node_A = None
        self.node_B = None

        # Tạo Frame cho bản đồ
        self.frame = tk.Frame(self.master)
        self.frame.pack(fill=tk.BOTH, expand=1)

        # Tạo Figure và Axes cho matplotlib với màu nền trắng và màu sắc đẹp hơn
        self.fig, self.ax = ox.plot_graph(
            self.graph,
            show=False,
            close=False,
            edge_color='#999999',
            node_size=0,
            bgcolor='white'
        )
        self.ax.set_facecolor('white')  # Đặt màu nền cho Axes

        # Tạo Canvas cho matplotlib và nhúng vào tkinter
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # Thêm nút Reset
        self.reset_button = tk.Button(self.master, text="Reset", command=self.reset_selection)
        self.reset_button.pack(side=tk.BOTTOM, pady=10)

        # Thêm nhãn để hiển thị chi phí đường đi
        self.cost_label = tk.Label(self.master, text="Chi phí đường đi: N/A", font=("Arial", 12))
        self.cost_label.pack(side=tk.BOTTOM, pady=5)

        # Kết nối sự kiện click chuột
        self.cid = self.fig.canvas.mpl_connect('button_press_event', self.on_click)

    def on_click(self, event):
        if event.xdata and event.ydata:
            # Chuyển đổi từ hệ trục matplotlib sang latitude và longitude
            lon, lat = event.xdata, event.ydata
            print(f"Bạn đã chọn điểm: Latitude={lat}, Longitude={lon}")
            self.points.append((lat, lon))
            # Vẽ điểm trên bản đồ
            self.ax.plot(lon, lat, marker='o', markersize=8, markeredgecolor='red', markerfacecolor='yellow')
            self.canvas.draw()
            if len(self.points) == 2:
                # Ngắt kết nối sự kiện sau khi chọn đủ hai điểm
                self.fig.canvas.mpl_disconnect(self.cid)
                self.find_and_plot_route()

    def find_and_plot_route(self):
        point_A = self.points[0]
        point_B = self.points[1]

        try:
            # Tìm node gần nhất với hai điểm đã chọn
            self.node_A = ox.nearest_nodes(self.graph, X=point_A[1], Y=point_A[0])
            self.node_B = ox.nearest_nodes(self.graph, X=point_B[1], Y=point_B[0])

            print(f"Node A: {self.node_A}, Node B: {self.node_B}")

            # Tìm đường đi ngắn nhất sử dụng thuật toán Dijkstra
            self.route = shortest_path(self.graph, self.node_A, self.node_B, weight='length')
            print(f"Đường đi ngắn nhất: {self.route}")

            # Chuyển tuyến đường đi thành GeoDataFrame và tính tổng độ dài
            route_gdf = ox.routing.route_to_gdf(self.graph, self.route)
            total_length = route_gdf['length'].sum()
            print(f"Chi phí đường đi: {total_length:.2f} meters")

            # Hiển thị chi phí đường đi trong giao diện người dùng
            self.cost_label.config(text=f"Chi phí đường đi: {total_length:.2f} meters")

            # Vẽ đường đi trên bản đồ
            self.ax.cla()  # Xóa bản đồ hiện tại

            # Vẽ lại bản đồ với màu sắc tùy chỉnh
            ox.plot_graph(
                self.graph,
                ax=self.ax,
                show=False,
                close=False,
                edge_color='#999999',
                node_size=0,
                bgcolor='white'
            )

            # Vẽ lại các điểm đã chọn
            for point in self.points:
                self.ax.plot(point[1], point[0], marker='o', markersize=8, markeredgecolor='red', markerfacecolor='yellow')

            # Vẽ đường đi
            ox.plot_graph_route(
                self.graph,
                self.route,
                ax=self.ax,
                route_color='blue',
                route_linewidth=4,
                node_size=0,
                show=False,
                close=False
            )

            self.ax.legend(['Điểm chọn', 'Đường đi ngắn nhất'], loc='best')
            self.canvas.draw()

        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tìm đường đi: {e}")
            print(e)

    def reset_selection(self):
        # Xóa các điểm và đường đi
        self.points = []
        self.route = []
        self.node_A = None
        self.node_B = None

        # Vẽ lại bản đồ gốc
        self.ax.cla()
        ox.plot_graph(
            self.graph,
            ax=self.ax,
            show=False,
            close=False,
            edge_color='#999999',
            node_size=0,
            bgcolor='white'
        )
        self.ax.set_facecolor('white')
        self.ax.legend([], loc='best')
        self.canvas.draw()

        # Reset nhãn chi phí đường đi
        self.cost_label.config(text="Chi phí đường đi: N/A")

        # Kết nối lại sự kiện click chuột
        self.cid = self.fig.canvas.mpl_connect('button_press_event', self.on_click)
        print("Đã reset lựa chọn.")

# Bước 3: Chạy ứng dụng
def main():
    ward_name = "Dien Bien Ward"  # Tên phường
    district_name = "Ba Dinh District"  # Tên quận
    city_name = "Ha Noi City"  # Tên thành phố

    place_name = f"{ward_name}, {district_name}, {city_name}, Vietnam"
    graph_filepath = f'graphs/{ward_name}_{district_name}_{city_name}.graphml'  # Đường dẫn lưu đồ thị

    G = load_map(place_name, filepath=graph_filepath)

    root = tk.Tk()
    app = MapApp(root, G)
    root.mainloop()

if __name__ == "__main__":
    main()
