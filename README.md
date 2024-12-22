# MapRoute Solver

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Adding New Algorithms](#adding-new-algorithms)
- [Dependencies](#dependencies)
- [Contributing](#contributing)
- [License](#license)

## Overview

**MapRoute Solver** is a Python-based application that provides an interactive graphical interface to visualize various pathfinding algorithms on a map. Built with Tkinter and leveraging the power of OSMnx and NetworkX, this tool allows users to select two points on a map and observe how different algorithms find the shortest path between them. The application supports an extensible architecture, enabling easy addition of new algorithms without modifying the core GUI code.

## Features

- **Interactive Map Interface:** Click on the map to select start and end points for pathfinding.
- **Multiple Pathfinding Algorithms:** Choose from algorithms like BFS, DFS, Dijkstra, A*, Greedy, and more.
- **Animated Path Drawing:** Watch the path being drawn step-by-step for better understanding.
- **Dynamic Legend:** Automatically updates with new algorithms and their corresponding colors.
- **Extensible Architecture:** Easily add new algorithms by simply placing them in the `algorithms/` directory.
- **Reset Functionality:** Clear all selections and paths with a single click.
- **Cost Display:** View the total cost (e.g., distance) of each path found by different algorithms.

## Installation

### Prerequisites

- **Python 3.6+**: Ensure you have Python installed. You can download it from [python.org](https://www.python.org/downloads/).
- **pip**: Python package installer (usually comes with Python).

### Clone the Repository

```bash
git clone https://github.com/Kouhakouu/MapRoute-Solver.git
cd MapRoute-Solver
```

### Install Dependencies

All required libraries are listed in the `requirements.txt` file. Install them using `pip`:

```bash
pip install -r requirements.txt
```

### Prepare Graph Data

Ensure that the `graphs/` directory contains the necessary .graphml files for the areas you want to visualize. You can generate these files using OSMnx based on your desired location.

## Usage

Run the application using the following command:

```bash
python main.py
```

## How to Use

1. **Select Two Points:**

* Click on the map to choose the start and end points for pathfinding.
* Once two points are selected, the algorithm selection dropdown will appear on the right.

2. **Choose an Algorithm:**

* Select a pathfinding algorithm from the dropdown menu.
* The path will be drawn incrementally on the map, and its cost will be displayed.

3. **View Results:**

* Each algorithm's path is displayed in a unique color.
* The legend updates dynamically to show all selected algorithms and their colors.
* The cost (e.g., distance) of each path is listed for comparison.

4. **Add More Algorithms:**

* You can select multiple algorithms sequentially to compare their paths and costs without resetting.

5. **Reset Selections:**

* Click the "Reset" button to clear all points, paths, and legends, allowing you to start a new search.

## Project Structure

The project is organized as follows:

```plaintext
MapRoute-Solver/
├── algorithms/
│   ├── __init__.py
│   ├── a_star.py
│   ├── bfs.py
│   ├── bidirectional_dijkstra.py
│   ├── dfs.py
│   ├── dijkstra.py
│   └── greedy.py
├── gui/
│   ├── __init__.py
│   └── map_app.py
├── loader/
│   ├── __init__.py
│   └── loader.py
├── graphs/
│   └── your_map.graphml
├── main.py
├── requirements.txt
└── README.md
```

* `algorithms/:` Contains all pathfinding algorithm modules. Each module defines a specific algorithm and registers it.
* `gui/:` Houses the graphical user interface components.
* `loader/:` Responsible for loading map data and graph files.
* `graphs/:` Directory to store .graphml files representing different maps.
* `main.py:` Entry point of the application.
* `requirements.txt:` Lists all Python dependencies.
* `README.md:` This documentation file.

## Adding New Algorithms

One of the key strengths of MapRoute Solver is its extensible architecture. Adding a new pathfinding algorithm is straightforward and doesn't require modifying the GUI code.

### Steps to Add a New Algorithm

1. **Create a New Module:**

* Navigate to the `algorithms/` directory.
* Create a new Python file for your algorithm, e.g., `bidirectional_dijkstra.py`.

2. **Define the Algorithm Function:**

* Ensure your function follows the standardized interface, accepting `graph`, `start`, `goal`, `weight='length'`, and `**kwargs`.
* Implement the pathfinding logic within this function.

3. **Register the Algorithm:**

* At the end of your module, register the algorithm using the `register_algorithm` function.
* Example:

```python
# algorithms/bidirectional_dijkstra.py

import networkx as nx
from typing import List, Optional
from algorithms import register_algorithm

def bidirectional_dijkstra(graph, start, goal, weight='length', **kwargs) -> Optional[List]:
    try:
        path = nx.bidirectional_dijkstra(graph, start, goal, weight=weight)[1]
        return path
    except Exception as e:
        print(f"Error in Bidirectional Dijkstra: {e}")
        return None

# Register the algorithm
register_algorithm(name='Bidirectional Dijkstra', func=bidirectional_dijkstra)
```

4. **Automatic Integration:**

* Upon running the application, the new algorithm will automatically appear in the dropdown menu with a unique color.

### Notes

* **Color Assignment:** Colors are automatically generated to ensure uniqueness and visual distinction.
* **Error Handling:** Ensure your algorithm handles exceptions gracefully to prevent the application from crashing.
* **Performance:** For complex algorithms, consider optimizing for performance to maintain smooth animations.

### Dependencies

The application relies on the following Python libraries:

* `OSMnx`: For downloading and modeling street networks.
* `NetworkX`: For graph-based algorithms and operations.
* `Matplotlib`: For plotting and visualization.
* `Tkinter`: For the graphical user interface.
* `Pillow`: (If using images for screenshots or additional GUI elements)
* All dependencies are listed in `requirements.txt`.

### Contributing

Contributions are welcome! If you have ideas for new algorithms, improvements, or bug fixes, feel free to submit a pull request or open an issue.

### Guidelines

* Fork the Repository
* Create a New Branch for your feature or bugfix.
* Commit Your Changes with clear and descriptive messages.
* Push to Your Fork
* Submit a Pull Request detailing your changes.
* Please ensure your code adheres to the project's coding standards and includes appropriate documentation.

### License

This project is licensed under the MIT License. See the `LICENSE` file for more details.