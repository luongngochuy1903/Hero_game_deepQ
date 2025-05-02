import pygame
import sys
from UI.maze_static import run_static_mode
from UI.maze_dynamic import run_dynamic_mode

def run_menu():
    # Khởi tạo Pygame
    if not pygame.get_init():
        try:
            pygame.init()
        except Exception as e:
            print(f"Pygame initialization failed: {e}")
            return None
        
    pygame.mixer.init()

    # #Tải và phát nhạc nền
    # pygame.mixer.music.load("assets/sounds/horror-tension-suspense-322304.mp3")  # Đường dẫn tới tệp nhạc
    # pygame.mixer.music.play(-1)  # -1 để phát lặp vô hạn

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

    # Font
    button_font = pygame.font.SysFont("Arial", 36, bold=True)  # Change to bold instead of italic

    # Nút chế độ
    button_width = 200
    button_height = 60
    button_spacing = 30

    # Tính vị trí X sao cho các nút canh giữa màn hình
    center_x = WIDTH // 2 - button_width // 2

    # Tính vị trí Y bắt đầu (từ trên xuống)
    start_y = 225

    # Tạo danh sách các nút
    buttons = [
        {"text": "Dynamic", "rect": pygame.Rect(center_x, start_y, button_width, button_height)},
        {"text": "Static", "rect": pygame.Rect(center_x, start_y + button_height + button_spacing, button_width, button_height)},
        {"text": "Quit", "rect": pygame.Rect(center_x, start_y + 2 * (button_height + button_spacing), button_width, button_height)},
    ]

    # Hàm vẽ nút
    def draw_buttons(button_list, mouse_pos):
        for button in button_list:
            is_hovered = button["rect"].collidepoint(mouse_pos)
            if is_hovered:
                color = (255, 200, 100)  # Lighter orange for hover effect
            else:
                color = (255, 140, 0)  # Default orange

            pygame.draw.rect(screen, color, button["rect"], border_radius=20)
            text_surf = button_font.render(button["text"], True, (WHITE))
            text_rect = text_surf.get_rect(center=button["rect"].center)
            screen.blit(text_surf, text_rect)

    # Vòng lặp chính
    current_screen = "menu"
    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()  # Get mouse position for hover effect

        if current_screen == "menu":
            screen.blit(menu_img, (0, 0))
            # Hướng dẫn bấm space
            hint_surface = button_font.render("PRESS SPACE TO START", True, WHITE)
            hint_rect = hint_surface.get_rect(center=(WIDTH//2, HEIGHT - 50))
            screen.blit(hint_surface, hint_rect)

        elif current_screen == "mode_select":
            screen.blit(select_mode_img, (0, 0))
            draw_buttons(buttons, mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if current_screen == "menu" and event.key == pygame.K_SPACE:
                    current_screen = "mode_select"

            if event.type == pygame.MOUSEBUTTONDOWN:
                if current_screen == "mode_select":
                    for button in buttons:
                        if button["rect"].collidepoint(event.pos):
                            if button["text"] == "Dynamic":
                                pygame.mixer.music.stop()
                                run_dynamic_mode()
                            elif button["text"] == "Static":
                                pygame.mixer.music.stop()
                                run_static_mode()
                            elif button["text"] == "Quit":
                                pygame.quit()

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    run_menu()