from board.static_board import StaticBoard
from algorithms.bfs import BFS
from algorithms.dfs import DFS
from algorithms.dijkstra import Dijkstra
from board.dynamic_wall import main as dynamic_main
from algorithms.q_learning_agent import QLearningAgent
from board.dynamic_wall import MazeGame

Q_TABLE_PATH = "../Hero_game_deepQ/dynamic_model/q_table.pkl"
princesses = [(2, 1), (9, 4), (12, 12)]

class MainConsoleApp:
    def __init__(self):
        self.board = StaticBoard(13, 13, princesses)
        # self.board = DynamicBoard(10, 10)
        self.algorithms = {
            "BFS": BFS(),
            "DFS": DFS(),
            "Dijkstra": Dijkstra(),
        }

    def run(self):
        self.board.generate_board()
        start = (0, 0)
        end = [(12, 12), (2, 1), (9, 4)]

        for name, algorithm in self.algorithms.items():
            print(f"\n--- {name} ---")
            result = algorithm.run(self.board, start)
            print("Path:", result["path"])
            print("Visited:", result["visited"])
            print("\nQuá trình thăm các ô:")
            self.board.print_visited_step_by_step(result["visited"], start,end)
            if result["path"]:
                print("\nToàn bộ đường đi sau khi hoàn thành:")
                self.board.print_board(result["path"])
            else:
                print("Không tìm thấy đường đi.")
        princesses = [(2, 1), (9, 4), (12, 12)]
        game = MazeGame(13, 13, princesses=princesses)
        agent = QLearningAgent(game, Q_TABLE_PATH)
        agent.run()
if __name__ == "__main__":
    app = MainConsoleApp()
    app.run()
