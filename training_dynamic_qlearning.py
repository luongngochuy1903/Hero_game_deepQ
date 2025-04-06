import random
import time
from collections import deque
import numpy as np
import pickle
import os

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

c_learning_rate = 0.2
c_discount_value = 0.9

c_no_of_eps = 8000
v_epsilon = 0.9
c_start_ep_epsilon_decay = 1
c_end_ep_epsilon_decay = c_no_of_eps // 1.5
v_epsilon_decay = v_epsilon / (c_end_ep_epsilon_decay - c_start_ep_epsilon_decay)

successful_paths = []

DIRECTION = [(-1, 0), (1, 0), (0, -1), (0, 1)]
ACTIONS = ["UP", "DOWN", "LEFT", "RIGHT"]
state_size = [13, 13]
ROWS = 13
COLS = 13
q_table = None
save_path = "A:/AI_cuoiki/Hero_game_deepQ/dynamic_model/q_table.pkl"
if os.path.exists(save_path):
    with open(save_path, "rb") as f:
        q_table = pickle.load(f)
else:
    q_table = np.random.uniform(low=-1, high=1, size=(ROWS, COLS, len(ACTIONS)))

def get_reward(current_path, state, end, maze):
    if state in end:
        return 69
    if state in current_path:
        return -4
    return -2

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

rows, cols = 13, 13
maze = [[0 for _ in range(cols)] for _ in range(rows)]
num_walls = 20  
maze = update_walls(maze, num_walls, end)

max_step = 200
max_ep_reward = -2000
ep_max = -1

for ep in range(c_no_of_eps):
    print(f"Ep thứ: {ep}")
    maze = [[0 for _ in range(cols)] for _ in range(rows)]
    num_walls = 20  
    maze = update_walls(maze, num_walls, end)
    start = (0, 0)  
    end = [(12, 12), (2, 1), (9, 4)]  
    for x,y in end:
        maze[x][y] = 2
    ep_reward = 0
    state = start
    step = 0
    count_to_change = 0
    princess_found = 0
    current_path = []
    while step < max_step and princess_found < 3:
        if count_to_change == 3:
            count_to_change = 0
            maze = update_walls(maze, num_walls, end)
        
        if np.random.random() < v_epsilon:
            action = random.choice(ACTIONS)
        else:
            action = ACTIONS[np.argmax(q_table[state])]
        next_state = move_q_learning(state, action)
        x,y = next_state
        if x < 0 or x >= rows or y < 0 or y >= cols or maze[x][y] == 1:
            next_state = state
        
        current_path.append(state)
        reward = get_reward(current_path, next_state, end, maze)
        ep_reward += reward
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

            if princess_found == 3:
                print(f"đã hoàn thành cứu 3 công chúa tại ep {ep} với reward = {ep_reward}")
                if ep_reward > max_ep_reward:
                    max_ep_reward = ep_reward
                    ep_max = ep
                    successful_paths.append((ep_max, current_path))
        if ep == 7999:
            print_maze(maze, state, end)
            print(f"Q value của state hiện tại: {q_table[state]}")

        count_to_change += 1

    if c_end_ep_epsilon_decay >= ep > 0.25:
        v_epsilon = v_epsilon - v_epsilon_decay


with open(save_path, "wb") as f:
    pickle.dump(q_table, f)
successful_paths.sort(key=lambda x:x[0], reverse=True)