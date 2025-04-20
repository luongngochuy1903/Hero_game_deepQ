import pygame
import sys

def run_static_mode():
    # Khởi tạo
    pygame.init()

    WIDTH, HEIGHT = 1024, 750
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Mode Static")

    ROWS, COLS = 15, 10
    TILE_SIZE = 40
    PLAYER_SIZE = 90
    OFFSET = (PLAYER_SIZE - TILE_SIZE) // 2

    wall_img = pygame.image.load("assets/build_maze/wall.png")
    wall_img = pygame.transform.scale(wall_img, (TILE_SIZE, TILE_SIZE))
    floor_img = pygame.image.load("assets/build_maze/floor.png")
    floor_img = pygame.transform.scale(floor_img, (TILE_SIZE, TILE_SIZE))
    hero_img = pygame.image.load("assets/characters/hero.png")
    hero_img = pygame.transform.scale(hero_img, (PLAYER_SIZE, PLAYER_SIZE))
    monster_img = pygame.image.load("assets/characters/monster.png")
    monster_img = pygame.transform.scale(monster_img, (PLAYER_SIZE, PLAYER_SIZE))

    maze_map = [
        [1,1,1,1,1,1,1,1,1,1],
        [1,0,0,0,1,0,0,0,0,1],
        [1,0,1,0,1,0,1,1,0,1],
        [1,0,1,0,0,0,0,1,0,1],
        [1,0,1,1,1,1,0,1,0,1],
        [1,0,0,0,0,1,0,1,0,1],
        [1,1,1,1,0,1,0,1,0,1],
        [1,0,0,1,0,0,0,1,0,1],
        [1,0,0,0,0,1,0,0,0,1],
        [1,1,1,1,1,1,1,1,1,1],
        [1,0,0,0,0,0,0,0,0,1],
        [1,0,1,1,1,1,1,1,0,1],
        [1,0,0,0,0,0,0,1,0,1],
        [1,1,1,1,1,1,0,1,0,1],
        [1,1,1,1,1,1,1,1,1,1],
    ]

    player1_pos = [1, 1]
    player2_pos = [1, 1]

    def draw_maze(maze, offset_x, player_pos):
        for row in range(ROWS):
            for col in range(COLS):
                tile = maze[row][col]
                x = offset_x + col * TILE_SIZE
                y = row * TILE_SIZE
                if tile == 1:
                    screen.blit(wall_img, (x, y))
                else:
                    screen.blit(floor_img, (x, y))

        # Vẽ người chơi
        px, py = player_pos[1] * TILE_SIZE - OFFSET, player_pos[0] * TILE_SIZE - OFFSET
        screen.blit(hero_img if offset_x != WIDTH//2 + 50 else monster_img, (offset_x + px, py))

    clock = pygame.time.Clock()
    running = True
    while running:
        screen.fill((0, 0, 0))
        draw_maze(maze_map, 50, player1_pos)
        draw_maze(maze_map, WIDTH//2 + 50, player2_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()