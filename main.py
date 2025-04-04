import random
from collections import deque
import time

# Game Constants
WIDTH, HEIGHT = 10, 10

def print_board(snake, apples):
    board = [["."] * WIDTH for _ in range(HEIGHT)]
    for x, y in snake:
        board[y][x] = "S"
    for ax, ay in apples:
        board[ay][ax] = "A"
    for row in board:
        print(" ".join(row))
    print()

# Directions
DIRECTIONS = {
    "UP": (0, -1),
    "DOWN": (0, 1),
    "LEFT": (-1, 0),
    "RIGHT": (1, 0)
}

def bfs(snake, apple):
    queue = deque([(snake[0], [])])
    visited = set()
    while queue:
        (x, y), path = queue.popleft()
        if (x, y) == apple:
            return path
        for dx, dy in DIRECTIONS.values():
            nx, ny = x + dx, y + dy
            if 0 <= nx < WIDTH and 0 <= ny < HEIGHT and (nx, ny) not in visited and (nx, ny) not in snake:
                queue.append(((nx, ny), path + [(nx, ny)]))
                visited.add((nx, ny))
    return []
def dfs(snake, apple):
    stack = [(snake[0], [])]
    visited = set([snake[0]])  # Đánh dấu điểm bắt đầu

    while stack:
        (x, y), path = stack.pop()
        if (x, y) == apple:
            return path

        for dx, dy in reversed(DIRECTIONS.values()):  # Duyệt ngược để kết quả giống BFS hơn
            nx, ny = x + dx, y + dy
            if (0 <= nx < WIDTH and 0 <= ny < HEIGHT and 
                (nx, ny) not in visited and (nx, ny) not in snake):
                stack.append(((nx, ny), path + [(nx, ny)]))
                visited.add((nx, ny))  # Đánh dấu ngay khi thêm vào stack

    return []

def main(search_algo):
    snake = [(WIDTH // 2, HEIGHT // 2)]
    apples = [(1, 1), (8, 8), (5, 5)]  # Fixed apple locations
    total_time = 0
    
    for apple in apples:
        start_time = time.time()
        while True:
            print_board(snake, [apple])
            path = search_algo(snake, apple)
            if not path:
                print("Game Over!")
                return
            
            next_move = path[0]
            snake.insert(0, next_move)
            if next_move == apple:
                elapsed_time = time.time() - start_time
                total_time += elapsed_time
                print(f"Apple at {apple} eaten! Time elapsed: {elapsed_time:.2f} seconds")
                user_input = input("Press 'n' to continue: ").strip().lower()
                while user_input != 'n':
                    user_input = input("Press 'n' to continue: ").strip().lower()
                break
            else:
                snake.pop()
            
            time.sleep(0.5)
    
    print(f"Total time for all apples: {total_time:.2f} seconds")

if __name__ == "__main__":
    algo = input("Enter algorithm (bfs/dfs): ").strip().lower()
    if algo == "bfs":
        main(bfs)
    else:
        main(dfs)
