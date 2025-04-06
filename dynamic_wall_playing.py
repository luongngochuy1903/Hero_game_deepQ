import random
import time
from collections import deque
import numpy as np
import os
import pickle
import threading

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
    
    return None  

def move_hero(maze, start, end):
    path = bfs(maze, start, end)
    if path:
        return path[1] if len(path) > 1 else start
    return start 

def agent_bfs(maze):
    state = shared_state["bfs_pos"]
    ends = shared_state["princesses"]

    while ends:
        nearest = min(ends, key=lambda e: abs(state[0]-e[0]) + abs(state[1]-e[1]))
        path = bfs(maze, state, nearest)
        if not path:
            print("[BFS] Không tìm được đường tới công chúa.")
            return

        for step in path[1:]:
            state = step
            shared_state["bfs_pos"] = state
            print_maze_sync(maze)
            time.sleep(0.1)
            if state == nearest:
                print(f"[BFS] Cứu công chúa tại {state}")
                ends.remove(state)
                break

def update_walls(maze, num_walls, end):
    rows, cols = len(maze), len(maze[0])
    maze = [[0 for _ in range(cols)] for _ in range(rows)]
    
    walls_placed = 0
    while walls_placed < num_walls:
        x, y = random.randint(0, rows - 1), random.randint(0, cols - 1)
        if maze[x][y] == 0 and (x, y) != (0, 0) and (x,y) not in end and (x, y) != (rows - 1, cols - 1): 
            maze[x][y] = 1
            walls_placed += 1
    return maze

def print_maze_sync(maze):
    with print_lock:
        q = shared_state["q_pos"]
        b = shared_state["bfs_pos"]
        ends = shared_state["princesses"]

        for i in range(len(maze)):
            for j in range(len(maze[0])):
                pos = (i, j)
                if pos == q and pos == b:
                    print("X", end=" ")  # cùng chỗ
                elif pos == q:
                    print("Q", end=" ")  # Q-learning
                elif pos == b:
                    print("B", end=" ")  # BFS
                elif pos in ends:
                    print("E", end=" ")  # Công chúa
                elif maze[i][j] == 1:
                    print("#", end=" ")  # tường
                else:
                    print(".", end=" ")  # đường
            print()
        print("-" * 40)
        time.sleep(0.2)

successful_paths = []

DIRECTION = [(-1, 0), (1, 0), (0, -1), (0, 1)]
ACTIONS = ["UP", "DOWN", "LEFT", "RIGHT"]
state_size = [13, 13]
q_table = None
q_table_path = "A:/AI_cuoiki/Hero_game_deepQ/dynamic_model/q_table.pkl"
if os.path.exists(q_table_path):
    with open(q_table_path, "rb") as f:
        q_table = pickle.load(f)
    print("Đã load q_table từ file.")
else:
    raise FileNotFoundError("Không tìm thấy file q_table.pkl trong thư mục")

def move_q_learning(state, ACTIONS):
    x,y = state
    if ACTIONS == "UP":
        return x-1, y
    elif ACTIONS == "DOWN":
        return x+1, y
    elif ACTIONS == "RIGHT":
        return x, y+1
    elif ACTIONS == "LEFT":
        return x,y-1
    return state

start = (0, 0)  
end = [(12, 12)]  

def agent_q_learning(maze):
    state = shared_state["q_pos"]
    ends = shared_state["princesses"]

    while ends:
        action = ACTIONS[np.argmax(q_table[state])]
        next_state = move_q_learning(state, action)

        x, y = next_state
        if 0 <= x < rows and 0 <= y < cols and maze[x][y] != 1:
            state = next_state

        shared_state["q_pos"] = state
        print_maze_sync(maze)
        time.sleep(0.1)

        if state in ends:
            print(f"[Q-Learning] Cứu công chúa tại {state}")
            ends.remove(state)


print_lock = threading.Lock()

shared_state = {
    "q_pos": (0, 0),
    "bfs_pos": (12, 12),
    "princesses": [(2, 1), (6, 6), (12, 12)]
}

if __name__ == "__main__":
    rows, cols = 13, 13
    maze = [[0 for _ in range(cols)] for _ in range(rows)]
    shared_state["princesses"] = [(2, 1), (6, 6), (12, 12)]  # có thể đổi

    maze = update_walls(maze, num_walls=20, end=shared_state["princesses"])

    t1 = threading.Thread(target=agent_q_learning, args=(maze,))
    t2 = threading.Thread(target=agent_bfs, args=(maze,))

    t1.start()
    t2.start()

    t1.join()
    t2.join()
