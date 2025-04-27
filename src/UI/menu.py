import pygame
import sys
from UI.maze_static import run_static_mode
# from maze_dynamic import run_dynamic_mode

def run_menu():
    # Khởi tạo Pygame
    if not pygame.get_init():
        try:
            pygame.init()
        except Exception as e:
            print(f"Pygame initialization failed: {e}")
            return None
        
    pygame.mixer.init()

    # Tải và phát nhạc nền
    pygame.mixer.music.load("assets/sounds/horror-tension-suspense-322304.mp3")  # Đường dẫn tới tệp nhạc
    pygame.mixer.music.play(-1)  # -1 để phát lặp vô hạn

    # Cửa sổ game
    WIDTH, HEIGHT = 1200, 750
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("RESCUE THE RESIDENTS")

    # Load ảnh nền
    menu_img = pygame.image.load("assets/back_ground/bg_menu.png")
    menu_img = pygame.transform.scale(menu_img, (WIDTH, HEIGHT))
    select_mode_img = pygame.image.load("assets/back_ground/bg_select_mode.png")
    select_mode_img = pygame.transform.scale(select_mode_img, (WIDTH, HEIGHT))

    # Màu sắc
    WHITE = (255, 255, 255)
    BROWN = (139, 69, 19)

    # Font
    button_font = pygame.font.SysFont("Arial", 36, "ITALIC")

    # Nút chế độ
    # Kích thước và khoảng cách giữa các nút
    button_width = 200
    button_height = 60
    button_spacing = 30  # khoảng cách giữa các nút

    # Tính vị trí X sao cho các nút canh giữa màn hình
    center_x = WIDTH // 2 - button_width // 2

    # Tính vị trí Y bắt đầu (từ trên xuống)
    start_y = 225

    # Tạo các nút theo hàng dọc
    dynamic_button = pygame.Rect(center_x, start_y, button_width, button_height)
    static_button  = pygame.Rect(center_x, start_y + button_height + button_spacing, button_width, button_height)
    quit_button    = pygame.Rect(center_x, start_y + 2 * (button_height + button_spacing), button_width, button_height)

    # Hàm vẽ nút
    def draw_button(rect, image_path):
        img = pygame.image.load(image_path).convert_alpha()
        img = pygame.transform.scale(img, (rect.width, rect.height))
        screen.blit(img, rect.topleft)
        
    # Vòng lặp chính
    current_screen = "menu" # Trạng thái màn hình
    running = True
    while running:
        if current_screen == "menu":
            screen.blit(menu_img, (0, 0))
            # Hướng dẫn bấm space
            hint_surface = button_font.render("PRESS SPACE TO START", True, WHITE)
            hint_rect = hint_surface.get_rect(center=(WIDTH//2, HEIGHT - 50))  # Dịch xuống dưới cùng
            screen.blit(hint_surface, hint_rect)

        elif current_screen == "mode_select":
            screen.blit(select_mode_img, (0, 0))
            draw_button(dynamic_button, "assets/buttons/button_dynamic.png")
            draw_button(static_button, "assets/buttons/button_static.png")
            draw_button(quit_button, "assets/buttons/button_quit.png")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if current_screen == "menu" and event.key == pygame.K_SPACE:
                    current_screen = "mode_select"

            if event.type == pygame.MOUSEBUTTONDOWN:
                if current_screen == "mode_select":
                    if dynamic_button.collidepoint(event.pos):
                        pygame.mixer.music.stop()
                        print("hí")
                        # run_dynamic_mode()
                    elif static_button.collidepoint(event.pos):
                        pygame.mixer.music.stop()
                        run_static_mode()
                    elif quit_button.collidepoint(event.pos):
                        pygame.quit()

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    run_menu()