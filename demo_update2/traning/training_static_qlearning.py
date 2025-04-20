import random
import time
from collections import deque
import numpy as np
import pickle
import os


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

c_no_of_eps = 10000
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
save_path = "../Hero_game_deepQ/static_model/q_table.pkl"
if os.path.exists(save_path):
    with open(save_path, "rb") as f:
        q_table = pickle.load(f)
else:
    q_table = np.random.uniform(low=-1, high=1, size=(ROWS, COLS, len(ACTIONS)))

best_steps_to_win = float("inf")
def get_reward(current_path, state, end, princess_saved, best_path):
    current_reward = -1
    if state in best_path:
        current_reward += 20
    else:
        current_reward -=4
    if state in end:
        if princess_saved == 1:
            current_reward += 20
        elif princess_saved == 2:
            current_reward += 40
        elif princess_saved == 3:
            current_reward += 60
    if state in current_path:
        current_reward -=5
    return current_reward

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
end = [(12, 12), (2, 1), (9, 4)]  

rows, cols = 13, 13
maze = [[0 for _ in range(cols)] for _ in range(rows)]
fixed_walls = [
    (6, 0), (6, 1), (6, 2), (6, 3), (6, 4), (6, 5), (6, 7), (6, 8), (6, 9), (6, 10), (6, 11), (6, 12),
    (0, 1), (12, 11), (1, 2), (1, 3), (11, 10), (11, 9), (3, 0), (3, 1), (3, 2), (3, 3), (3, 4), (3, 5),
    (2, 6), (0, 9), (0, 10), (2, 8), (2, 9), (2, 10), (2, 11), (3, 10), (4, 3), (5, 7), (4, 7), (5, 11),
    (7, 1), (9, 12), (9, 11), (9, 10), (9, 9), (9, 8), (9, 7), (10, 6), (12, 2), (12, 3), (10, 1),
    (10, 2), (10, 3), (10, 4), (9, 2), (8, 9), (7, 5), (8, 5)
]
for x, y in fixed_walls:
    maze[x][y] = 1

max_step = 200
max_ep_reward = -2000
ep_max = -1

for ep in range(c_no_of_eps):
    print(f"Ep thứ: {ep}")
    maze = [[0 for _ in range(cols)] for _ in range(rows)]
    for x, y in fixed_walls:
        maze[x][y] = 1
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
        if np.random.random() < v_epsilon:
            action = random.choice(ACTIONS)
        else:
            action = ACTIONS[np.argmax(q_table[state])]
        next_state = move_q_learning(state, action)
        x,y = next_state
        if x < 0 or x >= rows or y < 0 or y >= cols or maze[x][y] == 1:
            next_state = state
        
        current_path.append(state)
        reward = get_reward(current_path, next_state, end, princess_found, successful_paths)
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



maze = [[0 for _ in range(COLS)] for _ in range(ROWS)]
for x, y in fixed_walls:
    maze[x][y] = 1

test_princess_found = 0
test_state = (0,0)
current_path = []
temp_end = [(12, 12), (2, 1), (9, 4)]
while test_princess_found < 3:
    test_action = ACTIONS[np.argmax(q_table[test_state])]

    test_next_state = move_q_learning(test_state, test_action)
    x, y = test_next_state
    if x < 0 or x >= ROWS or y < 0 or y >= COLS or maze[x][y] == 1:
        test_next_state = test_state 
    current_path.append(test_state)
    print_maze(maze, test_state, temp_end)
    test_state = test_next_state

    if test_state in temp_end:
        test_princess_found += 1
        temp_end.remove(test_state)
        maze[test_state[0]][test_state[1]] = 0
if princess_found == 3:
    print(f"đã cứu được {test_princess_found} công chúa")