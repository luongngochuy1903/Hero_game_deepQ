from collections import deque

class DFS:
    def __init__(self):
        self.name = "DFS"

    def run(self, board, start):
        return self.find_path(board, start)

    def find_path_between(self, board, start, end):
        """Tìm đường từ start đến end bằng DFS, theo dõi thứ tự các node đã thăm."""
        visited = set()  # Tập hợp lưu các vị trí đã thăm để tránh lặp
        visited_order = []  # Danh sách lưu thứ tự các vị trí được thăm
        stack = deque()  # Ngăn xếp (stack) để lưu các node cần xử lý
        stack.append((start, [start]))  # Thêm điểm bắt đầu và đường đi ban đầu vào stack
        visited.add(start)  # Đánh dấu điểm bắt đầu đã thăm
        visited_order.append(start)  # Thêm điểm bắt đầu vào danh sách thứ tự thăm

        while stack:
            current, path = stack.pop()  # Lấy node hiện tại và đường đi tương ứng ra khỏi stack
            if current == end:  # Nếu node hiện tại là đích (end)
                return {
                    "path": path,  # Trả về đường đi từ start đến end
                    "visited": visited_order  # Trả về danh sách thứ tự các node đã thăm
                }
            # Duyệt qua các hàng xóm của node hiện tại
            for neighbor in self.get_neighbors(board, current):
                # Kiểm tra xem vị trí lân cận có hợp lệ và chưa được thăm
                if board.is_valid_move(neighbor) and neighbor not in visited:
                    visited.add(neighbor)  # Đánh dấu vị trí lân cận đã thăm
                    visited_order.append(neighbor)  # Thêm vào danh sách thứ tự thăm
                    stack.append((neighbor, path + [neighbor]))  # Thêm và đường đi mới vào stack
        # Nếu không tìm thấy đường đi, trả về đường đi rỗng và danh sách thứ tự thăm
        return {
            "path": [],
            "visited": visited_order
        }

    # Tìm đường đi qua tất cả các cư dân (residents) từ điểm bắt đầu
    def find_path(self, board, start):
        visited_set = set()  # Tập hợp lưu các vị trí đã thăm
        visited_order = []  # Danh sách lưu thứ tự các vị trí được thăm
        final_path = []  # Danh sách lưu đường đi cuối cùng
        residents = board.residents.copy()  # Sao chép danh sách các cư dân cần thăm

        # Nếu không có cư dân, trả về đường đi rỗng và danh sách thứ tự thăm
        if not residents:
            return {"path": [], "visited": visited_order}

        current_start = start  
        visited_set.add(start)  # Đánh dấu điểm bắt đầu đã thăm
        visited_order.append(start)  # Thêm điểm bắt đầu vào danh sách thứ tự thăm

        for resident in residents:
            # Tìm đường từ current_start đến cư dân hiện tại
            result = self.find_path_between(board, current_start, resident)
            path_to_resident = result["path"]  # Lấy đường đi đến cư dân
            segment_visited = result["visited"]  # Lấy danh sách các node đã thăm trong đoạn này

            # Nếu không tìm thấy đường đi đến cư dân
            if not path_to_resident:
                print(f"Không tìm thấy đường từ {current_start} đến cư dân {resident}")
                break

            # Thêm đoạn đường đi vào đường đi cuối cùng
            if final_path:
                final_path.extend(path_to_resident[1:])  # Bỏ qua vị trí đầu để tránh trùng lặp
            else:
                final_path.extend(path_to_resident)  # Thêm toàn bộ đường đi nếu là đoạn đầu tiên

            # Cập nhật điểm bắt đầu mới là vị trí của cư dân vừa thăm
            current_start = resident

            # Cập nhật tập hợp và danh sách các vị trí đã thăm
            for pos in segment_visited:
                if pos not in visited_set:
                    visited_set.add(pos)  # Thêm vị trí vào tập hợp đã thăm
                    visited_order.append(pos)  # Thêm vị trí vào danh sách thứ tự thăm

        # Trả về đường đi cuối cùng và danh sách thứ tự thăm
        return {
            "path": final_path,
            "visited": visited_order
        }

    # Lấy danh sách các vị trí lân cận của một vị trí
    def get_neighbors(self, board, pos):
        row, col = pos  # Lấy tọa độ của vị trí hiện tại
        neighbors = []  # Danh sách các vị trí
        # Duyệt qua 4 hướng di chuyển (lên, xuống, phải, trái)
        for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            neighbors.append((row + dr, col + dc))  # Thêm tọa độ của vị trí lân cận vào danh sách
        return neighbors