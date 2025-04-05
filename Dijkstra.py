import heapq
import time

# Game Constants
WIDTH, HEIGHT = 10, 10

# Directions
DIRECTIONS = {
    "UP": (0, -1),
    "DOWN": (0, 1),
    "LEFT": (-1, 0),
    "RIGHT": (1, 0)
}

# In bảng game
def print_board(snake, apples):
    board = [["."] * WIDTH for _ in range(HEIGHT)]
    for x, y in snake:
        board[y][x] = "S"
    for ax, ay in apples:
        board[ay][ax] = "A"
    for row in board:
        print(" ".join(row))
    print()

# Tìm đường đi ngắn nhất bằng Dijkstra
def dijkstra(snake, apple):
    start = snake[0]
    goal = apple
    pq = []  # Hàng đợi ưu tiên
    heapq.heappush(pq, (0, start, []))  # (Chi phí, vị trí, đường đi)
    visited = set()
    
    while pq:
        cost, current, path = heapq.heappop(pq)
        if current in visited:
            continue
        visited.add(current)
        
        if current == goal:
            return path
        
        for dx, dy in DIRECTIONS.values():
            nx, ny = current[0] + dx, current[1] + dy
            if 0 <= nx < WIDTH and 0 <= ny < HEIGHT and (nx, ny) not in snake and (nx, ny) not in visited:
                heapq.heappush(pq, (cost + 1, (nx, ny), path + [(nx, ny)]))
    
    return []  # Không tìm thấy đường đi

# Main game loop
def main(search_algo):
    snake = [(WIDTH // 2, HEIGHT // 2)]
    apples = [(1, 1), (8, 8), (5, 5)]
    total_time = 0
    
    for apple in apples:
        start_time = time.time()
        while True:
            print_board(snake, [apple])
            
            if search_algo == "dijkstra":
                path = dijkstra(snake, apple)
            
            if not path:
                print("Game Over!")
                return
            
            next_move = path[0]
            snake.insert(0, next_move)
            if next_move == apple:
                elapsed_time = time.time() - start_time
                total_time += elapsed_time
                print(f"Apple at {apple} eaten! Time elapsed: {elapsed_time:.2f} seconds")
                input("Press 'n' to continue: ")
                break
            else:
                snake.pop()
            
            time.sleep(0.5)
    
    print(f"Total time for all apples: {total_time:.2f} seconds")

if __name__ == "__main__":
    algo = "dijkstra"
    main(algo)
