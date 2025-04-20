# from board.static_board import StaticBoard
# from algorithms.bfs import BFS
# from algorithms.dfs import DFS
# from algorithms.dijkstra import Dijkstra
# from board.dynamic_wall import main as dynamic_main
# from algorithms.q_learning_agent import QLearningAgent
# from board.dynamic_wall import MazeGame

# Q_TABLE_PATH = "../Hero_game_deepQ/dynamic_model/q_table.pkl"
# princesses = [(2, 1), (9, 4), (12, 12)]

# class MainConsoleApp:
#     def __init__(self):
#         choose = input("Chọn chế độ (1: Tường tĩnh, 2: Tường động): ")
#         if choose == "1":
#             self.board = StaticBoard(13, 13, princesses)
#         elif choose == "2":
#             self.board = MazeGame(13, 13, princesses)
#         else:
#             print("Lựa chọn không hợp lệ. Sử dụng chế độ tường tĩnh.")
#         # self.board = StaticBoard(13, 13, princesses)
#         # self.board = MazeGame(13, 13,princesses)
#         self.algorithms = {
#             "BFS": BFS(),
#             "DFS": DFS(),
#             "Dijkstra": Dijkstra(),
#         }

#     def run(self):
#         self.board.generate_board()
#         start = (0, 0)
#         end = [(12, 12), (2, 1), (9, 4)]

#         for name, algorithm in self.algorithms.items():
#             print(f"\n--- {name} ---")
#             result = algorithm.run(self.board, start)
#             print("Path:", result["path"])
#             print("Visited:", result["visited"])
#             print("\nQuá trình thăm các ô:")
#             # self.board.print_visited_step_by_step(result["visited"], start,end)
#             if result["path"]:
#                 print("\nToàn bộ đường đi sau khi hoàn thành:")
#                 self.board.print_board(result["path"])
#             else:
#                 print("Không tìm thấy đường đi.")
#         princesses = [(2, 1), (9, 4), (12, 12)]
#         game = MazeGame(13, 13, princesses=princesses)
#         agent = QLearningAgent(game, Q_TABLE_PATH)
#         agent.run()
# if __name__ == "__main__":
#     app = MainConsoleApp()
#     app.run()
from board.static_board import StaticBoard
from board.dynamic_wall import MazeGame
from algorithms.bfs import BFS
from algorithms.dfs import DFS
from algorithms.dijkstra import Dijkstra
from algorithms.q_learning_agent_dynamic import QLearningAgent as QLearningAgentDynamic
from algorithms.q_learning_agent_static import QLearningAgent as QLearningAgentStatic
Q_TABLE_PATH_DYNAMIC = "../Hero_game_deepQ/dynamic_model/q_table.pkl"
Q_TABLE_PATH_STATIC = "F:/visual studio code/python/projectAI/Hero_game_deepQ/static_model/q_table.pkl"
PRINCESSES = [(2, 1), (9, 4), (12, 12)]

class MainConsoleApp:
    def __init__(self):
        self.board = StaticBoard(13, 13, PRINCESSES)
        self.algorithms = {
            "BFS": BFS(),
            "DFS": DFS(),
            "Dijkstra": Dijkstra(),
        }

    def run(self):
        self.board.generate_board()
        start = (0, 0)
        end = PRINCESSES

        for name, algorithm in self.algorithms.items():
            print(f"\n--- {name} ---")
            result = algorithm.run(self.board, start)
            print("Path:", result["path"])
            print("Visited:", result["visited"])
            print("\nQuá trình thăm các ô:")
            # self.board.print_visited_step_by_step(result["visited"], start,end)
            if result["path"]:
                print("\nToàn bộ đường đi sau khi hoàn thành:")
                self.board.print_board(result["path"])
            else:
                print("Không tìm thấy đường đi.")

        # Sau khi chạy xong BFS, DFS, Dijkstra => chạy tiếp QLearning
        choose = input("1.Chạy Qleaning trên tường tĩnh\n2.Chạy Qleaning trên tường động.\nChọn chế độ: ")
        if choose == "1":
            print("\n--- QLearning ---")
            game = StaticBoard(13, 13, princesses=end)
            agent = QLearningAgentStatic(game, Q_TABLE_PATH_STATIC)
            agent.run()
        elif choose == "2":
            print("\n--- QLearning ---")
            game = MazeGame(13, 13, princesses=end)
            agent = QLearningAgentDynamic(game, Q_TABLE_PATH_DYNAMIC)
            agent.run()
        # print("\n--- QLearning ---")
        # game = MazeGame(13, 13, princesses=end)
        # agent = QLearningAgent(game, Q_TABLE_PATH)
        # agent.run()
        # game = StaticBoard(13, 13, princesses=end)
        # agent = q(game, Q_TABLE_PATH_STATIC)
        # agent.run()
if __name__ == "__main__":
    app = MainConsoleApp()
    app.run()
