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
        visited_order = []  # Keep track of visited positions in order
        final_path = []
        princesses = board.princesses.copy()  # Copy the list of princesses to visit

        if not princesses:
            return {"path": [], "visited": visited_order}

        current_start = start
        visited_set.add(start)
        visited_order.append(start)

        # Process each princess sequentially
        for resident in princesses:
            # Run BFS from current_start to the current resident
            queue = deque()
            queue.append((current_start, [current_start]))
            temp_visited = set([current_start])  # Temporary visited set for this segment
            found = False
            path_to_resident = []

            while queue and not found:
                current, path = queue.popleft()
                if current == resident:
                    path_to_resident = path
                    found = True
                    break
                for neighbor in self.get_neighbors(board, current):
                    if board.is_valid_move(neighbor) and neighbor not in temp_visited:
                        temp_visited.add(neighbor)
                        queue.append((neighbor, path + [neighbor]))

            if not found:
                print(f"No path found from {current_start} to resident {resident}")
                break

            # Add the path segment to the final path (excluding the start position if it's already in the path)
            if final_path:
                final_path.extend(path_to_resident[1:])  # Skip the first position to avoid duplicates
            else:
                final_path.extend(path_to_resident)

            # Update the starting point for the next segment
            current_start = resident

            # Add intermediate positions to visited_set and visited_order
            for pos in path_to_resident:
                if pos not in visited_set:
                    visited_set.add(pos)
                    visited_order.append(pos)

        return {
            "path": final_path,
            "visited": visited_order
        }

    def get_neighbors(self, board, pos):
        row, col = pos
        neighbors = []
        for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            neighbors.append((row + dr, col + dc))
        return neighbors