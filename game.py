import time
from collections import deque
import numpy as np
import random

fixed_walls = [
    (6, 0), (6, 1), (6, 2), (6,3), (6, 4), (6, 5), (6, 7), (6, 8), (6, 9), (6, 10), (6, 11), (6, 12),
    (0, 1), (12, 11), (1, 2), (1, 3), (11, 10), (11, 9), (3, 0), (3, 1), (3, 2), (3,3), (3, 4), (3, 5), (2, 6), (0, 9), (0, 10),
    (2, 8), (2, 9), (2, 10), (2, 11), (3, 10), (4, 3), (5, 7), (4, 7), (5, 11), (7, 1),
    (9, 12), (9, 11), (9, 10), (9, 9), (9, 8), (9, 7), (10, 6), (12, 2), (12, 3), (10, 1), (10, 2), (10, 3), (10, 4), (9, 2),
    (8, 9), (7, 5), (8, 5)
]

# Hàm di chuyển anh hùng theo đường đi
def move_hero_for_bfs(maze, start, end):
    path = bfs(maze, start, end)
    if path:
        return path[1] if len(path) > 1 else start
    return start  

rows, cols = 13, 13
maze = [[0 for _ in range(cols)] for _ in range(rows)]

# Hàm BFS 
def bfs(maze, start, end):
    rows, cols = len(maze), len(maze[0])
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    queue = deque([(start[0], start[1], [])])
    visited = set()
    visited.add(start)

    while queue:
        x, y, path = queue.popleft()

        if (x, y) == end:
            return path + [(x, y)]

        for dx, dy in directions:
            nx, ny = x + dx, y + dy

            if 0 <= nx < rows and 0 <= ny < cols and maze[nx][ny] != 1 and (nx, ny) not in visited:
                visited.add((nx, ny))
                queue.append((nx, ny, path + [(x, y)]))

    return None 

c_learning_rate = 0.2
c_discount_value = 0.9

c_no_of_eps = 2500
v_epsilon = 0.9
c_start_ep_epsilon_decay = 1
c_end_ep_epsilon_decay = c_no_of_eps // 2
v_epsilon_decay = v_epsilon / (c_end_ep_epsilon_decay - c_start_ep_epsilon_decay)

successful_paths = []

DIRECTION = [(-1, 0), (1, 0), (0, -1), (0, 1)]
ACTIONS = ["UP", "DOWN", "LEFT", "RIGHT"]
state_size = [13, 13]
q_table = np.random.uniform(low=-1, high=1, size=(state_size[0], state_size[1], len(ACTIONS)))

def get_reward(state, end, maze):
    if state in end:
        return 3
    x,y = state
    # if maze[x][y] == 1:
    #     return -100
    return -1

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

def print_maze(maze, start, ends):
    rows, cols = len(maze), len(maze[0])
    for i in range(rows):
        for j in range(cols):
            if (i, j) == start:
                print("S", end=" ")  
            elif (i, j) in ends:
                print("E", end=" ")  
            elif maze[i][j] == 1:
                print("#", end=" ")  
            else:
                print(".", end=" ") 
        print()
    print("----------------------------------------")
    time.sleep(0.5)

for x, y in fixed_walls:
    maze[x][y] = 1

# start = (0, 0)  
# end = [(12, 12), (2, 1), (9, 4)]  
# for x,y in end:
#     maze[x][y] = 2
max_step = 120
max_ep_reward = -2000
ep_max = -1

for ep in range(c_no_of_eps):
    print(f"Ep thứ: {ep}")
    start = (0, 0)  
    end = [(12, 12), (2, 1), (9, 4)]  
    for x,y in end:
        maze[x][y] = 2
    ep_reward = 0
    state = start
    step = 0
    princess_found = 0
    current_path = []
    while step < max_step and princess_found < 3:
        if np.random.random() < v_epsilon:
            action = random.choice(ACTIONS)
        else:
            action = ACTIONS[np.argmax(q_table[state])]
        # action = ACTIONS[np.argmax(q_table[state])]
        next_state = move_q_learning(state, action)
        x,y = next_state
        if x < 0 or x >= rows or y < 0 or y >= cols or maze[x][y] == 1:
            next_state = state
        
        reward = get_reward(next_state, end, maze)
        ep_reward += reward
        current_path.append(state)
        current_state_q_value = q_table[state][ACTIONS.index(action)]
        new_q_value = (1 - c_learning_rate)*current_state_q_value + c_learning_rate * (reward + c_discount_value*np.max(q_table[next_state]))
        q_table[state][ACTIONS.index(action)] = new_q_value

        state = next_state
        step += 1
        if state in end:
            print(f"đã cứu 1 công chúa tại {state[0]}, {state[1]}")
            princess_found += 1
            end.remove(state)
            maze[state[0]][state[1]] = 0
            # for v1, v2 in end:
            #     print(v1, v2)
            if princess_found == 3:
                print(f"đã hoàn thành cứu 3 công chúa tại ep {ep} với reward = {ep_reward}")
                if ep_reward > max_ep_reward:
                    max_ep_reward = ep_reward
                    ep_max = ep
                    successful_paths.append((ep_max, current_path))
        # if ep == 4999:
        #     print_maze(maze, state, end)

    if c_end_ep_epsilon_decay >= ep > c_start_ep_epsilon_decay:
        v_epsilon = v_epsilon - v_epsilon_decay

print(f"Max reward đạt qua tất cả ep là: {max_ep_reward} tại ep {ep_max}")
print(f"giả lập game đã thành công: ")
successful_paths.sort(key=lambda x:x[0], reverse=True)
start = (0, 0)  
end = [(12, 12), (2, 1), (9, 4)]  
for x,y in end:
    maze[x][y] = 2
for my_ep, i in successful_paths:
    for item in i:
        if item in end:
            end.remove(item)
        print_maze(maze, item, end)
    break