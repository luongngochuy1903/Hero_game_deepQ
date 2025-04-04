import random
import time
from collections import deque

# Hàm BFS để tìm đường từ S (anh hùng) đến E (công chúa)
def bfs(maze, start, end):
    rows, cols = len(maze), len(maze[0])
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    queue = deque([(start[0], start[1], [])])
    visited = set()
    visited.add(start)
    
    while queue:
        
        x, y, path = queue.popleft()
        
        # Nếu đạt đến công chúa
        if (x, y) == end:
            check = True
            return path + [(x, y)]
        
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            
            if 0 <= nx < rows and 0 <= ny < cols and maze[nx][ny] != 1 and (nx, ny) not in visited:
                visited.add((nx, ny))
                queue.append((nx, ny, path + [(x, y)]))
    
    return None  # Không tìm được đường đi

# Hàm thay đổi bức tường
def update_walls(maze, num_walls):
    rows, cols = len(maze), len(maze[0])
    maze = [[0 for _ in range(cols)] for _ in range(rows)]
    
    walls_placed = 0
    while walls_placed < num_walls:
        x, y = random.randint(0, rows - 1), random.randint(0, cols - 1)
        if maze[x][y] == 0 and (x, y) != (0, 0) and (x, y) != (rows - 1, cols - 1):  # Tránh đặt tường tại start và end
            maze[x][y] = 1
            walls_placed += 1
    return maze

# Hàm in ma trận môi trường
def print_maze(maze, start, end):
    rows, cols = len(maze), len(maze[0])
    for i in range(rows):
        for j in range(cols):
            if (i, j) == start:
                print("S", end=" ")  # In vị trí anh hùng
            elif (i, j) == end:
                print("E", end=" ")  # In vị trí công chúa
            elif maze[i][j] == 1:
                print("#", end=" ")  # In bức tường với ký hiệu '#'
            else:
                print(".", end=" ")  # In ô trống
        print()  # Chuyển dòng sau mỗi hàng

# Hàm di chuyển anh hùng theo đường đi
def move_hero(maze, start, end):
    path = bfs(maze, start, end)
    if path:
        return path[1] if len(path) > 1 else start
    return start  

rows, cols = 12, 12
maze = [[0 for _ in range(cols)] for _ in range(rows)]
maze[0][0] = 0  # Vị trí anh hùng
maze[11][11] = 0  # Vị trí công chúa

# Vị trí của anh hùng (S) và công chúa (E)
start = (0, 0)  # Vị trí anh hùng
end = (11, 11)  # Vị trí công chúa
prince_pos = end
num_walls = 20  

# Biến để theo dõi thời gian
start_time = time.time()

check = False
while True:
    start = move_hero(maze, start, end)  # Di chuyển anh hùng đến công chúa
    print("Môi trường hiện tại:")
    print_maze(maze, start, end) 
    
    # Kiểm tra nếu bức tường đã thay đổi sau mỗi 3 giây
    if time.time() - start_time >= 3:
        maze = update_walls(maze, num_walls)  # Cập nhật bức tường
        start_time = time.time()  # Cập nhật thời gian bắt đầu lại
    
    print(f"Vị trí anh hùng: {start}")  # In vị trí anh hùng
    
    time.sleep(1)  # Chờ 1 giây trước khi di chuyển lần tiếp theo
