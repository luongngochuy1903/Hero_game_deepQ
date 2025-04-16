from collections import deque

class DFS():
    def __init__(self):
        self.name = "DFS"

    def run(self, board, start, end):
        return self.find_path(board, start, end)
    ## thứ tự thăm không đúng
    # def find_path(self,board,start,end):
    #     visited = set()
    #     stack = deque()
    #     stack.append((start, [start]))
    #     visited.add(start)

    #     while stack:
    #         current, path = stack.pop()
    #         if current == end:
    #             return {
    #                 "path": path,
    #                 "visited": visited
    #             }
    #         for neighbor in self.get_neighbors(board,current):
    #             if board.is_valid_move(neighbor) and neighbor not in visited:
    #                 visited.add(neighbor)
    #                 stack.append((neighbor, path + [neighbor]))
    #     return {
    #         "path": [],
    #         "visited": list(visited)
    #         }
    def find_path(self, board, start, end):
        visited_set = set()
        visited_order = []  # Lưu đúng thứ tự thăm
        stack = deque()
        stack.append((start, [start]))
        visited_set.add(start)
        visited_order.append(start)

        while stack:
            current, path = stack.pop()
            if current == end:
                return {
                    "path": path,
                    "visited": visited_order
                }
            for neighbor in self.get_neighbors(board, current):
                if board.is_valid_move(neighbor) and neighbor not in visited_set:
                    visited_set.add(neighbor)
                    visited_order.append(neighbor)
                    stack.append((neighbor, path + [neighbor]))
        return {
            "path": [],
            "visited": visited_order
        }
    def get_neighbors(self,board,pos):
        row,col = pos
        neighbors = []
        for dr, dc in [(1,0),(-1,0),(0,1),(0,-1)]:
            neighbors.append((row+dr,col+dc))
        return neighbors