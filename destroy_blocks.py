import pygame
import traceback

pygame.init()

# Definir janela que ocorrera o jogo
background_colour = (255,255,255)
(width, height) = (600,600)

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Destroy Blocks")
screen.fill(background_colour)

clock = pygame.time.Clock()

player1_x = 50
player1_y = 440
player2_x = 50
player2_y = 500

def draw():
    global player1_x
    global player1_y
    global player2_x
    global player2_y
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player1_x > 15:
        player1_x -= 1
    if keys[pygame.K_RIGHT] and player1_x < width - 15:
        player1_x += 1
    if keys[pygame.K_a] and player2_x > 15:
        player2_x -= 1
    if keys[pygame.K_d] and player2_x < width - 15:
        player2_x += 1
    screen.fill(background_colour)
    pygame.draw.circle(screen, (255,0,0), (player1_x, player1_y), 15)
    pygame.draw.circle(screen, (255,0,0), (player2_x, player2_y), 15)
    pygame.display.update()
def get_input():
    keys_pressed = pygame.key.get_pressed()
    mouse_buttons = pygame.mouse.get_pressed()
    mouse_position = pygame.mouse.get_pos()
    mouse_rel = pygame.mouse.get_rel()
    for event in pygame.event.get():
        if   event.type == pygame.QUIT: return False
    return True
def main():
    pygame.event.set_grab(True)
    while True:
        if not get_input(): break
        draw()
        clock.tick(72)
    pygame.event.set_grab(False)
    pygame.quit()
if __name__ == "__main__":
    try:
        main()
    except:
        traceback.print_exc()
        pygame.quit()
        input()