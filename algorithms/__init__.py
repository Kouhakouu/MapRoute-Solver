# algorithms/__init__.py

import pkgutil
import importlib
from typing import Callable, Dict
import matplotlib.colors as mcolors
import itertools

# Registry để lưu trữ các thuật toán
ALGORITHMS: Dict[str, Dict] = {}

# Tạo một generator để tạo màu sắc khác nhau
def color_generator():
    # Sử dụng hệ màu HSV và phân chia đều các màu theo hue
    for i in itertools.count():
        hue = (i * 0.618033988749895) % 1  # Sử dụng số vàng phi để phân bố màu
        rgb = mcolors.hsv_to_rgb((hue, 0.5, 0.95))  # Điều chỉnh độ bão hòa và giá trị
        yield mcolors.to_hex(rgb)

# Khởi tạo bộ tạo màu
color_gen = color_generator()

def register_algorithm(name: str, func: Callable, color: str = None):
    if name in ALGORITHMS:
        raise ValueError(f"Thuật toán '{name}' đã được đăng ký.")
    if color is None:
        color = next(color_gen)
    ALGORITHMS[name] = {
        'color': color,
        'func': func
    }

# Tự động tải tất cả các module trong thư mục algorithms/
for finder, name, ispkg in pkgutil.iter_modules(__path__):
    module = importlib.import_module(f".{name}", package=__name__)
