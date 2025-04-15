import heapq

class Dijkstra:
    def __init__(self):
        self.name = "Dijkstra"
    
    def find_path(self, board, start, end):
        visited = set()
        distance = {start: 0}
        previous = {}
        heap = [(0, start)]  # (distance, position)

        while heap:
            current_dist,current = heapq.heappop(heap)
            if current == end:
                path = []
                while current in previous:
                    path.insert(0, current)
                    current = previous[current]
                path.insert(0, start)
                return {
                    "path": path,
                    "visited": visited
                }

            if current in visited:
                continue

            visited.add(current)
            for neighbor in self.get_neighbors(board, current):
                if board.is_valid_move(neighbor):
                    new_dist = current_dist + 1
                    if neighbor not in distance or new_dist < distance[neighbor]:
                        distance[neighbor] = new_dist
                        previous[neighbor] = current
                        heapq.heappush(heap, (new_dist, neighbor))
        return {
            "path": [],
            "visited": list(visited)
        }
    def get_neighbors(self, board, pos):
        row, col = pos
        neighbors = []
        for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            neighbors.append((row + dr, col + dc))
        return neighbors
