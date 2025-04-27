import heapq

class Dijkstra:
    def __init__(self):
        self.name = "Dijkstra"      
    def run(self, board, start):
        return self.find_path(board, start)
    # thứ tự đến không đúng
    # def find_path(self, board, start, end):
    #     visited = set()
    #     distance = {start: 0}
    #     previous = {}
    #     heap = [(0, start)]  # (distance, position)

    #     while heap:
    #         current_dist,current = heapq.heappop(heap)
    #         if current == end:
    #             path = []
    #             while current in previous:
    #                 path.insert(0, current)
    #                 current = previous[current]
    #             path.insert(0, start)
    #             return {
    #                 "path": path,
    #                 "visited": visited
    #             }

    #         if current in visited:
    #             continue

    #         visited.add(current)
    #         for neighbor in self.get_neighbors(board, current):
    #             if board.is_valid_move(neighbor):
    #                 new_dist = current_dist + 1
    #                 if neighbor not in distance or new_dist < distance[neighbor]:
    #                     distance[neighbor] = new_dist
    #                     previous[neighbor] = current
    #                     heapq.heappush(heap, (new_dist, neighbor))
    #     return {
    #         "path": [],
    #         "visited": list(visited)
    #     }
    # def find_path(self, board, start, end):
    #     visited_set = set()
    #     visited_order = []  # Để in theo thứ tự thăm
    #     distance = {start: 0}
    #     previous = {}
    #     heap = [(0, start)]
    #     final_path = []

    #     while heap and board.princesses:
    #         current_dist, current = heapq.heappop(heap)
    #         if current in visited_set:
    #             continue

    #         visited_set.add(current)
    #         visited_order.append(current)
    #         # if current in board.princesses:
    #         #     path = []
    #         #     while current in previous:
    #         #         path.insert(0, current)
    #         #         current = previous[current]
    #         #     path.insert(0, start)
    #         #     board.princesses.remove(current)  # bỏ công chúa đã cứu
    #         #     final_path += path  # thêm đường đi vào
    #         #     return {
    #         #         "path": final_path,
    #         #         "visited": visited_order
    #         #     }
    #         if current in board.princesses:
    #             princess_pos = current   # Lưu lại vị trí công chúa ngay lúc phát hiện
    #             path = []
    #             while current in previous:
    #                 path.insert(0, current)
    #                 current = previous[current]
    #             path.insert(0, start)
                
    #             board.princesses.remove(princess_pos)  # Xóa bằng vị trí gốc
    #             final_path += path

    #             temp = {
    #                 "path": final_path,
    #                 "visited": visited_order
    #             }


    #         for neighbor in self.get_neighbors(board, current):
    #             if board.is_valid_move(neighbor) and neighbor not in visited_set:
    #                 new_dist = current_dist + 1
    #                 if neighbor not in distance or new_dist < distance[neighbor]:
    #                     distance[neighbor] = new_dist
    #                     previous[neighbor] = current
    #                     heapq.heappush(heap, (new_dist, neighbor))
    #     if final_path:
    #         return temp                
    #     return {
    #         "path": [],
    #         "visited": visited_order
    #     }
    def find_path(self, board, start):
        visited_order = []  # Để lưu toàn bộ thứ tự thăm
        final_path = []     # Đường đi nối liên tục cứu các công chúa
        current_start = start
        princesses = board.princesses.copy()
        while princesses:
            # Mỗi lần cứu 1 công chúa gần nhất
            visited_set = set()
            distance = {current_start: 0}
            previous = {}
            heap = [(0, current_start)]
            found_princess = False

            while heap:
                current_dist, current = heapq.heappop(heap)
                if current in visited_set:
                    continue

                visited_set.add(current)
                visited_order.append(current)

                if current in princesses:
                    # Cứu được công chúa tại current
                    path = []
                    node = current
                    while node in previous:
                        path.insert(0, node)
                        node = previous[node]
                    path.insert(0, current_start)

                    if final_path and final_path[-1] == path[0]:
                        # Nếu điểm đầu path trùng cuối final_path, bỏ đi để tránh lặp
                        path = path[1:]

                    final_path += path
                    princesses.remove(current)
                    current_start = current  # Bắt đầu cứu tiếp từ công chúa vừa cứu
                    found_princess = True
                    break  # Thoát khỏi vòng while heap, cứu công chúa tiếp theo

                for neighbor in self.get_neighbors(board, current):
                    if board.is_valid_move(neighbor) and neighbor not in visited_set:
                        new_dist = current_dist + 1
                        if neighbor not in distance or new_dist < distance[neighbor]:
                            distance[neighbor] = new_dist
                            previous[neighbor] = current
                            heapq.heappush(heap, (new_dist, neighbor))

            if not found_princess:
                # Không còn đường cứu được nữa
                break

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
