import tkinter as tk
from tkinter import messagebox, ttk
import osmnx as ox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.lines import Line2D  # Để tạo các đối tượng Line2D cho legend
from typing import List, Tuple

from algorithms import ALGORITHMS  # Import registry từ algorithms/__init__.py
from loader.loader import load_map

class MapApp:
    def __init__(self, master, graph):
        self.master = master
        self.master.title("Tìm Đường Đi Ngắn Nhất")
        self.graph = graph
        self.points = []
        self.node_A = None
        self.node_B = None

        # Tạo Frame chính để chứa map và control
        self.main_frame = tk.Frame(self.master)
        self.main_frame.pack(fill=tk.BOTH, expand=1)

        # Tạo Frame cho bản đồ (bên trái)
        self.map_frame = tk.Frame(self.main_frame)
        self.map_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        # Tạo Frame cho các điều khiển (bên phải)
        self.control_frame = tk.Frame(self.main_frame, padx=10, pady=10)
        self.control_frame.pack(side=tk.RIGHT, fill=tk.Y)

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
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.map_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # Thêm nút Reset
        self.reset_button = tk.Button(self.control_frame, text="Reset", command=self.reset_selection, width=15)
        self.reset_button.pack(pady=(0, 10))  # Đặt khoảng cách dưới

        # Thêm nhãn để hiển thị chi phí đường đi
        self.cost_label = tk.Label(self.control_frame, text="Chi phí đường đi:\n", font=("Arial", 12), justify=tk.LEFT)
        self.cost_label.pack(pady=(0, 10))

        # Thêm nhãn để chọn thuật toán
        self.algorithm_label = tk.Label(self.control_frame, text="Chọn thuật toán:", font=("Arial", 12))
        self.algorithm_label.pack(pady=(0, 5))
        self.algorithm_label.pack_forget()  # Ẩn label ban đầu

        # Thêm Dropdown để chọn thuật toán (ẩn ban đầu)
        self.selected_algorithm = tk.StringVar()
        self.algorithm_dropdown = ttk.Combobox(
            self.control_frame,
            textvariable=self.selected_algorithm,
            state='readonly',
            values=list(ALGORITHMS.keys()),  # Lấy tên các thuật toán từ registry
            width=17
        )
        self.algorithm_dropdown.pack(pady=(0, 10))
        self.algorithm_dropdown.bind("<<ComboboxSelected>>", self.on_algorithm_selected)
        self.algorithm_dropdown.pack_forget()  # Ẩn dropdown ban đầu

        # Kết nối sự kiện click chuột
        self.cid = self.fig.canvas.mpl_connect('button_press_event', self.on_click)

        # Định nghĩa màu sắc cho từng thuật toán từ registry
        self.algorithm_colors = {name: info['color'] for name, info in ALGORITHMS.items()}

        # Tạo danh sách để lưu các Line2D cho legend
        self.legend_handles = []
        self.legend_labels = []

        # Biến để quản lý animation
        self.current_animation = None  # Giữ trạng thái animation hiện tại
        self.animation_speed = 100  # Milliseconds giữa mỗi bước vẽ

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
                self.find_nodes()
                self.show_algorithm_selection()

    def find_nodes(self):
        point_A = self.points[0]
        point_B = self.points[1]

        try:
            # Tìm node gần nhất với hai điểm đã chọn
            self.node_A = ox.nearest_nodes(self.graph, X=point_A[1], Y=point_A[0])
            self.node_B = ox.nearest_nodes(self.graph, X=point_B[1], Y=point_B[0])

            print(f"Node A: {self.node_A}, Node B: {self.node_B}")

        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tìm node gần nhất: {e}")
            print(e)

    def show_algorithm_selection(self):
        # Hiển thị dropdown và label để chọn thuật toán
        self.algorithm_label.pack(pady=(0, 5))
        self.algorithm_dropdown.pack(pady=(0, 10))

    def on_algorithm_selected(self, event):
        algorithm_name = self.selected_algorithm.get()
        print(f"Thuật toán được chọn: {algorithm_name}")
        self.find_and_plot_route(algorithm_name)

    def find_and_plot_route(self, algorithm_name):
        try:
            # Kiểm tra xem thuật toán đã được vẽ chưa
            if algorithm_name in self.legend_labels:
                messagebox.showinfo("Thông báo", f"Thuật toán {algorithm_name} đã được chọn và tuyến đường đã được vẽ.")
                print(f"{algorithm_name} đã được vẽ trước đó.")
                return

            algorithm_info = ALGORITHMS.get(algorithm_name)
            if not algorithm_info:
                messagebox.showerror("Lỗi", f"Thuật toán {algorithm_name} không hỗ trợ.")
                return

            func = algorithm_info['func']
            color = algorithm_info['color']

            print(f"Tìm đường đi bằng thuật toán {algorithm_name}...")

            # Gọi hàm thuật toán với các tham số chuẩn hóa
            path = func(self.graph, self.node_A, self.node_B, weight='length')

            if path:
                route_gdf = ox.routing.route_to_gdf(self.graph, path)
                total_length = route_gdf['length'].sum()
                print(f"{algorithm_name} đường đi: {path} với chi phí {total_length:.2f} meters")

                # Cập nhật nhãn chi phí đường đi trên dòng mới
                current_text = self.cost_label.cget("text")
                new_text = f"{current_text}{algorithm_name}: {total_length:.2f} meters\n"
                self.cost_label.config(text=new_text)

                # Lấy danh sách các node trong path và chuyển thành danh sách tọa độ
                node_coords = [(self.graph.nodes[node]['x'], self.graph.nodes[node]['y']) for node in path]

                # Bắt đầu animation vẽ đường đi
                self.animate_route(node_coords, color, algorithm_name)
            else:
                messagebox.showinfo("Thông báo", f"Thuật toán {algorithm_name} không tìm thấy đường đi.")
                print(f"{algorithm_name}: Không tìm thấy đường đi.")

        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tìm đường đi: {e}")
            print(f"Lỗi khi tìm đường đi: {e}")

    def animate_route(self, node_coords: List[Tuple[float, float]], color: str, algorithm_name: str):
        if len(node_coords) < 2:
            print("Không đủ điểm để vẽ đường.")
            return

        # Tạo danh sách các đoạn cần vẽ
        segments = []
        for i in range(len(node_coords) - 1):
            segments.append((node_coords[i], node_coords[i + 1]))

        # Khởi tạo danh sách vẽ
        self.current_animation = {
            'segments': segments,
            'current_index': 0,
            'color': color,
            'algorithm_name': algorithm_name
        }

        # Bắt đầu vẽ lần đầu tiên
        self.draw_next_segment()

    def draw_next_segment(self):
        if not self.current_animation:
            return

        segments = self.current_animation['segments']
        index = self.current_animation['current_index']
        color = self.current_animation['color']
        algorithm_name = self.current_animation['algorithm_name']

        if index >= len(segments):
            # Hoàn thành animation, thêm vào legend
            legend_line = Line2D(
                [0], [0],
                color=color,
                lw=4,
                label=algorithm_name
            )

            if algorithm_name not in self.legend_labels:
                self.legend_handles.append(legend_line)
                self.legend_labels.append(algorithm_name)

                # Cập nhật legend
                self.ax.legend(handles=self.legend_handles, labels=self.legend_labels, loc='upper right', title="Thuật toán")

            self.canvas.draw()
            self.current_animation = None  # Reset trạng thái animation
            return

        # Lấy đoạn hiện tại
        segment = segments[index]
        (x_start, y_start), (x_end, y_end) = segment

        # Vẽ đoạn
        line, = self.ax.plot([x_start, x_end], [y_start, y_end], color=color, linewidth=4)

        self.canvas.draw()

        # Cập nhật chỉ số
        self.current_animation['current_index'] += 1

        # Đặt thời gian cho lần vẽ tiếp theo
        self.master.after(self.animation_speed, self.draw_next_segment)

    def reset_selection(self):
        try:
            # Hủy bất kỳ animation nào đang chạy
            if self.current_animation:
                self.current_animation = None

            # Xóa các điểm và đường đi
            self.points = []
            self.node_A = None
            self.node_B = None

            # Clear legend handles và labels
            self.legend_handles = []
            self.legend_labels = []

            # Clear axes và vẽ lại bản đồ gốc
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
            self.ax.legend([], loc='upper right')  # Đặt lại legend trống
            self.canvas.draw()

            # Reset nhãn chi phí đường đi với dòng mới
            self.cost_label.config(text="Chi phí đường đi:\n")

            # Ẩn dropdown và label chọn thuật toán
            self.algorithm_label.pack_forget()
            self.algorithm_dropdown.set('')
            self.algorithm_dropdown.pack_forget()

            # Kết nối lại sự kiện click chuột
            self.cid = self.fig.canvas.mpl_connect('button_press_event', self.on_click)
            print("Đã reset lựa chọn.")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể reset giao diện: {e}")
            print(f"Lỗi khi reset giao diện: {e}")
