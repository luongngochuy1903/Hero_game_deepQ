from collections import deque

class BFS:
    def __init__(self):
        self.name = "BFS"

    def run(self, board, start):
        # Gọi hàm tìm đường từ điểm bắt đầu trên bảng (board)
        return self.find_path(board, start)

    # Tìm đường đi từ điểm bắt đầu đến các cư dân bằng BFS
    def find_path(self, board, start):
        visited_set = set()  # Tập hợp lưu các vị trí đã thăm để tránh lặp
        visited_order = []  # Danh sách lưu thứ tự các vị trí được thăm

        queue = deque()  # Hàng đợi (queue) để lưu các node cần xử lý
        queue.append((start, [start]))  # Thêm điểm bắt đầu và đường đi ban đầu vào queue
        visited_set.add(start)  # Đánh dấu điểm bắt đầu đã thăm
        visited_order.append(start)  # Thêm điểm bắt đầu vào danh sách thứ tự thăm
        final_path = []  # Danh sách lưu đường đi cuối cùng
        residents = board.residents.copy()  # Sao chép danh sách các cư dân cần thăm

        while queue and residents:
            current, path = queue.popleft()  # Lấy node hiện tại và đường đi tương ứng từ đầu queue
            if current in residents:  # Nếu node hiện tại là một cư dân
                residents.remove(current)  # Xóa cư dân khỏi danh sách cần thăm
                final_path += path  # Thêm đường đi đến cư dân vào đường đi cuối cùng
                temp = {
                    "path": final_path,  # Lưu đường đi cuối cùng
                    "visited": visited_order  # Lưu thứ tự các node đã thăm
                }
            # Duyệt qua các vị trí lân cận của node hiện tại
            for neighbor in self.get_neighbors(board, current):
                # Kiểm tra xem vị trí lân cận có hợp lệ và chưa được thăm
                if board.is_valid_move(neighbor) and neighbor not in visited_set:
                    visited_set.add(neighbor)  # Đánh dấu đã thăm
                    visited_order.append(neighbor)  # Thêm vào danh sách thứ tự thăm
                    queue.append((neighbor, path + [neighbor]))  # Thêm vị trí lân cận và đường đi mới vào queue
        
        if final_path:
            return temp
        return {
            "path": [],
            "visited": visited_order
        }

    # Lấy danh sách các vị trí lân cận của một vị trí
    def get_neighbors(self, board, pos):
        row, col = pos  # Lấy tọa độ của vị trí hiện tại
        neighbors = []  # Danh sách các vị trí lân cận
        # Duyệt qua 4 hướng di chuyển (lên, xuống, phải, trái)
        for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            neighbors.append((row + dr, col + dc))  # Thêm tọa độ vị trí lân cận vào danh sách
        return neighbors