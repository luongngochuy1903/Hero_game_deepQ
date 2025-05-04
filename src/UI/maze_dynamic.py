import pygame
import sys
import numpy as np
import os
import time
from collections import deque

# Thêm đường dẫn đến dynamic_board và algorithms
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from board.dynamic_wall import DynamicBoard
from algorithms.bfs import BFS
from algorithms.dfs import DFS
from algorithms.q_learning_agent_dynamic import QLearningAgent

def run_dynamic_mode():
    # Khởi tạo Pygame
    if not pygame.get_init():
        try:
            pygame.init()
        except Exception as e:
            print(f"Khởi tạo Pygame thất bại: {e}")
            return None

    # Cài đặt cửa sổ
    WIDTH, HEIGHT = 1200, 750
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Chế độ Động")

    # Cài đặt mê cung
    ROWS, COLS = 13, 13
    TILE_SIZE = 40
    PLAYER_SIZE = 90
    OFFSET = (PLAYER_SIZE - TILE_SIZE) // 2
    MAZE_WIDTH = COLS * TILE_SIZE
    MAZE_HEIGHT = ROWS * TILE_SIZE

    # Xác định vị trí mê cung
    LEFT_MAZE_X = 30
    LEFT_MAZE_Y = 70
    RIGHT_MAZE_X = LEFT_MAZE_X + MAZE_WIDTH + 100
    RIGHT_MAZE_Y = 70

    # Tải hình ảnh
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
        bg_maze = pygame.image.load("assets/back_ground/bg_maze_dynamic.png")
        bg_maze = pygame.transform.scale(bg_maze, (WIDTH, HEIGHT))
        bg_algorithm = pygame.image.load("assets/back_ground/bg_algorithm.png")
        bg_algorithm = pygame.transform.scale(bg_algorithm, (WIDTH, HEIGHT))
    except FileNotFoundError as e:
        print(f"Tải hình ảnh thất bại: {e}")
        return None

    # Thêm màu để tô sáng các ô đã thăm
    VISITED_COLOR = (255, 0, 0)  # Màu đỏ cho các ô đã thăm trong quá trình di chuyển

    # Khởi tạo hai instance DynamicBoard
    residents = [(2, 1), (9, 4), (12, 12)]
    board1 = DynamicBoard(ROWS, COLS, residents)
    board1._update_walls(num_walls=20)
    maze_map1 = board1.grid
    player1_pos = list(board1.q_pos)  # Vị trí người chơi mê cung trái (quái vật)
    resident1_pos = board1.residents

    board2 = DynamicBoard(ROWS, COLS, residents)
    board2._update_walls(num_walls=20)
    maze_map2 = board2.grid
    player2_pos = list(board2.q_pos)  # Vị trí người chơi mê cung phải (anh hùng)
    resident2_pos = board2.residents

    # Cài đặt nút
    try:
        button_font = pygame.font.SysFont("arial", 30, bold=True)
        title_font = pygame.font.SysFont("arial", 30, italic=True, bold=True)
    except Exception as e:
        print(f"Tải font thất bại: {e}")
        return None

    # Nút màn hình chính (nằm giữa dưới mê cung)
    button_width, button_height = 150, 50
    button_margin = 20
    button_y = LEFT_MAZE_Y + MAZE_HEIGHT + 50
    total_button_width = 3 * button_width + 2 * button_margin
    start_x = (WIDTH - total_button_width) // 2
    buttons = [
        {"text": "Start", "rect": pygame.Rect(start_x, button_y, button_width, button_height)},
        {"text": "Back", "rect": pygame.Rect(start_x + button_width + button_margin, button_y, button_width, button_height)},
        {"text": "Restart", "rect": pygame.Rect(start_x + 2 * (button_width + button_margin), button_y, button_width, button_height)},
    ]

    # Nút chọn thuật toán (nằm giữa)
    algo_button_width, algo_button_height = 200, 50
    algo_button_margin = 10
    algo_y_start = 280
    algorithms = ["BFS", "DFS", "Q-Learning"]
    left_algo_x = (WIDTH // 4) - (algo_button_width // 2)
    left_algo_buttons = [
        {"text": algo, "rect": pygame.Rect(left_algo_x, algo_y_start + i * (algo_button_height + algo_button_margin), algo_button_width, algo_button_height)}
        for i, algo in enumerate(algorithms)
    ]
    right_algo_x = (3 * WIDTH // 4) - (algo_button_width // 2)
    right_algo_buttons = [
        {"text": algo, "rect": pygame.Rect(right_algo_x, algo_y_start + i * (algo_button_height + algo_button_margin), algo_button_width, algo_button_height)}
        for i, algo in enumerate(algorithms)
    ]
    confirm_cancel_width = 150 + 20 + 150
    confirm_x = (WIDTH - confirm_cancel_width) // 2
    confirm_button = {"text": "Confirm", "rect": pygame.Rect(confirm_x, algo_y_start + 4 * (algo_button_height + algo_button_margin) + 20, 150, 50)}
    cancel_button = {"text": "Cancel", "rect": pygame.Rect(confirm_x + 150 + 20, algo_y_start + 4 * (algo_button_height + algo_button_margin) + 20, 150, 50)}

    # Theo dõi thuật toán, đường đi, danh sách thăm và trạng thái
    left_algo = None
    right_algo = None
    left_visited = []
    right_visited = []
    left_visited_index = 0
    right_visited_index = 0
    left_finished = False
    right_finished = False
    left_visited_residents = []
    right_visited_residents = []
    last_move_time = 0
    last_wall_update_time = 0
    MOVE_DELAY = 0.2
    WALL_UPDATE_INTERVAL = 5.0
    current_mode = "main"

    def draw_maze(maze, offset_x, offset_y, player_pos, resident_pos, visited_residents, player_img, resident_img, visited, current_index):
        # Vẽ lưới mê cung
        for row in range(ROWS):
            for col in range(COLS):
                tile = maze[row][col]
                x = offset_x + col * TILE_SIZE
                y = offset_y + row * TILE_SIZE
                if tile == 1:
                    screen.blit(wall_img, (x, y))
                else:
                    screen.blit(floor_img, (x, y))

        # Vẽ các ô đã thăm (đến chỉ số hiện tại)
        for i, pos in enumerate(visited[:current_index + 1]):
            x = offset_x + pos[1] * TILE_SIZE
            y = offset_y + pos[0] * TILE_SIZE
            pygame.draw.rect(screen, VISITED_COLOR, (x, y, TILE_SIZE, TILE_SIZE), 2)

        # Vẽ cư dân (trừ những người đã thăm)
        for resident in resident_pos:
            if resident not in visited_residents:
                px, py = resident[1] * TILE_SIZE - OFFSET, resident[0] * TILE_SIZE - OFFSET
                screen.blit(resident_img, (offset_x + px, offset_y + py))

        # Vẽ người chơi
        px, py = player_pos[1] * TILE_SIZE - OFFSET, player_pos[0] * TILE_SIZE - OFFSET
        screen.blit(player_img, (offset_x + px, offset_y + py))

    def draw_buttons(button_list, mouse_pos, side=None):
        for button in button_list:
            is_hovered = button["rect"].collidepoint(mouse_pos)
            if is_hovered:
                color = (255, 200, 100)
            else:
                if side == "left":
                    color = (255, 69, 0) if button["text"] == left_algo else (255, 140, 0)
                elif side == "right":
                    color = (255, 69, 0) if button["text"] == right_algo else (255, 140, 0)
                else:
                    color = (255, 140, 0)

            pygame.draw.rect(screen, color, button["rect"], border_radius=10)
            text_surf = button_font.render(button["text"], True, (255, 255, 255))
            text_rect = text_surf.get_rect(center=button["rect"].center)
            screen.blit(text_surf, text_rect)

    def draw_algorithm_select():
        # Vẽ màn hình chọn thuật toán
        screen.blit(bg_algorithm, (0, 0))
        title_left = title_font.render("Left Maze Algorithm", True, (255, 255, 255))
        title_left_rect = title_left.get_rect(center=(left_algo_x + algo_button_width // 2, algo_y_start - 40))
        screen.blit(title_left, title_left_rect)
        title_right = title_font.render("Right Maze Algorithm", True, (255, 255, 255))
        title_right_rect = title_right.get_rect(center=(right_algo_x + algo_button_width // 2, algo_y_start - 40))
        screen.blit(title_right, title_right_rect)
        mouse_pos = pygame.mouse.get_pos()
        draw_buttons(left_algo_buttons, mouse_pos, side="left")
        draw_buttons(right_algo_buttons, mouse_pos, side="right")
        draw_buttons([confirm_button, cancel_button], mouse_pos)

    def get_path(algorithm, board, start):
        # Ánh xạ thuật toán
        algorithm_map = {
            "BFS": BFS,
            "DFS": DFS,
            "Q-Learning": QLearningAgent,
        }
        algo_class = algorithm_map.get(algorithm)
        if algo_class:
            algo_instance = algo_class()
            result = algo_instance.run(board, start)
            path = result.get("path", [])
            visited = result.get("visited", [])
            if not visited:
                print(f"{algorithm}: Không tìm thấy đường đi hợp lệ")
                return [], []
            if not path and len(visited) > 1:
                print(f"{algorithm}: Không tìm thấy cư dân, nhưng có đường đi tạm thời")
            print(f"Thứ tự thăm của {algorithm}: {visited}")
            return visited, path
        else:
            print(f"Thuật toán {algorithm} không tồn tại")
            return [], []

    def update_walls(board, maze_map, num_walls):
        # Cập nhật tường động
        board._update_walls(num_walls)
        return board.grid

    clock = pygame.time.Clock()
    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        current_time = time.time()

        # Cập nhật tường định kỳ và tìm lại đường đi
        if current_mode == "moving" and current_time - last_wall_update_time >= WALL_UPDATE_INTERVAL:
            if not left_finished:
                maze_map1 = update_walls(board1, maze_map1, num_walls=20)
                left_visited, left_path = get_path(left_algo, board1, tuple(player1_pos))
                left_visited_index = 0
                if not left_visited:
                    print("Mê cung trái: Không tìm thấy đường đi, chờ cập nhật tường tiếp theo")
                else:
                    print("Mê cung trái: Đã tìm thấy đường đi mới sau khi cập nhật tường")

            if not right_finished:
                maze_map2 = update_walls(board2, maze_map2, num_walls=20)
                right_visited, right_path = get_path(right_algo, board2, tuple(player2_pos))
                right_visited_index = 0
                if not right_visited:
                    print("Mê cung phải: Không tìm thấy đường đi, chờ cập nhật tường tiếp theo")
                else:
                    print("Mê cung phải: Đã tìm thấy đường đi mới sau khi cập nhật tường")

            last_wall_update_time = current_time
            print("Đã cập nhật tường cho các mê cung chưa hoàn tất")

        if current_mode == "main":
            screen.blit(bg_maze, (0, 0))
            draw_maze(maze_map1, LEFT_MAZE_X, LEFT_MAZE_Y, player1_pos, resident1_pos, left_visited_residents, monster_img, resident_img, left_visited, left_visited_index)
            draw_maze(maze_map2, RIGHT_MAZE_X, RIGHT_MAZE_Y, player2_pos, resident2_pos, right_visited_residents, hero_img, resident_img, right_visited, right_visited_index)
            draw_buttons(buttons, mouse_pos)
        elif current_mode == "algorithm_select":
            draw_algorithm_select()
        elif current_mode == "moving":
            screen.blit(bg_maze, (0, 0))
            draw_maze(maze_map1, LEFT_MAZE_X, LEFT_MAZE_Y, player1_pos, resident1_pos, left_visited_residents, monster_img, resident_img, left_visited, left_visited_index)
            draw_maze(maze_map2, RIGHT_MAZE_X, RIGHT_MAZE_Y, player2_pos, resident2_pos, right_visited_residents, hero_img, resident_img, right_visited, right_visited_index)
            draw_buttons(buttons, mouse_pos)

            if current_time - last_move_time >= MOVE_DELAY:
                # Xử lý mê cung trái nếu chưa hoàn tất
                if not left_finished and left_visited_index < len(left_visited):
                    next_pos = left_visited[left_visited_index]
                    if board1.is_valid_move(next_pos):
                        player1_pos = list(next_pos)
                        if tuple(player1_pos) in resident1_pos and tuple(player1_pos) not in left_visited_residents:
                            left_visited_residents.append(tuple(player1_pos))
                            print(f"Mê cung trái: Đã đến cư dân tại {player1_pos}")
                        if len(left_visited_residents) == len(resident1_pos):
                            left_finished = True
                            print("Mê cung trái: Đã tìm thấy tất cả cư dân, dừng thuật toán")
                        else:
                            left_visited_index += 1
                    else:
                        print(f"Mê cung trái: Đường đi bị chặn tại {next_pos}, chờ cập nhật tường")
                        left_visited, left_path = get_path(left_algo, board1, tuple(player1_pos))
                        left_visited_index = 0
                        if not left_visited:
                            print("Mê cung trái: Không tìm thấy đường đi, chờ cập nhật tường tiếp theo")

                # Xử lý mê cung phải nếu chưa hoàn tất
                if not right_finished and right_visited_index < len(right_visited):
                    next_pos = right_visited[right_visited_index]
                    if board2.is_valid_move(next_pos):
                        player2_pos = list(next_pos)
                        if tuple(player2_pos) in resident2_pos and tuple(player2_pos) not in right_visited_residents:
                            right_visited_residents.append(tuple(player2_pos))
                            print(f"Mê cung phải: Đã đến cư dân tại {player2_pos}")
                        if len(right_visited_residents) == len(resident2_pos):
                            right_finished = True
                            print("Mê cung phải: Đã tìm thấy tất cả cư dân, dừng thuật toán")
                        else:
                            right_visited_index += 1
                    else:
                        print(f"Mê cung phải: Đường đi bị chặn tại {next_pos}, chờ cập nhật tường")
                        right_visited, right_path = get_path(right_algo, board2, tuple(player2_pos))
                        right_visited_index = 0
                        if not right_visited:
                            print("Mê cung phải: Không tìm thấy đường đi, chờ cập nhật tường tiếp theo")

                if left_finished and right_finished:
                    print("Cả hai mê cung: Đã tìm thấy tất cả cư dân, dừng thuật toán")
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
                            print(f"Đã nhấn {button['text']}")
                            if button["text"] == "Back":
                                return "mode_select"
                            elif button["text"] == "Start":
                                current_mode = "algorithm_select"
                            elif button["text"] == "Restart":
                                player1_pos = list(board1.q_pos)
                                player2_pos = list(board2.q_pos)
                                left_visited_residents = []
                                right_visited_residents = []
                                left_visited = []
                                right_visited = []
                                left_visited_index = 0
                                right_visited_index = 0
                                left_finished = False
                                right_finished = False
                                last_move_time = 0
                                last_wall_update_time = 0
                                left_algo = None
                                right_algo = None
                                board1._update_walls(num_walls=20)
                                board2._update_walls(num_walls=20)
                                maze_map1 = board1.grid
                                maze_map2 = board2.grid
                                print("Trò chơi đã khởi động lại")
                            break
                elif current_mode == "algorithm_select":
                    for button in left_algo_buttons:
                        if button["rect"].collidepoint(mouse_pos):
                            left_algo = button["text"]
                            print(f"Đã chọn thuật toán mê cung trái: {left_algo}")
                            break
                    for button in right_algo_buttons:
                        if button["rect"].collidepoint(mouse_pos):
                            right_algo = button["text"]
                            print(f"Đã chọn thuật toán mê cung phải: {right_algo}")
                            break
                    if confirm_button["rect"].collidepoint(mouse_pos):
                        if left_algo and right_algo:
                            print(f"Xác nhận thuật toán: Trái={left_algo}, Phải={right_algo}")
                            start_pos = tuple(board1.q_pos)  # Sử dụng vị trí ban đầu của board
                            left_visited, left_path = get_path(left_algo, board1, start_pos)
                            right_visited, right_path = get_path(right_algo, board2, start_pos)
                            current_mode = "moving"
                            left_visited_index = 0
                            right_visited_index = 0
                            left_finished = False
                            right_finished = False
                            last_move_time = current_time
                            last_wall_update_time = current_time
                        else:
                            print("Vui lòng chọn thuật toán cho cả hai mê cung")
                    elif cancel_button["rect"].collidepoint(mouse_pos):
                        left_algo = None
                        right_algo = None
                        current_mode = "main"

        pygame.display.flip()
        clock.tick(60)

    return None

if __name__ == "__main__":
    run_dynamic_mode()