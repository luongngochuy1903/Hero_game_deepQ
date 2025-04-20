from collections import deque
class BFS():
    def __init__(self):
        self.name = "BFS"

    def run(self, board, start):
        return self.find_path(board, start)
    #thứ tự thăm không đúng
    # def find_path(self,board,start,end): 
    #     visited = set()
    #     queue = deque()
    #     queue.append((start, [start]))
    #     visited.add(start)

    #     while queue:
    #         current, path = queue.popleft()
    #         if current == end:
    #             return {
    #                 "path": path,
    #                 "visited": visited
    #             }
    #         for neighbor in self.get_neighbors(board,current):
    #             if board.is_valid_move(neighbor) and neighbor not in visited:
    #                 visited.add(neighbor)
    #                 queue.append((neighbor, path + [neighbor]))
    #     return {
    #         "path": [],
    #         "visited": list(visited)
    #         }
    def find_path(self, board, start):
        
        visited_set = set()
        visited_order = []  # Lưu thứ tự ô đã đến thăm

        queue = deque()
        queue.append((start, [start]))
        visited_set.add(start)
        visited_order.append(start)
        final_path = []
        princesses = board.princesses.copy()  # Lưu lại danh sách công chúa ban đầu

        while queue and princesses:
            current, path = queue.popleft()
            if current in princesses:
                princesses.remove(current)
                final_path += path
                temp = {
                    "path": final_path,
                    "visited": visited_order  # Trả về đúng thứ tự
                }
            for neighbor in self.get_neighbors(board, current):
                if board.is_valid_move(neighbor) and neighbor not in visited_set:
                    visited_set.add(neighbor)
                    visited_order.append(neighbor)
                    queue.append((neighbor, path + [neighbor]))
        if final_path:
            return temp
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