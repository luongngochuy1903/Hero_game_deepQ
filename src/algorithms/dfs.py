from collections import deque

class DFS:
    def __init__(self):
        self.name = "DFS"

    def run(self, board, start):
        return self.find_path(board, start)

    def find_path_between(self, board, start, end):
        """Find a path from start to end using DFS, tracking visited order."""
        visited = set()
        visited_order = []  # Track the order of visited nodes
        stack = deque()
        stack.append((start, [start]))
        visited.add(start)
        visited_order.append(start)

        while stack:
            current, path = stack.pop()
            if current == end:
                return {
                    "path": path,
                    "visited": visited_order
                }
            for neighbor in self.get_neighbors(board, current):
                if board.is_valid_move(neighbor) and neighbor not in visited:
                    visited.add(neighbor)
                    visited_order.append(neighbor)
                    stack.append((neighbor, path + [neighbor]))
        return {
            "path": [],
            "visited": visited_order
        }

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
            # Run DFS from current_start to the current resident
            result = self.find_path_between(board, current_start, resident)
            path_to_resident = result["path"]
            segment_visited = result["visited"]

            if not path_to_resident:
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
            for pos in segment_visited:
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