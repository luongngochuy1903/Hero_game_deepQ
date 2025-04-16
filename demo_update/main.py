from board.static_board import StaticBoard
from algorithms.bfs import BFS
from algorithms.dfs import DFS
from algorithms.dijkstra import Dijkstra
from board.dynamic_wall import main as dynamic_main
class MainConsoleApp:
    def __init__(self):
        self.board = StaticBoard(10, 10)
        # self.board = DynamicBoard(10, 10)
        self.algorithms = {
            "BFS": BFS(),
            "DFS": DFS(),
            "Dijkstra": Dijkstra(),
        }

    def run(self):
        self.board.generate_board()
        start = (0, 0)
        end = (self.board.rows - 1, self.board.cols - 1) # đích

        for name, algorithm in self.algorithms.items():
            print(f"\n--- {name} ---")
            result = algorithm.run(self.board, start, end)
            print("Path:", result["path"])
            print("Visited:", result["visited"])
            print("\nQuá trình thăm các ô:")
            self.board.print_visited_step_by_step(result["visited"], start, end)
            if result["path"]:
                print("\nToàn bộ đường đi sau khi hoàn thành:")
                self.board.print_board(result["path"])
            else:
                print("Không tìm thấy đường đi.")
        dynamic_main()
if __name__ == "__main__":
    app = MainConsoleApp()
    app.run()
