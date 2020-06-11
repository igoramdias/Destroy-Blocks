import pygame
import traceback
from collections import deque
import random

pygame.init()

# Definir janela que ocorrera o jogo
background_colour = (255,255,255)
(width, height) = (600,600)

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Destroy Blocks")

clock = pygame.time.Clock()
font12 = pygame.font.SysFont("Times New Roman",12)
font18 = pygame.font.SysFont("Times New Roman",18)
font24 = pygame.font.SysFont("Times New Roman",24)

BLUE = (0,0,255)
RED = (255,0,0)
refresh = 300
blink = -1*refresh/2

'''class Game():
    def run(self):
        running = True
        while running:
            running = self.get_input
            self.draw
            clock.tick(300)

    def draw():
        global player1_x
        global player1_y
        global player2_x
        global player2_y
        screen.fill(background_colour)
        pygame.draw.circle(screen, (255,0,0), (player1_x, player1_y), 15)
        pygame.draw.circle(screen, (255,0,0), (player2_x, player2_y), 15)
        pygame.display.update()

    def get_input():
        global player1_x
        global player1_y
        global player2_x
        global player2_y
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event == pygame.QUIT: return False
            if event == pygame.K_ESCAPE : return False
            if event == pygame.K_LEFT and player1_x > 15:
                player1_x -= 1
            if event == pygame.K_RIGHT and player1_x < width - 15:
                player1_x += 1
            if event == pygame.K_a and player2_x > 15:
                player2_x -= 1
            if event == pygame.K_d and player2_x < width - 15:
                player2_x += 1
        pygame.display.update()
        return True'''



blocks_type = deque()
line_org = [0,0,0,0]
score_1 = 0
score_2 = 0

class Game():
    

def movement():
    for i in range(0,2): line_org[2*i+1] = 1
    if blocks_type and blocks_type[0][1][1] > height:
        blocks_type.popleft()
    for elem in blocks_type:
        elem[1][1] = elem[1][1] + 1
        if line_org[2*elem[3]] > 0 and line_org[2*elem[3]+1] == 1: 
            line_org[2*elem[3]] = line_org[2*elem[3]] - 1
            line_org[2*elem[3]+1] = 0
        pygame.draw.rect(screen, elem[0], (elem[1][0], elem[1][1], elem[1][2], elem[1][3]))
    
    line = random.randrange(1,7)
    color = random.randrange(2)
    if line_org[2*color] == 0:
        if blocks_type and blocks_type[-1][2] == line: return
        if color: block = [RED, [75*line,0,50,70], line, color]
        else: block = [BLUE, [75*line,0,50,70], line, color]
        blocks_type.append(block)
        line_org[2*color] = 200
        pygame.draw.rect(screen, block[0], (block[1][0], block[1][1], block[1][2], block[1][3]))

def destroy_iguinho(x, y, player):
    isRemove = False
    for elem in blocks_type:
        if elem[1][0] < x and (elem[1][0] + elem[1][2]) > x:
            if elem[1][1] < y and (elem[1][1] + elem[1][3]) > y:
                if player == elem[3] or (player-2) == elem[3]:
                    isRemove = True
                    item = elem
                    break
    if isRemove: blocks_type.remove(item)

    
    
def main():
    player1_x = 50
    player1_y = 440
    player2_x = 50
    player2_y = 500
    radius = 15
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: running = False
            if event.type == pygame.K_ESCAPE : running = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player1_x > radius:
            player1_x -= 1
        if keys[pygame.K_RIGHT] and player1_x < width - radius:
            player1_x += 1
        if keys[pygame.K_a] and player2_x > radius:
            player2_x -= 1
        if keys[pygame.K_d] and player2_x < width - radius:
            player2_x += 1
        if keys[pygame.K_DOWN]:
            destroy_iguinho(player1_x, player1_y, 1)
        if keys[pygame.K_s]:
            destroy_iguinho(player2_x, player2_y, 2)
        screen.fill(background_colour)
        movement()
        pygame.draw.circle(screen, RED, (player1_x, player1_y), radius)
        pygame.draw.circle(screen, BLUE, (player2_x, player2_y), radius)
        pygame.display.update()
        clock.tick(200)
if __name__ == "__main__":
    try:
        main()
    except:
        traceback.print_exc()
        pygame.quit()
        input()

'''class Game():
    def run(self):
        running = True
        while running:
            running = self.get_input
            self.draw
            clock.tick(300)

    def draw():
        global player1_x
        global player1_y
        global player2_x
        global player2_y
        screen.fill(background_colour)
        pygame.draw.circle(screen, (255,0,0), (player1_x, player1_y), 15)
        pygame.draw.circle(screen, (255,0,0), (player2_x, player2_y), 15)
        pygame.display.update()

    def get_input():
        global player1_x
        global player1_y
        global player2_x
        global player2_y
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event == pygame.QUIT: return False
            if event == pygame.K_ESCAPE : return False
            if event == pygame.K_LEFT and player1_x > 15:
                player1_x -= 1
            if event == pygame.K_RIGHT and player1_x < width - 15:
                player1_x += 1
            if event == pygame.K_a and player2_x > 15:
                player2_x -= 1
            if event == pygame.K_d and player2_x < width - 15:
                player2_x += 1
        pygame.display.update()
        return True

def draw():
    global blink
    screen.fill(background_colour)
    screen.blit(font24.render("Destroy::Blocks",True,(255,0,0)),(220,80))
    screen.blit(font18.render("Time dos Codadores Insanos Cabulosos",True,(255,0,0)),(150,105))
    if blink < 0:
        screen.blit(font18.render("PRESS ANY KEY",True,(255,0,0)),(230,300))
    blink += 1
    if blink == 150:
        blink = -150
    pygame.display.flip()
    
def get_input():
    for event in pygame.event.get():
        if   event.type == pygame.QUIT: return False
        elif event.type == pygame.KEYDOWN:
            if   event.key == pygame.K_ESCAPE: return False

            game = Game()
            game.run()
    return True
def main():
    global refresh
    #pygame.event.set_grab(True)
    game = Game()
    game.run()
    #while True:
    #    if not get_input(): break
    #    draw()
    #    clock.tick(refresh)
    #pygame.event.set_grab(False)
    pygame.quit()
'''