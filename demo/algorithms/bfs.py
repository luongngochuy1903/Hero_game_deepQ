from collections import deque

class BFS():
    def __init__(self):
        self.name = "BFS"
    
    def find_path(self,board,start,end):
        visited = set()
        queue = deque()
        queue.append((start, [start]))
        visited.add(start)

        while queue:
            current, path = queue.popleft()
            if current == end:
                return {
                    "path": path,
                    "visited": visited
                }
            for neighbor in self.get_neighbors(board,current):
                if board.is_valid_move(neighbor) and neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
        return {
            "path": [],
            "visited": list(visited)
            }
    def get_neighbors(self,board,pos):
        row,col = pos
        neighbors = []
        for dr, dc in [(1,0),(-1,0),(0,1),(0,-1)]:
            neighbors.append((row+dr,col+dc))
        return neighbors
            