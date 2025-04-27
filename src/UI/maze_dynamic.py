import pygame
import sys
import numpy as np
import os
import time
from collections import deque

# Add path to dynamic_board and algorithms
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from board.dynamic_wall import DynamicBoard
from algorithms.bfs import BFS
from algorithms.dfs import DFS
from algorithms.dijkstra import Dijkstra
from algorithms.q_learning_agent_dynamic import QLearningAgent

def run_dynamic_mode():
    # Initialize Pygame
    if not pygame.get_init():
        try:
            pygame.init()
        except Exception as e:
            print(f"Pygame initialization failed: {e}")
            return None

    # Window settings
    WIDTH, HEIGHT = 1200, 750
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Mode Dynamic")

    # Maze settings
    ROWS, COLS = 13, 13
    TILE_SIZE = 40
    PLAYER_SIZE = 90
    OFFSET = (PLAYER_SIZE - TILE_SIZE) // 2
    MAZE_WIDTH = COLS * TILE_SIZE
    MAZE_HEIGHT = ROWS * TILE_SIZE

    # Load images
    try:
        wall_img = pygame.image.load("assets/build_maze/wall.png")
        wall_img = pygame.transform.scale(wall_img, (TILE_SIZE, TILE_SIZE))
        floor_img = pygame.image.load("assets/build_maze/floor.png")
        floor_img = pygame.transform.scale(floor_img, (TILE_SIZE, TILE_SIZE))
        hero_img = pygame.image.load("assets/characters/hero.png")
        hero_img = pygame.transform.scale(hero_img, (PLAYER_SIZE, PLAYER_SIZE))
        monster_img = pygame.image.load("assets/characters/monster.png")
        monster_img = pygame.transform.scale(monster_img, (PLAYER_SIZE, PLAYER_SIZE))
        resident_img = pygame.image.load("assets/characters/resident.png")
        resident_img = pygame.transform.scale(resident_img, (PLAYER_SIZE, PLAYER_SIZE))
    except FileNotFoundError as e:
        print(f"Image loading failed: {e}")
        return None

    # Initialize two DynamicBoard instances
    residents = [(2, 1), (9, 4), (12, 12)]
    board1 = DynamicBoard(ROWS, COLS, residents)
    board1._update_walls(num_walls=20)  # Initialize with 20 walls (adjust as needed)
    maze_map1 = board1.grid
    player1_pos = list(board1.q_pos)  # Left maze player (monster)
    resident1_pos = board1.princesses

    board2 = DynamicBoard(ROWS, COLS, residents)
    board2._update_walls(num_walls=20)  # Initialize with 20 walls
    maze_map2 = board2.grid
    player2_pos = list(board2.q_pos)  # Right maze player (hero)
    resident2_pos = board2.princesses

    # Button settings
    try:
        font = pygame.font.SysFont("arial", 30)
    except Exception as e:
        print(f"Font loading failed: {e}")
        return None

    # Main screen buttons (centered)
    button_width, button_height = 150, 50
    button_margin = 20
    button_y = MAZE_HEIGHT + 50
    total_button_width = 3 * button_width + 2 * button_margin
    start_x = (WIDTH - total_button_width) // 2
    buttons = [
        {"text": "Start", "rect": pygame.Rect(start_x, button_y, button_width, button_height)},
        {"text": "Back", "rect": pygame.Rect(start_x + button_width + button_margin, button_y, button_width, button_height)},
        {"text": "Restart", "rect": pygame.Rect(start_x + 2 * (button_width + button_margin), button_y, button_width, button_height)},
    ]

    # Algorithm selection buttons (centered)
    algo_button_width, algo_button_height = 200, 50
    algo_button_margin = 10
    algo_y_start = 100
    algorithms = ["BFS", "DFS", "Dijkstra", "Q-Learning"]
    left_algo_x = (WIDTH // 4) - (algo_button_width // 2)  # 200
    left_algo_buttons = [
        {"text": algo, "rect": pygame.Rect(left_algo_x, algo_y_start + i * (algo_button_height + algo_button_margin), algo_button_width, algo_button_height)}
        for i, algo in enumerate(algorithms)
    ]
    right_algo_x = (3 * WIDTH // 4) - (algo_button_width // 2)  # 800
    right_algo_buttons = [
        {"text": algo, "rect": pygame.Rect(right_algo_x, algo_y_start + i * (algo_button_height + algo_button_margin), algo_button_width, algo_button_height)}
        for i, algo in enumerate(algorithms)
    ]
    confirm_cancel_width = 150 + 20 + 150
    confirm_x = (WIDTH - confirm_cancel_width) // 2
    confirm_button = {"text": "Confirm", "rect": pygame.Rect(confirm_x, algo_y_start + 4 * (algo_button_height + algo_button_margin) + 20, 150, 50)}
    cancel_button = {"text": "Cancel", "rect": pygame.Rect(confirm_x + 150 + 20, algo_y_start + 4 * (algo_button_height + algo_button_margin) + 20, 150, 50)}

    # Track selected algorithms, paths, and visited residents
    left_algo = None
    right_algo = None
    left_path = []  # Single path to all residents for left maze
    right_path = []  # Single path to all residents for right maze
    current_path_index = 0  # Index in the path for movement
    left_finished = False  # Track if left maze has finished
    right_finished = False  # Track if right maze has finished
    left_visited_residents = []  # Track residents visited by left maze
    right_visited_residents = []  # Track residents visited by right maze
    last_move_time = 0
    last_wall_update_time = 0
    MOVE_DELAY = 0.5  # Seconds between moves
    WALL_UPDATE_INTERVAL = 5.0  # Seconds between wall updates
    current_mode = "main"  # main, algorithm_select, moving

    def draw_maze(maze, offset_x, player_pos, resident_pos, visited_residents, player_img, resident_img):
        for row in range(ROWS):
            for col in range(COLS):
                tile = maze[row][col]
                x = offset_x + col * TILE_SIZE
                y = row * TILE_SIZE
                if tile == 1:
                    screen.blit(wall_img, (x, y))
                else:
                    screen.blit(floor_img, (x, y))

        # Draw only residents that haven't been visited
        for resident in resident_pos:
            if resident not in visited_residents:
                px, py = resident[1] * TILE_SIZE - OFFSET, resident[0] * TILE_SIZE - OFFSET
                screen.blit(resident_img, (offset_x + px, py))

        px, py = player_pos[1] * TILE_SIZE - OFFSET, player_pos[0] * TILE_SIZE - OFFSET
        screen.blit(player_img, (offset_x + px, py))

    def draw_buttons(button_list):
        for button in button_list:
            color = (150, 150, 150) if button["text"] in [left_algo, right_algo] else (100, 100, 100)
            pygame.draw.rect(screen, color, button["rect"])
            text_surf = font.render(button["text"], True, (255, 255, 255))
            text_rect = text_surf.get_rect(center=button["rect"].center)
            screen.blit(text_surf, text_rect)

    def draw_algorithm_select():
        screen.fill((0, 0, 0))
        title_left = font.render("Left Maze Algorithm", True, (255, 255, 255))
        title_left_rect = title_left.get_rect(center=(left_algo_x + algo_button_width // 2, algo_y_start - 40))
        screen.blit(title_left, title_left_rect)
        title_right = font.render("Right Maze Algorithm", True, (255, 255, 255))
        title_right_rect = title_right.get_rect(center=(right_algo_x + algo_button_width // 2, algo_y_start - 40))
        screen.blit(title_right, title_right_rect)
        draw_buttons(left_algo_buttons)
        draw_buttons(right_algo_buttons)
        draw_buttons([confirm_button, cancel_button])

    def get_path(algorithm, board, start):
        algorithm_map = {
            "BFS": BFS,
            "DFS": DFS,
            "Dijkstra": Dijkstra,
            "Q-Learning": QLearningAgent,
        }
        algo_class = algorithm_map.get(algorithm)
        if algo_class:
            # Instantiate the class
            if algorithm == "Q-Learning":
                algo_instance = algo_class()  # QLearningAgent may need specific initialization
            else:
                algo_instance = algo_class()
            result = algo_instance.run(board, start)
            path = result.get("path", [])
            if not path:
                print(f"{algorithm} failed to find a path to residents")
            return path
        else:
            print(f"Algorithm {algorithm} not found")
            return []

    def update_walls(board, maze_map, num_walls):
        """Update walls on the board and refresh the maze map."""
        board._update_walls(num_walls)
        return board.grid

    clock = pygame.time.Clock()
    running = True
    while running:
        screen.fill((0, 0, 0))

        # Update walls periodically in moving mode
        current_time = time.time()
        if current_mode == "moving" and current_time - last_wall_update_time >= WALL_UPDATE_INTERVAL:
            maze_map1 = update_walls(board1, maze_map1, num_walls=20)
            maze_map2 = update_walls(board2, maze_map2, num_walls=20)
            last_wall_update_time = current_time
            print("Walls updated for both mazes")

        if current_mode == "main":
            draw_maze(maze_map1, 50, player1_pos, resident1_pos, left_visited_residents, monster_img, resident_img)
            draw_maze(maze_map2, 50 + MAZE_WIDTH + 50, player2_pos, resident2_pos, right_visited_residents, hero_img, resident_img)
            draw_buttons(buttons)
        elif current_mode == "algorithm_select":
            draw_algorithm_select()
        elif current_mode == "moving":
            draw_maze(maze_map1, 50, player1_pos, resident1_pos, left_visited_residents, monster_img, resident_img)
            draw_maze(maze_map2, 50 + MAZE_WIDTH + 50, player2_pos, resident2_pos, right_visited_residents, hero_img, resident_img)
            draw_buttons(buttons)

            # Move players along their paths
            if current_time - last_move_time >= MOVE_DELAY:
                # Left maze
                if not left_finished and current_path_index < len(left_path):
                    next_pos = left_path[current_path_index]
                    # Check if the next position is valid after wall updates
                    if board1.is_valid_move(next_pos):
                        player1_pos = list(next_pos)
                        # Check if the current position is a resident
                        if tuple(player1_pos) in resident1_pos and tuple(player1_pos) not in left_visited_residents:
                            left_visited_residents.append(tuple(player1_pos))
                            print(f"Left maze: Reached resident at {player1_pos}, removing from display")
                        if current_path_index == len(left_path) - 1:
                            left_finished = True
                            print("Left maze: All residents reached, waiting for right maze")
                    else:
                        # Path is blocked; recompute path from current position
                        print(f"Left maze: Path blocked at {next_pos}, recomputing path")
                        left_path = get_path(left_algo, board1, tuple(player1_pos))
                        current_path_index = 0
                        left_finished = False
                        if not left_path:
                            left_finished = True
                            print("Left maze: No valid path found after wall update")
                # Right maze
                if not right_finished and current_path_index < len(right_path):
                    next_pos = right_path[current_path_index]
                    # Check if the next position is valid after wall updates
                    if board2.is_valid_move(next_pos):
                        player2_pos = list(next_pos)
                        # Check if the current position is a resident
                        if tuple(player2_pos) in resident2_pos and tuple(player2_pos) not in right_visited_residents:
                            right_visited_residents.append(tuple(player2_pos))
                            print(f"Right maze: Reached resident at {player2_pos}, removing from display")
                        if current_path_index == len(right_path) - 1:
                            right_finished = True
                            print("Right maze: All residents reached, waiting for left maze")
                    else:
                        # Path is blocked; recompute path from current position
                        print(f"Right maze: Path blocked at {next_pos}, recomputing path")
                        right_path = get_path(right_algo, board2, tuple(player2_pos))
                        current_path_index = 0
                        right_finished = False
                        if not right_path:
                            right_finished = True
                            print("Right maze: No valid path found after wall update")
                # Increment index only if at least one maze is still moving
                if not (left_finished and right_finished):
                    current_path_index += 1
                # Check if both mazes have finished
                if left_finished and right_finished:
                    print("Both mazes: All residents reached or no valid paths")
                    current_mode = "main"
                last_move_time = current_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return None
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if current_mode == "main":
                    for button in buttons:
                        if button["rect"].collidepoint(mouse_pos):
                            print(f"{button['text']} clicked")
                            if button["text"] == "Back":
                                return "mode_select"
                            elif button["text"] == "Start":
                                current_mode = "algorithm_select"
                            elif button["text"] == "Restart":
                                # Reset game state to start from the beginning
                                player1_pos = list(board1.q_pos)  # Reset to (0, 0)
                                player2_pos = list(board2.q_pos)  # Reset to (0, 0)
                                left_visited_residents = []  # Clear visited residents
                                right_visited_residents = []  # Clear visited residents
                                left_path = []  # Clear path
                                right_path = []  # Clear path
                                current_path_index = 0  # Reset path index
                                left_finished = False  # Reset finished flag
                                right_finished = False  # Reset finished flag
                                last_move_time = 0  # Reset move timer
                                last_wall_update_time = 0  # Reset wall update timer
                                left_algo = None  # Clear selected algorithm
                                right_algo = None  # Clear selected algorithm
                                # Regenerate boards
                                board1._update_walls(num_walls=20)
                                board2._update_walls(num_walls=20)
                                maze_map1 = board1.grid
                                maze_map2 = board2.grid
                                print("Game restarted")
                            break
                elif current_mode == "algorithm_select":
                    for button in left_algo_buttons:
                        if button["rect"].collidepoint(mouse_pos):
                            left_algo = button["text"]
                            print(f"Left maze algorithm selected: {left_algo}")
                            break
                    for button in right_algo_buttons:
                        if button["rect"].collidepoint(mouse_pos):
                            right_algo = button["text"]
                            print(f"Right maze algorithm selected: {right_algo}")
                            break
                    if confirm_button["rect"].collidepoint(mouse_pos):
                        if left_algo and right_algo:
                            print(f"Algorithms confirmed: Left={left_algo}, Right={right_algo}")
                            # Compute a single path to all residents for each maze
                            start_pos = (0, 0)
                            left_path = get_path(left_algo, board1, start_pos)
                            right_path = get_path(right_algo, board2, start_pos)
                            current_mode = "moving"
                            current_path_index = 0
                            left_finished = False
                            right_finished = False
                            last_move_time = current_time
                            last_wall_update_time = current_time
                        else:
                            print("Please select an algorithm for both mazes")
                    elif cancel_button["rect"].collidepoint(mouse_pos):
                        left_algo = None
                        right_algo = None
                        current_mode = "main"

        pygame.display.flip()
        clock.tick(60)

    return None

if __name__ == "__main__":
    run_dynamic_mode()