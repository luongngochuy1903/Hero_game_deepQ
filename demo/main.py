#from UI.visualizer import Visualizer
from board.static_board import StaticBoard
#from board.board_dynamic import DynamicBoard
from algorithms.bfs import BFS
from algorithms.dfs import DFS
from algorithms.dijkstra import Dijkstra
#from algorithms.q_learning import QLearning
from utils.threading_utils import run_algorithms_in_parallel

class MainConsoleApp:
    def __init__(self):
        self.board_type = "static"
        self.board_size = (10, 10)  #có thể bỏ qua vì đã tọa board cứng không random board ngẫu nhiên
        self.board = None
        self.algorithms = {
            "BFS": BFS(),
            "DFS": DFS(),
            "Dijkstra": Dijkstra(),
            # "Q-learning": QLearning()
        }
        self.results = {}

    def create_board(self):
        if self.board_type == "static":
            self.board = StaticBoard(*self.board_size)
        # else:
        #     self.board = DynamicBoard(*self.board_size)
        self.board.generate_board()

    def run_algorithms(self):
        start = (0, 0)
        end = (self.board_size[0]-1, self.board_size[1]-1)
        self.results = run_algorithms_in_parallel(self.algorithms, self.board, start, end)

    def display_results(self):
        for name, result in self.results.items():
            print(f"\n--- {name} ---")
            print("Path:", result["path"])
            print("Visited:", result["visited"])

            # Hiển thị board với đường đi
            print("Board with path:")
            self.print_board_with_path(result["path"])

    def print_board_with_path(self, path):
        path_set = set(path)
        for r in range(self.board.rows):
            for c in range(self.board.cols):
                if (r, c) in path_set:
                    print("P", end=" ")
                elif self.board.grid[r][c] == 1:
                    print("█", end=" ")
                else:
                    print(".", end=" ")
            print()

    def run(self):
        self.create_board()
        self.run_algorithms()
        self.display_results()

if __name__ == "__main__":
    app = MainConsoleApp()
    app.run()